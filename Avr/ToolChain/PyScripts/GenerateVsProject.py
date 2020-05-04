import pathlib, os, sys, string, uuid, json

srcItemTemplate = """
    <ClCompile Include="$filePath"/>"""

def GenerateVsTemplate( project, projectRoot, toolsRoot, avrGcc ):
    destPath = pathlib.Path(projectRoot);

    targetConfigs = {}
    configPath = pathlib.Path(toolsRoot) / "Config" / "TargetConfig.json"

    with open( str(configPath), "r" ) as f:
        targetConfigs = json.load(f)

    hardwarePlatform = "__AVR_DEV_LIB_NAME__=m32"
    if targetConfigs['target'] == "atmega328":
        hardwarePlatform = "__AVR_ATmega328P__=1"
    destFile = destPath / "{0}.vcxproj".format(project)
    sources = [ x.name for x in destPath.iterdir() if x.suffix == ".c"]
    srcItemTemplateInstance = string.Template(srcItemTemplate)
    clCompileList = "".join( map( lambda x: srcItemTemplateInstance.safe_substitute(filePath=str(x)), sources))
    templatePath = pathlib.Path(toolsRoot) / "VsProjectTemplate" / "VsProjectTemplate.vcxproj"
    with open( str(templatePath), "r") as fr:
        data = fr.read()
        t = string.Template(data)
        proj = t.safe_substitute(project = project, sources = clCompileList, avrGcc = avrGcc, uuid_ = str(uuid.uuid1()), toolchain=toolsRoot, HardwarePlatform=hardwarePlatform)
        with open(str(pathlib.Path(destFile)), "w") as fw:
            fw.write(proj)

if __name__ == '__main__':
    project = os.environ['Project']
    projectRoot = os.environ['ProjectRoot']
    avrGcc = os.environ['AvrGcc']
    toolsRoot =  os.environ['ToolsRoot']
    assert( project )
    assert( projectRoot )
    assert( avrGcc )
    assert( toolsRoot )
    GenerateVsTemplate( project, projectRoot, toolsRoot, avrGcc )
