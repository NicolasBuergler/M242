import xml.etree.ElementTree as xet

Namespace =  {'e':'http://tempuri.org/EntityDescription.xsd',
              'xsi':'http://www.w3.org/2001/XMLSchema-instance'}

IntegerTypeMap = {  "B": "uint8_t",
                    "H": "uint16_t",
                    "I": "uint32_t",
                    "c": "int8_t",
                    "h": "int16_t",
                    "i": "int32_t"}

SignedIntFormatMap = {1:'c',2:'h',4:'i',8:'q'}
UnsignedIntFormatMap = {1:'B',2:'H',4:'I',8:'Q'}

KnownTypes = {}
MemorySections = []

def ReadDezOrHexInteger(numString):
    base=10
    if numString.startswith('0x'):
        base=16
    return int(numString, base)

class ModelNode:
    def __init__(self, node):
        self._node = node
        self._name = self._node.get('Name')

    def GetName(self):
        return self._name

    def GetXmlElement(self):
        return self._node

    def AcceptModelWriter(self, writer):
        pass

class MemorySymbol(ModelNode):
    def __init__( self, node, baseAddress ):
        ModelNode.__init__(self, node)
        self._baseAddress = baseAddress
        self._type = None

    def AcceptModelWriter(self, writer):
        writer.VisitMemorySymbol(self)

    def GetType(self):
        if self._type == None:
            typeName = self._node.get('Type')
            self._type = KnownTypes[typeName]
        return self._type

    def GetAddress(self):
        address = ReadDezOrHexInteger(self._node.get('Offset')) + self._baseAddress
        return address


class MemorySection(ModelNode):
    def __init__(self, node):
        ModelNode.__init__(self, node)
        self._address = ReadDezOrHexInteger( self._node.get('Address'))
        self._symbols = []
        for sym in self._node.findall('e:Symbol', Namespace):
            self._symbols.append( MemorySymbol( sym, self._address ))
        MemorySections.append(self)

    def GetBaseAddress(self):
        return self._address

    def GetMemorySymbols(self):
        return self._symbols

    def AcceptModelWriter(self, writer):
        writer.VisitMemorySection(self)

class Bitfield(ModelNode):
    def __init__(self, node, definedIn):
        ModelNode.__init__(self, node)
        self._definedIn = definedIn
        self._pos = -1
        self._width = -1
        self._mask = None
        print("creating bitfield", self.GetName())
        valueSet = node.find('e:ValueSet', Namespace)
        if valueSet:
            EnumType(valueSet)

    def GetDecoratedName(self, suffix):
        name = self._definedIn.GetName()
        namePrefix = name[:name.index('_T')]
        bitfieldName = self.GetName()
        if bitfieldName.startswith('_'):
            bitfieldName = bitfieldName[1:]
        return "{0}_{1}_{2}".format(namePrefix, bitfieldName, suffix )

    def GetPosition(self):
        if self._pos == -1:
            self._pos = ReadDezOrHexInteger( self._node.get('Position'))
        return self._pos

    def GetMask(self):
        if self._mask == None:
            maskValue = ((1<<self.GetWidth())-1)<<self.GetPosition()
            maskFormat = "0x{{0:0{0}X}}".format(self._definedIn.GetSize()*2)
            self._mask = maskFormat.format(maskValue)
        return self._mask

    def GetWidth(self):
        if self._width == -1:
            self._width = ReadDezOrHexInteger( self._node.get('Width'))
        return self._width

    def AcceptModelWriter(self, writer):
        writer.VisitBitfield(self)



class Field(ModelNode):
    def __init__( self, node, stereotype):
        ModelNode.__init__(self, node)
        self._type = None
        self._isAligned = False
        self._alignementBoundary = 0
        self._parentStereotype = stereotype #this is used to generate volatile members
        alignemetBoundary = self._node.get('Aligned')
        if alignemetBoundary:
            self._isAligned = True
            self._alignementBoundary = int(alignemetBoundary)

    def GetParentStereotype(self):
        return self._parentStereotype

    def SetOffset(self, offset):
        size = self.GetType().GetSize()
        if _isAligned:
            if (offset % self._alignementBoundary) != 0:
                offset = (offset + size)&~(self._alignementBoundary-1)
            self._offset = offset
        else:
            self._offset = ReadDezOrHexInteger( self._node.find('e:Position', Namespace).text )
        return self._offset + size

    def GetType(self):
        if self._type == None:
            t = self._node.get('FieldType').strip()
            assert  t in KnownTypes, "unknown field type {0}".format(t)
            self._type = KnownTypes[t]
        return self._type

    def AcceptModelWriter(self, writer):
        writer.VisitField(self)

def CreateType(xmlNode):
    type = xmlNode.get('{{{0}}}type'.format(Namespace['xsi']))
    if type == 'StructType':
        return StructType(xmlNode)
    if type == 'IntegerType':
        return IntegerType(xmlNode)
    if type == 'EnumType':
        return EnumType(xmlNode)

class TypeDefinition(ModelNode):
    def __init__(self, node):
        ModelNode.__init__(self, node)
        KnownTypes[self.GetName()] = self
        self._stereotype = self._node.find("e:Stereotype", Namespace)
        if self._stereotype != None:
            self._stereotype = self._stereotype.text

    def GetStereotype(self):
        return self._stereotype

    def GetFormatString(self):
        pass

    def GetSize(self):
        pass

class EnumType(TypeDefinition):

    def __init__(self, t):
        TypeDefinition.__init__(self, t)
        self._size = -1
        self._enums = []

    def GetSize(self):
        if self._size == -1:
            size = self._node.get('Size')
            if size != None:
                maxValue = (1 << (int( size )*8))-1
            else:
                maxValue = 0
            value = 0
            for e in self._node.findall('e:Enum', Namespace):
                enumValue = e.get('Value')
                enumName = e.get('Name')
                if not enumValue:
                    enumValue = value
                else:
                    enumValue = int(enumValue)
                self._enums.append((enumName, enumValue))
                value = enumValue + 1
                posValue = abs(enumValue)
                if maxValue < posValue:
                    maxValue = posValue
            if maxValue < 256:
                self._size = 1
            elif maxValue < 1<<16:
                self._size = 2
            elif maxValue < 1 <<32:
                self._size = 4
            else:
                self._size = 8
        return self._size

    def GetEnumeration(self):
        return self._enums

    def GetFormatString(self):
        size = self.GetSize()
        return UnsignedIntFormatMap[size]

    def AcceptModelWriter(self, writer):
        writer.VisitEnum(self)

class IntegerType(TypeDefinition):

    def __init__(self, node):
        TypeDefinition.__init__(self, node)
        self._size = -1
        self._bitfields = None
        print( "creating integer", self.GetName() )
        self._bitfields = list(map(lambda x: Bitfield( x, self), self._node.findall('e:Bitfield', Namespace)))

    def GetBitfields(self):
        return self._bitfields

    def GetSize(self):
        if self._size == -1:
            self._size = int( self._node.get('Size'))
            self._isSigned = self._node.get('Signed') == 'true'
        return self._size

    def GetFormatString(self):
        size = self.GetSize()
        if self._isSigned:
            return SignedIntFormatMap[size]
        return UnsignedIntFormatMap[size]

    def AcceptModelWriter(self, writer):
        writer.VisitInteger(self)

class StructType(TypeDefinition):
    def __init__(self, node):
        TypeDefinition.__init__(self, node)
        self._fields = list(map(lambda x: Field(x, self._stereotype), self._node.findall('e:Field', Namespace)))

        self._size = -1
        self._formatString = ""

    def GetStructFields(self):
        return self._fields

    def GetSize(self):
        if self._size == -1:
            offset = 0
            for f in self._fields:
                offset = f.SetOffset(offset)
            self._size = offset
        return self._size

    def GetFormatString(self):
        if self._formatString == "":
            self._formatString = "".join( map( lambda f: f.GetType().GetFormatString(), self._fields))
        return self._formatString

    def AcceptModelWriter(self, writer):
        writer.VisitStruct(self)
