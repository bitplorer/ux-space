// Runs the three.js Peer under node with a minimal THREE stand-in (no WebGL).
// argv: <adapter path> <mount plan JSON> <update plan JSON>
// Prints the node_ids of the meshes in the scene after mount and after update.
"use strict";

function Vec() {
  this.set = function (x, y, z) { this.x = x; this.y = y; this.z = z; };
}
function Obj() {
  this.position = new Vec();
  this.rotation = new Vec();
  this.scale = new Vec();
  this.userData = {};
}
function Material(opts) {
  Object.assign(this, opts || {});
  this.color = { set: function () {} };
  this.dispose = function () {};
}
function Geometry() { this.dispose = function () {}; }
function Mesh(geometry, material) {
  Obj.call(this);
  this.isMesh = true;
  this.geometry = geometry;
  this.material = material;
}
function Scene() {
  this.children = [];
  this.add = function (o) { this.children.push(o); };
  this.remove = function (o) { this.children = this.children.filter(function (c) { return c !== o; }); };
}

globalThis.THREE = {
  Scene: Scene,
  Color: function () {},
  PerspectiveCamera: function () { Obj.call(this); this.updateProjectionMatrix = function () {}; },
  WebGLRenderer: function () {
    this.domElement = { style: {}, addEventListener: function () {}, removeEventListener: function () {} };
    this.setPixelRatio = this.setSize = this.render = this.dispose = function () {};
  },
  AmbientLight: Obj,
  DirectionalLight: Obj,
  Mesh: Mesh,
  MeshStandardMaterial: function (o) { Material.call(this, o); this.isMeshStandardMaterial = true; },
  MeshBasicMaterial: function (o) { Material.call(this, o); this.isMeshBasicMaterial = true; },
  BoxGeometry: Geometry,
  SphereGeometry: Geometry,
  PlaneGeometry: Geometry,
  CylinderGeometry: Geometry,
  ConeGeometry: Geometry,
  TorusGeometry: Geometry,
  TextureLoader: function () { this.load = function () {}; },
  Raycaster: function () {},
  Vector2: function () {},
};
globalThis.window = globalThis;
globalThis.requestAnimationFrame = function () {};

var adapter = null;
globalThis.uxBridge = { register: function (name, a) { adapter = a; } };
require(process.argv[2]);

function meshIds(scene) {
  return scene.children.filter(function (c) { return c.isMesh; }).map(function (c) { return c.userData.node_id; });
}

var scene = null;
var realScene = THREE.Scene;
THREE.Scene = function () { realScene.call(this); scene = this; };

var el = { style: {}, innerHTML: "", appendChild: function () {} };
adapter.mount(el, { plan: JSON.parse(process.argv[3]) }).then(function (handle) {
  var mounted = meshIds(scene);
  adapter.update(handle, { plan: JSON.parse(process.argv[4]) });
  process.stdout.write(JSON.stringify({ mount: mounted, update: meshIds(scene) }));
  handle.destroy();
});
