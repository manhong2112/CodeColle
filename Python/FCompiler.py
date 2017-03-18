def interp(src):
    pass


class Token(object):
    Tokens = {
        "EOS": 1,
        "COLON": 2,
        "SEMICOLON": 3,
        "LEFTPAREN": 4,
        "RIGHTPAREN": 5,
        "LEFTBRACE": 6,
        "RIGHTBRACE": 7,
        "MOD": 8,
        "VAR": 9,
        "TYPE": 10,
        "BOOL": 11,
        "IF": 12,
        "ELSE": 13,
        "WHILE": 14,
        "PRINT": 15,
        "VARID": 16,
    }
    for k in Tokens.copy():
        Tokens[Tokens[k]] = k

    def __init(self, type, text=None):
        self.type = type
        self.text = text


class Reader(object):
    def __init__(self, str):
        self.data = str
        self.pos = -1
        self.dataLen = len(str)

    def nextChar(self):
        self.pos += 1
        if(self.pos >= self.dataLen):
            return None
        else:
            return self.data[self.pos]

    def retract(self, n=1):
        self.pos -= n
        if(self.pos < 0):
            self.pos = -1


class Scanner(object):
    States = {
        "START_STATE": 0,
        "IDENTIFIER_STATE": 1
    }

    def __init__(self, reader):
        self.reader = reader
        self.currentToken = Token()
        self.currLine = 0
        self.state = Scanner.States["START_STATE"]
        self.bufferStr = ""

    def makeToken(self, type, text=None):
        self.currentToken.type = type
        self.currentToken.text = text
        return type

    def nextToken(self):
        while True:
            c = self.reader.nextChar()
            if(self.state == Scanner.States["START_STATE"]):
                if c.isalpha():
                    self.state = Scanner.States["IDENTIFIER_STATE"]
                    self.bufferStr = c
                    return
                try:
                    return self.makeToken({
                        ":": Token.Tokens["COLON"],
                        ";": Token.Tokens["SEMICOLON"],
                        "(": Token.Tokens["LEFTPAREN"],
                        ")": Token.Tokens["RIGHTPAREN"],
                        "{": Token.Tokens["LEFTBRACE"],
                        "}": Token.Tokens["RIGHTBRACE"],
                        "%": Token.Tokens["MOD"],
                        -1: Token.Tokens["EOS"],
                    }[c])
                except KeyError:
                    if(c == "\r" or c == "\n"):
                        self.currLine += 1
            elif(self.state == Scanner.States["IDENTIFIER_STATE"]):
                if c.isalpha():
                    self.bufferStr += c
                else:
                    self.reader.retract()
                    self.state = Scanner.States["START_STATE"]
                    try:
                        return self.makeToken({
                            "var": Token.Tokens["VAR"],
                            "if": Token.Tokens["IF"],
                            "else": Token.Tokens["ELSE"],
                            "while": Token.Tokens["WHILE"],
                            "print": Token.Tokens["PRINT"]
                        }[self.bufferStr])
                    except KeyError:
                        pass
                    try:
                        return {
                            "int": self.makeToken(Token.Tokens["TYPE"], "int"),
                            "bool": self.makeToken(Token.Tokens["TYPE"], "bool"),
                            "true": self.makeToken(Token.Tokens["BOOL"], "true"),
                            "false": self.makeToken(Token.Tokens["BOOL"], "false"),
                        }[self.bufferStr]
                    except KeyError:
                        return self.makeToken(Token.Tokens["VARID"], self.bufferStr)


r = Reader("var x:int = 5;var y:bool = false;var z:int = 233;")
s = Scanner(r)
x = r.nextChar()
a = False
while True:
    token = s.nextToken()
    if (token == Token.Tokens["EOS"]):
        break
    print("Read token: " + Token.Tokens[token])
