/**
 * ux-space Peer — thin three.js adapter.
 * Package name: "ux-space" (wraps three; product surface ≠ Channel demo "three").
 *
 * Plan IR (v: "1"): { graph: { nodes: [{ id, kind, ... }] } }
 * Soft 2 leftover: locked geometry map (box/sphere/plane/cylinder).
 * Soft 3 leftover: optional camera/light node kinds
 *   (perspective / ambient / directional). Mesh nodes still apply.
 * Soft 4 leftover: mesh rotation / scale + material {basic}
 *   (color + opacity → MeshBasicMaterial). Default mesh stays
 *   MeshStandardMaterial when material is absent. Camera may take rotation.
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
  var loading = null;

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

  // Soft 2 leftover: thin geometry map. Not the full three.js catalog.
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

        function applyMeshMaterial(n) {
          var color = meshColor(n);
          if (isBasicMaterial(n)) {
            var opacity = n.material.opacity != null ? n.material.opacity : 1;
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
            return;
          }
          if (!mat.isMeshStandardMaterial) {
            try {
              mat.dispose();
            } catch (e) {}
            mat = new THREE.MeshStandardMaterial({
              color: color,
              metalness: 0.35,
              roughness: 0.35,
            });
            mesh.material = mat;
          } else {
            mat.color.set(color);
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
