@rem taskarg: ${file}

@Echo off
set OLDHOME_FOLDER=%~dp0
pushd %OLDHOME_FOLDER%
call .\activate_with_vars.bat

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------


set INPATH=%~dp1
set INFILE=%~nx1
set INFILEBASE=%~n1
pushd %INPATH%
mkdir %WORKSPACEDIR_BATCH%\text_profiling
python -m cProfile -s cumtime %INFILE% > %WORKSPACEDIR_BATCH%\text_profiling\[%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%]_%INFILEBASE%.txt



