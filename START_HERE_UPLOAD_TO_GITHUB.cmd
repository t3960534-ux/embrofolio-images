@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Embrofolio - Upload JPG Pins to GitHub
set "OWNER=t3960534-ux"
set "REPO=embrofolio-images"
echo.
echo  EMBROFOLIO - 64 FULL-RESOLUTION JPGs
 echo  GitHub destination: %OWNER%/%REPO%
 echo  The repository must be PUBLIC so Pinterest can fetch images.
 echo.
echo  Note: This requires Git and GitHub CLI (gh), signed into the correct account.
echo.
where git >nul 2>&1
if errorlevel 1 (echo ERROR: Install Git for Windows first: https://git-scm.com/download/win& goto end)
where gh >nul 2>&1
if errorlevel 1 (echo ERROR: Install GitHub CLI first: https://cli.github.com/& goto end)
gh auth status >nul 2>&1
if errorlevel 1 (
 echo Sign in to GitHub in the browser...
 gh auth login
 if errorlevel 1 goto end
)
for /f "delims=" %%U in ('gh api user --jq .login') do set "SIGNED_IN=%%U"
if /I not "%SIGNED_IN%"=="%OWNER%" (
 echo ERROR: GitHub CLI must be signed into %OWNER%. Run gh auth login --web and select that account.
 goto end
)
cd /d "%~dp0"
if not exist ".git" (
  git init -b main
  if errorlevel 1 goto end
)
git config --local credential.https://github.com.username "%OWNER%"
git config --local --replace-all credential.https://github.com.helper ""
git config --local --add credential.https://github.com.helper manager
git add pins README.md metadata TOOLS *.cmd *.txt .gitignore
if errorlevel 1 goto end
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Add 64 Embrofolio full-resolution JPG Pin images"
  if errorlevel 1 (
    echo ERROR: Configure git user.name and user.email before committing.
    goto end
  )
)
git branch -M main
if errorlevel 1 goto end
gh repo view "%OWNER%/%REPO%" >nul 2>&1
if errorlevel 1 (
 echo Creating PUBLIC image repository...
 gh repo create "%OWNER%/%REPO%" --public --description "Embrofolio Pinterest images" --disable-issues --disable-wiki
 if errorlevel 1 goto end
)
git remote get-url origin >nul 2>&1
if errorlevel 1 (
 git remote add origin "https://github.com/%OWNER%/%REPO%.git"
) else (
 git remote set-url origin "https://github.com/%OWNER%/%REPO%.git"
)
git push -u origin main
if errorlevel 1 (echo ERROR: Push failed. Check permissions and repo ownership.& goto end)
for /f "delims=" %%H in ('git rev-parse HEAD') do set "COMMIT=%%H"
cd /d "%~dp0"
echo.
echo Upload successful. Commit: %COMMIT%
echo Creating Pinterest imports only after checking PUBLIC media URLs...
where py >nul 2>&1
if not errorlevel 1 (
 py "TOOLS\BUILD_IMPORT_CSV.py" --owner "%OWNER%" --repo "%REPO%" --ref "%COMMIT%" --verify
) else (
 python "TOOLS\BUILD_IMPORT_CSV.py" --owner "%OWNER%" --repo "%REPO%" --ref "%COMMIT%" --verify
)
if errorlevel 1 (echo Some GitHub links may need time. Run RECHECK_BUILD_PINTREST_CSV.cmd shortly.)
:end
echo.
echo If successful, open PINTEREST_READY, and test ONE PIN before importing all.
pause
