@echo of
git add .
git commit -m "Script commit at %DATE:~0,10% %TIME:~0,8%"
git push github --force