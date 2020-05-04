python %PyScripts%\GenerateMake.py %ProjectRoot% %ProjectBuild% a
pushd %ProjectBuild%
call make.exe -f "%ProjectBuild%\Makefile" %1
popd
