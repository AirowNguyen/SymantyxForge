//
// Symantyx Hypertuple Detail Pane
// Priority 1 Debugging — Photic Detail Layer
//
// Displays full hypertuple information when a node is clicked.
//

const detailPane = document.getElementById("detailPane");

// ------------------------------------------------------------
// Show Detail Pane
// ------------------------------------------------------------
function showDetailPane(h) {
    detailPane.style.display = "block";

    const pretty = JSON.stringify(h, null, 2);

    detailPane.innerHTML = `
        <h3 style="margin-top:0;">Hypertuple Detail</h3>
        <pre style="white-space:pre-wrap;">${pretty}</pre>
        <button id="closeDetail" style="
            margin-top:10px;
            padding:6px 12px;
            background:#444;
            color:#fff;
            border:none;
            border-radius:4px;
        ">Close</button>
    `;

    document.getElementById("closeDetail").onclick = hideDetailPane;
}

// ------------------------------------------------------------
// Hide Detail Pane
// ------------------------------------------------------------
function hideDetailPane() {
    detailPane.style.display = "none";
}

// ------------------------------------------------------------
// External API for CanvasRenderer.js
// ------------------------------------------------------------
window.SymantyxDetail = {
    showDetailPane,
    hideDetailPane
};
