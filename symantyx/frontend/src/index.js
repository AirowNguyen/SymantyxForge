//
// Symantyx SPA Root
// Priority 1 Debugging — SPA Loader
//

const root = document.getElementById("root");

root.innerHTML = `
    <div style="padding:20px;">
        <h2>Symantyx Canvas SPA</h2>
        <p>Type text below to hydrate and render:</p>
        <input id="inputText" type="text" style="
            width:80%;
            padding:10px;
            font-size:16px;
            border-radius:6px;
            border:none;
        " placeholder="Enter text..." />

        <button id="renderBtn" style="
            padding:10px 20px;
            margin-left:10px;
            background:#4CAF50;
            color:#fff;
            border:none;
            border-radius:6px;
            font-size:16px;
        ">Render</button>

        <div id="canvasContainer" style="margin-top:20px;">
            <iframe id="canvasFrame"
                src="../symantyx_canvas.html"
                style="width:100%; height:70vh; border:none;">
            </iframe>
        </div>
    </div>
`;

document.getElementById("renderBtn").onclick = () => {
    const text = document.getElementById("inputText").value;
    const frame = document.getElementById("canvasFrame").contentWindow;

    if (frame && frame.SymantyxCanvas) {
        frame.SymantyxCanvas.renderFromText(text);
    }
};
