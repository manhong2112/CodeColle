fun main(args: Array<String>) {
    println(atoi("2147483648"))
    println("2147483648".toInt())
}
fun atoi(str: String): Int {
    // TODO Overflow Check
    var nve = false
    val len = str.length
    if(len == 0) {
        throw NumberFormatException("Empty String")
    }
    var end = 0
    when (str[0]) {
        '-' -> {
            end = 1
            nve = true
        }
        '+' -> {
            end = 1
        }
    }
    if(len==end) {
        throw NumberFormatException("Sign Only")
    }
    var res = 0
    var mul = 1
    for (i in len - 1 downTo end) {
        val c = (str[i] - '0').toInt()
        if (c in 0 .. 9) {
            res += c * mul
            mul *= 10
        } else {
            throw NumberFormatException("${str[i]}")
        }
    }
    if(nve) {
        return -res
    } else {
        return res
    }
}