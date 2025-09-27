@echo off

echo %RANDOM% > supports/dummy.txt
echo Add dummy file dummy.txt

git add .

rem echo Git pushed a dummy file for CI Demo
echo.
echo git commit -m "Add a dummy file to trigger Jenkins Webhooks and Github Workflow Actions ..."
git commit -m "Add a dummy file to trigger Jenkins/Github CI..."

REM Ensure branch is main
git branch -M main

git remote add origin https://github.com/luckyjoy/robotics_tdd.git >nul 2>&1

echo.
echo git push -u origin main
git push -u origin main

curl -u "luckyjoy:11ce1755fa745c0bf522d169a9cac2ca11" -k -X POST "https://localhost:8443/job/robotics_tdd/build"

echo.
echo A new build has been triggred at secured Github server: https://github.com/luckyjoy/robotics_tdd
echo.
echo A new build has been triggred at secured Jenkins server: https://localhost:8443/view/all/builds
echo.
echo Open secured GitHub server and Jenkins server
sleep 4

 start "" "https://github.com/luckyjoy/robotics_tdd/actions"
 start "" https://localhost:8443/view/all/builds
