import os, glob, time, ConfigParser, subprocess

# Takes the site name and the list of options from the ini and makes the batch file to run on the Data Warehouse.
# Returns the name of the batch file created.

def test236(sitedict):
    batchfiles236=[]
    resultfiles236=[]
    allsiteresults={}
    for site in sitedict:
        siteresultdict={}
        batchfile236, resultfile236=makebatch236(site, sitedict[site])
        siteresultdict['test236batchfile']=batchfile236
        siteresultdict['test236resultfiles']=resultfile236
        allsiteresults[site]=siteresultdict
        process = subprocess.Popen(batchfile236, stdout=subprocess.PIPE)
        siteresultdict['test236batchfileoutput']=process.communicate()
    return allsiteresults

def makebatch236(site, optiondict):
	ACD1=optiondict['acd1']
	ACD2=optiondict['acd2']
	VMCA1=optiondict['vmca1']
	VMCA2=optiondict['vmca2']

	batchfile236=site+'.bat'
	resultfiles236=[site+'-acd1-vmca1-results.txt', site+'-acd2-vmca2-results.txt']

	f=open(batchfile236,'w')
	f.write('cd c:\\temp\\ \n')
	f.write('wmic /node:'+ ACD1 + ' /user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendAddr > c:\\Temp\\McsSendAddr.txt"\n')
	f.write('\n')
	f.write('wait 2\n')
	f.write('wmic /node:'+ ACD1+ '	/user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendPort > c:\\Temp\\McsSendPort.txt"\n')
	f.write('\n')
	f.write('wait 2\n')
	f.write('copy /Y \\\\'+ ACD1+ '\c$\\Temp\\McsSendAddr.txt c:\\temp\\McsSendAddr.txt\n')
	f.write('copy /Y \\\\'+ ACD1+ '\c$\\Temp\\McsSendPort.txt c:\\temp\\McsSendPort.txt\n')
	f.write('for /F "tokens=2,3*" %%i in (c:\\temp\\McsSendAddr.txt) do @echo %%j > c:\\temp\\McsSendAddr.txt\n')
	f.write('for /F "tokens=2,3*" %%i in (c:\\temp\\McsSendPort.txt) do @echo %%j > c:\\temp\\McsSendPort.txt\n')
	f.write('for /F %%i in (c:\Temp\McsSendPort.txt) do set "a=%%i"\n')
	f.write('set /a b=decimal=%a%\n')
	f.write('type c:\\Temp\McsSendAddr.txt > c:\\temp\\receivetestarg.txt\n')
	f.write('type c:\\Temp\McsSendPortDec.txt >> c:\\temp\\receivetestarg.txt\n')
	f.write('copy /Y c:\\temp\\receivetestarg.txt \\\\'+ VMCA1+ '\\c$\\Temp\\receivetestarg.txt\n')
	f.write('wmic /node: '+ VMCA1+ ' /user:administrator /password:itv process call create "cmd.exe /c c:\\itv\\exe\\receivetest < c:\\temp\\receivetestarg.txt > c:\\temp\\receivetestout.txt"\n')
	f.write('\n')
	f.write('wait 10\n')
	f.write('wmic /node: '+ VMCA1+ ' /user:administrator /password:itv process call create "cmd.exe /c taskkill /F /im ReceiveTest.exe"\n')
	f.write('\n')
	f.write('copy /Y \\\\'+ VMCA1+ '\c$\\temp\\receivetestout.txt c:\\temp\\' + str(resultfiles236[0]) +'\n')
	
	f.write('wait 2\n')
	f.write('wmic /node:'+ ACD2 + ' /user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendAddr > c:\\Temp\\McsSendAddr.txt"\n')
	f.write('\n')
	f.write('wait 2\n')
	f.write('wmic /node:'+ ACD2+ '	/user:administrator /password:itv process call create "cmd.exe /c reg query HKLM\SOFTWARE\seachange\ITV\CurrentVersion\Services\AdAgent /v McsSendPort > c:\\Temp\\McsSendPort.txt"\n')
	f.write('\n')
	f.write('wait 2\n')
	f.write('copy /Y \\\\'+ ACD2+ '\c$\\Temp\\McsSendAddr.txt c:\\temp\\McsSendAddr.txt\n')
	f.write('copy /Y \\\\'+ ACD2+ '\c$\\Temp\\McsSendPort.txt c:\\temp\\McsSendPort.txt\n')
	f.write('for /F "tokens=2,3*" %%i in (c:\\temp\\McsSendAddr.txt) do @echo %%j > c:\\temp\\McsSendAddr.txt\n')
	f.write('for /F "tokens=2,3*" %%i in (c:\\temp\\McsSendPort.txt) do @echo %%j > c:\\temp\\McsSendPort.txt\n')
	f.write('for /F %%i in (c:\Temp\McsSendPort.txt) do set "a=%%i"\n')
	f.write('set /a b=decimal=%a%\n')
	f.write('type c:\\Temp\McsSendAddr.txt > c:\\temp\\receivetestarg.txt\n')
	f.write('type c:\\Temp\McsSendPortDec.txt >> c:\\temp\\receivetestarg.txt\n')
	f.write('copy /Y c:\\temp\\receivetestarg.txt \\\\'+ VMCA2+ '\\c$\\Temp\\receivetestarg.txt\n')
	f.write('wmic /node: '+ VMCA2+ ' /user:administrator /password:itv process call create "cmd.exe /c c:\\itv\\exe\\receivetest < c:\\temp\\receivetestarg.txt > c:\\temp\\receivetestout.txt"\n')
	f.write('\n')
	f.write('wait 10\n')
	f.write('wmic /node: '+ VMCA2+ ' /user:administrator /password:itv process call create "cmd.exe /c taskkill /F /im ReceiveTest.exe"\n')
	f.write('\n')
	f.write('copy /Y \\\\'+ VMCA2+ '\c$\\temp\\receivetestout.txt c:\\temp\\' + str(resultfiles236[1]) +'\n')
	f.close()
	return batchfile236, resultfiles236

# Parses the INI with the list of sites and thier VMCA/ACDs.
# Returns a dictionary of dictionaries houseing the site and the options from that site.
def parseini(filename):
	sitedict={}
	Config = ConfigParser.ConfigParser()
	Config.read(filename)
	for section in Config.sections():
		optinosdict={}
		options = Config.options(section)
		for option in options: 
			options = Config.options(section)
			optinosdict[option] = Config.get(section, option)
		sitedict[section]=optinosdict	
	return sitedict

# Here is the action!
if __name__ == '__main__':
	sitedict=parseini('audit.ini')
	results236=test236(sitedict)
	


