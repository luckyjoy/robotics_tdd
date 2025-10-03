@echo off
for /L %%i in (1, 1, 100) do (
setlocal
echo Loop iteration %%i
endlocal
)

EXIT /B