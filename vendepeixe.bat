@echo off
color a
echo Instalando todas as dependencias..
	pip install -r requirements.txt
	cls
color b
echo Iniciando a interface de terminal...
cls
	start cmd /k python terminal_interface.py
color a
echo Iniciando o servidor FastAPI...
	uvicorn main:app --reload
