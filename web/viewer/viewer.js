// The anatomy viewer. Scene, camera, controls, the population mean document, structure toggles,
// the segment overlay and manual coordinates. Nothing here computes a result.
import * as THREE from 'three';
import { OrbitControls } from '../vendor/OrbitControls.js';
import { GLTFLoader } from '../vendor/GLTFLoader.js';
import { Document, Modes } from './modes.js';
import { ReadError, listMaps, readCarto } from './readers/carto.js';
import { readArgo, readArgoValues } from './readers/argo.js';

const $ = (id) => document.getElementById(id);

const AHA = [
  'Basal anterior', 'Basal anteroseptal', 'Basal inferoseptal', 'Basal inferior', 'Basal inferolateral',
  'Basal anterolateral', 'Mid anterior', 'Mid anteroseptal', 'Mid inferoseptal', 'Mid inferior',
  'Mid inferolateral', 'Mid anterolateral', 'Apical anterior', 'Apical septal', 'Apical inferior',
  'Apical lateral', 'Apex',
];
const SEGMENT_COLOURS = [
  0xe6194b, 0x3cb44b, 0xffe119, 0x4363d8, 0xf58231, 0x911eb4, 0x46f0f0, 0xf032e6, 0xbcf60c, 0xfabebe,
  0x008080, 0xe6beff, 0x9a6324, 0xfffac8, 0x800000, 0xaaffc3, 0x808000,
];
const UNSEGMENTED = new THREE.Color(0xd9d6cf);

// Structure families, for telling parts apart. Ids from structures.json.
function family(id) {
  if (id <= 2) return 'ventricle';
  if (id <= 4) return 'atrium';
  if (id <= 6) return 'vessel';
  if (id <= 10) return 'valve';
  if (id <= 17) return 'inlet';
  return 'border';
}
const FAMILY_COLOUR = {
  ventricle: 0xc48f7c, atrium: 0xd4b09c, vessel: 0xb4bfcf, valve: 0xa6b8a0, inlet: 0xb3b0cc, border: 0xcdbfa9,
};
const POINT_COLOUR = 0x1d6fe0;          // typed coordinates
const MAPPED_COLOUR = 0x2a9d8f;         // a study's mapped points
const ABLATION_COLOUR = 0xd1495b;       // a study's ablation sites
const STUDY_VIEW = { up: [0, 1, 0], anterior: [0, 0, 1] };
// Patient axes of each study frame, as unit vectors in the export's own coordinates. null means the
// convention has not been verified against evidence, and the standard views stay disabled (ADR-0007).
// CARTO: +X left, +Y superior, +Z anterior, as SlicerEAMapReader and OpenEP both encode it; recorded
// in the vault note carto3-export. ARGO: its publisher states no frame, so null.
const STUDY_AXES = { carto: { anterior: [0, 0, 1], up: [0, 1, 0] }, argo: null };
const OBLIQUE_DEG = 45;
// Value colour scale, low to high, in the order clinicians expect on a mapping system: red for
// low voltage, purple for high. The same scale serves activation time.
const VALUE_SCALE = [0xd7191c, 0xf4a141, 0xffff8c, 0x74c476, 0x2c7bb6, 0x8e44ad];
const NO_VALUE = 0x9aa0a6;
const LOOK = {
  plain: { background: 0xf3f2ee, shell: 0xc9b8a8, ablation: 0xd1495b, ablationScale: 0.015 },
  map: { background: 0x15181c, shell: 0x8f959c, ablation: 0x3bbf4a, ablationScale: 0.022 },
};
const LOAD_TIMEOUT_MS = 10000;

// Exposed for the browser tests. Not an API.
const state = { ready: false, frameTimes: [], manifest: null, names: null, initial: null };
window.aleViewer = state;

function webglAvailable() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) {
    return false;
  }
}

function showFallback(reason) {
  $('stage').hidden = true;
  $('loading').hidden = true;
  $('fallback-reason').textContent = reason;
  $('fallback').hidden = false;
}

function showError(text) {
  $('loading').hidden = true;
  const e = $('error');
  e.hidden = false;
  e.textContent = text + ' ';
  const a = document.createElement('a');
  a.href = '/projects/ale/';
  a.textContent = 'Back to the section.';
  e.append(a);
}

async function fetchJson(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url} answered ${r.status}`);
  return r.json();
}

function loadGlb(url, ms) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`the heart did not load within ${ms / 1000} seconds`)), ms);
    new GLTFLoader().load(
      url,
      (gltf) => { clearTimeout(timer); resolve(gltf); },
      undefined,
      () => { clearTimeout(timer); reject(new Error('the heart could not be loaded')); },
    );
  });
}

if (new URLSearchParams(location.search).has('still')) document.body.classList.add('still');

if (!webglAvailable()) {
  showFallback('WebGL is not available in this browser, so this is a still image of the same heart at its starting view.');
} else {
  main().catch((err) => showError(`The viewer stopped: ${err.message}.`));
}

async function main() {
  const canvas = $('stage');
  const box = $('stage-box');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(matchMedia('(prefers-color-scheme: dark)').matches ? 0x1f2124 : 0xf3f2ee);
  const camera = new THREE.PerspectiveCamera(40, 4 / 3, 1, 5000);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8a8a, 1.1));
  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(60, 80, 120);
  camera.add(key);
  scene.add(camera);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.12;
  controls.enablePan = false;
  const modes = new Modes(scene);
  Object.assign(state, { renderer, scene, camera, controls, modes });

  function resize() {
    // The stage height is the viewport minus whatever the site bar and the strip measure here.
    const bar = document.querySelector('.site-bar');
    const strip = $('research-use');
    const root = document.documentElement.style;
    if (bar) root.setProperty('--ale-bar', `${bar.offsetHeight}px`);
    if (strip) root.setProperty('--ale-strip', `${strip.offsetHeight}px`);
    const w = box.clientWidth || 800;
    const h = box.clientHeight || 600;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(box);
  resize();

  let last = performance.now();
  renderer.setAnimationLoop(() => {
    const now = performance.now();
    state.frameTimes.push(now - last);
    if (state.frameTimes.length > 240) state.frameTimes.shift();
    last = now;
    controls.update();
    renderer.render(scene, camera);
  });

  const [manifest, names] = await Promise.all([fetchJson('data/heart.manifest.json'), fetchJson('structures.json')]);
  state.manifest = manifest;
  state.names = names.names || names;

  modes.onChange((doc) => {
    applyLook();
    if (doc.kind !== 'patient') { $('values-box').hidden = true; $('value-on').checked = false; }
    const m = $('mode');
    m.textContent = doc.label;
    m.dataset.mode = doc.kind;
    $('frame-label').textContent = doc.frame;
    $('close-study').hidden = doc.kind !== 'patient';
    $('study-summary').textContent = doc.study
      ? `${doc.study.mapped} mapped points and ${doc.study.ablation} ablation sites from ${doc.study.label}, drawn where the export puts them.`
      : '';
    renderPoints();
  });

  await openMean();
  wireControls();
  wireImports();
  wireLook();
  wireValues();
}

async function openMean() {
  const { modes, manifest } = state;
  if (modes.mean && modes.mean.model) {
    modes.activate(modes.mean);
    frameCamera(modes.mean.bounds, manifest.output.view || STUDY_VIEW);
    buildStructureList(modes.mean.model.children);
    buildSegments(modes.mean.model.children);
    return;
  }
  const doc = new Document('mean', 'Population mean', 'the population mean, millimetres');
  const gltf = await loadGlb('data/heart.glb', LOAD_TIMEOUT_MS);
  const ids = Object.keys(manifest.output.per_structure).map(Number).sort((a, b) => a - b);
  const meshes = [];
  gltf.scene.traverse((o) => { if (o.isMesh) meshes.push(o); });
  if (meshes.length !== ids.length) throw new Error(`expected ${ids.length} structures, found ${meshes.length}`);
  const model = new THREE.Group();
  meshes.forEach((m, i) => {
    const id = ids[i];
    const expected = manifest.output.per_structure[String(id)].triangles;
    const got = m.geometry.index.count / 3;
    if (got !== expected) throw new Error(`structure ${id} has ${got} triangles, the manifest says ${expected}`);
    m.name = `structure-${id}`;
    m.userData.structure = id;
    m.userData.plain = new THREE.MeshLambertMaterial({ color: FAMILY_COLOUR[family(id)], side: THREE.DoubleSide });
    m.userData.segmented = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide });
    m.material = m.userData.plain;
    model.add(m);
  });
  doc.model = model;
  doc.group.add(model);
  doc.bounds = new THREE.Box3().setFromObject(model);
  modes.activate(doc);
  frameCamera(doc.bounds, manifest.output.view || STUDY_VIEW);
  buildStructureList(meshes);
  buildSegments(meshes);
  $('loading').hidden = true;
  state.ready = true;
}

function frameCamera(bounds, view) {
  const { camera, controls } = state;
  const sphere = bounds.getBoundingSphere(new THREE.Sphere());
  const r = sphere.radius;
  // The bounding sphere overstates the heart, so a factor under one still keeps it inside the view.
  const dist = (r / Math.sin(THREE.MathUtils.degToRad(camera.fov / 2))) * 0.84;
  camera.near = r * 0.05;
  camera.far = dist * 10;
  camera.updateProjectionMatrix();
  // For the mean, the starting view is anterior with the base up, from two vectors the build
  // measured on the source coordinates. A study frame has no such vectors: look along -z.
  camera.up.fromArray(view.up).normalize();
  camera.position.copy(sphere.center).addScaledVector(new THREE.Vector3().fromArray(view.anterior).normalize(), dist);
  controls.target.copy(sphere.center);
  controls.minDistance = r * 1.1;
  controls.maxDistance = dist * 3;
  controls.update();
  controls.saveState();
  state.radius = r;
  state.initial = { position: camera.position.clone(), target: controls.target.clone() };
}

function buildStructureList(meshes) {
  const list = $('structures');
  list.textContent = '';
  for (const m of meshes) {
    const id = m.userData.structure;
    const label = document.createElement('label');
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = true;
    cb.dataset.structure = id;
    cb.addEventListener('change', () => { m.visible = cb.checked; });
    label.append(cb, ` ${m.userData.label || state.names[String(id)] || `structure ${id}`}`);
    list.append(label);
  }
  $('all-on').onclick = () => list.querySelectorAll('input').forEach((cb) => { cb.checked = true; cb.dispatchEvent(new Event('change')); });
  $('all-off').onclick = () => list.querySelectorAll('input').forEach((cb) => { cb.checked = false; cb.dispatchEvent(new Event('change')); });
}

function buildSegments(meshes) {
  const seg = state.manifest.output.segments;
  const cb = $('segments');
  const reason = $('segments-reason');
  const legend = $('legend');
  legend.textContent = '';
  AHA.forEach((name, i) => {
    const li = document.createElement('li');
    li.style.setProperty('--c', `#${SEGMENT_COLOURS[i].toString(16).padStart(6, '0')}`);
    li.textContent = `${i + 1} ${name}`;
    legend.append(li);
  });

  // One colour attribute shared by every structure: segment colour on the left ventricle,
  // one neutral tone everywhere else.
  const segAttr = meshes[0].geometry.getAttribute('_segment');
  const n = segAttr.count;
  const colours = new Float32Array(n * 3);
  const c = new THREE.Color();
  for (let i = 0; i < n; i++) {
    const s = segAttr.getX(i);
    if (s > 0) c.setHex(SEGMENT_COLOURS[s - 1]); else c.copy(UNSEGMENTED);
    colours[3 * i] = c.r; colours[3 * i + 1] = c.g; colours[3 * i + 2] = c.b;
  }
  const attr = new THREE.BufferAttribute(colours, 3);
  meshes.forEach((m) => m.geometry.setAttribute('color', attr));

  state.segmentCounts = () => {
    const out = {};
    for (const m of meshes) {
      const idx = m.geometry.index.array;
      const seen = new Set();
      let coloured = 0;
      for (let k = 0; k < idx.length; k++) {
        const v = idx[k];
        if (seen.has(v)) continue;
        seen.add(v);
        if (segAttr.getX(v) > 0) coloured++;
      }
      out[m.userData.structure] = coloured;
    }
    return out;
  };

  const apply = () => {
    const on = cb.checked;
    meshes.forEach((m) => { m.material = on ? m.userData.segmented : m.userData.plain; });
    legend.hidden = !on;
  };
  cb.onchange = apply;

  if (seg.shipped) {
    cb.disabled = false;
    cb.removeAttribute('aria-disabled');
    reason.textContent = `Derived from the coordinates the mesh carries; origin at PHI ${seg.origin_phi_deg} degrees. Off by default.`;
  } else {
    cb.checked = false;
    cb.disabled = true;
    cb.setAttribute('aria-disabled', 'true');
    reason.textContent = `Not available: the insertion check failed, ${seg.reason}; checked ${state.manifest.built}. `;
    const a = document.createElement('a');
    a.href = '/projects/ale/derived-heart-geometry';
    a.textContent = 'Evidence';
    reason.append(a);
  }
  apply();
}

const sphereGeometry = new THREE.SphereGeometry(1, 20, 14);

function addPoint(x, y, z) {
  const doc = state.modes.active;
  if (!doc || !doc.bounds) return;
  const r = state.radius * 0.012;
  const mesh = new THREE.Mesh(sphereGeometry, new THREE.MeshLambertMaterial({ color: POINT_COLOUR }));
  mesh.scale.setScalar(r);
  mesh.position.set(x, y, z);
  doc.group.add(mesh);
  doc.points.push({ x, y, z, mesh, outside: !doc.bounds.containsPoint(mesh.position) });
  renderPoints();
}

function removePoint(i) {
  const doc = state.modes.active;
  const p = doc.points.splice(i, 1)[0];
  if (p) { doc.group.remove(p.mesh); p.mesh.material.dispose(); }
  renderPoints();
}

function renderPoints() {
  const doc = state.modes.active;
  const list = $('points');
  list.textContent = '';
  if (!doc) return;
  doc.points.forEach((p, i) => {
    const li = document.createElement('li');
    li.textContent = `${p.x}, ${p.y}, ${p.z} in ${doc.frame}`;
    if (p.outside) {
      const f = document.createElement('span');
      f.className = 'flag';
      f.textContent = ' outside the geometry';
      li.append(f);
    }
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = 'Remove';
    b.addEventListener('click', () => removePoint(i));
    li.append(b);
    list.append(li);
  });
}

let pendingFiles = null;

function showReadError(err) {
  const e = $('error');
  e.hidden = false;
  e.textContent = `The export could not be read: ${err.message}. The view is unchanged.`;
}

function segmentsUnavailableForStudy() {
  const cb = $('segments');
  cb.checked = false;
  cb.disabled = true;
  cb.setAttribute('aria-disabled', 'true');
  $('segments-reason').textContent = 'Not available in patient mode: a study shell carries no ventricular coordinates to derive segments from.';
  $('legend').hidden = true;
}

function openStudy(study) {
  const doc = new Document('patient', `Patient: ${study.label}, this study's own frame`,
    `this study's own frame (${study.source}), millimetres`);
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(study.geometry.positions, 3));
  geometry.setIndex(new THREE.BufferAttribute(study.geometry.indices, 1));
  geometry.computeVertexNormals();
  const shell = new THREE.Mesh(geometry, new THREE.MeshLambertMaterial({ color: 0xc9b8a8, side: THREE.DoubleSide }));
  shell.name = 'shell';
  shell.userData.structure = 0;
  shell.userData.label = `${study.label} shell`;
  const model = new THREE.Group();
  model.add(shell);
  doc.model = model;
  doc.group.add(model);
  doc.bounds = new THREE.Box3().setFromObject(model);
  const r = doc.bounds.getBoundingSphere(new THREE.Sphere()).radius;
  let mapped = 0, ablation = 0;
  for (const pt of study.points) {
    const colour = pt.origin === 'ablation' ? ABLATION_COLOUR : MAPPED_COLOUR;
    if (pt.origin === 'ablation') ablation++; else mapped++;
    const s = new THREE.Mesh(sphereGeometry, new THREE.MeshLambertMaterial({ color: colour }));
    s.scale.setScalar(r * 0.015);
    s.position.fromArray(pt.position);
    s.name = pt.label;
    s.userData.origin = pt.origin;
    doc.studyPoints.push(s);
    doc.group.add(s);
  }
  doc.study = { source: study.source, label: study.label, mapped, ablation };
  doc.studyPoints.forEach((s, i) => { s.userData.values = study.points[i].values || null; });
  doc.files = state.lastFiles || null;
  doc.vertexCount = study.geometry.positions.length / 3;
  doc.valueFields = null;
  $('values-box').hidden = false;
  buildValueControl(doc);
  state.modes.activate(doc);
  state.radius = r;
  frameCamera(doc.bounds, STUDY_VIEW);
  buildStructureList([shell]);
  segmentsUnavailableForStudy();
  $('error').hidden = true;
}

async function onCartoFolder(files) {
  try {
    const maps = listMaps(files);
    if (maps.length === 0) throw new ReadError('expected at least one .mesh file in the folder, found none');
    if (maps.length === 1) {
      await openCartoMap(files, maps[0]);
      return;
    }
    pendingFiles = files;
    const select = $('map-choice');
    select.textContent = '';
    for (const name of maps) {
      const o = document.createElement('option');
      o.value = name;
      o.textContent = name;
      select.append(o);
    }
    $('map-chooser').hidden = false;
  } catch (err) {
    showReadError(err);
  }
}

async function openCartoMap(files, map) {
  try {
    state.lastFiles = files;
    const study = await readCarto(files, map);
    $('map-chooser').hidden = true;
    pendingFiles = null;
    openStudy(study);
  } catch (err) {
    showReadError(err);
  }
}

async function closeStudy() {
  await openMean();
  $('error').hidden = true;
}

function wireImports() {
  const input = $('pick-carto');
  if (!input) return;
  $('load-carto').addEventListener('click', () => { input.value = ''; input.click(); });
  input.addEventListener('change', () => { if (input.files && input.files.length) onCartoFolder(input.files); });
  $('map-open').addEventListener('click', () => { if (pendingFiles) openCartoMap(pendingFiles, $('map-choice').value); });
  $('close-study').querySelector('button').addEventListener('click', closeStudy);
  const argo = $('pick-argo');
  $('load-argo').addEventListener('click', () => { argo.value = ''; argo.click(); });
  argo.addEventListener('change', async () => {
    if (!argo.files || !argo.files.length) return;
    try { state.lastFiles = argo.files; openStudy(await readArgo(argo.files)); } catch (err) { showReadError(err); }
  });
}

// Which way is which, for the standard views. Returns {anterior, up, left} unit vectors in the
// frame of the active document, or null when that frame's convention is unverified.
function axesOf(doc) {
  let v = null;
  if (doc.kind === 'mean') v = state.manifest.output.view || null;
  else if (doc.study) v = STUDY_AXES[doc.study.source] || null;
  if (!v) return null;
  const anterior = new THREE.Vector3().fromArray(v.anterior).normalize();
  const up = new THREE.Vector3().fromArray(v.up).normalize();
  const left = new THREE.Vector3().crossVectors(up, anterior).normalize();   // S x A = L in a right-handed frame
  return { anterior, up, left };
}

// Camera direction (from the centre towards the camera) and camera up for each standard view.
function standardView(name, ax) {
  const rad = THREE.MathUtils.degToRad(OBLIQUE_DEG);
  const c = Math.cos(rad), s = Math.sin(rad);
  const A = ax.anterior, P = A.clone().negate(), L = ax.left, R = L.clone().negate(), S = ax.up, I = S.clone().negate();
  const mix = (a, b) => a.clone().multiplyScalar(c).addScaledVector(b, s).normalize();
  switch (name) {
    case 'AP': return { dir: A, up: S };
    case 'PA': return { dir: P, up: S };
    case 'LL': return { dir: L, up: S };
    case 'RL': return { dir: R, up: S };
    case 'SUP': return { dir: S, up: A };
    case 'INF': return { dir: I, up: A };
    case 'RAO': return { dir: mix(A, R), up: S };
    case 'LAO': return { dir: mix(A, L), up: S };
    case 'RPO': return { dir: mix(P, R), up: S };
    case 'LPO': return { dir: mix(P, L), up: S };
    default: return null;
  }
}

function goToView(name) {
  const doc = state.modes.active;
  const ax = doc && axesOf(doc);
  if (!ax) return;
  const v = standardView(name, ax);
  const { camera, controls } = state;
  const dist = controls.getDistance();
  camera.up.copy(v.up);
  camera.position.copy(controls.target).addScaledVector(v.dir, dist);
  controls.enableDamping = false;
  controls.update();
  controls.enableDamping = true;
}

function applyLook() {
  const on = $('maplook').checked;
  document.body.classList.toggle('maplook', on);
  const look = on ? LOOK.map : LOOK.plain;
  const doc = state.modes.active;
  if (state.scene) state.scene.background.setHex(look.background);
  if (doc && doc.kind === 'patient' && doc.model) {
    if (!doc.valuesOn) doc.model.traverse((o) => { if (o.isMesh) o.material.color.setHex(look.shell); });
    for (const s of doc.studyPoints) {
      if (s.userData.origin === 'ablation') {
        s.material.color.setHex(look.ablation);
        s.scale.setScalar(state.radius * look.ablationScale);
      }
    }
  }
  // Lesion counter, as the mapping system shows it, in patient mode with the look on.
  const lesions = $('lesions');
  if (on && doc && doc.study) {
    lesions.textContent = `Lesions: ${doc.study.ablation}`;
    lesions.hidden = false;
  } else {
    lesions.hidden = true;
  }
  // Standard views: shown with the look, live only when the frame's axes are known.
  const strip = $('orient');
  const reason = $('orient-reason');
  strip.hidden = !on;
  const ax = doc ? axesOf(doc) : null;
  for (const b of strip.querySelectorAll('button')) {
    b.disabled = !ax;
    if (ax) b.removeAttribute('aria-disabled'); else b.setAttribute('aria-disabled', 'true');
  }
  if (on && !ax && doc && doc.study) {
    reason.textContent = `Not available: the publisher of this ${doc.study.source.toUpperCase()} data states no patient frame for its coordinates, checked 2026-09-26.`;
    reason.hidden = false;
  } else {
    reason.hidden = true;
  }
}

function wireLook() {
  $('maplook').addEventListener('change', applyLook);
  for (const b of $('orient').querySelectorAll('button')) {
    b.addEventListener('click', () => goToView(b.dataset.view));
  }
  applyLook();
}

// ---- A study's own values on the study's own geometry (FR-006a, ADR-0010) ------------------

function scaleColour(x, lo, hi, out) {
  if (!Number.isFinite(x)) return out.setHex(NO_VALUE);
  const u = Math.min(1, Math.max(0, (x - lo) / (hi - lo || 1)));
  const k = u * (VALUE_SCALE.length - 1);
  const i = Math.min(VALUE_SCALE.length - 2, Math.floor(k));
  const a = new THREE.Color(VALUE_SCALE[i]), b = new THREE.Color(VALUE_SCALE[i + 1]);
  return out.copy(a).lerp(b, k - i);
}

function finiteRange(arr) {
  let lo = Infinity, hi = -Infinity;
  for (const x of arr) if (Number.isFinite(x)) { if (x < lo) lo = x; if (x > hi) hi = x; }
  return Number.isFinite(lo) ? [lo, hi] : [0, 1];
}

// Default display range: the 2nd and 98th percentiles, so a few extreme values do not wash out
// the map. The reader can type any other range; the full range is always stated on the bar.
function percentileRange(arr) {
  const v = Array.from(arr).filter(Number.isFinite).sort((a, b) => a - b);
  if (!v.length) return [0, 1];
  const at = (q) => v[Math.min(v.length - 1, Math.floor(q * (v.length - 1)))];
  const lo = at(0.02), hi = at(0.98);
  return hi > lo ? [lo, hi] : finiteRange(v);
}

// The clip range from the inputs, or the percentile default when they are blank or out of order.
function clipRange(data, reset) {
  const lowEl = $('value-low'), highEl = $('value-high');
  let lo = parseFloat(lowEl.value), hi = parseFloat(highEl.value);
  if (reset || !Number.isFinite(lo) || !Number.isFinite(hi) || hi <= lo) {
    [lo, hi] = percentileRange(data);
    lowEl.value = lo.toFixed(2);
    highEl.value = hi.toFixed(2);
  }
  return [lo, hi];
}

// What this document can colour by: per-vertex fields (ARGO) or per-point fields (CARTO).
function valueOptions(doc) {
  if (doc.study.source === 'argo') {
    return [
      { key: 'voltage', label: 'Bipolar voltage', unit: 'mV', file: 'MESHcoloring.txt', where: 'shell' },
      { key: 'lat', label: 'Local activation time', unit: 'ms', file: 'MESHcoloring.txt', where: 'shell' },
    ];
  }
  return [
    { key: 'bipolar_mV', label: 'Bipolar voltage', unit: 'mV', file: `${doc.study.label}_car.txt`, where: 'points' },
    { key: 'unipolar_mV', label: 'Unipolar voltage', unit: 'mV', file: `${doc.study.label}_car.txt`, where: 'points' },
  ];
}

function buildValueControl(doc) {
  const select = $('value-field');
  select.textContent = '';
  for (const o of valueOptions(doc)) {
    const opt = document.createElement('option');
    opt.value = o.key;
    opt.textContent = `${o.label}, ${o.unit}, from ${o.file}`;
    select.append(opt);
  }
  $('value-on').checked = false;
  $('value-bar').hidden = true;
  $('value-low').value = '';
  $('value-high').value = '';
  state.valueKey = null;
  $('value-note').textContent = valueOptions(doc)[0].where === 'shell'
    ? 'Colours the shell by a value this export carries per vertex. Unmapped vertices stay grey.'
    : 'This export carries voltages per mapped point, not per vertex, so the points are coloured and the shell is not.';
}

function clearValues(doc) {
  doc.valuesOn = false;
  if (doc.model) doc.model.traverse((o) => { if (o.isMesh) { o.material.vertexColors = false; o.material.needsUpdate = true; } });
  for (const s of doc.studyPoints) if (s.userData.origin === 'mapped') s.material.color.setHex(MAPPED_COLOUR);
  $('value-bar').hidden = true;
  applyLook();
}

async function applyValues() {
  const doc = state.modes.active;
  if (!doc || doc.kind !== 'patient') return;
  const on = $('value-on').checked;
  if (!on) { clearValues(doc); return; }
  const key = $('value-field').value;
  const opt = valueOptions(doc).find((o) => o.key === key);
  try {
    let data, lo, hi;
    if (opt.where === 'shell') {
      if (!doc.valueFields) {
        if (!doc.files) throw new ReadError('the folder is no longer available; load the study again');
        doc.valueFields = (await readArgoValues(doc.files, doc.vertexCount)).fields;
      }
      data = doc.valueFields[key].data;
      [lo, hi] = clipRange(data, state.valueKey !== key);
      const colours = new Float32Array(data.length * 3);
      const c = new THREE.Color();
      for (let i = 0; i < data.length; i++) {
        scaleColour(data[i], lo, hi, c);
        colours[3 * i] = c.r; colours[3 * i + 1] = c.g; colours[3 * i + 2] = c.b;
      }
      doc.model.traverse((o) => {
        if (!o.isMesh) return;
        o.geometry.setAttribute('color', new THREE.BufferAttribute(colours, 3));
        o.material.color.setHex(0xffffff);
        o.material.vertexColors = true;
        o.material.needsUpdate = true;
      });
    } else {
      const pts = doc.studyPoints.filter((s) => s.userData.origin === 'mapped');
      data = pts.map((s) => (s.userData.values && s.userData.values[key] !== undefined) ? s.userData.values[key] : NaN);
      [lo, hi] = clipRange(data, state.valueKey !== key);
      const c = new THREE.Color();
      pts.forEach((s, i) => { s.material.color.copy(scaleColour(data[i], lo, hi, c)); });
    }
    doc.valuesOn = true;
    state.valueKey = key;
    const [fullLo, fullHi] = finiteRange(data);
    const bar = $('value-bar');
    bar.hidden = false;
    $('value-bar-label').textContent = `${opt.label}, ${opt.unit}, shown from ${lo.toFixed(2)} to ${hi.toFixed(2)}; the data run ${fullLo.toFixed(2)} to ${fullHi.toFixed(2)}. ${doc.study.label}'s own values from ${opt.file}, unchanged. Not a result of this project.`;
    $('value-bar-scale').style.background = `linear-gradient(to right, ${VALUE_SCALE.map((h) => '#' + h.toString(16).padStart(6, '0')).join(', ')})`;
  } catch (err) {
    $('value-on').checked = false;
    clearValues(doc);
    showReadError(err);
  }
}

function wireValues() {
  $('value-on').addEventListener('change', applyValues);
  $('value-field').addEventListener('change', () => { if ($('value-on').checked) applyValues(); });
  for (const id of ['value-low', 'value-high']) {
    $(id).addEventListener('change', () => { if ($('value-on').checked) applyValues(); });
  }
}

function wireControls() {
  $('reset').addEventListener('click', () => {
    // With damping on, a drag leaves a decaying delta that would move the camera after reset.
    // One undamped update applies and clears it first.
    const c = state.controls;
    c.enableDamping = false;
    c.update();
    c.reset();
    c.enableDamping = true;
  });
  const read = (id) => {
    const el = $(id);
    const v = parseFloat(el.value);
    el.setCustomValidity(Number.isFinite(v) ? '' : 'a number is needed');
    return v;
  };
  const add = () => {
    const x = read('cx'), y = read('cy'), z = read('cz');
    if ([x, y, z].every(Number.isFinite)) addPoint(x, y, z);
    else $('cx').reportValidity();
  };
  $('add-point').addEventListener('click', add);
  for (const id of ['cx', 'cy', 'cz']) {
    $(id).addEventListener('keydown', (e) => { if (e.key === 'Enter') add(); });
  }
  $('clear-points').addEventListener('click', () => {
    const doc = state.modes.active;
    while (doc.points.length) removePoint(0);
  });
}
