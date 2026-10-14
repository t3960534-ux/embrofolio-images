@echo off
setlocal
cd /d "%~dp0"
set "OWNER=t3960534-ux"
set "REPO=embrofolio-images"
for /f "delims=" %%H in ('git rev-parse HEAD') do set "COMMIT=%%H"
if "%COMMIT%"=="" set "COMMIT=main"
where py >nul 2>&1
if not errorlevel 1 (
 py "TOOLS\BUILD_IMPORT_CSV.py" --owner "%OWNER%" --repo "%REPO%" --ref "%COMMIT%" --verify
) else (
 python "TOOLS\BUILD_IMPORT_CSV.py" --owner "%OWNER%" --repo "%REPO%" --ref "%COMMIT%" --verify
)
pause
