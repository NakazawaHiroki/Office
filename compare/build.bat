@echo on

echo Dugong�����e�X�g�c�[���̃r���h���s���܂�

echo �O��̏o�̓f�[�^���N���A���܂�

del /Q .\CompareLedger.spec
rmdir /S /Q .\dist
rmdir /S /Q .\build

pyinstaller .\CompareLedger.py

echo �r���h���������܂����B�K�v�ȃt�@�C�����R�s�[���܂�

rem xcopy .\config.inf ".\dist\CompareLedger\"

echo �r���h���������܂���
