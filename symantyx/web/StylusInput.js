//
// Symantyx Stylus Input Handler
// Priority 1 Debugging — Interaction Layer
//
// Captures stylus/mouse drawing on the canvas,
// converts strokes to text, and sends to backend for hydration.
//

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let drawing = false;
let strokePoints = [];

// ------------------------------------------------------------
// Start Drawing
// ------------------------------------------------------------
canvas.addEventListener("pointerdown", (e) => {
    drawing = true;
    strokePoints = [];
    addPoint(e);
});

// ------------------------------------------------------------
// Drawing Movement
// ------------------------------------------------------------
canvas.addEventListener("pointermove", (e) => {
    if (!drawing) return;
    addPoint(e);
    drawStroke();
});

// ------------------------------------------------------------
// End Drawing → Convert Stroke → Hydrate
// ------------------------------------------------------------
canvas.addEventListener("pointerup", async () => {
    drawing = false;

    const text = await strokeToText(strokePoints);
    if (text && text.trim().length > 0) {
        window.SymantyxCanvas.renderFromText(text);
    }
});

// ------------------------------------------------------------
// Add Point
// ------------------------------------------------------------
function addPoint(e) {
    const rect = canvas.getBoundingClientRect();
    strokePoints.push({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    });
}

// ------------------------------------------------------------
// Draw Stroke (visual feedback)
// ------------------------------------------------------------
function drawStroke() {
    if (strokePoints.length < 2) return;

    const p1 = strokePoints[strokePoints.length - 2];
    const p2 = strokePoints[strokePoints.length - 1];

    ctx.strokeStyle = "#00E5FF";
    ctx.lineWidth = 3;

    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
}

// ------------------------------------------------------------
// Convert Stroke → Text (placeholder)
// ------------------------------------------------------------
async function strokeToText(points) {
    // Placeholder: real OCR stroke recognition can be added later.
    // For now, treat strokes as a "gesture" that triggers a prompt.
    return prompt("Enter text to hydrate:");
}

// ------------------------------------------------------------
// Expose API
// ------------------------------------------------------------
window.SymantyxStylus = {
    strokeToText
};
