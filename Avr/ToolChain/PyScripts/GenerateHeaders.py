import os, sys, pathlib, string
import xml.etree.ElementTree as xet
import PeripheralModel as PM
import HeaderWriter as HW


Namespace =  {'e':'http://tempuri.org/EntityDescription.xsd',
              'xsi':'http://www.w3.org/2001/XMLSchema-instance'}


def LoadModel(calledFrom, fileName):
    print( "* Load types {0}".format(fileName) )
    filePath = pathlib.Path(fileName)
    assert filePath.suffix == '.xml', "for now only xml files supported"
    if not filePath.exists():
        filePath = pathlib.Path(calledFrom).parent / filePath
    assert filePath.exists(), "file {0} does not exist".format(filePath)
    tree = xet.parse(str(filePath))
    root = tree.getroot()
    for _import_ in root.iter('{http://tempuri.org/EntityDescription.xsd}Import'):
        referenced = _import_.get('LibraryOrFile')
        print("** ", referenced )
        if _import_.get('ByReference') == 'true':
            LoadModel( fileName, referenced  )

    for td in root.iter('{{{0}}}TypeDefinition'.format(PM.Namespace['e'])):
        #print(td.tag, td.attrib)
        PM.CreateType(td)

    for mem in root.iter('{{{0}}}MemorySection'.format(PM.Namespace['e'])):
        PM.MemorySection(mem)


def GeneratePeripherals(xmlName, output, includes):
    LoadModel( "", xmlName )

    for t in PM.KnownTypes.values():
        print( "**", t.GetName(), t.GetFormatString())

    HW.HeaderWriter(output, includes)


if __name__ == "__main__":
    p = pathlib.Path(__file__)
    xmlPath = (((p.parent.parent.parent.parent / 'XmlModel') / 'HardwareDescription') / 'Avr')
    xmlFile = xmlPath / 'Atmega328P.xml'
    dest = ((p.parent.parent / 'AvrLib') / 'Include') / 'Atmega328P.h'
    includes = ['<avr/sfr_defs.h>', '<avr/common.h>', '<inttypes.h>']
    GeneratePeripherals(xmlFile, dest, includes )
