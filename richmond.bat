cd c:\temp\ 
wmic /node:10.161.66.200 /user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendAddr > c:\Temp\McsSendAddr.txt"

wait 2
wmic /node:10.161.66.200	/user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendPort > c:\Temp\McsSendPort.txt"

wait 2
copy /Y \\10.161.66.200\c$\Temp\McsSendAddr.txt c:\temp\McsSendAddr.txt
copy /Y \\10.161.66.200\c$\Temp\McsSendPort.txt c:\temp\McsSendPort.txt
for /F "tokens=2,3*" %%i in (c:\temp\McsSendAddr.txt) do @echo %%j > c:\temp\McsSendAddr.txt
for /F "tokens=2,3*" %%i in (c:\temp\McsSendPort.txt) do @echo %%j > c:\temp\McsSendPort.txt
for /F %%i in (c:\Temp\McsSendPort.txt) do set "a=%%i"
set /a b=decimal=%a%
type c:\Temp\McsSendAddr.txt > c:\temp\receivetestarg.txt
type c:\Temp\McsSendPortDec.txt >> c:\temp\receivetestarg.txt
copy /Y c:\temp\receivetestarg.txt \\172.19.70.71\c$\Temp\receivetestarg.txt
wmic /node: 172.19.70.71 /user:administrator /password:itv process call create "cmd.exe /c c:\itv\exe\receivetest < c:\temp\receivetestarg.txt > c:\temp\receivetestout.txt"

wait 10
wmic /node: 172.19.70.71 /user:administrator /password:itv process call create "cmd.exe /c taskkill /F /im ReceiveTest.exe"

copy /Y \\172.19.70.71\c$\temp\receivetestout.txt c:\temp\richmond-acd1-vmca1-results.txt
wait 2
wmic /node:10.161.66.202 /user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendAddr > c:\Temp\McsSendAddr.txt"

wait 2
wmic /node:10.161.66.202	/user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendPort > c:\Temp\McsSendPort.txt"

wait 2
copy /Y \\10.161.66.202\c$\Temp\McsSendAddr.txt c:\temp\McsSendAddr.txt
copy /Y \\10.161.66.202\c$\Temp\McsSendPort.txt c:\temp\McsSendPort.txt
for /F "tokens=2,3*" %%i in (c:\temp\McsSendAddr.txt) do @echo %%j > c:\temp\McsSendAddr.txt
for /F "tokens=2,3*" %%i in (c:\temp\McsSendPort.txt) do @echo %%j > c:\temp\McsSendPort.txt
for /F %%i in (c:\Temp\McsSendPort.txt) do set "a=%%i"
set /a b=decimal=%a%
type c:\Temp\McsSendAddr.txt > c:\temp\receivetestarg.txt
type c:\Temp\McsSendPortDec.txt >> c:\temp\receivetestarg.txt
copy /Y c:\temp\receivetestarg.txt \\172.19.70.73\c$\Temp\receivetestarg.txt
wmic /node: 172.19.70.73 /user:administrator /password:itv process call create "cmd.exe /c c:\itv\exe\receivetest < c:\temp\receivetestarg.txt > c:\temp\receivetestout.txt"

wait 10
wmic /node: 172.19.70.73 /user:administrator /password:itv process call create "cmd.exe /c taskkill /F /im ReceiveTest.exe"

copy /Y \\172.19.70.73\c$\temp\receivetestout.txt c:\temp\richmond-acd2-vmca2-results.txt
