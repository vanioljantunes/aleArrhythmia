// ARGO reader (PhysioNet 10.13026/8gh2-e660). Reads four named plain-text files from one patient
// folder and nothing else (contracts/study-shape.md). MESHcoloring.txt holds voltage and activation
// values, which are results, and is never opened.
//
// Verified 2026-09-26 against the archive: every file is comma separated with a header row.
// XYZmesh.txt "X,Y,Z"; ConnectivityList.txt "node1,node2,node3", 1-based; POS_POINTS.txt
// "Point,X,Y,Z"; AblationPoints.txt "X,Y,Z".
import { ReadError } from './carto.js';

export { ReadError };

function byName(files, name) {
  for (const f of files) if (f.name === name) return f;
  return null;
}

function csv(text, name, expectedColumns) {
  const lines = text.split(/\r?\n/).filter((l) => l.trim());
  if (!lines.length) throw new ReadError(`expected a header row in ${name}, found an empty file`);
  const head = lines[0].replace(/^\ufeff/, '').trim().split(',').map((s) => s.trim());
  if (head.length !== expectedColumns) {
    throw new ReadError(`expected ${expectedColumns} columns in ${name}, found ${head.length} (${head.join(',')})`);
  }
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const f = lines[i].split(',').map(Number);
    if (f.length !== expectedColumns || f.some((x) => !Number.isFinite(x))) {
      throw new ReadError(`expected ${expectedColumns} numbers on line ${i + 1} of ${name}, found ${lines[i].slice(0, 40)}`);
    }
    rows.push(f);
  }
  return rows;
}

async function required(files, name) {
  const f = byName(files, name);
  if (!f) throw new ReadError(`expected ${name} in the folder, found no such file`);
  return f.text();
}

// The Study for one patient folder.
export async function readArgo(files) {
  const xyz = csv(await required(files, 'XYZmesh.txt'), 'XYZmesh.txt', 3);
  const tri = csv(await required(files, 'ConnectivityList.txt'), 'ConnectivityList.txt', 3);
  const pos = csv(await required(files, 'POS_POINTS.txt'), 'POS_POINTS.txt', 4);
  const abl = csv(await required(files, 'AblationPoints.txt'), 'AblationPoints.txt', 3);

  const nv = xyz.length;
  const positions = new Float32Array(nv * 3);
  xyz.forEach((r, i) => { positions[3 * i] = r[0]; positions[3 * i + 1] = r[1]; positions[3 * i + 2] = r[2]; });
  const indices = new Uint32Array(tri.length * 3);
  tri.forEach((r, i) => {
    for (let k = 0; k < 3; k++) {
      const v = r[k] - 1;   // the source is 1-based
      if (!(v >= 0 && v < nv)) throw new ReadError(`triangle ${i + 1} points at vertex ${r[k]}, outside 1 to ${nv}`);
      indices[3 * i + k] = v;
    }
  });
  const points = [
    ...pos.map((r) => ({ label: `P${r[0]}`, position: [r[1], r[2], r[3]], origin: 'mapped' })),
    ...abl.map((r, i) => ({ label: `Ablation ${i + 1}`, position: [r[0], r[1], r[2]], origin: 'ablation' })),
  ];
  const first = files[0] && files[0].webkitRelativePath ? files[0].webkitRelativePath.split('/')[0] : '';
  return { source: 'argo', label: first || 'ARGO study', frame: 'study', geometry: { positions, indices }, points };
}
