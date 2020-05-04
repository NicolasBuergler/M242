import string, pathlib
import PeripheralModel as PM

fileHeaderTemplate = """/**
* @file: $name
*
* automatically generated; do not edit
*/

#ifndef $guard
#define $guard

$includes
"""



class HeaderWriter:

    def __init__(self, fileName, includes_ ):
        self._filePath = pathlib.Path(fileName)
        guard = "__{0}__".format( self._filePath.name.replace('.','_'))
        includes = "\n".join(map(lambda x: "#include {0}".format(x), includes_))
        self._codeLines = []
        t = string.Template(fileHeaderTemplate)
        self._codeLines.append(t.substitute(name=self._filePath.name, guard = guard, includes = includes))

        #dump type definitions
        for t in PM.KnownTypes.values():
            t.AcceptModelWriter(self)

        #dump memory sections
        for m in PM.MemorySections:
            m.AcceptModelWriter(self)

        self.DumpCode()

    def DumpCode(self):
        with self._filePath.open('w') as f:
            f.write("\n".join(self._codeLines))
            f.write("\n#endif\n")

    def VisitStruct(self, typeNode):
        name = typeNode.GetName()
        self._codeLines.append( "typedef struct {0}_tag".format( name ))
        self._codeLines.append( "{")
        for f in typeNode.GetStructFields():
            f.AcceptModelWriter(self)
        self._codeLines.append( "}} {0};".format(name))

    def VisitEnum(self, enumNode ):
        name = enumNode.GetName()
        self._codeLines.append( "typedef enum" )
        self._codeLines.append( "{")
        for e in enumNode.GetEnumeration():
            self._codeLines.append("    {0}={1},".format(e[0], e[1]))
        self._codeLines.append( "}} {0};".format(name))
        self._codeLines.append("")


    def VisitInteger( self, integerNode):
        for bf in integerNode.GetBitfields():
            bf.AcceptModelWriter(self)

    def VisitField(self, f):
        fieldName = f.GetName()
        fieldType = f.GetType()
        c_type = PM.IntegerTypeMap.get(fieldType.GetFormatString(), fieldType.GetName())
        modifier = ""
        if f.GetParentStereotype() == 'HardwarePeripheral':
            modifier = "volatile"
        self._codeLines.append("    {0} {1} {2};".format(modifier, c_type, fieldName))

    def VisitMemorySection( self, sectionNode):
        address = sectionNode.GetBaseAddress()
        for sym in sectionNode.GetMemorySymbols():
            sym.AcceptModelWriter(self)

    def VisitMemorySymbol( self, symbolNode):
        name = symbolNode.GetName()
        symbolType = symbolNode.GetType()
        stereotype = symbolType.GetStereotype()
        c_type = PM.IntegerTypeMap.get(symbolType.GetFormatString(), symbolType.GetName())
        modifer = ""
        if( stereotype == 'HardwarePeripheral' or stereotype == 'HardwareRegister'):
            modifier = "volatile"
        address = symbolNode.GetAddress()
        self._codeLines.append("#define {0} (*(({1} {2}*)0x{3:08X}))".format(name, modifier, c_type, address))

    def VisitBitfield(self, bitfieldNode):

        maskName = bitfieldNode.GetDecoratedName( 'mask')
        posName = bitfieldNode.GetDecoratedName( 'pos')
        widthName = bitfieldNode.GetDecoratedName('width')
        self._codeLines.append("/**")
        self._codeLines.append("* bitfield {0}".format( bitfieldNode.GetName()))
        self._codeLines.append("*/")
        self._codeLines.append("#define {0} {1}".format(maskName, bitfieldNode.GetMask()))
        self._codeLines.append("#define {0} {1}".format(posName, bitfieldNode.GetPosition()))
        self._codeLines.append("#define {0} {1}".format(widthName, bitfieldNode.GetWidth()))
        self._codeLines.append("")
