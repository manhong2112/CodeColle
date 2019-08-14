var agdaRTS = require("agda-rts");

exports["N"] = {};
exports["N"]["zero"] = function (x0) {
    return x0["zero"]();
  };
exports["N"]["succ"] = function (x0) {
    return function (x1) {
      return x1["succ"](x0);
    };
  };

exports["main"](function (x0) {
  return {};
})