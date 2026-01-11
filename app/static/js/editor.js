// --- 1. GLOBAL STATE ---
let editorState = {
    videoFile: null,
    layers: [],
    videoVolume: 1.0,
    musicVolume: 0.3,
    isMuted: false
};

// --- 2. HANDLE VIDEO UPLOAD ---
document.getElementById('video-upload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        editorState.videoFile = file;
        const url = URL.createObjectURL(file);
        const video = document.getElementById('main-preview');
        
        video.src = url;
        video.style.display = 'block';
        video.load();

        video.onloadedmetadata = () => {
            document.getElementById('video-duration').innerText = 
                Math.floor(video.duration) + "s";
            // Sesuaikan ukuran overlay dengan ukuran video yang tampil
            adjustOverlaySize();
        };
    }
});

function adjustOverlaySize() {
    const video = document.getElementById('main-preview');
    const overlay = document.getElementById('preview-overlay');
    overlay.style.width = video.clientWidth + 'px';
    overlay.style.height = video.clientHeight + 'px';
}

// --- 3. ADD TEXT & INTERACTIVITY ---
function addText() {
    const textInput = document.getElementById('text-input').value;
    const fontSize = document.getElementById('font-size').value || 40;
    const color = document.getElementById('text-color').value || '#ffffff';
    const overlay = document.getElementById('preview-overlay');

    if (!textInput) return alert("Ketik teks dulu!");

    const id = 'layer-' + Date.now();
    const textEl = document.createElement('div');
    textEl.id = id;
    textEl.className = 'draggable-item';
    textEl.innerText = textInput;
    
    // CSS Inline untuk Preview
    Object.assign(textEl.style, {
        fontSize: fontSize + 'px',
        color: color,
        fontWeight: 'bold',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 1000
    });

    overlay.appendChild(textEl);
    makeDraggable(textEl, id);

    // Simpan ke State (Koordinat 0-1 untuk MoviePy)
    editorState.layers.push({
        id: id,
        type: 'text',
        text: textInput,
        fontSize: parseInt(fontSize),
        color: color,
        x: 0.5, // Center default
        y: 0.5
    });

    updateLayerList();
    document.getElementById('text-input').value = '';
}

// --- 4. DRAG LOGIC ---
function makeDraggable(el, id) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    el.onmousedown = (e) => {
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = () => {
            document.onmouseup = null;
            document.onmousemove = null;
        };
        document.onmousemove = (e) => {
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;

            const newTop = el.offsetTop - pos2;
            const newLeft = el.offsetLeft - pos1;

            el.style.top = newTop + "px";
            el.style.left = newLeft + "px";
            el.style.transform = "none"; // Hilangkan transform center saat di-drag

            // Update State dalam rasio 0.0 - 1.0
            const layer = editorState.layers.find(l => l.id === id);
            if (layer) {
                layer.x = newLeft / el.parentElement.clientWidth;
                layer.y = newTop / el.parentElement.clientHeight;
            }
        };
    };
}

// --- 5. AUDIO CONTROLS ---
document.getElementById('video-volume').addEventListener('input', (e) => {
    const val = e.target.value;
    document.getElementById('v-val').innerText = val + '%';
    document.getElementById('main-preview').volume = val / 100;
    editorState.videoVolume = val / 100;
});

document.getElementById('mute-checkbox').addEventListener('change', (e) => {
    document.getElementById('main-preview').muted = e.target.checked;
    editorState.isMuted = e.target.checked;
});

// --- 6. RENDER SINKRONISASI ---
async function renderVideo() {
    if (!editorState.videoFile) return alert("Pilih video dulu!");

    const btn = document.getElementById('render-btn');
    btn.innerText = "Processing...";
    btn.disabled = true;

    const formData = new FormData();
    formData.append('video', editorState.videoFile);
    formData.append('settings', JSON.stringify({
        texts: editorState.layers,
        volume: editorState.isMuted ? 0 : editorState.videoVolume
    }));

    try {
        const response = await fetch('/render', { method: 'POST', body: formData });
        const result = await response.json();
        alert("Render Selesai: " + result.filename);
    } catch (err) {
        alert("Error: " + err);
    } finally {
        btn.innerText = "RENDER MP4";
        btn.disabled = false;
    }
}

function updateLayerList() {
    const list = document.getElementById('layer-list');
    list.innerHTML = editorState.layers.map(l => `
        <div class="layer-item" style="display:flex; justify-content:space-between; padding:5px; border-bottom:1px solid #334155;">
            <span>📝 ${l.text.substring(0, 10)}</span>
            <button onclick="removeLayer('${l.id}')" style="background:none; color:red; border:none; cursor:pointer;">✕</button>
        </div>
    `).join('');
}

function removeLayer(id) {
    editorState.layers = editorState.layers.filter(l => l.id !== id);
    document.getElementById(id).remove();
    updateLayerList();
}