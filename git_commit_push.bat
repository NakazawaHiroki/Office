@echo off
REM バッチファイルの開始

REM リポジトリのパスを設定
SET REPO_PATH=C:\development\MyProject

REM コミットメッセージを設定（デフォルトは "Auto commit"）
SET COMMIT_MESSAGE=Auto commit

REM コミットメッセージの引数がある場合、それを使用
IF NOT "%~1"=="" (
    SET COMMIT_MESSAGE=%~1
)

REM リポジトリディレクトリに移動
cd /d "%REPO_PATH%"

REM Gitリポジトリか確認
git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo This is not a valid Git repository.
    pause
    EXIT /b 1
)

REM ステージング
echo Staging changes...
git add -A

REM コミット
echo Committing changes with message: "%COMMIT_MESSAGE%"
git commit -m "%COMMIT_MESSAGE%"

REM プッシュ
echo Pushing to the remote repository...
git push origin main --force

REM 終了メッセージ
IF ERRORLEVEL 0 (
    echo Changes pushed successfully.
) ELSE (
    echo Failed to push changes.
)

REM 終了
pause
