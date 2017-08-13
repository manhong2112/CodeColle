var YetAnotherPromise = (func) => { // func :: (resolve) -> Unit
   let o = {}
   o.__type = "YetAnotherPromise"
   o.status = "pending"
   o.value = null
   o._then = null
   o.then = (func) => {
      if (o.status == "resolved") {
         k = func(o.value)
         if (k && k.__type && k.__type == "YetAnotherPromise") {
            return k
         } else {
            return YetAnotherPromise((resolve) => {
               resolve(k)
            })
         }
      } else {
         o._then = func
      }
   }
   func((value) => {
      if (o.status == "pending") {
         o.value = value
         o.status = "resolved"
         if (o._then) {
            o._then(o.value)
         }
      }
   })
   return o
}

function f(value){
   console.log('start' + value)
   return YetAnotherPromise((resolve) => {
      setTimeout(function () {
         resolve(value + 1)
       console.log(value)
     }, 1000)
   })
 }
 
f(1).then(f)