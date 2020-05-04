import os, pathlib, sys, string, json
import Preprocess

targetConfigs = {}
configPath = pathlib.Path(os.environ['ToolsRoot']) / "Config" / "TargetConfig.json"

with open( str(configPath), "r" ) as f:
    targetConfigs = json.load(f)

flashTargetTemplate = """
flash: $(OUT_FILE_PATH)
\t$(AvrDude)\\AvrDude.exe -c $programmer -P $port -p $device -U flash:w:"$(ProjectBuild)\\$(Project).elf":e
"""

elfLinkerTemplate = """
$(OUT_FILE_PATH): $(OBJS) $(LIB_DEP) $(LINKER_SCRIPT_DEP)
\t@echo Building target: $@
\t@echo Invoking  AVR\\GNU Linker : 5.4.0
\t$(AVR_TOOLS_PATH)\\bin\\avr-gcc.exe -o$(OUT_FILE_PATH) $(OBJS_AS_ARGS) $(LIB_DEP) -Wl,-Map="$(ProjectBuild)\\$(Project).map" -Wl,--start-group -Wl,-lm  -Wl,--end-group -Wl,--gc-sections -mmcu=$(MMCU) -B "$(AVR_TOOLS_PATH)\\avr\\Lib"
\t@echo Finished building target: $@
\t$(AVR_TOOLS_PATH)\\bin\\avr-objcopy.exe -O ihex -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures  "$(ProjectBuild)\\$(Project).elf" "$(ProjectBuild)\\$(Project).hex"
\t$(AVR_TOOLS_PATH)\\bin\\avr-objcopy.exe -j .eeprom  --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0  --no-change-warnings -O ihex "$(ProjectBuild)\\$(Project).elf" "$(ProjectBuild)\\$(Project).eep" || exit 0
\t$(AVR_TOOLS_PATH)\\bin\\avr-objdump.exe -h -S "$(ProjectBuild)\\$(Project).elf" > "$(ProjectBuild)\\$(Project).lss"
\t$(AVR_TOOLS_PATH)\\bin\\avr-objcopy.exe -O srec -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures "$(ProjectBuild)\\$(Project).elf" "$(ProjectBuild)\\$(Project).srec"
\t$(AVR_TOOLS_PATH)\\bin\\avr-size.exe $(OUT_FILE_PATH)
"""

aLinkerTemplate = """
$(OUT_FILE_PATH): $(OBJS) $(OUTPUT_FILE_DEP)
\t@echo Building target: $@
\t@echo Invoking: AVR/GNU Archiver : 5.4.0
\t$(AVR_TOOLS_PATH)\\bin\\avr-ar.exe -ro $(OUT_FILE_PATH) $(OBJS) $(LIBS)
\t@echo Finished building target: $@
"""

compileSrcTemplate = """
$objectFile: $sourceFile
\t@echo Building file: $<
\t@echo Invoking: AVR\\GNU C Compiler : 5.4.0
\t$(AVR_TOOLS_PATH)\\bin\\avr-gcc.exe $lang $langSpec -Werror -funsigned-char -funsigned-bitfields -DDEBUG -D$(AVR_FAMILY) -I "$(AVR_LIB_PATH)\\include" -I"$(AVR_TOOLS_PATH)\\avr\\include" -I"$(ProjectRoot)"  -O1 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -g2 -Wall -mmcu=$(MMCU) -B "$(AVR_TOOLS_PATH)\\avr\\Lib" -c  -save-temps -MD -MP -MF "$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)"   -o "$@" "$<"
\t@echo Finished building: $<
"""

makeFileTemplate = """
################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL := cmd.exe
PY := Python.exe
RM := del /F

PROJECT := $(Project)
PREPROCESSING_SRCS :=
OBJS :=
OBJS_AS_ARGS :=
C_DEPS :=
C_DEPS_AS_ARGS :=
EXECUTABLES :=
OUT_FILE_PATH := $(ProjectBuild)\\$(Project).$extension
AVR_TOOLS_PATH := $(AvrGcc)
AVR_LIB_PATH := $(ToolsRoot)\\AvrLib
AVR_FAMILY := $AvrFamily
QUOTE := "
OUTPUT_FILE_DEP:=
LIB_DEP:=
MMCU:=$target

# Add inputs and outputs from these tool invocations to the build variables
C_SRCS +=  $cSources

ASM_SRCS += $asmSources

OBJS +=  $objects

OBJS_AS_ARGS +=  $objects

C_DEPS +=  $cDependencies

C_DEPS_AS_ARGS +=  $cDependencies

LIB_DEP+= $(AVR_LIB_PATH)\\$AvrFamilyPath\\AvrLib.a

LINKER_SCRIPT_DEP+=

# compile sources
$compileSources


# AVR32\\GNU Preprocessing Assembler

# AVR32\\GNU Assembler

#include dependencies if it's not make clean
ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

# Add inputs and outputs from these tool invocations to the build variables

#flash to device; includes building
$flashTarget

# All Target
all: $(OUT_FILE_PATH)

$linkerStage

# Other Targets
clean:
\t$(RM) $(ProjectBuild)\\*.c
\t$(RM) $(ProjectBuild)\\*.i
\t$(RM) $(ProjectBuild)\\*.d
\t$(RM) $(ProjectBuild)\\*.o
\t$(RM) $(ProjectBuild)\\$(Project).*
"""

def GenerateMake( inputDir, outputDir, toolsRoot, linkerStage = 'elf'):

    def MakeFileList( s, outDir, extension ):
        return list(map( lambda x: "{0}\\{1}.{2}".format(outDir, x.stem, extension), s ))

    def FillCompilerTemplate(dest, source):
        print ( "compile {0} => {1}".format(source, dest))
        langSpec = ""
        lang = ""
        sourcePath = pathlib.Path( source )
        if sourcePath.suffix == '.c':
            langSpec = "-std=gnu99"
            lang = "-x c"
        m = {
        'lang': lang,
        'langSpec': langSpec,
        'objectFile': str(dest),
        'sourceFile': str(source) }
        t = string.Template(compileSrcTemplate)
        return t.safe_substitute(m)

    p = pathlib.Path(inputDir)
    print( inputDir )
    print("********************************")
    sources = [x  for x in p.iterdir() if x.suffix == ('.c')]
    print ( sources )
    Preprocess.InitPreprocessor([], [])
    for s in sources:
        Preprocess.Rewrite(str(s), outputDir)
    Preprocess.DumpTraceRecords(outputDir)
    asmSources =  [x  for x in p.iterdir() if x.suffix == ('.s')]
    asmSourceList = list(map( str, asmSources))
    print( asmSources )
    ppSourceList = MakeFileList(sources, outputDir, 'c') + asmSourceList
    print (ppSourceList)
    objectList = MakeFileList(sources + asmSources, outputDir, 'o')
    print ( objectList )
    flashTarget = ''

    if linkerStage == 'elf': #otherwise we should not generate a flash target!
        flashTarget = string.Template(flashTargetTemplate).safe_substitute(
            programmer=targetConfigs['programmer'],
            port=targetConfigs['port'],
            device = targetConfigs['device'])

    device = targetConfigs['device']
    AvrFamily = '__AVR_DEV_LIB_NAME__={0}'.format(device)
    if device == 'm328p':
        AvrFamily = '__AVR_ATmega328P__=1'
    replaceMap = {
        'linkerStage': eval("{0}LinkerTemplate".format(linkerStage)),
        'cSources': " ".join( map(str, sources ) ),
        'AvrFamily': AvrFamily,
        'AvrFamilyPath': targetConfigs['target'],
        'asmSources': "",
        'ToolsRoot' : toolsRoot,
        'ppSources': " ".join( ppSourceList ),
        'objects' : " ".join( objectList ),
        'cDependencies': " ".join( MakeFileList(sources, outputDir, 'd')),
        'compileSources' : "\n".join( list(map( FillCompilerTemplate, objectList, ppSourceList))),
        'target' : targetConfigs['target'],
        'flashTarget' : flashTarget,
        'extension' : linkerStage
        }

    ppSourceList = None
    objectList = None
    temp = string.Template(makeFileTemplate)
    makeFile = temp.safe_substitute(replaceMap)
    with open( pathlib.Path(outputDir) / "Makefile", "w") as f:
        f.write(makeFile)

if __name__ == "__main__":
    assert( len(sys.argv) == 4 )
    projRoot = sys.argv[1]
    projBuild = sys.argv[2]
    linkerStage = sys.argv[3]
    toolsRoot = os.environ['ToolsRoot']
    GenerateMake( projRoot, projBuild, toolsRoot, linkerStage )

#GenerateMake(r'C:\Users\rolfl\Documents\GitHub\Avr\HelloWorld', r'C:\Users\rolfl\Documents\GitHub\Avr\HelloWorld\Build')
