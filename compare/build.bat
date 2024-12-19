@echo on

echo Dugong自動テストツールのビルドを行います

echo 前回の出力データをクリアします

del /Q .\CompareLedger.spec
rmdir /S /Q .\dist
rmdir /S /Q .\build

pyinstaller .\CompareLedger.py

echo ビルドが完了しました。必要なファイルをコピーします

rem xcopy .\config.inf ".\dist\CompareLedger\"

echo ビルドが完了しました
