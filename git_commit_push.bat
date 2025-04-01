@echo off
REM �o�b�`�t�@�C���̊J�n

REM ���|�W�g���̃p�X��ݒ�
SET REPO_PATH=C:\development\MyProject

REM �R�~�b�g���b�Z�[�W��ݒ�i�f�t�H���g�� "Auto commit"�j
SET COMMIT_MESSAGE=Auto commit

REM �R�~�b�g���b�Z�[�W�̈���������ꍇ�A������g�p
IF NOT "%~1"=="" (
    SET COMMIT_MESSAGE=%~1
)

REM ���|�W�g���f�B���N�g���Ɉړ�
cd /d "%REPO_PATH%"

REM Git���|�W�g�����m�F
git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo This is not a valid Git repository.
    pause
    EXIT /b 1
)

REM �X�e�[�W���O
echo Staging changes...
git add -A

REM �R�~�b�g
echo Committing changes with message: "%COMMIT_MESSAGE%"
git commit -m "%COMMIT_MESSAGE%"

REM �v�b�V��
echo Pushing to the remote repository...
git push origin main --force

REM �I�����b�Z�[�W
IF ERRORLEVEL 0 (
    echo Changes pushed successfully.
) ELSE (
    echo Failed to push changes.
)

REM �I��
pause
