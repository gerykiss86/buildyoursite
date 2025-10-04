@echo off
REM Deploy Claude Execution Server to remote server
REM Requires: plink.exe and pscp.exe in PATH or current directory

SET SERVER=skykey.at
SET USER=root
SET PORT=22
SET REMOTE_DIR=/opt/claude-server

echo ========================================
echo Deploying Claude Execution Server
echo ========================================
echo.

REM Check if plink and pscp exist
where plink >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: plink.exe not found in PATH
    echo Please download from: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
    pause
    exit /b 1
)

where pscp >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pscp.exe not found in PATH
    echo Please download from: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
    pause
    exit /b 1
)

echo Step 1: Creating directories on server...
plink -P %PORT% %USER%@%SERVER% "mkdir -p %REMOTE_DIR% /var/log/claude-server"

echo.
echo Step 2: Copying files to server...
pscp -P %PORT% claude-execution-server.py %USER%@%SERVER%:%REMOTE_DIR%/
pscp -P %PORT% test-claude-server.py %USER%@%SERVER%:%REMOTE_DIR%/
pscp -P %PORT% setup-server.sh %USER%@%SERVER%:%REMOTE_DIR%/

echo.
echo Step 3: Making scripts executable...
plink -P %PORT% %USER%@%SERVER% "chmod +x %REMOTE_DIR%/*.py %REMOTE_DIR%/*.sh"

echo.
echo Step 4: Running server setup script...
plink -P %PORT% %USER%@%SERVER% "cd %REMOTE_DIR% && ./setup-server.sh"

echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo.
echo Server should be running on http://%SERVER%:5555
echo.
echo Test with: curl http://%SERVER%:5555/health
echo.
pause