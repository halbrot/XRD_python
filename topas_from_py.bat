@echo off

rem �x�����ϐ��̏����i�s���Ƃɏォ�珇�ɏ��������s�j
setlocal enabledelayedexpansion

rem ���݂̃f�B���N�g�����������I�Ɏ擾
set param1=%~dp0
echo %param1%

rem TOPAS�ŉ�͂��s�����`�Ƃ��āAINP�t�@�C���̖��O���w��
set inpname=for_python.inp
rem �ȉ����ݒ�\
rem Cementite-1       : original setting using 2 flames data
rem Cementite-2       : TOPAS�Ɠ������ʁDCrySizeL���o�́D
rem Cementite-2_SD    : SampleDisplacement�������D
rem Cementite-2_CS    : CrySizeL���Œ�D
rem Cementite-2_CS_SD : CrySizeL���Œ�DSampleDisplacement�������D
rem Cementite-3       : 56:115


rem ���ʂ��o�͂���t�@�C�������w��
set resultname=Cementite-result

echo %1 >> %param1%%resultname%.txt
echo CrySizeL = %2 >> %param1%%resultname%.txt


rem ���ʃt�@�C����1�s�ڂɁA�e���ڂ̌��o�����������ށi������₷�����邽�߁j
set flag=FALSE
IF %1==Cementite-2_CS set flag=TRUE
IF %1==Cementite-2_CS_SD set flag=TRUE
IF "%flag%"=="FALSE" (
	echo "FileName	Austenite(wt%%)	Austenite_error	AusteniteCS(nm)	Austenite_error	Cementite(wt%%)	Cementite_error	CementiteCS(nm)	Cementite_error	Martensite(wt%%)	Martensite_error	MartensiteCS(nm)	Martensite_error">> %param1%%resultname%.txt
) ELSE (
	echo "FileName	Austenite(wt%%)	Austenite_error	Cementite(wt%%)	Cementite_error	Martensite(wt%%)	Martensite_error">> %param1%%resultname%.txt
)

rem .raw�t�@�C���������ԂɎ擾���A���ꂼ���͂����s
echo -----------------------�t�@�C����
for %%A in (*.raw) do (
	set filename=%%~nA
	echo !filename!
	c:\topas6\tc %param1%%inpname% "macro FileName {"!filename!"}"
	rem ���s����
	echo; >> %param1%%resultname%.txt
)


echo; >> %param1%%resultname%.txt
echo; >> %param1%%resultname%.txt

rem ��͎��Ɉꎞ�I�ɍ쐬���ꂽ�`.out�t�@�C�����폜����
del %param1%for_python.out
