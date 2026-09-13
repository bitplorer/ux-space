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
 * HOLD materials catalog, look-at / orbit controls.
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

        function applyCameraNode(next) {
          var cam = firstCamera(next);
          if (!cam) return;
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
        scene.add(mesh);
        var currentShape = node.shape || "box";
        var authoredRotation = !!node.rotation;

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
        }

        return {
          apply: applyPlan,
          update: applyPlan,
          destroy: function () {
            running = false;
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
