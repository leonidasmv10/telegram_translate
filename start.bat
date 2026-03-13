@echo off
title Traductor Magic Send
echo ==============================================
echo    Iniciando Traductor "Magic Send"
echo ==============================================
echo.

:: 1. Verificamos si existe el entorno virtual
if not exist ".venv\" (
    echo [INFO] No se encontro un entorno virtual. Creando uno nuevo en la carpeta .venv...
    python -m venv .venv
    echo [INFO] Entorno virtual creado exitosamente.
)

:: 2. Activamos el entorno virtual
echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate.bat

:: 3. Instalamos las dependencias necesarias en modo silencioso (-q)
echo [INFO] Verificando dependencias...
pip install -r requirements.txt -q

:: 4. Comprobamos si el usuario ya se logueo en Telegram (si existe el archivo de sesion)
if not exist "mi_sesion.session" (
    echo.
    echo ==============================================
    echo [ALERTA] No se encontro la sesion de Telegram.
    echo Necesitas autorizar tu cuenta por primera y unica vez.
    echo ==============================================
    echo.
    python login.py
) else (
    echo.
    echo [INFO] Todo listo. Levantando la interfaz...
    python main.py
)

:: 5. Pausa al final en caso de que ocurra un error, asi no se cierra de golpe
echo.
pause
