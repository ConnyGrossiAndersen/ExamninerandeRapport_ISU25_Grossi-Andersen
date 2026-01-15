#
# Vill testa att skapa ett signeringsscript så att scriptet certifikatsigneras 
#
$cert = Get-ChildItem Cert:\CurrentUser\My |
    Where-Object { $_.EnhancedKeyUsageList.FriendlyName -contains "Code Signing" } |
    Select-Object -First 1

if (-not $cert) {
    Write-Error "Inget kodsigneringscertifikat hittades"
    exit 1
}

Set-AuthenticodeSignature `
    -FilePath ".\Powershell_Automation.ps1" `
    -Certificate $cert

Write-Host "Powershell_Automation.ps1 är nu signerat"



# i GPO GÖR DU DINA inställningar
<# Computer Configuration
 └─ Administrative Templates
    └─ Windows Components
       └─ Windows PowerShell
          └─ Turn on Script Execution → Allow only signed scripts ... etc. etc för att policy skall vara att endast signerade skripts får köras
#>    
#   INNE I POWERSHELL TERMINAL SKRIV.... 
#   Set-ExecutionPolicy AllSigned -Scope LocalMachine



<# Kör dessa EN GÅNG i terminalen 

icacls logginsamling.ps1 /inheritance:r
icacls logginsamling.ps1 /grant "Administrators:R"
icacls logginsamling.ps1 /grant "LoggCollectorUser:R"

#>