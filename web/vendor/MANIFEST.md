# Vendored library

| File | From | SHA-256 |
|---|---|---|
| `three.module.min.js` | three.js 0.170.0, https://cdn.jsdelivr.net/npm/three@0.170.0/ | `08fd7545d13d2c7fb65ab691530a802dafefd638596501854f267d0fb13c39e7` |
| `OrbitControls.js` | three.js 0.170.0, https://cdn.jsdelivr.net/npm/three@0.170.0/ | `80efaadea4f8a636a65fb0bd08bfef62f3d93a0bb94e2e7500f23176c5c07f4e` |
| `GLTFLoader.js` | three.js 0.170.0, https://cdn.jsdelivr.net/npm/three@0.170.0/ | `8a7db5a19d1018d79fb9a7a8b8372f317682027321a67d86023002e264ea479d` |
| `BufferGeometryUtils.js` | three.js 0.170.0, https://cdn.jsdelivr.net/npm/three@0.170.0/ | `c25b7930e570e9ec56173cd3b866ec8d2e10016630db3937efb439daf1cedbf6` |
| `LICENSE` | three.js 0.170.0, https://cdn.jsdelivr.net/npm/three@0.170.0/ | `4c40a1ef62450b857c3b2aaf294936304cd552d965fbcd9d32d4c5bcf4ba4454` |

Licence: MIT, in `LICENSE`.

One edit was made after download: in `GLTFLoader.js` the import of `BufferGeometryUtils.js` was
changed from `../utils/BufferGeometryUtils.js` to `./BufferGeometryUtils.js`, because the files are
vendored flat. Its hash above is of the edited file. Nothing else was changed.

The page maps the bare specifier `three` to `three.module.min.js` with an import map.
