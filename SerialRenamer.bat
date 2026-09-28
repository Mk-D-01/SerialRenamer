@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "self=%~nx0"
set "counter=1"

for /f "delims=" %%F in ('dir /b /a-d /on') do (
    if /I not "%%F"=="!self!" (
        set "ext=%%~xF"
        echo Renaming: %%F -^> !counter!!ext!
        ren "%%F" "!counter!!ext!"
        set /a counter+=1
    )
)

set /a renamed=!counter!-1
echo.
echo Done. Renamed !renamed! file(s).
pause
endlocal
