/**
 * ux-space Peer — thin 2D canvas adapter (Soft 5 leftover).
 * Package name: "ux-space" (swap replaces the engine; not a second product).
 *
 * Plan IR (v: "1"): { graph: { nodes: [{ id, kind, ... }] } }
 * Soft 2 leftover: locked shapes as filled 2D (box/sphere/plane/cylinder).
 * Soft 3 leftover: camera/light nodes ignored (2D proof — no camera API).
 * Soft 4 leftover: mesh rotation / scale + material {basic}
 *   (color + opacity). Top-level color KEEP; material.color wins.
 * Day-1 default stays peers/threejs. This file proves the swap path.
 */
(function (global) {
  "use strict";
  if (!global.uxBridge) {
    console.warn("[ux-space] uxBridge missing");
    return;
  }

  function allNodes(plan) {
    var graph = (plan && plan.graph) || plan || {};
    return graph.nodes || [];
  }

  function isMesh(node) {
    return !node.kind || node.kind === "node";
  }

  function meshNodes(plan) {
    var nodes = allNodes(plan);
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      if (isMesh(nodes[i])) out.push(nodes[i]);
    }
    return out;
  }

  // Soft 4 leftover: material.color wins over top-level color shorthand.
  function meshColor(node) {
    return (node.material && node.material.color) || node.color || "#6366f1";
  }

  function meshOpacity(node) {
    if (node.material && node.material.opacity != null) return node.material.opacity;
    return 1;
  }

  function isBasicMaterial(node) {
    return !!(node.material && (node.material.type === "basic" || !node.material.type));
  }

  function scaleXY(scale) {
    if (scale == null) return [1, 1];
    if (typeof scale === "number") return [scale, scale];
    return [scale[0], scale[1]];
  }

  function rotation2d(rotation) {
    if (!rotation) return 0;
    return rotation[2] || 0;
  }

  function drawShape(ctx, node) {
    var shape = node.shape || "box";
    var pos = node.position || [0, 0, 0];
    var xy = scaleXY(node.scale);
    ctx.save();
    ctx.translate(pos[0] * 48, -pos[1] * 48);
    ctx.rotate(rotation2d(node.rotation));
    ctx.scale(xy[0], xy[1]);
    ctx.globalAlpha = isBasicMaterial(node) ? meshOpacity(node) : 1;
    ctx.fillStyle = meshColor(node);
    if (shape === "sphere") {
      ctx.beginPath();
      ctx.arc(0, 0, 28, 0, Math.PI * 2);
      ctx.fill();
    } else if (shape === "plane") {
      ctx.fillRect(-40, -6, 80, 12);
    } else if (shape === "cylinder") {
      ctx.beginPath();
      ctx.ellipse(0, -22, 18, 8, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillRect(-18, -22, 36, 44);
      ctx.beginPath();
      ctx.ellipse(0, 22, 18, 8, 0, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.fillRect(-24, -24, 48, 48);
    }
    ctx.restore();
  }

  global.uxBridge.register("ux-space", {
    mount: function (el, props) {
      props = props || {};
      var plan = props.plan || props;
      el.style.position = el.style.position || "relative";
      el.style.overflow = "hidden";

      var canvas = document.createElement("canvas");
      var width = el.clientWidth || 640;
      var height = el.clientHeight || 360;
      canvas.width = width;
      canvas.height = height;
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      canvas.style.display = "block";
      el.innerHTML = "";
      el.appendChild(canvas);

      var ctx = canvas.getContext("2d");

      function paint(next) {
        var w = canvas.width;
        var h = canvas.height;
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = "#0b1020";
        ctx.fillRect(0, 0, w, h);
        ctx.translate(w / 2, h / 2);
        var meshes = meshNodes(next);
        for (var i = 0; i < meshes.length; i++) {
          drawShape(ctx, meshes[i]);
        }
      }

      paint(plan);

      var ro = null;
      if (typeof ResizeObserver !== "undefined") {
        ro = new ResizeObserver(function () {
          canvas.width = el.clientWidth || width;
          canvas.height = el.clientHeight || height;
          paint(plan);
        });
        ro.observe(el);
      }

      function applyPlan(next) {
        plan = next || plan;
        paint(plan);
      }

      return {
        apply: applyPlan,
        update: applyPlan,
        destroy: function () {
          if (ro) ro.disconnect();
          el.innerHTML = "";
        },
      };
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
