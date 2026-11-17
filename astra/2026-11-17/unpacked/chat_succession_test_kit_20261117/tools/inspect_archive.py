"""Inventory every tar member without executing or extracting archived code."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
import zlib


def inspect_archive(path: Path):
    path = Path(path)
    inventory = []
    objects = []
    docs = {}
    all_files = {}
    metadata = {}
    with tarfile.open(path, "r:*") as tf:
        members = tf.getmembers()
        for member in members:
            pure = PurePosixPath(member.name)
            if pure.is_absolute() or ".." in pure.parts:
                raise ValueError("Unsafe archive path")
            if not (member.isfile() or member.isdir()):
                raise ValueError("Unexpected link or special archive member")
            data = tf.extractfile(member).read() if member.isfile() else b""
            inventory.append({
                "path": member.name, "type": "file" if member.isfile() else "directory",
                "size": member.size,
                "sha256": hashlib.sha256(data).hexdigest() if member.isfile() else None,
            })
            if member.isfile():
                all_files[member.name] = data
                if "/.git/" not in member.name:
                    docs[member.name] = data
    for name, data in all_files.items():
        match = re.search(r"/\.git/objects/([0-9a-f]{2})/([0-9a-f]{38})$", name)
        if match:
            oid = "".join(match.groups())
            unpacked = zlib.decompress(data)
            header, body = unpacked.split(b"\0", 1)
            kind, size = header.decode().split()
            valid = hashlib.sha1(unpacked).hexdigest() == oid and len(body) == int(size)
            if not valid:
                raise ValueError("Invalid local Git object")
            item = {"oid": oid, "kind": kind, "size": len(body), "object_verified": valid}
            if kind == "blob":
                item["matches_worktree"] = [k for k, v in docs.items() if v == body]
            elif kind == "commit":
                item["text"] = body.decode()
            elif kind == "tree":
                entries = []
                pos = 0
                while pos < len(body):
                    end = body.index(b"\0", pos)
                    mode, filename = body[pos:end].decode().split(" ", 1)
                    entries.append({"mode": mode, "name": filename,
                                    "oid": body[end + 1:end + 21].hex()})
                    pos = end + 21
                item["entries"] = entries
            objects.append(item)
        elif name.endswith("/.git/index"):
            metadata["index"] = {
                "signature": data[:4].decode(),
                "version": int.from_bytes(data[4:8], "big"),
                "entries": int.from_bytes(data[8:12], "big"),
                "checksum_valid": hashlib.sha1(data[:-20]).digest() == data[-20:],
            }
        elif "/.git/" in name and "/hooks/" not in name:
            metadata[name.split("/.git/", 1)[1]] = data.decode()
    return {
        "mode": "OFFLINE_ARCHIVE_INSPECTION",
        "archive_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "compressed_bytes": path.stat().st_size,
        "member_count": len(inventory),
        "file_count": sum(x["type"] == "file" for x in inventory),
        "directory_count": sum(x["type"] == "directory" for x in inventory),
        "uncompressed_file_bytes": sum(x["size"] for x in inventory),
        "worktree_documents": [{
            "path": k, "bytes": len(v), "lines": len(v.decode().splitlines()),
            "sha256": hashlib.sha256(v).hexdigest(),
        } for k, v in docs.items()],
        "git_objects": objects, "git_metadata": metadata,
        "sample_hook_count": sum("/.git/hooks/" in k for k in all_files),
        "source_snapshots_file_count": sum("/source_snapshots/" in k for k in all_files),
        "inventory": inventory,
        "limits": [
            "Content hashes are delivery/audit evidence, not successor-launch requirements.",
            "Remote branch references in documents are not verified remote objects.",
            "No archived hook/script was executed; no network call was made.",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    result = inspect_archive(args.archive)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("member_count", "file_count", "archive_sha256")}))


if __name__ == "__main__":
    main()
