"use strict"
// k / (150 * size)
var createCanvas = (w, h) => {
   var c = document.createElement('canvas');
   c.width = w
   c.height = h
   return c
}
var getSakura = (size) => {
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

