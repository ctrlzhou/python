@echo on
set num = 2
echo %num%
for /L %%i in (1,1,%num%) do (
for /L %%k in (1,1,255) do (
F:\pythoncode\syeptest\syeptest.exe  -LP 10002 -H 123.207.39.248 -P 9000 -D 00:11:22:33:11:16 -F -t connect -F -t status1 -a 5-1-%%k-0 -dt 79 -ds 6 -des autotest -E
)
)
pause
