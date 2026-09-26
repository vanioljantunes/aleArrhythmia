// The two documents and the switch between them (research R-006).
//
// A Document owns its geometry and its point list. Only one Document is ever attached to the scene,
// so a point cannot be drawn on the wrong geometry: there is no point list outside a Document.
// Leaving the mean detaches its children and keeps them, so typed coordinates survive a study
// visit. Leaving a patient document disposes it: nothing of the study stays behind.
import * as THREE from 'three';

export class Document {
  constructor(kind, label, frame) {
    this.kind = kind;          // 'mean' or 'patient'
    this.label = label;        // what the mode indicator shows
    this.frame = frame;        // the frame every coordinate in this document belongs to
    this.group = new THREE.Group();
    this.group.name = kind;
    this.points = [];          // typed coordinates: {x, y, z, mesh, outside}
    this.studyPoints = [];     // spheres for a study's own points, patient documents only
    this.model = null;         // THREE.Group of structure meshes
    this.bounds = null;        // THREE.Box3 of the model
    this.study = null;         // {source, label, mapped, ablation} for a patient document
  }

  // Take every child out of the group but keep the references.
  sleep() {
    this.group.clear();
  }

  // Put the model and the points back into the group.
  wake() {
    if (this.model && this.model.parent !== this.group) this.group.add(this.model);
    for (const p of this.points) if (p.mesh.parent !== this.group) this.group.add(p.mesh);
    for (const s of this.studyPoints) if (s.parent !== this.group) this.group.add(s);
  }

  dispose() {
    const all = [this.model, ...this.points.map((p) => p.mesh), ...this.studyPoints].filter(Boolean);
    this.group.clear();
    this.points.length = 0;
    this.studyPoints.length = 0;
    this.model = null;
    this.bounds = null;
    this.study = null;
    for (const child of all) {
      child.traverse((o) => {
        if (o.geometry) o.geometry.dispose();
        if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => m.dispose());
      });
    }
  }
}

export class Modes {
  constructor(scene) {
    this.scene = scene;
    this.mean = null;
    this.patient = null;
    this.active = null;
    this.listeners = [];
  }

  // Attach doc. The document that was active is detached: a mean document sleeps, a patient
  // document is disposed and forgotten.
  activate(doc) {
    const out = this.active;
    if (out && out !== doc) {
      this.scene.remove(out.group);
      if (out.kind === 'patient') {
        out.dispose();
        this.patient = null;
      } else {
        out.sleep();
      }
    }
    this.active = doc;
    this[doc.kind] = doc;
    doc.wake();
    if (doc.group.parent !== this.scene) this.scene.add(doc.group);
    for (const f of this.listeners) f(doc);
  }

  inactive() {
    return this.active === this.mean ? this.patient : this.mean;
  }

  onChange(f) {
    this.listeners.push(f);
  }
}
