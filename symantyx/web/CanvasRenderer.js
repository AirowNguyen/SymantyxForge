//
// Symantyx Canvas Renderer
// Priority 1 Debugging — Photic Layer Core
//
// Renders hypertuples, membrane tags, and TabRs force vectors.
// Works with WebView2, backend API, and stylus input.
//

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// ------------------------------------------------------------
// State
// ------------------------------------------------------------
let hypertuples = [];
let tabrs = [];
let selected = null;

// ------------------------------------------------------------
// Fetch + Render Pipeline
// ------------------------------------------------------------
async function renderFromText(text) {
    const response = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, domain: "canvas" })
    });

    const data = await response.json();
    hypertuples = data.hypertuples || [];
    tabrs = data.tabrs || [];

    draw();
}

// ------------------------------------------------------------
// Draw Loop
// ------------------------------------------------------------
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawHypertuples();
    drawTabRsVectors();
}

// ------------------------------------------------------------
// Hypertuple Rendering
// ------------------------------------------------------------
function drawHypertuples() {
    hypertuples.forEach((h, index) => {
        const x = 100 + (index * 120);
        const y = canvas.height / 2;

        ctx.fillStyle = "#4CAF50";
        ctx.beginPath();
        ctx.arc(x, y, 40, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#fff";
        ctx.font = "14px Arial";
        ctx.fillText(h.fields.word || h.id, x - 30, y + 5);

        // clickable region
        h._x = x;
        h._y = y;
    });
}

// ------------------------------------------------------------
// TabRs Force Vectors
// ------------------------------------------------------------
function drawTabRsVectors() {
    tabrs.forEach((force, index) => {
        const x = 100 + (index * 120);
        const y = canvas.height / 2;

        ctx.strokeStyle = "#FF5722";
        ctx.lineWidth = 2;

        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + force.magnitude * 10, y - force.magnitude * 5);
        ctx.stroke();
    });
}

// ------------------------------------------------------------
// Interaction: Click → Detail Pane
// ------------------------------------------------------------
canvas.addEventListener("click", (e) => {
    const mx = e.clientX;
    const my = e.clientY;

    hypertuples.forEach((h) => {
        const dx = mx - h._x;
        const dy = my - h._y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 40) {
            selected = h;
            showDetailPane(h);
        }
    });
});

// ------------------------------------------------------------
// Detail Pane
// ------------------------------------------------------------
function showDetailPane(h) {
    const pane = document.getElementById("detailPane");
    pane.style.display = "block";

    pane.innerHTML = `
        <h3>Hypertuple Detail</h3>
        <pre>${JSON.stringify(h, null, 2)}</pre>
    `;
}

// ------------------------------------------------------------
// Expose renderer to StylusInput.js
// ------------------------------------------------------------
window.SymantyxCanvas = {
    renderFromText,
    draw
};
