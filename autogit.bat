echo off
git add .
set /p "userInput=Type a commit message:"
if "%userInput%"=="" (
    git commit -m "commit made at %time% date:%date%"
) else (
    git commit -m "commit made at %time% date:%date% with description:%userInput%"
)
git push origin master
pause


