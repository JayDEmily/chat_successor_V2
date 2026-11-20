(() => {
    "use strict";

    const uuid = "[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}";
    const savedChat = new RegExp(`^/g/(g-p-[0-9a-f]+)(?:-[a-zA-Z0-9-]+)?/c/(${uuid})/?$`);
    const messageId = new RegExp(`^${uuid}$`);
    const finalStatus = /^(?:CHAT_STATUS: )?(?:NEED_MORE_TIME|TASK_COMPLETE|ERROR)$/;
    const projects = new Set(chrome.runtime.getManifest().content_scripts[0].matches
        .map(pattern => pattern.match(/^https:\/\/chatgpt\.com\/g\/(g-p-[0-9a-f]+)\*$/)?.[1]));
    let field;

    function readTurn(turn) {
        const userHeadings = turn.querySelectorAll('h4[data-conversation-role="user"]');
        const assistantHeadings = turn.querySelectorAll('h4[data-conversation-role="assistant"]');
        const keys = turn.querySelectorAll("[data-turn-key]");
        const users = turn.querySelectorAll("[data-user-message-bubble]");
        const states = turn.querySelectorAll("[data-talvt-turn-state]");
        if (keys.length > 1 || users.length > 1 || states.length > 1 ||
            userHeadings.length > 1 || assistantHeadings.length > 1) {
            return {phase: "unqualified"};
        }
        const key = keys[0]?.getAttribute("data-turn-key");
        const user = users[0]?.innerText;
        if (!messageId.test(key ?? "") || !user || userHeadings.length !== 1) {
            return {phase: "loading"};
        }
        const complete = states[0]?.getAttribute("data-talvt-turn-state") === "complete";
        const result = {phase: "observed", key, user, reply: null,
            userAfterAssistant: !complete && assistantHeadings.length === 0};
        if (!complete || assistantHeadings.length !== 1) {
            return result;
        }
        const bodies = turn.querySelectorAll("[data-response-body]");
        if (bodies.length > 1) {
            return {phase: "unqualified"};
        }
        const body = bodies[0];
        const ids = body?.querySelectorAll("[data-chatgpt-selection-message-id]");
        if (ids?.length > 1) {
            return {phase: "unqualified"};
        }
        const replyId = ids?.[0]?.getAttribute("data-chatgpt-selection-message-id");
        const text = body?.innerText;
        if (!messageId.test(replyId ?? "") || !text) {
            return result;
        }
        const prose = [...body.querySelectorAll("p")]
            .filter(paragraph => paragraph.getClientRects().length &&
                !paragraph.closest("blockquote, pre, code") && !paragraph.querySelector("code"));
        const last = text.trim().split(/\r?\n/).at(-1).trim();
        const paragraph = prose.at(-1);
        let final = false;
        if (paragraph && finalStatus.test(last) && paragraph.innerText.trim().split(/\r?\n/).at(-1).trim() === last) {
            const after = document.createRange();
            after.setStartAfter(paragraph);
            after.setEnd(body, body.childNodes.length);
            final = after.toString().trim() === "";
        }
        result.reply = {id: replyId, text, final, handoff: prose.some(element =>
            element.innerText.split(/\r?\n/).some(line => line.trim().startsWith("CHAT_HANDOFF_BRANCH: ")))};
        return result;
    }

    function readConversation() {
        const regions = document.querySelectorAll('div.thread-scroll-container[role="region"][aria-label="Conversation"]');
        if (regions.length !== 1) {
            return {phase: regions.length === 0 ? "loading" : "unqualified"};
        }
        const region = regions[0];
        if (region.clientHeight < 1) {
            return {phase: "loading"};
        }
        if (region.scrollHeight - region.clientHeight - region.scrollTop > 2) {
            return {phase: "offscreen"};
        }
        const turns = [...region.querySelectorAll("[data-virtualized-turn]")];
        if (!turns.length) {
            return {phase: "loading"};
        }
        const list = turns[0].parentElement;
        if (list.children.length !== turns.length || turns.some(turn => turn.parentElement !== list)) {
            return {phase: "unqualified"};
        }
        const current = readTurn(turns.at(-1));
        if (current.key && turns.slice(0, -1).some(turn =>
            [...turn.querySelectorAll("[data-turn-key]")].some(node => node.getAttribute("data-turn-key") === current.key))) {
            return {phase: "unqualified"};
        }
        const previous = turns.length > 1 ? readTurn(turns.at(-2)) : null;
        return {...current, previous: previous?.reply?.final ? {
            key: previous.key, reply: {id: previous.reply.id}
        } : null};
    }

    function refresh() {
        const route = savedChat.exec(location.pathname);
        if (!route || !projects.has(route[1])) {
            field?.remove();
            return;
        }
        if (!field?.isConnected) {
            field = document.createElement("input");
            field.type = "text";
            field.readOnly = true;
            field.tabIndex = -1;
            field.className = "chat-succession-readback";
            field.setAttribute("aria-label", "Chat Succession Chrome readback");
            field.style.cssText = "position:fixed;left:0;top:0;width:1px;height:1px;opacity:0;pointer-events:none";
            document.body.append(field);
        }
        let turn;
        try {
            turn = readConversation();
        } catch {
            turn = {phase: "unqualified"};
        }
        field.value = JSON.stringify({project: route[1], chat: route[2], observedAt: Date.now(), ...turn});
    }

    refresh();
    new MutationObserver(refresh).observe(document.body, {
        attributes: true, characterData: true, childList: true, subtree: true
    });
    document.addEventListener("scroll", refresh, {capture: true, passive: true});
    // Renew the sample so Windows can distinguish a live read from a leftover field.
    setInterval(refresh, 750);
})();
