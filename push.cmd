@echo off
cd C:\manhong\WorkSpace\Code
git add .
git commit -m "Script commit at %DATE:~0,10% %TIME:~0,8% UTC+8"
git push github --force