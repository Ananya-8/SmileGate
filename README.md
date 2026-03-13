<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SmileGate – Smart Attendance</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet" />
  <style>
    /* ── Root design tokens ───────────────────────────────────── */
    :root {
      --bg:         #0a0c10;
      --surface:    #111318;
      --border:     #1e2128;
      --accent:     #00e5a0;
      --accent2:    #7b61ff;
      --warn:       #ff6b35;
      --text:       #e8eaf0;
      --muted:      #5a6070;
      --font-head:  'Syne', sans-serif;
      --font-mono:  'DM Mono', monospace;
    }

    /* ── Base ─────────────────────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-head);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* subtle grid overlay */
    body::before {
      content: '';
      position: fixed; inset: 0;
      background-image:
        linear-gradient(rgba(0,229,160,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,160,.03) 1px, transparent 1px);
      background-size: 48px 48px;
      pointer-events: none;
      z-index: 0;
    }

    /* ── Nav ──────────────────────────────────────────────────── */
    nav {
      position: sticky; top: 0; z-index: 100;
      background: rgba(10,12,16,.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: .75rem 2rem;
      display: flex; align-items: center; gap: 2rem;
    }
    .brand {
      font-size: 1.25rem; font-weight: 800;
      color: var(--accent);
      letter-spacing: -.5px;
      display: flex; align-items: center; gap: .5rem;
    }
    .brand span { color: var(--text); }
    .nav-links { display: flex; gap: 1.25rem; margin-left: auto; }
    .nav-links a {
      color: var(--muted); text-decoration: none;
      font-size: .875rem; font-weight: 600;
      transition: color .2s;
      display: flex; align-items: center; gap: .35rem;
    }
    .nav-links a:hover, .nav-links a.active { color: var(--accent); }

    /* ── Layout ───────────────────────────────────────────────── */
    .main-grid {
      position: relative; z-index: 1;
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 1.5rem;
      max-width: 1200px;
      margin: 2rem auto;
      padding: 0 1.5rem 3rem;
    }

    /* ── Panel / card ─────────────────────────────────────────── */
    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
    }
    .panel-header {
      padding: .9rem 1.25rem;
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; gap: .6rem;
      font-size: .8rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 1px;
      color: var(--muted);
    }
    .panel-header .dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 8px var(--accent);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%,100% { opacity: 1; transform: scale(1); }
      50% { opacity: .4; transform: scale(.7); }
    }

    /* ── Camera feed ──────────────────────────────────────────── */
    .camera-wrap {
      position: relative;
      background: #000;
      aspect-ratio: 4/3;
    }
    #videoEl {
      width: 100%; height: 100%;
      object-fit: cover;
      display: block;
    }
    #annotatedImg {
      position: absolute; inset: 0;
      width: 100%; height: 100%;
      object-fit: cover;
      display: none;
    }
    .camera-overlay {
      position: absolute; inset: 0;
      border: 2px solid transparent;
      border-radius: 0;
      transition: border-color .4s;
      pointer-events: none;
    }
    .camera-overlay.success { border-color: var(--accent); box-shadow: inset 0 0 32px rgba(0,229,160,.15); }
    .camera-overlay.denied  { border-color: var(--warn);   box-shadow: inset 0 0 32px rgba(255,107,53,.15); }
    .camera-overlay.dupe    { border-color: #f5a623;        box-shadow: inset 0 0 32px rgba(245,166,35,.12); }

    /* corner reticle */
    .reticle {
      position: absolute; width: 24px; height: 24px;
      border-color: var(--accent); border-style: solid;
      pointer-events: none;
    }
    .reticle.tl { top: 12px; left: 12px; border-width: 2px 0 0 2px; }
    .reticle.tr { top: 12px; right: 12px; border-width: 2px 2px 0 0; }
    .reticle.bl { bottom: 12px; left: 12px; border-width: 0 0 2px 2px; }
    .reticle.br { bottom: 12px; right: 12px; border-width: 0 2px 2px 0; }

    /* scanning bar */
    .scan-bar {
      position: absolute; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--accent), transparent);
      animation: scan 2.5s linear infinite;
      opacity: .7;
    }
    @keyframes scan {
      0% { top: 0; }
      100% { top: 100%; }
    }

    /* ── Camera controls ──────────────────────────────────────── */
    .camera-controls {
      padding: 1rem 1.25rem;
      display: flex; gap: .75rem; align-items: center;
    }
    .btn-scan {
      flex: 1;
      background: var(--accent);
      color: #000;
      border: none;
      padding: .7rem 1.25rem;
      border-radius: 10px;
      font-family: var(--font-head);
      font-weight: 700;
      font-size: .9rem;
      cursor: pointer;
      transition: opacity .2s, transform .1s;
      display: flex; align-items: center; justify-content: center; gap: .5rem;
    }
    .btn-scan:hover { opacity: .85; }
    .btn-scan:active { transform: scale(.97); }
    .btn-scan.loading { opacity: .6; pointer-events: none; }

    .btn-auto {
      background: var(--border);
      color: var(--text);
      border: 1px solid var(--border);
      padding: .7rem 1rem;
      border-radius: 10px;
      font-family: var(--font-head);
      font-weight: 600;
      font-size: .85rem;
      cursor: pointer;
      transition: background .2s;
      white-space: nowrap;
    }
    .btn-auto:hover { background: #252830; }
    .btn-auto.on { background: rgba(0,229,160,.15); color: var(--accent); border-color: var(--accent); }

    /* ── Status card ──────────────────────────────────────────── */
    .status-card {
      margin: 0 1.25rem 1.25rem;
      border-radius: 12px;
      padding: 1rem 1.25rem;
      border: 1px solid var(--border);
      background: rgba(255,255,255,.03);
      min-height: 90px;
      transition: background .4s, border-color .4s;
    }
    .status-card.success { background: rgba(0,229,160,.06); border-color: rgba(0,229,160,.3); }
    .status-card.denied  { background: rgba(255,107,53,.06);  border-color: rgba(255,107,53,.3);  }
    .status-card.dupe    { background: rgba(245,166,35,.06);  border-color: rgba(245,166,35,.3);  }

    .status-badge {
      display: inline-flex; align-items: center; gap: .4rem;
      font-size: .7rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 1px;
      padding: .25rem .65rem; border-radius: 20px;
      margin-bottom: .5rem;
    }
    .status-badge.success { background: rgba(0,229,160,.15); color: var(--accent); }
    .status-badge.denied  { background: rgba(255,107,53,.15);  color: var(--warn);   }
    .status-badge.dupe    { background: rgba(245,166,35,.15);  color: #f5a623;        }
    .status-badge.idle    { background: rgba(90,96,112,.15);   color: var(--muted);   }

    .status-msg { font-size: .95rem; font-weight: 600; margin-bottom: .5rem; }
    .status-detail {
      font-family: var(--font-mono);
      font-size: .78rem; color: var(--muted);
      display: flex; flex-direction: column; gap: .15rem;
    }

    /* ── Smile meter ──────────────────────────────────────────── */
    .smile-meter { margin-top: .75rem; }
    .smile-label {
      display: flex; justify-content: space-between;
      font-size: .72rem; color: var(--muted); margin-bottom: .3rem;
    }
    .smile-track {
      height: 6px;
      background: var(--border);
      border-radius: 99px;
      overflow: hidden;
    }
    .smile-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--accent2), var(--accent));
      border-radius: 99px;
      width: 0%;
      transition: width .6s cubic-bezier(.34,1.56,.64,1);
    }
    .smile-fill.below { background: linear-gradient(90deg, #ff4b4b, var(--warn)); }

    /* ── Sidebar ──────────────────────────────────────────────── */
    .sidebar { display: flex; flex-direction: column; gap: 1.5rem; }

    /* Threshold config */
    .threshold-display {
      padding: 1.25rem;
      display: flex; flex-direction: column; gap: .75rem;
    }
    .threshold-val {
      font-size: 3rem; font-weight: 800;
      color: var(--accent); line-height: 1;
      font-family: var(--font-mono);
    }
    .threshold-val span { font-size: 1.5rem; color: var(--muted); }
    .threshold-desc { font-size: .8rem; color: var(--muted); line-height: 1.5; }

    /* Recent log */
    .log-list { padding: 0; max-height: 320px; overflow-y: auto; }
    .log-list::-webkit-scrollbar { width: 4px; }
    .log-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
    .log-item {
      padding: .8rem 1.25rem;
      border-bottom: 1px solid var(--border);
      display: flex; align-items: flex-start; gap: .75rem;
    }
    .log-item:last-child { border-bottom: none; }
    .log-avatar {
      width: 36px; height: 36px; border-radius: 50%;
      background: var(--border);
      display: flex; align-items: center; justify-content: center;
      font-size: .8rem; font-weight: 700; flex-shrink: 0;
      color: var(--accent);
    }
    .log-name { font-size: .85rem; font-weight: 600; }
    .log-meta { font-family: var(--font-mono); font-size: .7rem; color: var(--muted); }
    .log-score {
      margin-left: auto; flex-shrink: 0;
      font-family: var(--font-mono); font-size: .75rem;
      padding: .2rem .5rem;
      border-radius: 6px;
      background: rgba(0,229,160,.1);
      color: var(--accent);
    }
    .log-empty {
      padding: 2rem; text-align: center;
      color: var(--muted); font-size: .85rem;
    }

    /* ── Stats row ────────────────────────────────────────────── */
    .stats-row {
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 1rem; margin-bottom: 1.5rem;
    }
    .stat-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.1rem 1.25rem;
    }
    .stat-val { font-size: 2rem; font-weight: 800; color: var(--accent); }
    .stat-lbl { font-size: .72rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }

    /* ── Responsive ───────────────────────────────────────────── */
    @media (max-width: 900px) {
      .main-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

<!-- ── Navigation ──────────────────────────────────────────────────────────── -->
<nav>
  <div class="brand">
    <i class="bi bi-shield-check-fill"></i>
    Smile<span>Gate</span>
  </div>
  <div class="nav-links">
    <a href="/" class="active"><i class="bi bi-camera-video-fill"></i> Scanner</a>
    <a href="/register"><i class="bi bi-person-plus-fill"></i> Register</a>
    <a href="/attendance_log"><i class="bi bi-journal-check"></i> Log</a>
  </div>
</nav>

<!-- ── Stats row ────────────────────────────────────────────────────────────── -->
<div class="main-grid">
  <div style="grid-column: 1/-1">
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-val" id="statStudents">–</div>
        <div class="stat-lbl">Registered Students</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" id="statToday">–</div>
        <div class="stat-lbl">Present Today</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">{{ smile_threshold|int }}%</div>
        <div class="stat-lbl">Smile Threshold</div>
      </div>
    </div>
  </div>

  <!-- ── Left: Camera panel ─────────────────────────────────────────────────── -->
  <div>
    <div class="panel">
      <div class="panel-header">
        <div class="dot"></div>
        Live Camera Feed
      </div>

      <div class="camera-wrap">
        <video id="videoEl" autoplay muted playsinline></video>
        <img id="annotatedImg" alt="Annotated frame" />
        <div class="camera-overlay" id="camOverlay"></div>
        <div class="scan-bar" id="scanBar"></div>
        <div class="reticle tl"></div>
        <div class="reticle tr"></div>
        <div class="reticle bl"></div>
        <div class="reticle br"></div>
      </div>

      <div class="camera-controls">
        <button class="btn-scan" id="btnScan" onclick="captureAndScan()">
          <i class="bi bi-camera"></i> Scan Now
        </button>
        <button class="btn-auto" id="btnAuto" onclick="toggleAuto()">
          <i class="bi bi-play-circle"></i> Auto
        </button>
      </div>

      <!-- Status card -->
      <div class="status-card" id="statusCard">
        <div class="status-badge idle" id="statusBadge">
          <i class="bi bi-circle"></i> Idle
        </div>
        <div class="status-msg" id="statusMsg">Point camera at a registered student and press Scan.</div>
        <div class="status-detail" id="statusDetail"></div>
        <div class="smile-meter" id="smileMeter" style="display:none">
          <div class="smile-label">
            <span>Smile Score</span>
            <span id="smileVal">0%</span>
          </div>
          <div class="smile-track">
            <div class="smile-fill" id="smileFill"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Right: Sidebar ───────────────────────────────────────────────────────── -->
  <div class="sidebar">
    <!-- Threshold info -->
    <div class="panel">
      <div class="panel-header"><i class="bi bi-sliders"></i> Smile Threshold</div>
      <div class="threshold-display">
        <div class="threshold-val">{{ smile_threshold|int }}<span>%</span></div>
        <div class="threshold-desc">
          The system requires a <strong>happy emotion score ≥ {{ smile_threshold|int }}%</strong>
          from the DeepFace model before granting access. Modify
          <code>SMILE_THRESHOLD</code> in <code>recognize_and_attend.py</code>.
        </div>
      </div>
    </div>

    <!-- Recent log -->
    <div class="panel" style="flex:1">
      <div class="panel-header"><i class="bi bi-clock-history"></i> Recent Entries</div>
      <div class="log-list" id="logList">
        <div class="log-empty">No entries yet.</div>
      </div>
    </div>
  </div>
</div><!-- end .main-grid -->

<script>
// ══════════════════════════════════════════════════════════
//  Camera initialisation
// ══════════════════════════════════════════════════════════
const video    = document.getElementById('videoEl');
const imgEl    = document.getElementById('annotatedImg');
const THRESHOLD = {{ smile_threshold }};

async function initCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
  } catch (err) {
    alert('Could not access webcam: ' + err.message);
  }
}

// ══════════════════════════════════════════════════════════
//  Capture a frame and send it to the Flask API
// ══════════════════════════════════════════════════════════
async function captureAndScan() {
  const btn = document.getElementById('btnScan');
  btn.classList.add('loading');
  btn.innerHTML = '<i class="bi bi-arrow-repeat"></i> Scanning…';

  // Draw the current video frame to an off-screen canvas
  const canvas = document.createElement('canvas');
  canvas.width  = video.videoWidth  || 640;
  canvas.height = video.videoHeight || 480;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const b64 = canvas.toDataURL('image/jpeg', 0.85);  // JPEG at 85% quality

  try {
    const resp = await fetch('/api/recognize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: b64 })
    });
    const data = await resp.json();
    displayResult(data);
  } catch (err) {
    displayResult({ status: 'error', message: 'Network error: ' + err.message });
  }

  btn.classList.remove('loading');
  btn.innerHTML = '<i class="bi bi-camera"></i> Scan Now';
}

// ══════════════════════════════════════════════════════════
//  Update the UI based on the API response
// ══════════════════════════════════════════════════════════
function displayResult(data) {
  const card    = document.getElementById('statusCard');
  const badge   = document.getElementById('statusBadge');
  const msg     = document.getElementById('statusMsg');
  const detail  = document.getElementById('statusDetail');
  const overlay = document.getElementById('camOverlay');
  const meter   = document.getElementById('smileMeter');
  const fill    = document.getElementById('smileFill');
  const valEl   = document.getElementById('smileVal');

  // Reset classes
  card.className    = 'status-card';
  badge.className   = 'status-badge';
  overlay.className = 'camera-overlay';

  // Show annotated image if provided
  if (data.annotated_img) {
    imgEl.src = 'data:image/jpeg;base64,' + data.annotated_img;
    imgEl.style.display = 'block';
    setTimeout(() => { imgEl.style.display = 'none'; }, 3000);
  }

  // Apply per-status styling
  if (data.status === 'success') {
    card.classList.add('success');
    badge.classList.add('success');
    overlay.classList.add('success');
    badge.innerHTML = '<i class="bi bi-check-circle-fill"></i> ACCESS GRANTED';
    refreshLog();
    refreshStats();
  } else if (data.status === 'duplicate') {
    card.classList.add('dupe');
    badge.classList.add('dupe');
    overlay.classList.add('dupe');
    badge.innerHTML = '<i class="bi bi-info-circle-fill"></i> ALREADY MARKED';
  } else if (data.status === 'denied') {
    card.classList.add('denied');
    badge.classList.add('denied');
    overlay.classList.add('denied');
    badge.innerHTML = '<i class="bi bi-x-circle-fill"></i> ACCESS DENIED';
  } else {
    badge.classList.add('idle');
    badge.innerHTML = '<i class="bi bi-exclamation-triangle-fill"></i> ERROR';
  }

  msg.textContent = data.message || '–';

  // Student info detail
  if (data.name) {
    detail.innerHTML =
      `<span>👤 ${data.name}</span>` +
      `<span>🎓 ${data.enrollment_no}</span>`;
  } else {
    detail.innerHTML = '';
  }

  // Smile meter
  if (data.smile_score !== undefined && data.smile_score !== null) {
    meter.style.display = 'block';
    const pct = Math.min(100, data.smile_score);
    fill.style.width = pct + '%';
    fill.className   = 'smile-fill' + (pct < THRESHOLD ? ' below' : '');
    valEl.textContent = pct.toFixed(1) + '%';
  } else {
    meter.style.display = 'none';
  }
}

// ══════════════════════════════════════════════════════════
//  Auto-scan toggle (every 3 seconds)
// ══════════════════════════════════════════════════════════
let autoTimer = null;

function toggleAuto() {
  const btn = document.getElementById('btnAuto');
  if (autoTimer) {
    clearInterval(autoTimer);
    autoTimer = null;
    btn.classList.remove('on');
    btn.innerHTML = '<i class="bi bi-play-circle"></i> Auto';
  } else {
    autoTimer = setInterval(captureAndScan, 3000);
    btn.classList.add('on');
    btn.innerHTML = '<i class="bi bi-stop-circle-fill"></i> Stop';
  }
}

// ══════════════════════════════════════════════════════════
//  Sidebar: recent log
// ══════════════════════════════════════════════════════════
async function refreshLog() {
  const list = document.getElementById('logList');
  try {
    const resp = await fetch('/api/attendance');
    const records = await resp.json();

    if (!records.length) {
      list.innerHTML = '<div class="log-empty">No entries yet.</div>';
      return;
    }

    list.innerHTML = records.slice(0, 8).map(r => {
      const initials = r.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2);
      return `
        <div class="log-item">
          <div class="log-avatar">${initials}</div>
          <div>
            <div class="log-name">${r.name}</div>
            <div class="log-meta">${r.enrollment_no} · ${r.date} ${r.time}</div>
          </div>
          <div class="log-score">${r.smile_score.toFixed(0)}%</div>
        </div>`;
    }).join('');
  } catch { /* silently ignore */ }
}

// ══════════════════════════════════════════════════════════
//  Stats
// ══════════════════════════════════════════════════════════
async function refreshStats() {
  try {
    const [sResp, aResp] = await Promise.all([
      fetch('/api/students'),
      fetch('/api/attendance')
    ]);
    const students   = await sResp.json();
    const attendance = await aResp.json();
    const today = new Date().toISOString().slice(0,10);
    const todayCount = attendance.filter(r => r.date === today).length;

    document.getElementById('statStudents').textContent = students.length;
    document.getElementById('statToday').textContent    = todayCount;
  } catch { /* ignore */ }
}

// ── Startup ────────────────────────────────────────────────
initCamera();
refreshStats();
refreshLog();
</script>
</body>
</html>
