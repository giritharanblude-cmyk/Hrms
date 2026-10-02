@echo off
REM Restore drill: restore Postgres from latest S3 backup into a local/scratch database
REM Usage: restore-drill.cmd <target-db-url>

if "%1"=="" (
    echo Usage: %~nx0 ^{target-database-url^}
    exit /b 1
)

set TARGET_DB=%1
set BACKUP_BUCKET=sangad-backups
set BACKUP_PATH=postgres/latest.dump
set LOCAL_FILE=_restore_dump.tmp

echo [restore-drill] Downloading backup from s3://%BACKUP_BUCKET%/%BACKUP_PATH% ...
aws s3 cp s3://%BACKUP_BUCKET%/%BACKUP_PATH% %LOCAL_FILE%
if %ERRORLEVEL% neq 0 (
    echo [FAIL] Download failed.
    exit /b 1
)

echo [restore-drill] Restoring to target database ...
pg_restore -d "%TARGET_DB%" -Fc --clean --if-exists %LOCAL_FILE%
if %ERRORLEVEL% neq 0 (
    echo [FAIL] Restore failed.
    del %LOCAL_FILE%
    exit /b 1
)

del %LOCAL_FILE%
echo [OK] Restore completed successfully.
exit /b 0