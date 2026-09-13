/**
 * ux-space Peer — thin three.js adapter.
 * Package name: "ux-space" (wraps three; product surface ≠ Channel demo "three").
 *
 * Plan IR (v: "1"): { graph: { nodes: [{ id, kind, ... }] } }
 * Soft 2 leftover: locked geometry map (box/sphere/plane/cylinder).
 * Soft 10 leftover: thin additive cone / torus (ConeGeometry /
 *   TorusGeometry). Soft 2 names KEEP. Not the catalog.
 * Soft 3 leftover: optional camera/light node kinds
 *   (perspective / ambient / directional). Mesh nodes still apply.
 * Soft 4 leftover: mesh rotation / scale + material {basic}
 *   (color + opacity → MeshBasicMaterial). Default mesh stays
 *   MeshStandardMaterial when material is absent. Camera may take rotation.
 * Soft 8 leftover: material.type {basic, standard}. standard →
 *   MeshStandardMaterial (color / opacity / metalness / roughness).
 * Soft 9 leftover: texture / gltf nodes. TextureLoader + GLTFLoader
 *   stay inside this adapter (not a public API dump). material.map
 *   is a texture node id. Load rides Cap-gated apply — no load()
 *   method.
 * Soft 6 leftover: optional mesh pickable. Pointer over the canvas
 *   raycasts pickable meshes and reports {node_id, point}. Hit becomes
 *   Channel Intent args via uxChannel.runAction when present — not a
 *   new pointer stack.
 * Soft 7 leftover: camera orbit / pan / zoom fields + Cap-gated
 *   call methods. Thin spherical pose — not a controls catalog.
 */
(function (global) {
  "use strict";
  if (!global.uxBridge) {
    console.warn("[ux-space] uxBridge missing");
    return;
  }

  var THREE_CDN =
    "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js";
  var GLTF_CDN =
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js";
  var BGU_CDN =
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/utils/BufferGeometryUtils.js";
  var loading = null;
  var gltfLoading = null;

  function loadThree() {
    if (global.THREE) return Promise.resolve(global.THREE);
    if (loading) return loading;
    loading = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = THREE_CDN;
      s.async = true;
      s.onload = function () {
        if (!global.THREE) reject(new Error("THREE global missing after load"));
        else resolve(global.THREE);
      };
      s.onerror = function () {
        loading = null;
        reject(new Error("Failed to load three.js CDN"));
      };
      document.head.appendChild(s);
    });
    return loading;
  }

  function isAllowedSrc(src) {
    if (typeof src !== "string" || !src.trim()) return false;
    var s = src.trim();
    if (s.indexOf("http://") === 0 || s.indexOf("https://") === 0 || s.charAt(0) === "/") {
      return true;
    }
    if (s.indexOf("://") !== -1) return false;
    var colon = s.indexOf(":");
    if (colon > 0 && /^[A-Za-z]+$/.test(s.slice(0, colon))) return false;
    return true;
  }

  function loadGltfLoader(THREE) {
    if (THREE.GLTFLoader) return Promise.resolve(THREE.GLTFLoader);
    if (gltfLoading) return gltfLoading;
    // JSM addon onto the day-1 UMD THREE global — not a second Three instance
    // and not a public GLTFLoader dump.
    function threeShimUrl() {
      var keys = [];
      for (var k in THREE) {
        if (/^[A-Za-z_$][A-Za-z0-9_$]*$/.test(k)) keys.push(k);
      }
      var shim =
        "const T = globalThis.THREE;\n" +
        keys
          .map(function (k) {
            return "export const " + k + " = T." + k + ";";
          })
          .join("\n") +
        "\nexport default T;\n";
      return URL.createObjectURL(new Blob([shim], { type: "text/javascript" }));
    }
    function asThreeModule(src, shimUrl) {
      return src.replace(/from\s+['"]three['"]/g, "from '" + shimUrl + "'");
    }
    gltfLoading = Promise.all([
      fetch(GLTF_CDN).then(function (res) {
        if (!res.ok) throw new Error("Failed to load GLTFLoader");
        return res.text();
      }),
      fetch(BGU_CDN).then(function (res) {
        if (!res.ok) throw new Error("Failed to load BufferGeometryUtils");
        return res.text();
      }),
    ]).then(function (texts) {
      var shimUrl = threeShimUrl();
      var bguUrl = URL.createObjectURL(
        new Blob([asThreeModule(texts[1], shimUrl)], { type: "text/javascript" })
      );
      var gltfSrc = asThreeModule(texts[0], shimUrl).replace(
        /from\s+['"]\.\.\/utils\/BufferGeometryUtils\.js['"]/g,
        "from '" + bguUrl + "'"
      );
      return import(URL.createObjectURL(new Blob([gltfSrc], { type: "text/javascript" })));
    })
      .then(function (mod) {
        if (!mod || !mod.GLTFLoader) throw new Error("GLTFLoader missing after load");
        THREE.GLTFLoader = mod.GLTFLoader;
        return THREE.GLTFLoader;
      })
      .catch(function (err) {
        gltfLoading = null;
        throw err;
      });
    return gltfLoading;
  }

  function allNodes(plan) {
    var graph = (plan && plan.graph) || plan || {};
    return graph.nodes || [];
  }

  function isMesh(node) {
    return !node.kind || node.kind === "node";
  }

  function firstMesh(plan) {
    var nodes = allNodes(plan);
    for (var i = 0; i < nodes.length; i++) {
      if (isMesh(nodes[i])) return nodes[i];
    }
    return {};
  }

  function firstCamera(plan) {
    var nodes = allNodes(plan);
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].kind === "camera") return nodes[i];
    }
    return null;
  }

  function lightNodes(plan) {
    var nodes = allNodes(plan);
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].kind === "light") out.push(nodes[i]);
    }
    return out;
  }

  function textureNodes(plan) {
    var nodes = allNodes(plan);
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].kind === "texture") out.push(nodes[i]);
    }
    return out;
  }

  function gltfNodes(plan) {
    var nodes = allNodes(plan);
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].kind === "gltf") out.push(nodes[i]);
    }
    return out;
  }

  // Soft 2 leftover: thin geometry map. Soft 10 leftover: cone / torus.
  // Not the full three.js catalog.
  var GEOMETRY = {
    "box": function (THREE) {
      return new THREE.BoxGeometry(1.4, 1.4, 1.4);
    },
    "sphere": function (THREE) {
      return new THREE.SphereGeometry(0.85, 32, 24);
    },
    "plane": function (THREE) {
      return new THREE.PlaneGeometry(1.8, 1.8);
    },
    "cylinder": function (THREE) {
      return new THREE.CylinderGeometry(0.7, 0.7, 1.4, 32);
    },
    "cone": function (THREE) {
      return new THREE.ConeGeometry(0.75, 1.4, 32);
    },
    "torus": function (THREE) {
      return new THREE.TorusGeometry(0.7, 0.25, 16, 32);
    },
  };

  function geometryFor(THREE, shape) {
    var make = GEOMETRY[shape] || GEOMETRY.box;
    return make(THREE);
  }

  // Soft 4 leftover: material.color wins over top-level color shorthand.
  function meshColor(node) {
    return (node.material && node.material.color) || node.color || "#6366f1";
  }

  function applyRotation(obj, rotation) {
    if (!rotation) return;
    obj.rotation.set(rotation[0], rotation[1], rotation[2]);
  }

  function applyScale(obj, scale) {
    if (scale == null) return;
    if (typeof scale === "number") {
      obj.scale.set(scale, scale, scale);
    } else {
      obj.scale.set(scale[0], scale[1], scale[2]);
    }
  }

  global.uxBridge.register("ux-space", {
    mount: function (el, props) {
      return loadThree().then(function (THREE) {
        props = props || {};
        var plan = props.plan || props;
        var node = firstMesh(plan);
        el.style.position = el.style.position || "relative";
        el.style.overflow = "hidden";

        var width = el.clientWidth || 640;
        var height = el.clientHeight || 360;

        var scene = new THREE.Scene();
        scene.background = new THREE.Color("#0b1020");

        var camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
        camera.position.set(0, 0.35, 4.2);

        var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.setSize(width, height, false);
        renderer.domElement.style.width = "100%";
        renderer.domElement.style.height = "100%";
        renderer.domElement.style.display = "block";
        el.innerHTML = "";
        el.appendChild(renderer.domElement);

        var lightObjs = [];

        function clearLights() {
          for (var i = 0; i < lightObjs.length; i++) {
            scene.remove(lightObjs[i]);
          }
          lightObjs = [];
        }

        function applyLights(next) {
          clearLights();
          var authored = lightNodes(next);
          if (!authored.length) {
            var amb = new THREE.AmbientLight(0xffffff, 0.5);
            var key = new THREE.DirectionalLight(0xffffff, 1.0);
            key.position.set(3, 4, 5);
            scene.add(amb);
            scene.add(key);
            lightObjs.push(amb, key);
            return;
          }
          for (var i = 0; i < authored.length; i++) {
            var ln = authored[i];
            var color = ln.color || "#ffffff";
            var obj;
            if (ln.light === "directional") {
              obj = new THREE.DirectionalLight(color, 1.0);
              if (ln.position) {
                obj.position.set(ln.position[0], ln.position[1], ln.position[2]);
              } else {
                obj.position.set(3, 4, 5);
              }
            } else {
              obj = new THREE.AmbientLight(color, 0.5);
            }
            scene.add(obj);
            lightObjs.push(obj);
          }
        }

        var control = { orbit: null, pan: null, zoom: null };

        function applyCameraControl(cam) {
          if (!cam) return;
          if (cam.orbit) control.orbit = cam.orbit;
          if (cam.pan) control.pan = cam.pan;
          if (cam.zoom != null) control.zoom = cam.zoom;
          var orbit = control.orbit || {};
          var pan = control.pan || {};
          var distance = typeof control.zoom === "number" ? control.zoom : 4.2;
          var azimuth = orbit.azimuth != null ? orbit.azimuth : 0;
          var polar = orbit.polar != null ? orbit.polar : Math.PI / 2;
          var tx = pan.x != null ? pan.x : 0;
          var ty = pan.y != null ? pan.y : 0;
          var x = tx + distance * Math.sin(polar) * Math.sin(azimuth);
          var y = ty + distance * Math.cos(polar);
          var z = distance * Math.sin(polar) * Math.cos(azimuth);
          camera.position.set(x, y, z);
          camera.rotation.set(polar - Math.PI / 2, azimuth, 0);
        }

        function applyCameraNode(next) {
          var cam = firstCamera(next);
          if (!cam) return;
          if (cam.orbit || cam.pan || cam.zoom != null) {
            applyCameraControl(cam);
            return;
          }
          if (cam.position) {
            camera.position.set(cam.position[0], cam.position[1], cam.position[2]);
          }
          applyRotation(camera, cam.rotation);
        }

        applyCameraNode(plan);
        applyLights(plan);

        var mat = new THREE.MeshStandardMaterial({
          color: meshColor(node),
          metalness: 0.35,
          roughness: 0.35,
        });
        var mesh = new THREE.Mesh(geometryFor(THREE, node.shape), mat);

        function isBasicMaterial(n) {
          return !!(n.material && (n.material.type === "basic" || !n.material.type));
        }

        function isStandardMaterial(n) {
          return !!(n.material && n.material.type === "standard");
        }

        function materialOpacity(n) {
          return n.material && n.material.opacity != null ? n.material.opacity : 1;
        }

        function materialMetalness(n) {
          return n.material && n.material.metalness != null ? n.material.metalness : 0.35;
        }

        function materialRoughness(n) {
          return n.material && n.material.roughness != null ? n.material.roughness : 0.35;
        }

        function applyMeshMaterial(n) {
          var color = meshColor(n);
          if (isBasicMaterial(n)) {
            var opacity = materialOpacity(n);
            if (!mat.isMeshBasicMaterial) {
              try {
                mat.dispose();
              } catch (e) {}
              mat = new THREE.MeshBasicMaterial({
                color: color,
                opacity: opacity,
                transparent: opacity < 1,
              });
              mesh.material = mat;
            } else {
              mat.color.set(color);
              mat.opacity = opacity;
              mat.transparent = opacity < 1;
            }
            applyMaterialMap(n);
            return;
          }
          var metalness = materialMetalness(n);
          var roughness = materialRoughness(n);
          var stdOpacity = isStandardMaterial(n) ? materialOpacity(n) : 1;
          if (!mat.isMeshStandardMaterial) {
            try {
              mat.dispose();
            } catch (e) {}
            mat = new THREE.MeshStandardMaterial({
              color: color,
              metalness: metalness,
              roughness: roughness,
              opacity: stdOpacity,
              transparent: stdOpacity < 1,
            });
            mesh.material = mat;
          } else {
            mat.color.set(color);
            mat.metalness = metalness;
            mat.roughness = roughness;
            mat.opacity = stdOpacity;
            mat.transparent = stdOpacity < 1;
          }
          applyMaterialMap(n);
        }

        var textures = {};
        var gltfObjs = {};
        var texLoader = new THREE.TextureLoader();

        function applyMaterialMap(n) {
          var mapId = n.material && n.material.map;
          var entry = mapId ? textures[mapId] : null;
          var tex = entry && entry.texture;
          if (tex) {
            mat.map = tex;
            mat.needsUpdate = true;
          } else if (mat.map) {
            mat.map = null;
            mat.needsUpdate = true;
          }
        }

        function applyTextures(next) {
          var authored = textureNodes(next);
          var keep = {};
          for (var i = 0; i < authored.length; i++) {
            var tn = authored[i];
            keep[tn.id] = true;
            var prev = textures[tn.id];
            if (prev && prev.src === tn.src) continue;
            if (prev && prev.texture) {
              try {
                prev.texture.dispose();
              } catch (e) {}
            }
            textures[tn.id] = { src: tn.src, texture: null };
            (function (id, src) {
              if (!isAllowedSrc(src)) return;
              texLoader.load(
                src,
                function (tex) {
                  if (!textures[id] || textures[id].src !== src) return;
                  textures[id].texture = tex;
                  applyMeshMaterial(currentNode);
                },
                undefined,
                function () {}
              );
            })(tn.id, tn.src);
          }
          for (var id in textures) {
            if (!keep[id]) {
              if (textures[id].texture) {
                try {
                  textures[id].texture.dispose();
                } catch (e) {}
              }
              delete textures[id];
            }
          }
        }

        function placeGltfObject(obj, gn) {
          if (gn.position) {
            obj.position.set(gn.position[0], gn.position[1], gn.position[2]);
          }
          applyRotation(obj, gn.rotation);
          applyScale(obj, gn.scale);
        }

        function applyGltfNodes(next) {
          var authored = gltfNodes(next);
          var keep = {};
          for (var i = 0; i < authored.length; i++) {
            var gn = authored[i];
            keep[gn.id] = true;
            var prev = gltfObjs[gn.id];
            if (prev && prev.src === gn.src) {
              if (prev.object) placeGltfObject(prev.object, gn);
              continue;
            }
            if (prev && prev.object) {
              scene.remove(prev.object);
            }
            gltfObjs[gn.id] = { src: gn.src, object: null };
            (function (id, src, node) {
              if (!isAllowedSrc(src)) return;
              loadGltfLoader(THREE)
                .then(function (GLTFLoader) {
                  var loader = new GLTFLoader();
                  loader.load(
                    src,
                    function (gltf) {
                      if (!gltfObjs[id] || gltfObjs[id].src !== src) return;
                      var obj = gltf && gltf.scene ? gltf.scene : null;
                      if (!obj) return;
                      placeGltfObject(obj, node);
                      scene.add(obj);
                      gltfObjs[id].object = obj;
                    },
                    undefined,
                    function () {}
                  );
                })
                .catch(function () {});
            })(gn.id, gn.src, gn);
          }
          for (var gid in gltfObjs) {
            if (!keep[gid]) {
              if (gltfObjs[gid].object) scene.remove(gltfObjs[gid].object);
              delete gltfObjs[gid];
            }
          }
        }

        applyMeshMaterial(node);
        applyRotation(mesh, node.rotation);
        applyScale(mesh, node.scale);
        if (node.position) {
          mesh.position.set(node.position[0], node.position[1], node.position[2]);
        }
        mesh.userData.node_id = node.id;
        mesh.userData.pickable = node.pickable === true;
        scene.add(mesh);
        var currentShape = node.shape || "box";
        var currentNode = node;
        applyTextures(plan);
        applyGltfNodes(plan);
        var authoredRotation = !!node.rotation;
        var lastHit = null;
        var raycaster = new THREE.Raycaster();
        var pointer = new THREE.Vector2();

        function isPickable(n) {
          return !!(n && n.pickable === true);
        }

        function hitFromEvent(ev) {
          if (!isPickable(currentNode)) return null;
          var rect = renderer.domElement.getBoundingClientRect();
          var w = rect.width || 1;
          var h = rect.height || 1;
          pointer.x = ((ev.clientX - rect.left) / w) * 2 - 1;
          pointer.y = -((ev.clientY - rect.top) / h) * 2 + 1;
          raycaster.setFromCamera(pointer, camera);
          var hits = raycaster.intersectObjects([mesh], false);
          if (!hits.length) return null;
          var p = hits[0].point;
          return {
            node_id: currentNode.id || mesh.userData.node_id,
            point: [p.x, p.y, p.z],
          };
        }

        function reportHit(hit) {
          if (!hit) return;
          lastHit = hit;
          var action = el.getAttribute && el.getAttribute("data-channel-action");
          if (
            action &&
            global.uxChannel &&
            typeof global.uxChannel.runAction === "function"
          ) {
            var cap = el.getAttribute("data-channel-cap") || undefined;
            var target = el.getAttribute("data-channel-target") || undefined;
            global.uxChannel.runAction(action, hit, cap, target);
          }
        }

        function onPointerDown(ev) {
          reportHit(hitFromEvent(ev));
        }
        renderer.domElement.addEventListener("pointerdown", onPointerDown);

        var running = true;
        function frame() {
          if (!running) return;
          requestAnimationFrame(frame);
          if (!authoredRotation) {
            mesh.rotation.y += 0.008;
            mesh.rotation.x += 0.003;
          }
          renderer.render(scene, camera);
        }
        frame();

        var ro = null;
        if (typeof ResizeObserver !== "undefined") {
          ro = new ResizeObserver(function () {
            var w = el.clientWidth || width;
            var h = el.clientHeight || height;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h, false);
          });
          ro.observe(el);
        }

        function applyPlan(next) {
          applyCameraNode(next);
          applyLights(next);
          var n = firstMesh(next);
          var nextShape = n.shape || "box";
          if (nextShape !== currentShape) {
            try {
              mesh.geometry.dispose();
            } catch (e) {}
            mesh.geometry = geometryFor(THREE, nextShape);
            currentShape = nextShape;
          }
          applyMeshMaterial(n);
          if (n.rotation) {
            applyRotation(mesh, n.rotation);
            authoredRotation = true;
          } else {
            authoredRotation = false;
          }
          applyScale(mesh, n.scale);
          if (n.position) {
            mesh.position.set(n.position[0], n.position[1], n.position[2]);
          }
          currentNode = n;
          mesh.userData.node_id = n.id;
          mesh.userData.pickable = n.pickable === true;
          applyTextures(next);
          applyGltfNodes(next);
        }

        return {
          apply: applyPlan,
          update: applyPlan,
          pick: function (hit) {
            if (hit && hit.node_id) lastHit = hit;
            return lastHit;
          },
          orbit: function (payload) {
            if (payload) applyCameraControl({ orbit: payload, pan: control.pan, zoom: control.zoom });
            return control.orbit;
          },
          pan: function (payload) {
            if (payload) applyCameraControl({ orbit: control.orbit, pan: payload, zoom: control.zoom });
            return control.pan;
          },
          zoom: function (payload) {
            var distance = payload && payload.distance != null ? payload.distance : payload;
            if (distance != null) {
              applyCameraControl({ orbit: control.orbit, pan: control.pan, zoom: distance });
            }
            return control.zoom;
          },
          destroy: function () {
            running = false;
            renderer.domElement.removeEventListener("pointerdown", onPointerDown);
            if (ro) ro.disconnect();
            try {
              mesh.geometry.dispose();
              mat.dispose();
              renderer.dispose();
            } catch (e) {}
            for (var tid in textures) {
              if (textures[tid].texture) {
                try {
                  textures[tid].texture.dispose();
                } catch (e) {}
              }
            }
            for (var gid in gltfObjs) {
              if (gltfObjs[gid].object) scene.remove(gltfObjs[gid].object);
            }
            el.innerHTML = "";
          },
        };
      });
    },
    update: function (handle, props) {
      if (!handle) return;
      var plan = props && (props.plan || props);
      if (handle.update) handle.update(plan);
      else if (handle.apply) handle.apply(plan);
    },
    call: function (handle, method, args) {
      if (!handle) return;
      if (typeof handle[method] === "function") {
        return handle[method].apply(handle, args || []);
      }
    },
    destroy: function (handle) {
      if (handle && handle.destroy) handle.destroy();
    },
  });
})(typeof window !== "undefined" ? window : globalThis);
