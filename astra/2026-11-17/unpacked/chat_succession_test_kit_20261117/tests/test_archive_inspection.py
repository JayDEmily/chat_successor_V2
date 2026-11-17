import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from tools.inspect_archive import inspect_archive

ROOT = Path(__file__).resolve().parents[1]

class ArchiveTests(unittest.TestCase):
    def test_I01_all_original_members_accounted_for(self):
        audit = inspect_archive(ROOT / "sources/original_archive.tar.gz")
        self.assertEqual((audit["member_count"], audit["file_count"], audit["directory_count"]),
                         (78, 47, 31))
        self.assertEqual(audit["archive_sha256"],
                         "8f137bdba31465f149b29df39f0e97cd1f764a2746ecdff8bf39c9f976e2100a")
        self.assertEqual(len(audit["worktree_documents"]), 10)

    def test_I02_git_objects_are_exactly_document_snapshot(self):
        audit = inspect_archive(ROOT / "sources/original_archive.tar.gz")
        kinds = [obj["kind"] for obj in audit["git_objects"]]
        self.assertEqual((kinds.count("commit"), kinds.count("tree"), kinds.count("blob")), (1, 3, 10))
        self.assertTrue(all(obj["object_verified"] for obj in audit["git_objects"]))
        blobs = [obj for obj in audit["git_objects"] if obj["kind"] == "blob"]
        self.assertTrue(all(len(obj["matches_worktree"]) == 1 for obj in blobs))
        self.assertTrue(audit["git_metadata"]["index"]["checksum_valid"])
        self.assertEqual(audit["git_metadata"]["index"]["entries"], 10)

    def test_I03_no_launcher_checkout_or_remote_heads_in_snapshot(self):
        audit = inspect_archive(ROOT / "sources/original_archive.tar.gz")
        self.assertEqual(audit["source_snapshots_file_count"], 0)
        meta = audit["git_metadata"]
        self.assertNotIn("[remote ", meta["config"])
        self.assertEqual(meta["refs/heads/master"].strip(),
                         "47d30baadb32be96996da537400fdd3cc0a78430")
        self.assertEqual(audit["sample_hook_count"], 14)
        for doc in audit["worktree_documents"]:
            self.assertTrue(doc["path"].endswith(".md"))

    def test_I04_inspector_rejects_traversal_and_links(self):
        for name, link in (("../escape.txt", False), ("root/link", True)):
            with tempfile.TemporaryDirectory() as tmp:
                archive = Path(tmp) / "bad.tar"
                with tarfile.open(archive, "w") as out:
                    member = tarfile.TarInfo(name)
                    if link:
                        member.type = tarfile.SYMTYPE
                        member.linkname = "../escape"
                        out.addfile(member)
                    else:
                        member.size = 1
                        out.addfile(member, io.BytesIO(b"x"))
                with self.assertRaises(ValueError):
                    inspect_archive(archive)
