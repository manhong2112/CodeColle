// k / (150 * size)
createCanvas = (w, h) => {
   var c = document.createElement('canvas');
   c.width = w
   c.height = h
   return c
}
drawSakura = (size) => {
   var canvas = createCanvas(size, size)
   let scale = 150 / size
   if (canvas.getContext) {
      var ctx = canvas.getContext('2d')
      ctx.scale_bezierCurveTo = (x1, y1, x2, y2, ex, ey) => {
         ctx.bezierCurveTo(x1 / scale, y1 / scale, x2 / scale, y2 / scale, ex / scale, ey / scale)
      }
      ctx.scale_moveTo = (x1, y1) => ctx.moveTo(x1 / scale, y1 / scale)
      ctx.fillColor = (color) => {
         var k = ctx.fillStyle
         ctx.fillStyle = color
         ctx.fill()
         ctx.fillStyle = k
      }
      ctx.beginPath();
      ctx.scale_moveTo(75, 40)
      ctx.scale_bezierCurveTo(75, 40, 70, 25, 50, 25)
      ctx.scale_bezierCurveTo(15, 25, 20, 62.5, 20, 62.5)
      ctx.scale_bezierCurveTo(20, 80, 40, 102, 75, 120)

      ctx.scale_bezierCurveTo(110, 102, 130, 80, 130, 62.5)
      ctx.scale_bezierCurveTo(130, 62.5, 130, 25, 100, 25)
      ctx.scale_bezierCurveTo(85, 25, 75, 37, 75, 40)
      ctx.fillColor("#FEDFE1")
   }
   return canvas
}

var canvas = createCanvas(100, 100)
document.body.appendChild(canvas)
canvas.getContext('2d').drawImage(drawSakura(50), 0, 0)