@echo off
cd C:\manhong\WorkSpace\Code
git add .
IF [%1] EQU [] (
git commit -m "Script auto commit at %DATE:~0,10% %TIME:~0,8% UTC+8"
) ELSE (
git commit -m "%1% %DATE:~0,10% %TIME:~0,8% UTC+8"
)
git push github --force