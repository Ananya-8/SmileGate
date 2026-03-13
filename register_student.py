<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SmileGate – Register Student</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet" />
  <style>
    :root {
      --bg:        #0a0c10;
      --surface:   #111318;
      --border:    #1e2128;
      --accent:    #00e5a0;
      --accent2:   #7b61ff;
      --warn:      #ff6b35;
      --text:      #e8eaf0;
      --muted:     #5a6070;
      --font-head: 'Syne', sans-serif;
      --font-mono: 'DM Mono', monospace;
    }
    *, *::before, *::after { box-sizing: border-box; margin:0; padding:0; }
    body {
      background: var(--bg); color: var(--text);
      font-family: var(--font-head);
      min-height: 100vh;
    }
    body::before {
      content:''; position:fixed; inset:0;
      background-image:
        linear-gradient(rgba(0,229,160,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,160,.03) 1px, transparent 1px);
      background-size: 48px 48px;
      pointer-events:none; z-index:0;
    }
    nav {
      position:sticky; top:0; z-index:100;
      background:rgba(10,12,16,.85);
      backdrop-filter:blur(16px);
      border-bottom:1px solid var(--border);
      padding:.75rem 2rem;
      display:flex; align-items:center; gap:2rem;
    }
    .brand { font-size:1.25rem; font-weight:800; color:var(--accent);
             letter-spacing:-.5px; display:flex; align-items:center; gap:.5rem; }
    .brand span { color:var(--text); }
    .nav-links { display:flex; gap:1.25rem; margin-left:auto; }
    .nav-links a { color:var(--muted); text-decoration:none; font-size:.875rem;
                   font-weight:600; transition:color .2s; display:flex; align-items:center; gap:.35rem; }
    .nav-links a:hover, .nav-links a.active { color:var(--accent); }

    .page-wrap {
      position:relative; z-index:1;
      max-width: 860px; margin: 2.5rem auto;
      padding: 0 1.5rem 4rem;
    }
    .page-title {
      font-size: 2rem; font-weight: 800;
      margin-bottom: .25rem;
    }
    .page-sub { color:var(--muted); font-size:.9rem; margin-bottom:2rem; }

    .reg-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    @media (max-width:700px) { .reg-grid { grid-template-columns:1fr; } }

    .panel {
      background:var(--surface);
      border:1px solid var(--border);
      border-radius:16px; overflow:hidden;
    }
    .panel-header {
      padding:.85rem 1.25rem;
      border-bottom:1px solid var(--border);
      font-size:.75rem; font-weight:700;
      text-transform:uppercase; letter-spacing:1px; color:var(--muted);
      display:flex; align-items:center; gap:.5rem;
    }

    /* ── Camera ─────────────────────────────── */
    .cam-wrap {
      position:relative; background:#000;
      aspect-ratio:4/3;
    }
    #videoEl {
      width:100%; height:100%; object-fit:cover; display:block;
    }
    #snapCanvas { display:none; }
    #previewImg {
      position:absolute; inset:0;
      width:100%; height:100%; object-fit:cover;
      display:none;
    }
    .cam-reticles { position:absolute; inset:0; pointer-events:none; }
    .rt {
      position:absolute; width:20px; height:20px;
      border-color:var(--accent); border-style:solid;
    }
    .rt.tl { top:10px; left:10px; border-width:2px 0 0 2px; }
    .rt.tr { top:10px; right:10px; border-width:2px 2px 0 0; }
    .rt.bl { bottom:10px; left:10px; border-width:0 0 2px 2px; }
    .rt.br { bottom:10px; right:10px; border-width:0 2px 2px 0; }

    .cam-btn-row {
      padding:.85rem 1rem; display:flex; gap:.65rem;
    }
    .btn-capture {
      flex:1; background:var(--accent2); color:#fff;
      border:none; border-radius:10px; padding:.65rem .9rem;
      font-family:var(--font-head); font-weight:700; font-size:.85rem;
      cursor:pointer; transition:opacity .2s;
      display:flex; align-items:center; justify-content:center; gap:.4rem;
    }
    .btn-capture:hover { opacity:.85; }
    .btn-retake {
      background:var(--border); color:var(--text);
      border:1px solid var(--border); border-radius:10px;
      padding:.65rem .9rem; font-family:var(--font-head);
      font-weight:600; font-size:.82rem; cursor:pointer;
      transition:background .2s;
    }
    .btn-retake:hover { background:#252830; }

    /* ── Form ───────────────────────────────── */
    .form-wrap { padding:1.5rem; display:flex; flex-direction:column; gap:1.1rem; }
    .field-lbl {
      font-size:.72rem; font-weight:700; text-transform:uppercase;
      letter-spacing:.5px; color:var(--muted); margin-bottom:.35rem;
    }
    .field-input {
      width:100%; background:#0d0f14; border:1px solid var(--border);
      color:var(--text); border-radius:10px; padding:.7rem .95rem;
      font-family:var(--font-mono); font-size:.88rem;
      outline:none; transition:border-color .2s;
    }
    .field-input:focus { border-color:var(--accent2); }
    .field-input::placeholder { color:var(--muted); }

    .btn-register {
      width:100%; background:var(--accent); color:#000;
      border:none; border-radius:12px; padding:.85rem;
      font-family:var(--font-head); font-weight:800; font-size:1rem;
      cursor:pointer; transition:opacity .2s, transform .1s;
      display:flex; align-items:center; justify-content:center; gap:.5rem;
    }
    .btn-register:hover { opacity:.85; }
    .btn-register:active { transform:scale(.97); }
    .btn-register:disabled { opacity:.4; pointer-events:none; }

    /* ── Alert box ──────────────────────────── */
    .alert-box {
      border-radius:12px; padding:.9rem 1.1rem;
      font-size:.88rem; display:none;
      margin-top:1rem;
    }
    .alert-box.success { background:rgba(0,229,160,.08); border:1px solid rgba(0,229,160,.3); color:var(--accent); }
    .alert-box.error   { background:rgba(255,107,53,.08); border:1px solid rgba(255,107,53,.3); color:var(--warn); }

    /* ── Steps guide ─────────────────────────── */
    .steps { padding:1.25rem; display:flex; flex-direction:column; gap:.85rem; }
    .step { display:flex; gap:.85rem; align-items:flex-start; }
    .step-num {
      width:28px; height:28px; border-radius:50%; flex-shrink:0;
      background:rgba(123,97,255,.15); border:1px solid rgba(123,97,255,.4);
      color:var(--accent2); font-size:.75rem; font-weight:800;
      display:flex; align-items:center; justify-content:center;
    }
    .step-txt { font-size:.83rem; color:var(--muted); line-height:1.5; padding-top:.2rem; }
    .step-txt strong { color:var(--text); }
  </style>
</head>
<body>

<nav>
  <div class="brand"><i class="bi bi-shield-check-fill"></i>Smile<span>Gate</span></div>
  <div class="nav-links">
    <a href="/"><i class="bi bi-camera-video-fill"></i> Scanner</a>
    <a href="/register" class="active"><i class="bi bi-person-plus-fill"></i> Register</a>
    <a href="/attendance_log"><i class="bi bi-journal-check"></i> Log</a>
  </div>
</nav>

<div class="page-wrap">
  <div class="page-title">Register New Student</div>
  <div class="page-sub">Capture the student's face and fill in their details to add them to the system.</div>

  <div class="reg-grid">

    <!-- ── Left: Camera capture ────────────────────────────── -->
    <div>
      <div class="panel">
        <div class="panel-header"><i class="bi bi-camera-fill"></i> Face Capture</div>
        <div class="cam-wrap">
          <video id="videoEl" autoplay muted playsinline></video>
          <img id="previewImg" alt="Captured face" />
          <canvas id="snapCanvas"></canvas>
          <div class="cam-reticles">
            <div class="rt tl"></div><div class="rt tr"></div>
            <div class="rt bl"></div><div class="rt br"></div>
          </div>
        </div>
        <div class="cam-btn-row">
          <button class="btn-capture" id="btnCapture" onclick="capturePhoto()">
            <i class="bi bi-camera-fill"></i> Capture Photo
          </button>
          <button class="btn-retake" id="btnRetake" onclick="retakePhoto()" style="display:none">
            <i class="bi bi-arrow-counterclockwise"></i> Retake
          </button>
        </div>
      </div>

      <!-- How it works steps -->
      <div class="panel" style="margin-top:1.25rem">
        <div class="panel-header"><i class="bi bi-info-circle"></i> How It Works</div>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-txt"><strong>Position your face</strong> clearly in front of the camera in good lighting.</div>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <div class="step-txt"><strong>Click "Capture Photo"</strong> once your face is visible and centred.</div>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <div class="step-txt"><strong>Fill in your details</strong> – name and unique enrollment number.</div>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <div class="step-txt"><strong>Click "Register"</strong> to save. The system will generate your face encoding.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Right: Form ─────────────────────────────────────── -->
    <div>
      <div class="panel">
        <div class="panel-header"><i class="bi bi-person-badge-fill"></i> Student Details</div>
        <div class="form-wrap">

          <div>
            <div class="field-lbl">Full Name</div>
            <input class="field-input" type="text" id="inputName"
                   placeholder="e.g. Aditya Kumar" />
          </div>

          <div>
            <div class="field-lbl">Enrollment Number</div>
            <input class="field-input" type="text" id="inputEnroll"
                   placeholder="e.g. CS2024001" />
          </div>

          <div>
            <div class="field-lbl">Captured Photo</div>
            <div style="font-family:var(--font-mono); font-size:.8rem; color:var(--muted);"
                 id="photoStatus">⚠ No photo captured yet.</div>
          </div>

          <button class="btn-register" id="btnRegister" onclick="submitRegistration()" disabled>
            <i class="bi bi-person-check-fill"></i> Register Student
          </button>

          <div class="alert-box" id="alertBox"></div>

        </div>
      </div>
    </div>

  </div>
</div>

<script>
const video      = document.getElementById('videoEl');
const canvas     = document.getElementById('snapCanvas');
const previewImg = document.getElementById('previewImg');
let capturedB64  = null;   // stores the captured JPEG as base64

// ── Start webcam ───────────────────────────────────────────
async function initCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video:true, audio:false });
    video.srcObject = stream;
  } catch (err) {
    alert('Webcam error: ' + err.message);
  }
}

// ── Snap a still from the video feed ──────────────────────
function capturePhoto() {
  canvas.width  = video.videoWidth  || 640;
  canvas.height = video.videoHeight || 480;
  canvas.getContext('2d').drawImage(video, 0, 0);

  capturedB64 = canvas.toDataURL('image/jpeg', 0.9);

  // Show preview instead of live feed
  previewImg.src = capturedB64;
  previewImg.style.display = 'block';

  document.getElementById('btnCapture').style.display = 'none';
  document.getElementById('btnRetake').style.display  = 'flex';
  document.getElementById('photoStatus').innerHTML = '✅ Photo captured successfully.';
  document.getElementById('photoStatus').style.color = '#00e5a0';
  document.getElementById('btnRegister').disabled = false;
}

// ── Discard snap and return to live feed ──────────────────
function retakePhoto() {
  capturedB64 = null;
  previewImg.style.display = 'none';
  document.getElementById('btnCapture').style.display = 'flex';
  document.getElementById('btnRetake').style.display  = 'none';
  document.getElementById('photoStatus').innerHTML = '⚠ No photo captured yet.';
  document.getElementById('photoStatus').style.color = '';
  document.getElementById('btnRegister').disabled = true;
}

// ── Submit registration to Flask API ─────────────────────
async function submitRegistration() {
  const name    = document.getElementById('inputName').value.trim();
  const enroll  = document.getElementById('inputEnroll').value.trim();
  const alertEl = document.getElementById('alertBox');

  if (!name || !enroll) {
    showAlert('error', 'Please enter both name and enrollment number.');
    return;
  }
  if (!capturedB64) {
    showAlert('error', 'Please capture a photo first.');
    return;
  }

  const btn = document.getElementById('btnRegister');
  btn.disabled = true;
  btn.innerHTML = '<i class="bi bi-arrow-repeat"></i> Registering…';

  try {
    const resp = await fetch('/api/register_student', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, enrollment_no: enroll, image: capturedB64 })
    });
    const data = await resp.json();

    if (data.status === 'success') {
      showAlert('success', `✅ ${data.message}`);
      // Clear form
      document.getElementById('inputName').value   = '';
      document.getElementById('inputEnroll').value = '';
      retakePhoto();
    } else {
      showAlert('error', `❌ ${data.message}`);
    }
  } catch (err) {
    showAlert('error', 'Network error: ' + err.message);
  }

  btn.disabled = false;
  btn.innerHTML = '<i class="bi bi-person-check-fill"></i> Register Student';
}

function showAlert(type, message) {
  const el = document.getElementById('alertBox');
  el.className = 'alert-box ' + type;
  el.textContent = message;
  el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 6000);
}

initCamera();
</script>
</body>
</html>
