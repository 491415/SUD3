@echo off
REM ============================================================================
REM SUD3 - Skripta za preuzimanje podataka iz Sudskog registra
REM ============================================================================
REM Ova skripta pokreće sud3.py koji preuzima sve tablice iz SUDREG API-ja
REM te ih sprema u Oracle bazu podataka putem blue-green deployment uzorka.
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo SUD3 - Preuzimanje podataka iz Sudskog registra
echo Pocetak izvrsavanja: %date% %time%
echo ============================================================================
echo.

REM Definiranje roota projekta
REM OVDJE OBAVEZNO PROMIJENITI ROOT KADA SE PROJEKT PREBACI NA PRODUKCIJU!!!
set "PROJECT_ROOT=C:\D\PycharmProjects\SUD3"
set "PYTHON_SCRIPT=%PROJECT_ROOT%\sud3.py"

echo ----------------------------------------------------------------------------
echo Pokretanje: sud3.py
echo Skripta: %PYTHON_SCRIPT%
echo Vrijeme: %time%
echo ----------------------------------------------------------------------------

REM Pokretanje skripte
cd /d "%PROJECT_ROOT%"
python "%PYTHON_SCRIPT%"

REM Provjera uspješnosti
if errorlevel 1 (
    echo.
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
    exit /b 1
)

echo.
echo ============================================================================
echo REZULTATI IZVRSAVANJA
echo ============================================================================
echo Status: USPJESNO
echo sud3.py uspjesno izvrsen.
echo Zavrsetak izvrsavanja: %date% %time%
echo ============================================================================
echo.

echo Sve tablice uspjesno preuzete iz Sudskog registra.
exit /b 0