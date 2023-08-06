@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
rem set BUILDDIR=build
set BUILDDIR=.
set ALLSPHINXOPTS=-a -E -d %BUILDDIR%\.doctrees %SPHINXOPTS% source
set I18NSPHINXOPTS=%SPHINXOPTS% source
if NOT "%PAPER%" == "" (
    set ALLSPHINXOPTS=-D latex_paper_size=%PAPER% %ALLSPHINXOPTS%
    set I18NSPHINXOPTS=-D latex_paper_size=%PAPER% %I18NSPHINXOPTS%
)

if "%1" == "" goto help

if "%1" == "help" (
    :help
    echo.Please use `make ^<target^>` where ^<target^> is one of
    echo.  apidoc    to make reference API files
    echo.  html       to make standalone HTML files
    goto end
)

if "%1" == "clean" (
    for /d %%i in (%BUILDDIR%\.doctrees\*) do rmdir /q /s %%i
    del /q /s %BUILDDIR%\.doctrees\*
    for /d %%i in (%BUILDDIR%\html\*) do rmdir /q /s %%i
    del /q /s %BUILDDIR%\html\*
    for /d %%i in (source\api\*) do rmdir /q /s %%i
    del /q /s source\api\*
    goto end
)


REM Check if sphinx-build is available and fallback to Python version if any
%SPHINXBUILD% 1>NUL 2>NUL
if errorlevel 9009 goto sphinx_python
goto sphinx_ok

:sphinx_python

set SPHINXBUILD=py -3 -m sphinx.__init__
%SPHINXBUILD% 2> nul
if errorlevel 9009 (
    echo.
    echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
    echo.installed, then set the SPHINXBUILD environment variable to point
    echo.to the full path of the 'sphinx-build' executable. Alternatively you
    echo.may add the Sphinx directory to PATH.
    echo.
    echo.If you don't have Sphinx installed, grab it from
    echo.http://sphinx-doc.org/
    exit /b 1
)


:sphinx_ok
SET PYTHONPATH=..
if "%1" == "apidoc" (
    py -3 .\source\gendoc.py .\source\toc.yaml .\source\api
    if errorlevel 1 exit /b 1
    echo.
    echo.Build finished. The RST pages are in source\api.
    goto end
)

if "%1" == "html" (
    %SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/html
    if errorlevel 1 exit /b 1
    echo.
    echo.Build finished. The HTML pages are in %BUILDDIR%/html.
    goto end
)

:end
