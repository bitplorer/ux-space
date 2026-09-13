# peers/threejs

Thin Channel bridge adapter. CDN three.js is OK for day-1.

- **Register:** `uxBridge.register("ux-space", { mount, update, call })`
- **Not:** `uxBridge.register("three", …)` (Channel demo package name)
- **Loads:** `three@0.160.0` UMD from jsDelivr when `THREE` is absent
- **Applies:** Plan IR `graph.nodes` (day-1 shape: `box`)

`mount` reads optional `props.plan`. `call(..., "apply", [plan])` is the
Cap-gated verb the Python side emits. `update` forwards `props.plan`.

Swap: see [`../README.md`](../README.md). Core Graph API does not change.
