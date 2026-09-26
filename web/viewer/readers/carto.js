// CARTO 3 export reader. Reads three named files from the folder the user picked and nothing
// else: the map shell, the map's point list, and the VisiTag ablation sites (contracts/study-shape.md).
//
// Verified 2026-09-25 against a real porcine export (Zenodo 10.5281/zenodo.6651600). In that export
// the point positions are not in <map>_Points_Export.xml, which only names per-point files; they
// are in <map>_car.txt, one line per point starting with P, id in the third field, x y z in the
// fifth to seventh. VisiTag sites are in VisiTagExport/Sites.txt with a header naming X, Y, Z.

export class ReadError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ReadError';
  }
}

const MESH = /^(.+)\.mesh$/i;

function byName(files, name) {
  for (const f of files) if (f.name === name) return f;
  return null;
}

function visiTagSites(files) {
  for (const f of files) {
    const rel = (f.webkitRelativePath || '').replace(/\\/g, '/');
    if (f.name === 'Sites.txt' && /(^|\/)VisiTagExport\/Sites\.txt$/.test(rel)) return f;
  }
  return null;
}

// Names of the maps in the folder, from the .mesh files present.
export function listMaps(files) {
  const names = [];
  for (const f of files) {
    const m = MESH.exec(f.name);
    if (m) names.push(m[1]);
  }
  return names.sort();
}

function section(text, name) {
  const start = text.indexOf(`[${name}]`);
  if (start < 0) throw new ReadError(`expected a [${name}] section in the mesh file, found none`);
  const rest = text.slice(start + name.length + 2);
  const end = rest.search(/^\[/m);
  return end < 0 ? rest : rest.slice(0, end);
}

function rows(block) {
  const out = [];
  for (const line of block.split(/\r?\n/)) {
    const eq = line.indexOf('=');
    if (eq < 0 || line.trimStart().startsWith(';')) continue;
    const fields = line.slice(eq + 1).trim().split(/\s+/);
    if (fields.length) out.push(fields);
  }
  return out;
}

export function parseMesh(text) {
  const header = section(text, 'GeneralAttributes');
  const nv = parseInt((/NumVertex\s*=\s*(\d+)/.exec(header) || [])[1], 10);
  const nt = parseInt((/NumTriangle\s*=\s*(\d+)/.exec(header) || [])[1], 10);
  if (!Number.isFinite(nv) || !Number.isFinite(nt)) {
    throw new ReadError('expected NumVertex and NumTriangle in [GeneralAttributes], found neither');
  }
  const v = rows(section(text, 'VerticesSection'));
  if (v.length !== nv) throw new ReadError(`expected ${nv} vertices, found ${v.length}`);
  const positions = new Float32Array(nv * 3);
  for (let i = 0; i < nv; i++) {
    const [x, y, z] = v[i];
    positions[3 * i] = +x; positions[3 * i + 1] = +y; positions[3 * i + 2] = +z;
    if (!Number.isFinite(positions[3 * i]) || !Number.isFinite(positions[3 * i + 1]) || !Number.isFinite(positions[3 * i + 2])) {
      throw new ReadError(`expected three numbers for vertex ${i}, found ${v[i].slice(0, 3).join(' ')}`);
    }
  }
  const t = rows(section(text, 'TrianglesSection'));
  if (t.length !== nt) throw new ReadError(`expected ${nt} triangles, found ${t.length}`);
  const kept = [];
  for (let i = 0; i < nt; i++) {
    const r = t[i];
    const group = r.length >= 7 ? parseInt(r[6], 10) : 0;
    if (group < 0) continue;   // CARTO marks removed triangles with a negative group id
    const a = parseInt(r[0], 10), b = parseInt(r[1], 10), c = parseInt(r[2], 10);
    if ([a, b, c].some((k) => !(k >= 0 && k < nv))) throw new ReadError(`triangle ${i} points outside the ${nv} vertices`);
    kept.push(a, b, c);
  }
  return { positions, indices: Uint32Array.from(kept) };
}

export function parseCar(text) {
  const points = [];
  for (const line of text.split(/\r?\n/)) {
    if (!/^P\s/.test(line)) continue;
    const f = line.trim().split(/\s+/);
    if (f.length < 7) throw new ReadError(`expected at least seven fields on a point line, found ${f.length}`);
    const position = [+f[4], +f[5], +f[6]];
    if (position.some((x) => !Number.isFinite(x))) throw new ReadError(`expected x y z for point ${f[2]}, found ${f.slice(4, 7).join(' ')}`);
    // Fields 11 and 12 are unipolar and bipolar voltage in mV, matching the per-point XML.
    const values = {};
    if (f.length > 11 && Number.isFinite(+f[10])) values.unipolar_mV = +f[10];
    if (f.length > 11 && Number.isFinite(+f[11])) values.bipolar_mV = +f[11];
    points.push({ label: `P${f[2]}`, position, origin: 'mapped', values });
  }
  return points;
}

export function parseSites(text) {
  const lines = text.split(/\r?\n/).filter((l) => l.trim());
  if (!lines.length) return [];
  const head = lines[0].trim().split(/\s+/);
  const ix = head.indexOf('X'), iy = head.indexOf('Y'), iz = head.indexOf('Z'), ii = head.indexOf('SiteIndex');
  if (ix < 0 || iy < 0 || iz < 0) throw new ReadError('expected columns X, Y and Z in Sites.txt, found ' + head.join(' '));
  const out = [];
  for (const line of lines.slice(1)) {
    const f = line.trim().split(/\s+/);
    if (f.length <= Math.max(ix, iy, iz)) continue;
    const position = [+f[ix], +f[iy], +f[iz]];
    if (position.some((x) => !Number.isFinite(x))) continue;
    out.push({ label: `Site ${ii >= 0 ? f[ii] : out.length + 1}`, position, origin: 'ablation' });
  }
  return out;
}

// The Study for one map (contracts/study-shape.md). Opens <map>.mesh, <map>_car.txt and, if present,
// VisiTagExport/Sites.txt. Nothing else in the folder is read.
export async function readCarto(files, map) {
  const meshFile = byName(files, `${map}.mesh`);
  if (!meshFile) throw new ReadError(`expected ${map}.mesh in the folder, found no such file`);
  const carFile = byName(files, `${map}_car.txt`);
  if (!carFile) throw new ReadError(`expected ${map}_car.txt beside the mesh, found no such file`);
  const geometry = parseMesh(await meshFile.text());
  const points = parseCar(await carFile.text());
  const sites = visiTagSites(files);
  if (sites) points.push(...parseSites(await sites.text()));
  return { source: 'carto', label: map, frame: 'study', geometry, points };
}
