@echo off

rem === General Info and Cleanup ===
echo Robotics Test-Driven Development (TDD) by Bang Thien Nguyen, ontario1998@gmail.com ...
echo.
echo.
echo pytest --alluredir=allure-results
pytest --alluredir=allure-results
echo.
rmdir /s /q __pycache__ .pytest_cache 2>nul
allure generate allure-results -o allure-report --clean
echo  allure serve allure-results 
allure serve allure-results
