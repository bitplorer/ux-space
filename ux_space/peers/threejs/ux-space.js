/**
 * ux-space Peer — thin three.js adapter.
 * Package name: "ux-space" (wraps three; product surface ≠ Channel demo "three").
 *
 * Plan IR (v: "1"): { graph: { nodes: [{ id, shape, color?, position? }] } }
 * Soft 2 leftover: locked geometry map (box/sphere/plane/cylinder).
 * HOLD the full three.js catalog.
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

  function firstNode(plan) {
    var graph = (plan && plan.graph) || plan || {};
    var nodes = graph.nodes || [];
    return nodes[0] || {};
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

  global.uxBridge.register("ux-space", {
    mount: function (el, props) {
      return loadThree().then(function (THREE) {
        props = props || {};
        var plan = props.plan || props;
        var node = firstNode(plan);
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

        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        var key = new THREE.DirectionalLight(0xffffff, 1.0);
        key.position.set(3, 4, 5);
        scene.add(key);

        var mat = new THREE.MeshStandardMaterial({
          color: node.color || "#6366f1",
          metalness: 0.35,
          roughness: 0.35,
        });
        var mesh = new THREE.Mesh(geometryFor(THREE, node.shape), mat);
        if (node.position) {
          mesh.position.set(node.position[0], node.position[1], node.position[2]);
        }
        scene.add(mesh);
        var currentShape = node.shape || "box";

        var running = true;
        function frame() {
          if (!running) return;
          requestAnimationFrame(frame);
          mesh.rotation.y += 0.008;
          mesh.rotation.x += 0.003;
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
          var n = firstNode(next);
          var nextShape = n.shape || "box";
          if (nextShape !== currentShape) {
            try {
              mesh.geometry.dispose();
            } catch (e) {}
            mesh.geometry = geometryFor(THREE, nextShape);
            currentShape = nextShape;
          }
          if (n.color) mat.color.set(n.color);
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
