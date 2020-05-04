import clr, os, sys, pathlib, re, itertools, functools, json

#link to dot net libraries
p = pathlib.Path(__file__)
dotNetPath = (p.parent.parent / 'DotNetLib').resolve()
# print( dotNetPath )
gccRoot = p.parent.parent / 'avr8-gnu-toolchain-win32_x86'
sys.path.append(str(dotNetPath))


clr.AddReference("Clang")
import Clang
from Clang.Preprocessor import PpContext
from Clang.Preprocessor import ClangScanner
from Clang.Preprocessor import ClangToken

__ppContext = None
__traceInfo = []

class TraceInfoEncoder(json.JSONEncoder):
    def default( self, obj):
        #print("encoding")
        if( isinstance(obj, TraceInfo)):
            return obj.GetAsJsonObj()
        return json.JSONEncoder.default( self, obj )

class TraceInfo:
    def __init__(self, id, traceString, fileName, lineNr, nrOfArguments ):
        self._id = id
        self._traceString = traceString
        self._file = fileName
        self._line = lineNr
        self._nrOfArgs = nrOfArguments
    def GetAsJsonObj(self):
        return {"class": "TraceInfo",
                "MsgId": self._id,
                "TraceString": self._traceString,
                "File": self._file,
                "LineNumber": self._line,
                "NumberOfArguments": self._nrOfArgs}


def InitPreprocessor(appInclues, sysIncludes):
    global __ppContext
    if not __ppContext:
        __ppContext = PpContext()
    for inc in appInclues:
        __ppContext.AddApplicationInclude(inc)
    for inc in sysIncludes:
        __ppContext.AddSystemInclude(inc)
    #print( "adding " + str((gccRoot / 'avr' / 'include')))
    __ppContext.AddSystemInclude(str((gccRoot / 'avr' / 'include')))
    __ppContext.SetPredefinedSymbol("__AVR_DEV_LIB_NAME__", "m32")
    __ppContext.SetPredefinedSymbol("__GNUC__", "5")
    __ppContext.SetPredefinedSymbol("__INT_MAX__", "0x7FFF")
    __ppContext.ResetMacros()
    return __ppContext

def DumpToken( token, f ):
    for ch in token.LeadingWhiteSpace:
        if ch == "\r": continue
        f.write( ch )
    f.write( token.TokenString )

def GetTokenStr(token):
    return functools.reduce(lambda x, y: x+y, token.LeadingWhiteSpace, '') + token.TokenString

def RewriteTrace( startToken, tokenizer, f ):
    global __traceInfo

    def EvalArgs( traceStr ):
        args = re.finditer('%(?P<size>\d\d?)', traceStr)
        arguments = list(map(lambda x: int(x.group('size')), args ))
        #print (arguments)
        sum = int(functools.reduce(lambda x, y: x+ y, arguments, 0 ) / 8)
        return sum, arguments

    def WriteTraceArg( x, y, f):
        argCast = {8:'uint8_t', 16: 'uint16_t', 32: 'uint32_t'}
        cast = argCast[x]
        while x > 8:
            f.write( "(uint8_t)(({0})({1})>>{2}),".format(cast, y.strip(), x-8))
            x-=8
        f.write("(uint8_t)(({0}){1})".format(cast, y.strip()))

    global __traceInfo

    traceId = len(__traceInfo) + 1
    t = tokenizer.GetNextToken()
    assert( t.Id == ClangToken.LPar )
    t = tokenizer.GetNextToken()
    assert( t.Id == ClangToken.String )
    traceString = t.TokenString
    nrOfBytes, arguments = EvalArgs(traceString)

    nesting = 1
    traceArgTokens = []
    nrOfArguments = 0
    t = tokenizer.GetNextToken()
    singleArg = []
    while True:
        assert( t )
        if t.Id == ClangToken.Comma:
            if nesting == 1 and len(singleArg) > 0:
                traceArgTokens.append( functools.reduce(lambda x, y: x + y, singleArg, '') )
                singleArg.clear()
        elif t.Id == ClangToken.LPar:
            nesting += 1
        elif t.Id == ClangToken.RPar:
            nesting -= 1
            if nesting == 0:
                traceArgTokens.append( functools.reduce(lambda x,y: x + y, singleArg, '') )
                break
        else:
            singleArg.append(GetTokenStr(t))

        t = tokenizer.GetNextToken()

    #print( len(arguments))
    #p#rint( traceArgTokens )
    trace = TraceInfo( traceId, traceString, t.FileName, t.LineNumber, len(arguments) )
    __traceInfo.append(trace)
    f.write( functools.reduce(  lambda x, y: x + y, startToken.LeadingWhiteSpace, '' ))
    f.write( 'Usart_Trace{}('.format(str(nrOfBytes)) )
    f.write( str(traceId) )

    if len(arguments) > 0:
        f.write( ',' )
        assert( len(traceArgTokens) == len(arguments))
        for i in range(len(traceArgTokens)-1):
            WriteTraceArg(arguments[i], traceArgTokens[i], f )
            f.write( ', ')
        WriteTraceArg(arguments[-1], traceArgTokens[-1], f )
    f.write(')')


def Preprocess( input, outDir ):
    global __ppContext
    scanner = ClangScanner(__ppContext, input)
    fileName = pathlib.Path(input).parts[-1]
    outputFile = pathlib.Path(outDir) / fileName
    #print (str(outputFile))
    with open(str(outputFile), "w") as f:
        while scanner.MoveNext():
            for ch in scanner.Current.LeadingWhiteSpace:
                f.write( ch )
            f.write( scanner.Current.TokenString )

def Rewrite( input, outDir):
    global __ppContext, __traceInfo
    scanner = ClangScanner(__ppContext, input)
    scanner.Reset()
    tokenizer = scanner.GetTokenizer();
    fileName = pathlib.Path(input).parts[-1]

    outputFile = pathlib.Path(outDir) / fileName
    #print ( outputFile )
    if outputFile.exists():
        os.remove(outputFile)
    try:
        with open(str(outputFile), "w") as f:
            t = tokenizer.GetNextToken()
            while t:
                if t.Id == ClangToken.Identifier and t.TokenString == "TRACE":
                    RewriteTrace(t, tokenizer, f)
                else:
                    DumpToken(t,f)
                t = tokenizer.GetNextToken()

    finally:
        f.close()

def ClearTraceRecords():
    global __traceInfo
    __traceInfo = []

def DumpTraceRecords(path):
    global __traceInfo
    #print("dumping traceinfo:")
    #print( __traceInfo )
    traceInfoFile = pathlib.Path(path) / "TraceRecords.json"
    with open(traceInfoFile, "w") as f:
        json.dump(__traceInfo,f, cls=TraceInfoEncoder)

if __name__ == "__main__":
    InitPreprocessor([], [])
    outputPath = sys.argv[1]
    for f in sys.argv[2:]:
        print ( "rewriting {0} => {1}".format( f, outputPath))
        Rewrite(f, outputPath)
