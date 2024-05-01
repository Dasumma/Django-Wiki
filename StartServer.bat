@echo off

call workon django-project & python manage.py runserver --insecure

pause