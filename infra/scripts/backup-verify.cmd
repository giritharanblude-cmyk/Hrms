@echo off
REM Verify latest Postgres backup in S3
REM Usage: backup-verify.cmd

set BACKUP_BUCKET=sangad-backups
set BACKUP_PATH=postgres/latest.dump

echo [backup-verify] Checking backup at s3://%BACKUP_BUCKET%/%BACKUP_PATH% ...
aws s3api head-object --bucket %BACKUP_BUCKET% --key %BACKUP_PATH% >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [FAIL] Backup not found at s3://%BACKUP_BUCKET%/%BACKUP_PATH%
    exit /b 1
)

aws s3api head-object --bucket %BACKUP_BUCKET% --key %BACKUP_PATH% --query "ContentLength" --output text > _backup_size.tmp
set /p BACKUP_SIZE=<_backup_size.tmp
del _backup_size.tmp

echo [OK] Backup found. Size: %BACKUP_SIZE% bytes.
exit /b 0