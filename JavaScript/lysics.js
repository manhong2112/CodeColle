floor = x => ~~x;

var _TEMPO = 0.458;
var COMMENT_LIST = [
    // delay, "lysics", "play length of each char", color
    [0, "", [], 0x000000],
];

var commentLocY = floor($.height * 0.8);
var firstLoc = 40;
var commentLocX = firstLoc;
var fontSize = 30;
var mainIndex = 0; // index of list

function f1() {
    if (mainIndex == COMMENT_LIST.length) return;
    commentLocX = firstLoc;
    commentLocY = floor($.height * 0.8);
    var eachData = COMMENT_LIST[mainIndex];
    var waitTime = eachData[0] * _TEMPO;
    return timer(
        function() {
            (function f2(comment, data, color, index) {
                if (index == data.length) {
                    mainIndex += 1;
                    return f1();
                }
                send(comment[index], data[index] * _TEMPO, color);
                return timer(
                    function() {
                        f2(comment, data, color, index + 1);
                    }, data[index] * _TEMPO * 1000);
            })(eachData[1].split(''), eachData[2], eachData[3], 0);
        }, waitTime * 1000);
}

function fadein(commentItem, lifeTime) {
    return (function ff1(commentItem, lifeTime, count) {
        commentItem.alpha += 0.1;
        if (count % 2 == 0) commentItem.y += 1;
        if (count <= 0) {
            commentItem.alpha = 1;
            return timer(function() {
                fadeout(commentItem, lifeTime);
            }, lifeTime * 1000 + 1000);
        }
        return timer(function() {
            ff1(commentItem, lifeTime, count - 1);
        }, 100 / 10);
    })(commentItem, lifeTime, 10);
}

function fadeout(commentItem, lifeTime) {
    return (function ff2(commentItem, lifeTime, count) {
        commentItem.alpha -= 0.1;
        if (count <= 0)
            return (
                function() {
                    commentItem.alpha = 0;
                })();
        return timer(function() {
            ff2(commentItem, lifeTime, count - 1);
        }, 100 / 10);
    })(commentItem, lifeTime, 10);
};

function send(commentChar, lifeTime, fontColor) {
    commentLocX += 30;
    var comment = $.createComment(
        commentChar, {
            x: commentLocX,
            y: commentLocY,
            lifeTime: 12,
            alpha: 0,
            color: fontColor
        }
    );
    return fadein(comment, lifeTime);
}

f1();