/**
 * ux-space Peer — thin 2D canvas adapter (Soft 5 leftover).
 * Package name: "ux-space" (swap replaces the engine; not a second product).
 *
 * Plan IR (v: "1"): { graph: { nodes: [{ id, kind, ... }] } }
 * Soft 2 leftover: locked shapes as filled 2D (box/sphere/plane/cylinder).
 * Soft 3 leftover: camera/light nodes ignored (2D proof — no camera API).
 * Soft 4 leftover: mesh rotation / scale + material {basic}
 *   (color + opacity). Top-level color KEEP; material.color wins.
 * Soft 6 leftover: optional mesh pickable. Pointer over the canvas
 *   hit-tests pickable 2D shapes and reports {node_id, point}.
 *   Channel owns click=Intent (uxChannel.runAction when present).
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

      var lastHit = null;

      function isPickable(node) {
        return !!(node && node.pickable === true);
      }

      function localPoint(ev) {
        var rect = canvas.getBoundingClientRect();
        var sx = (ev.clientX - rect.left) * (canvas.width / (rect.width || 1));
        var sy = (ev.clientY - rect.top) * (canvas.height / (rect.height || 1));
        return [sx - canvas.width / 2, sy - canvas.height / 2];
      }

      function shapeContains(node, x, y) {
        var pos = node.position || [0, 0, 0];
        var xy = scaleXY(node.scale);
        var rot = rotation2d(node.rotation);
        var lx = x - pos[0] * 48;
        var ly = y - (-pos[1] * 48);
        var c = Math.cos(-rot);
        var s = Math.sin(-rot);
        var rx = (lx * c - ly * s) / (xy[0] || 1);
        var ry = (lx * s + ly * c) / (xy[1] || 1);
        var shape = node.shape || "box";
        if (shape === "sphere") return rx * rx + ry * ry <= 28 * 28;
        if (shape === "plane") return Math.abs(rx) <= 40 && Math.abs(ry) <= 6;
        if (shape === "cylinder") return Math.abs(rx) <= 18 && Math.abs(ry) <= 30;
        return Math.abs(rx) <= 24 && Math.abs(ry) <= 24;
      }

      function hitFromEvent(ev) {
        var p = localPoint(ev);
        var meshes = meshNodes(plan);
        for (var i = meshes.length - 1; i >= 0; i--) {
          var node = meshes[i];
          if (!isPickable(node)) continue;
          if (shapeContains(node, p[0], p[1])) {
            return {
              node_id: node.id,
              point: [p[0] / 48, -p[1] / 48, 0],
            };
          }
        }
        return null;
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
      canvas.addEventListener("pointerdown", onPointerDown);

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
        pick: function (hit) {
          if (hit && hit.node_id) lastHit = hit;
          return lastHit;
        },
        destroy: function () {
          canvas.removeEventListener("pointerdown", onPointerDown);
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
