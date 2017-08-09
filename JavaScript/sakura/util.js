var initArray = (size, func) => {
   let arr = new Array(size);
   for (let x = 0; x < size; x++) {
      arr[x] = func(x)
   }
   return arr
}
var randint = (min, max) => {
   return min + ~~((Math.random() * (max - min)) + 0.5)
}
var rand = (min, max) => {
   return min + (Math.random() * (max - min))
}
var log = console.log