@echo off
set "EXE=main.exe"
set "NOMBRE=MiPrograma"
set "DEST=%USERPROFILE%\Desktop\%NOMBRE%.lnk"

powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DEST%');$s.TargetPath='%~dp0%EXE%';$s.WorkingDirectory='%~dp0';$s.Save()"

echo Acceso directo creado en el escritorio.
pause