import sys, pathlib, os, traceback, subprocess, string

sys.path.append(r'C:\Users\rolfl\Documents\GIBZ\py')

import StudentsInfo




batchFileTemplate = """
set ProjectRoot=$projectRoot
set ProjectBuild=%ProjectRoot%\\Build
set ToolsRoot=$toolsRoot
set PyScripts=%ToolsRoot%\\PyScripts
set AvrGcc=%ToolsRoot%\\avr8-gnu-toolchain-win32_x86
set AvrDude=%ToolsRoot%\\avrdude-6.3-mingw32
set DotNetLib=%ToolsRoot%\\DotNetLib
python %PyScripts%\GenerateMake.py %ProjectRoot% %ProjectBuild% elf
pushd %ProjectBuild%
call make.exe -f "%ProjectBuild%\\Makefile" flash
popd
"""


def GitCloneOrUpdateRepo(rootDir, folderName, repoName, repo ):
    p = pathlib.Path(rootDir) / folderName
    if not p.exists():
        os.makedirs(str(p))
        stat = subprocess.run("git clone {0} {1}".format(repo, repoName), capture_output=True, cwd=str(p) )

    else:
        pr = p / repoName
        if not pr.exists():
            print( "clone repo!!")
            stat = subprocess.run("git clone {0} {1}".format(repo, repoName), capture_output=True, cwd=str(p) )
            print( stat )
        else:
            stat = subprocess.run("git pull origin master", cwd=str(pr))
    stat.check_returncode()


def GenerateBatchFile(toolsRoot, projectRoot):
    template = string.Template( batchFileTemplate  )
    content = template.safe_substitute(projectRoot=projectRoot, toolsRoot=toolsRoot)
    batchfile = pathlib.Path(projectRoot) / "MakeAndRun.bat"
    with open(str(batchfile), "w") as f:
        f.write(content)
    return str(batchfile)


def BuildProject( rootDir, folderName, projectName ):
    toolsRoot = pathlib.Path( rootDir ) / "AVR" / "ToolChain"
    projectRoot = pathlib.Path(rootDir) / folderName / "M242" / projectName
    projectBuild = projectRoot / "Build"
    if not projectBuild.exists():
        os.makedirs(str(projectBuild))

    batchFile = GenerateBatchFile(toolsRoot, projectRoot )
    subprocess.run(batchFile)


#GitCloneOrUpdateRepo(r"e:\M242", "Lars_Voegtle", "M242", "https://github.com/laeshe1886/M242_Project")
#BuildProject(ProjectsRoot, "Lars_Voegtle", "M242")



#Send_E_Mail("test", ['rlaich@gibz.ch'], "blabla",
#    [r'C:\Users\rolfl\OneDrive - GIBZ\M242\Semester2020\Adress-Etiketten.docx']
#    )
