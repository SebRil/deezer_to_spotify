# Check if Python is already in good version
$downloadFolder = "$env:USERPROFILE\tempPython"
If(!(Test-Path("$env:LOCALAPPDATA\Programs\Python\Python310"))){
	# Create temp folder
	Write-Host "## CREATING TEMPORARY FOLDER TO DOWNLOAD PYTHON INSTALLER##" -ForegroundColor Blue
	Start-Sleep -Seconds 1	
	$null = New-Item -ItemType Directory -Path $downloadFolder -ErrorAction Stop
	Start-Sleep -Seconds 1
	Write-Host "Done."

	# Download & Install Python
	Write-Host
	Write-Host
	Write-Host "## DOWNLOADING & INSTALLING PYTHON" -ForegroundColor Blue
	Start-Sleep -Seconds 1
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
	$fileName = "python-3.10.0-amd64.exe"
	$null = Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.0/$fileName" -OutFile "$downloadFolder\$fileName"
	Start-process -File "$downloadFolder/$fileName" -ArgumentList "/quiet","InstallAllUsers=0","InstallLauncherAllUsers=0","PrependPath=0","Include_test=0","Include_pip=1","Include_tcltk=1","Include_launcher=1","CompileAll=1","AssociateFiles=1","Include_symbols=1","Include_debug=1","Shortcuts=0" -Wait
	Start-Sleep -Seconds 1
	Write-Host "Done."
	
	# Remove temp folder
	Write-Host
	Write-Host
	Write-Host "## REMOVING TEMP FOLDER ##" -ForegroundColor Blue
	Start-Sleep -Seconds 1
	$null = Remove-Item -Path $downloadFolder -Recurse -Force
	Start-Sleep -Seconds 1
	Write-Host "Done."
}

# Set alias so be sure to run this python even if a Python is already installed
Write-Host
Write-Host
Write-Host "## SETTING COMMAND ALIAS TO RUN PYTHON EASILY" -ForegroundColor Blue
Start-Sleep -Seconds 1
Set-Alias -Name python310 -Value "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
Start-Sleep -Seconds 1
Write-Host "Done."

# Create venv
Write-Host
Write-Host
Write-Host "## CREATING PYTHON VIRTUAL ENVIRONMENT ##" -ForegroundColor Blue
Start-Sleep -Seconds 1
python310 -m venv venv

# Activate venv
Write-Host
Write-Host
Write-Host "## ACTIVATING PYTHON VIRTUAL ENVIRONMENT ##" -ForegroundColor Blue
Start-Sleep -Seconds 1
./venv/Scripts/Activate

# Install requirements
Write-Host
Write-Host
Write-Host "## INSTALLING PYTHON LIBRARIES ##" -ForegroundColor Blue
Start-Sleep -Seconds 1
python -m pip install -r requirements.txt

# Run the streamlit application
Write-Host
Write-Host
Write-Host "## RUNNING APP ##" -ForegroundColor Blue
Start-Sleep -Seconds 1
python -m streamlit run app.py

pause