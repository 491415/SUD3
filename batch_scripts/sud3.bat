@echo off
REM ============================================================================
REM SUD3 - Skripta za preuzimanje podataka iz Sudskog registra
REM ============================================================================
REM Ova skripta pokre?e sud3.py koji preuzima sve tablice iz SUDREG API-ja
REM te ih sprema u Oracle bazu podataka putem blue-green deployment uzorka.
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo SUD3 - Preuzimanje podataka iz Sudskog registra
echo Pocetak izvrsavanja: %date% %time%
echo ============================================================================
echo.

REM Konfiguracija projekta
REM OVDJE OBAVEZNO PROMIJENITI ROOT KADA SE PROJEKT PREBACI NA PRODUKCIJU!!!
set "PROJECT_ROOT=C:\D\PycharmProjects\SUD3"
cd /D "%PROJECT_ROOT%"

REM Validacija project root direktorija
if not exist "%PROJECT_ROOT%\src" (
    echo GRESKA: Nije moguce pronaci project src direktorij!
    exit /b 1
)

echo Direktorij projekta: %PROJECT_ROOT%
echo.

REM Aktivacija virtual environmenta
set "VENV_PATH=%PROJECT_ROOT%\.venv"
echo Aktiviranje virtual environmenta...

if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo UPOZORENJE: Virtual environment nije pronaden!
    echo Pokusavam koristiti globalnu Python instalaciju...
    goto :use_global_python
)

call "%VENV_PATH%\Scripts\activate.bat"
goto :check_python

:use_global_python
REM Fallback na globalnu Python instalaciju ako venv ne postoji
for /f "delims=" %%i in ('where python 2^>nul') do (
    set "PYTHON_PATH=%%i"
    goto :found_python
)
echo GRESKA: Python nije pronaden ni u venv ni kao globalna instalacija!
exit /b 1

:found_python
echo Koristim globalnu Python instalaciju: %PYTHON_PATH%

:check_python
REM Provjera dostupnosti Pythona
python --version >nul 2>&1
if errorlevel 1 (
    echo GRESKA: Python nije dostupan!
    exit /b 1
)

echo Python environment spreman
python --version
echo.

REM Izvrsavanje skripte kao Python modul iz project roota
REM (osigurava ispravno razrjesavanje src.* importa)
set "MODULE_PATH=src.sud3"

echo Izvrsavanje modula: %MODULE_PATH%
echo ============================================================================
echo.

python -m %MODULE_PATH%
set "SCRIPT_EXIT_CODE=%errorlevel%"

echo.
echo ============================================================================
echo Izvrsavanje zavrseno sa exit kodom: %SCRIPT_EXIT_CODE%
echo Timestamp: %date% %time%
echo ============================================================================
echo.

REM Logiranje u Windows Event Log i prikaz rezultata
if %SCRIPT_EXIT_CODE% neq 0 (
    echo ============================================================================
    echo REZULTATI IZVRSAVANJA
    echo ============================================================================
    echo Status: GRESKA
    echo sud3.py nije uspjesno izvrsen.
    echo Zavrsetak izvrsavanja: %date% %time%
    echo ============================================================================
    echo.
    echo WARNING: Skripta nije uspjesno izvrsena.
    echo Provjerite logove za vise detalja.
    eventcreate /T ERROR /ID 100 /L APPLICATION /SO "SUD3" /D "SUD3 greska sa exit kodom %SCRIPT_EXIT_CODE%" >nul 2>&1
    call deactivate >nul 2>&1
    exit /b %SCRIPT_EXIT_CODE%
) else (
    echo ============================================================================
    echo REZULTATI IZVRSAVANJA
    echo ============================================================================
    echo Status: USPJESNO
    echo sud3.py uspjesno izvrsen.
    echo Zavrsetak izvrsavanja: %date% %time%
    echo ============================================================================
    echo.
    echo Sve tablice uspjesno preuzete iz Sudskog registra.
    eventcreate /T INFORMATION /ID 101 /L APPLICATION /SO "SUD3" /D "SUD3 uspjesno izvrsen" >nul 2>&1
)

call deactivate >nul 2>&1
endlocal
exit /b 0