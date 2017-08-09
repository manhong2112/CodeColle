// k / (150 * size)
var createElement = (tag, prop, style) => {
   let ele = document.createElement(tag)
   for (let i in (prop || [])) {
      ele[i] = prop[i]
   }
   for (let i in (style || [])) {
      ele.style[i] = style[i]
   }
   return ele
}
var createCanvas = (w, h) => {
   return createElement('canvas', {"width": w, "height": h})
}

{
   let style = createElement("style")
   document.body.appendChild(style)
   let stylesheet = style.sheet
   var addStyle = (rule) => {
      stylesheet.insertRule(rule, stylesheet.cssRules.length);
   }
}

var drawSakura = (size) => {
   let canvas = createCanvas(size, size)
   let scale = 150 / size
   if (canvas.getContext) {
      let ctx = canvas.getContext('2d')
      ctx.scale_bezierCurveTo = (x1, y1, x2, y2, ex, ey) => {
         ctx.bezierCurveTo(x1 / scale, y1 / scale, x2 / scale, y2 / scale, ex / scale, ey / scale)
      }
      ctx.scale_moveTo = (x1, y1) => ctx.moveTo(x1 / scale, y1 / scale)
      ctx.fillColor = (color) => {
         let k = ctx.fillStyle
         ctx.fillStyle = color
         ctx.fill()
         ctx.fillStyle = k
      }
      ctx.beginPath();
      ctx.scale_moveTo(75, 30)
      ctx.scale_bezierCurveTo(75, 30, 70, 20, 60, 10)
      ctx.scale_bezierCurveTo(60, 10, 10, 75, 75, 120)

      ctx.scale_moveTo(75, 30)
      ctx.scale_bezierCurveTo(75, 30, 80, 20, 90, 10)
      ctx.scale_bezierCurveTo(90, 10, 140, 75, 75, 120)
      ctx.fillColor("#FEDFE1")
   }
   return canvas
}

var createSakura = () => {
   let o = {
      size: randint(5, 80),
      vx: rand(0.2, 1.5),
      vy: rand(0.3, 2),
      rotatev: (Boolean(randint(0, 1)) ? -1 : +1) * rand(0.1, 0.5),
   }
   o.c = drawSakura(o.size)
   o.move = () => {
      o.x += o.vx
      o.y += o.vy
      if (o.x > window.innerWidth) {
         o.x = -50
      }
      if (o.y > window.innerHeight) {
         o.y = -50
      }
   }
   o.rotate = () => {
      o.rotatex += o.rotatevx
      o.rotatey += o.rotatevy
      o.rotatez += o.rotatevz
      if (o.rotatex > 360) {
         o.rotatex -= 360
      } else if (o.rotatex < 0) {
         o.rotatex += 360
      }
      if (o.rotatey > 360) {
         o.rotatey -= 360
      } else if (o.rotatey < 0) {
         o.rotatey += 360
      }
      if (o.rotatez > 360) {
         o.rotatez -= 360
      } else if (o.rotatez < 0) {
         o.rotatez += 360
      }
   }
   return o
}

var drawAnimation = (list, speed) => {
   // init
   let div = createElement('div', [], {"width": "100%", "height": "100%", "position": "fixed", "overflow": "hidden"})
   document.body.appendChild(div)
   list.forEach((obj, _index, _arr) => {
      obj.c.style.position = "absolute"
      let scalePosX = 1920 / speed
      let scalePosY = 1080 / speed
      let scaleRotate = 360 / speed
      obj.c.style.opacity = `${obj.size / 280}`
      obj.c.style.filter = `blur(${obj.size / 240}px)`
      obj.c.style.animation =
         `pX ${scalePosX / obj.vx}s infinite linear, \
          pY ${scalePosX / obj.vy}s infinite linear, \
          r ${scaleRotate / Math.abs(obj.rotatev)}s infinite linear ${obj.rotatev > 0 ? "" : "backwards"}`
      div.appendChild(obj.c)
   })
}

var sakura_main = (num, speed) => {
   addStyle("@keyframes pX {0% {left: -100px;} 100% {left: 100%;}}")
   addStyle("@keyframes pY {0% {top: -100px;} 100% {top: 100%;}}")
   addStyle("@keyframes r {0% {rotateX(0deg) rotateY(0deg) rotateZ(0deg);} \
                         100% {rotateX(360deg) rotateY(360deg) rotateZ(360deg);}}")
   var sakuraList = window.sakuraList = initArray(num || 300, createSakura)
   drawAnimation(sakuraList, speed || 60)
}
window.onload = () => { sakura_main(300) }