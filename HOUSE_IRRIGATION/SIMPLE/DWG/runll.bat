set exepath=AX2020_W32_20_05_28.exe
call :treeProcess
exit /b

:treeProcess
for %%f in (*.dwg) do call :processFile "%%f"
for /D %%d in (*) do (
    cd %%d
    call :treeProcess
    cd ..
)
exit /b

:processFile
set fName=%1:.dwg=.png%
del fName
%exepath% %1 -f=png -model -rsz=5000
exit /b