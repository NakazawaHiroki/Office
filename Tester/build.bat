@echo on

echo Dugong自動テストツールのビルドを行います

echo 前回の出力データをクリアします

del /Q .\AutoInput.spec
rmdir /S /Q .\dist
rmdir /S /Q .\build

pyinstaller .\AutoInput.py

echo ビルドが完了しました。必要なファイルをコピーします

xcopy .\msedgedriver.exe ".\dist\Autoinput\"
xcopy .\config.inf ".\dist\Autoinput\"
xcopy .\Sample.xlsx ".\dist\Autoinput\"

echo ビルドが完了しました
