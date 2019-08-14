// k / (150 * size)
var createCanvas = (w, h) => {
   return createElement("canvas", { width: w, height: h });
};

var createElement = (tag, prop, style) => {
   let ele = document.createElement(tag);
   for (let i in prop || []) {
      ele[i] = prop[i];
   }
   for (let i in style || []) {
      ele.style[i] = style[i];
   }
   return ele;
};

var drawSakura = size => {
   let canvas = createCanvas(size, size);
   let scale = 150 / size;
   if (canvas.getContext) {
      let ctx = canvas.getContext("2d");
      ctx.scale_bezierCurveTo = (x1, y1, x2, y2, ex, ey) => {
         ctx.bezierCurveTo(
            x1 / scale,
            y1 / scale,
            x2 / scale,
            y2 / scale,
            ex / scale,
            ey / scale
         );
      };
      ctx.scale_moveTo = (x1, y1) => ctx.moveTo(x1 / scale, y1 / scale);
      ctx.fillColor = color => {
         let k = ctx.fillStyle;
         ctx.fillStyle = color;
         ctx.fill();
         ctx.fillStyle = k;
      };
      ctx.beginPath();
      ctx.scale_moveTo(75, 30);
      ctx.scale_bezierCurveTo(75, 30, 70, 20, 60, 10);
      ctx.scale_bezierCurveTo(60, 10, 10, 75, 75, 120);

      ctx.scale_moveTo(75, 30);
      ctx.scale_bezierCurveTo(75, 30, 80, 20, 90, 10);
      ctx.scale_bezierCurveTo(90, 10, 140, 75, 75, 120);
      ctx.fillColor("#FEDFE1");
   }
   return canvas;
};

var createSakura = mesh => {
   let o = {
      mesh: mesh,
      vx: rand(2, 25) / 800,
      vy: -rand(1, 20) / 800,
      vz: (Boolean(randint(0, 1)) ? -1 : +1) * rand(0.005, 0.01)
   };
   o.mesh.position.z = rand(1, 3);
   return o;
};

var sakura_main = (num, speed) => {
   var scene = new THREE.Scene();
   var camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      1,
      1000
   );

   var renderer = new THREE.WebGLRenderer();
   renderer.setSize(window.innerWidth, window.innerHeight);
   document.body.appendChild(renderer.domElement);

   var texture = new THREE.CanvasTexture(drawSakura(256));

   var geometry = new THREE.PlaneGeometry(0.5, 0.5);
   var material = new THREE.MeshBasicMaterial({
      map: texture,
      transparent: true
   });

   var f = () => createSakura(new THREE.Mesh(geometry, material));
   var arr = [];
   for (let i = 0; i < num; i++) {
      arr[i] = f();
      arr[i].mesh.position.x = randint(0, 16) - 8;
      arr[i].mesh.position.y = randint(0, 16) - 8;
      scene.add(arr[i].mesh);
   }

   function f3to2({ x: x, y: y, z: z }) {
      var vector = new THREE.Vector3(x, y, z);
      vector.project(camera);
      var halfWidth = window.innerWidth / 2;
      var halfHeight = window.innerHeight / 2;
      var result = {
         x: Math.round(vector.x * halfWidth + halfWidth),
         y: Math.round(-vector.y * halfHeight + halfHeight)
      };
      return result;
   }

   function f2to3({ x: x, y: y, z: z }) {
      const closeEnough = (a, b) => {
         return Math.abs(a.x - b.x) < 0.01 && Math.abs(a.y - b.y) < 0.01;
      };

      let tryX = -1;
      let tryY = -10;

      let counter = 0;

      s = x => 1 / (1 + Math.exp(-x));

      while (counter < 50) {
         counter += 1;
         v = f3to2({ x: tryX, y: tryY, z: z });
         tryY += 0.5 - s(v.y - y);
      }
      while (counter < 100) {
         counter += 1;
         v = f3to2({ x: tryX, y: tryY, z: z });
         tryX -= 0.5 - s(v.x - x);
      }

      return { x: tryX, y: tryY, z: z };
   }

   camera.position.z = 7;
   camera.lookAt(scene.position);

   console.log(f2to3({ x: 0, y: 0, z: 7 }));

   var animate = function() {
      for (let s of arr) {
         s.mesh.position.x += s.vx;
         s.mesh.position.y += s.vy;

         s.mesh.rotation.x += s.vz;
         s.mesh.rotation.y += s.vz;
         s.mesh.rotation.z += s.vz;

         // mpos = f3to2(s.mesh.position)
      }
      renderer.render(scene, camera);

      requestAnimationFrame(animate);
   };

   animate();
   // addStyle("@keyframes pX {0% {left: -100px;} 100% {left: 100%;}}")
   // addStyle("@keyframes pY {0% {top: -100px;} 100% {top: 100%;}}")
   // addStyle("@keyframes r {0% {transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);}\
   //                         100% {transform: rotateX(360deg) rotateY(360deg) rotateZ(360deg);}}")
   // var sakuraList = window.sakuraList = initArray(num || 300, createSakura)
   // drawAnimation(sakuraList, speed || 60)
};
window.onload = () => {
   sakura_main(300);
};
