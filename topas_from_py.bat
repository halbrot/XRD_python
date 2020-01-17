@echo off

rem 遅延環境変数の処理（行ごとに上から順に処理を実行）
setlocal enabledelayedexpansion

rem 現在のディレクトリ名を自動的に取得
set param1=%~dp0
echo %param1%

rem TOPASで解析を行う雛形として、INPファイルの名前を指定
set inpname=for_python.inp
rem 以下が設定可能
rem Cementite-1       : original setting using 2 flames data
rem Cementite-2       : TOPASと同じ結果．CrySizeLを出力．
rem Cementite-2_SD    : SampleDisplacement精密化．
rem Cementite-2_CS    : CrySizeLを固定．
rem Cementite-2_CS_SD : CrySizeLを固定．SampleDisplacement精密化．
rem Cementite-3       : 56:115


rem 結果を出力するファイル名を指定
set resultname=Cementite-result

echo %1 >> %param1%%resultname%.txt
echo CrySizeL = %2 >> %param1%%resultname%.txt


rem 結果ファイルの1行目に、各項目の見出しを書き込む（分かりやすくするため）
set flag=FALSE
IF %1==Cementite-2_CS set flag=TRUE
IF %1==Cementite-2_CS_SD set flag=TRUE
IF "%flag%"=="FALSE" (
	echo "FileName	Austenite(wt%%)	Austenite_error	AusteniteCS(nm)	Austenite_error	Cementite(wt%%)	Cementite_error	CementiteCS(nm)	Cementite_error	Martensite(wt%%)	Martensite_error	MartensiteCS(nm)	Martensite_error">> %param1%%resultname%.txt
) ELSE (
	echo "FileName	Austenite(wt%%)	Austenite_error	Cementite(wt%%)	Cementite_error	Martensite(wt%%)	Martensite_error">> %param1%%resultname%.txt
)

rem .rawファイル名を順番に取得し、それぞれ解析を実行
echo -----------------------ファイル名
for %%A in (*.raw) do (
	set filename=%%~nA
	echo !filename!
	c:\topas6\tc %param1%%inpname% "macro FileName {"!filename!"}"
	rem 改行する
	echo; >> %param1%%resultname%.txt
)


echo; >> %param1%%resultname%.txt
echo; >> %param1%%resultname%.txt

rem 解析時に一時的に作成された～.outファイルを削除する
del %param1%for_python.out
