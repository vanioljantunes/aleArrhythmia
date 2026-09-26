// The two documents and the switch between them (research R-006).
//
// A Document owns its geometry and its point list. Only one Document is ever attached to the scene,
// so a point cannot be drawn on the wrong geometry: there is no point list outside a Document.
import * as THREE from 'three';

export class Document {
  constructor(kind, label, frame) {
    this.kind = kind;          // 'mean' or 'patient'
    this.label = label;        // what the mode indicator shows
    this.frame = frame;        // the frame every coordinate in this document belongs to
    this.group = new THREE.Group();
    this.group.name = kind;
    this.points = [];          // {x, y, z, mesh, outside}
    this.model = null;         // THREE.Group of structure meshes
    this.bounds = null;        // THREE.Box3 of the model
  }

  dispose() {
    this.points.length = 0;
    this.model = null;
    this.bounds = null;
    for (const child of [...this.group.children]) {
      this.group.remove(child);
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

  // Attach doc, detaching and disposing whichever document was active before.
  activate(doc) {
    if (this.active && this.active !== doc) {
      this.scene.remove(this.active.group);
      this.active.dispose();
    }
    this.active = doc;
    this[doc.kind] = doc;
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
