//
// Symantyx SPA Canvas Bridge
// Priority 1 Debugging — SPA → Canvas Integration
//

window.SymantyxSPA = {
    sendToCanvas(text) {
        const frame = document.getElementById("canvasFrame").contentWindow;
        if (frame && frame.SymantyxCanvas) {
            frame.SymantyxCanvas.renderFromText(text);
        }
    },

    highlight(id) {
        const frame = document.getElementById("canvasFrame").contentWindow;
        if (frame && frame.SymantyxSearch) {
            frame.SymantyxSearch.highlightHypertuple(id);
        }
    }
};
