//
// Symantyx SPA Search Popup Bridge
// Priority 1 Debugging — SPA → Canvas Search Integration
//

window.SymantyxSPA_Search = {
    search(domain) {
        const frame = document.getElementById("canvasFrame").contentWindow;
        if (frame && frame.SymantyxSearch) {
            frame.SymantyxSearch.searchByDomain(domain);
        }
    }
};
