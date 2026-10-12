//
// Symantyx TabRs Search Popup
// Priority 1 Debugging — Semantic Search Layer
//
// Provides a popup UI for searching hypertuples by domain,
// powered by TabRs semantic forces.
//

const popup = document.getElementById("searchPopup");

// ------------------------------------------------------------
// Show Popup
// ------------------------------------------------------------
function showSearchPopup(results) {
    popup.style.display = "block";

    popup.innerHTML = `
        <h3>Search Results</h3>
        <ul>
            ${results.map(r => `<li data-id="${r.id}">${r.id}</li>`).join("")}
        </ul>
    `;

    // click → highlight on canvas
    popup.querySelectorAll("li").forEach(li => {
        li.addEventListener("click", () => {
            const id = li.getAttribute("data-id");
            highlightHypertuple(id);
        });
    });
}

// ------------------------------------------------------------
// Hide Popup
// ------------------------------------------------------------
function hideSearchPopup() {
    popup.style.display = "none";
}

// ------------------------------------------------------------
// Search by Domain
// ------------------------------------------------------------
async function searchByDomain(domain) {
    const response = await fetch(`http://localhost:8000/registry/domain/${domain}`);
    const results = await response.json();

    if (results.length === 0) {
        popup.innerHTML = "<p>No results found.</p>";
        popup.style.display = "block";
        return;
    }

    showSearchPopup(results);
}

// ------------------------------------------------------------
// Highlight Hypertuple on Canvas
// ------------------------------------------------------------
function highlightHypertuple(id) {
    if (!window.SymantyxCanvas) return;

    const h = window.SymantyxCanvas.hypertuples?.find(x => x.id === id);
    if (!h) return;

    const ctx = document.getElementById("canvas").getContext("2d");

    ctx.strokeStyle = "#00E5FF";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.arc(h._x, h._y, 50, 0, Math.PI * 2);
    ctx.stroke();
}

// ------------------------------------------------------------
// Expose API
// ------------------------------------------------------------
window.SymantyxSearch = {
    searchByDomain,
    showSearchPopup,
    hideSearchPopup
};
