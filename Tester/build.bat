@echo on

echo Dugong�����e�X�g�c�[���̃r���h���s���܂�

echo �O��̏o�̓f�[�^���N���A���܂�

del /Q .\AutoInput.spec
rmdir /S /Q .\dist
rmdir /S /Q .\build

pyinstaller .\AutoInput.py

echo �r���h���������܂����B�K�v�ȃt�@�C�����R�s�[���܂�

xcopy .\msedgedriver.exe ".\dist\Autoinput\"
xcopy .\config.inf ".\dist\Autoinput\"
xcopy .\Sample.xlsx ".\dist\Autoinput\"

echo �r���h���������܂���
