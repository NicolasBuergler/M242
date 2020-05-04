echo off
if [%1] == [] (echo [41m** no GitRoot specified ** [0m ) & (goto :EOF)
set GitRoot=%1%
if [%2] == [] (echo [41m** no Project specified ** [0m ) & (goto :EOF)
set Project=%2
set ProjectRoot=%GitRoot%\%Project%
set ProjectBuild=%ProjectRoot%\Build
set ToolsRoot=%CD%\ToolChain
set PyScripts=%ToolsRoot%\PyScripts
set AvrGcc=%ToolsRoot%\avr8-gnu-toolchain-win32_x86
set AvrDude=%ToolsRoot%\avrdude-6.3-mingw32
set DotNetLib=%ToolsRoot%\DotNetLib
set Batch=%ToolsRoot%\Batch
if not exist %ProjectRoot% mkdir %ProjectRoot%
if not exist %ProjectRoot%\Build mkdir %ProjectRoot%\Build
if not exist %ProjectRoot%\make.bat copy %Batch%\make.bat %ProjectRoot%
if not exist %ProjectRoot%\%Project%.vcxproj python.exe %PyScripts%\GenerateVsProject.py
cd %ProjectRoot%
call cmd.exe /K echo  [32m **  environment set to %Project% ** [0m
