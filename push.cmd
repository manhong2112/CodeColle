@echo off
cd /d %~dp0
git add .
git commit -m "Script commit at %DATE:~0,10% %TIME:~0,8% UTC+8"
git push github --force