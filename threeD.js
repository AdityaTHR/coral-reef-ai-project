let scene = new THREE.Scene();

let camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);

let renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(300, 300);

document.getElementById("threeD").innerHTML = "";
document.getElementById("threeD").appendChild(renderer.domElement);

let geometry = new THREE.PlaneGeometry(2, 2);
let material = new THREE.MeshBasicMaterial({ color: 0xffffff });
let plane = new THREE.Mesh(geometry, material);

scene.add(plane);
camera.position.z = 3;

// FUNCTION THAT LOADS IMAGE INTO 3D
function load3DImage(imgData) {
  const texture = new THREE.TextureLoader().load(imgData);
  plane.material.map = texture;
  plane.material.needsUpdate = true;
}

window.load3DImage = load3DImage;

function animate() {
  requestAnimationFrame(animate);
  plane.rotation.y += 0.01;
  renderer.render(scene, camera);
}

animate();
