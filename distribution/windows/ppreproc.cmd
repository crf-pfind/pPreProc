@echo off
setlocal
set "PPREPROC_EXE=%~dp0runtime\pParse2Plus\pParse2Plus.exe"

if not exist "%PPREPROC_EXE%" (
  echo pPreProc runtime was not found: "%PPREPROC_EXE%" 1>&2
  exit /b 1
)

pushd "%~dp0runtime\pParse2Plus" >nul || exit /b 1
"%PPREPROC_EXE%" %*
set "PPREPROC_EXIT=%ERRORLEVEL%"
popd
exit /b %PPREPROC_EXIT%
