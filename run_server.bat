@echo off
cd %~dp0\library_project
python manage.py runserver 8080
pause
