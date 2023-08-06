::
::  before-test.cmd - Stages test and benchmark files for nrtest
::
::  Created: Oct 16, 2019
::  Updated: May 29, 2020
::
::  Author: See AUTHORS
::
::  Dependencies:
::    curl
::    7z
::
::  Environment Variables:
::    PROJECT
::    BUILD_HOME - defaults to "build"
::    PLATFORM
::    NRTESTS_URL - URL to set the test suite defaults to "https://github.com/OpenWaterAnalytics/%PROJECT%-nrtestsuite"
::
::  Arguments:
::    1 - (RELEASE_TAG) release tag for benchmark version (defaults to latest tag)
::
::  Note:
::    Tests and benchmark files are stored in the "%PROJECT%-nrtestsuite" repo.
::    This script retrieves them using a stable URL associated with a GitHub
::    release, stages the files, and sets up the environment for nrtest to run.
::

::@echo off

:: set global default
set "TEST_HOME=nrtests"

:: determine project directory
set "SCRIPT_HOME=%~dp0"
cd %SCRIPT_HOME%
pushd ..
pushd ..
set "PROJECT_DIR=%CD%"

setlocal


:: check that dependencies are installed
for %%d in (curl 7z) do (
  where %%d > nul
  if %ERRORLEVEL% neq 0 ( echo "ERROR: %%d not installed" & exit /B 1 )
)


:: set URL to github repo with test files
if not defined NRTESTS_URL (
  set NRTESTS_URL="https://github.com/OpenWaterAnalytics/%PROJECT%-nrtestsuite"
)

:: if release tag isn't provided latest tag will be retrieved
if [%1] == [] (set "RELEASE_TAG="
) else (set "RELEASE_TAG=%~1")


:: check env variables and apply defaults
for %%v in (PROJECT BUILD_HOME PLATFORM) do (
  if not defined %%v ( echo "ERROR: %%v must be defined" & exit /B 1 )
)

echo INFO: Staging files for regression testing


:: determine latest tag in the tests repo
if [%RELEASE_TAG%] == [] (
  for /F delims^=^"^ tokens^=2 %%g in ('curl --silent %NRTESTS_URL%/releases/latest') do (
    set "RELEASE_TAG=%%~nxg"
  )
)

if defined RELEASE_TAG (
  set TESTFILES_URL=%NRTESTS_URL%/archive/%RELEASE_TAG%.zip
  set BENCHFILES_URL=%NRTESTS_URL%/releases/download/%RELEASE_TAG%/benchmark-%PLATFORM%.zip
) else (
  echo ERROR: tag %RELEASE_TAG% is invalid & exit /B 1
)


:: create a clean directory for staging regression tests
if exist %TEST_HOME% (
  rmdir /s /q %TEST_HOME%
)
mkdir %TEST_HOME%
if %ERRORLEVEL% NEQ 0 ( echo "ERROR: unable to make %TEST_HOME% dir" & exit /B 1 )
cd %TEST_HOME%
if %ERRORLEVEL% NEQ 0 ( echo "ERROR: unable to cd %TEST_HOME% dir" & exit /B 1 )


:: retrieve nrtest cases and benchmark results for regression testing
curl -fsSL -o nrtestfiles.zip %TESTFILES_URL%
curl -fsSL -o benchmark.zip %BENCHFILES_URL%


:: extract tests, scripts, benchmarks, and manifest
7z x nrtestfiles.zip * > nul
7z x benchmark.zip -obenchmark\ > nul
7z e benchmark.zip -o. manifest.json -r > nul


:: set up symlinks for tests directory
mklink /D .\tests .\%PROJECT%-nrtestsuite-%RELEASE_TAG:~1%\public > nul


endlocal


:: determine REF_BUILD_ID from manifest file
for /F delims^=^"^ tokens^=4 %%d in ( 'findstr %PLATFORM% %TEST_HOME%\manifest.json' ) do (
  for /F "tokens=2" %%r in ( 'echo %%d' ) do ( set "REF_BUILD_ID=%%r" )
)
if not defined REF_BUILD_ID ( echo "ERROR: REF_BUILD_ID could not be determined" & exit /B 1 )

:: GitHub Actions
echo REF_BUILD_ID=%REF_BUILD_ID%>> %GITHUB_ENV%


:: return to users current directory
cd %PROJECT_DIR%
