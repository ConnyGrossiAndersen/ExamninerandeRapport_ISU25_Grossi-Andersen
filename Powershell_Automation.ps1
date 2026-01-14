<#
Syfte: 
Syftet med detta skript är att jag vill hämta ut loggar med wevtutil från den inbygda security-loggen och konvertera till en EvtxFil
Exportera den till Securitylogs som Python sen skall Analysera. 
Jag vill ha loggar för Vem som kör skriptet och från vilken enhet, med tidsstämplar. 
Jag vill att security_audit.log ska se ut som Bash audit.log filen. 
Meddelanden skrivs också ut till host för att visa användaren om programmet körs lyckat eller ej. 
#> 

<# -----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------Definitioner----------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------

1. Inbyggd logg som jag vill exportera
2. Här hamnar den exporterade loggen,
3. Definierar Filnamnet på evtx filen jag exporterar med tidstämpel,
4. Definierar Audit loggen så att vi har compliance och att den sparas i Bash auditlogen 
5. Formatet på den tidstämpel jag vill ha  #>

$logName = "Security" 
$Directory_for_securitylog = Join-Path $PSScriptRoot "securitylogs" 
$EvtxFile = Join-Path $Directory_for_securitylog "Security_$((Get-Date -Format 'yyyyMMdd_HHmmss')).evtx"
$AuditLog = Join-Path $PSScriptRoot "json_logs/audit.log"

<# -----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------Funktioner------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------

1. Skapar en mapp/katalog  om den inte redan finns, och undviker fel om den redan skulle vara skapad. 
2. Här skapas funktionen för Audit loggen. Med tidstämpel.
3. Loggmeddelanden i ordning efter varandra 
3. Try kör exporten , Lyckas exporten så skrivs den ut till Auditloggen.  Om det misslyckas, kommer ett felmeddelande och en exit kod.
4. Catch fångar upp om det blir fel och loggar detta 
5. Sist följer en utskrift att exporten är klar   
#>

if (-not (Test-Path $Directory_for_securitylog)) {
    New-Item -ItemType Directory -Path $Directory_for_securitylog | Out-Null
}
function Write-Audit {
    param([string]$Message) # Parametern $Message används för texten jag vill logga

    $Time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Line = "$Time $Message"

    # Skriv till audit-loggen
    $Line | Out-File -FilePath $AuditLog -Append -Encoding utf8

    # Skriv samma rad till terminalen
    Write-Host $Line
}


<# -----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------Huvudblock------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------
#>

#Loggar Starten av skriptet
$ScriptName = Split-Path -Leaf $PSCommandPath
$User = $env:USERNAME
$HostName = $env:COMPUTERNAME

Write-Audit "Skriptet $ScriptName kördes av användare: $User på host: $HostName"

# Exporterar.. och loggar om det fungerar. Jag vill att samma meddelande skall skrivas i terminalen vilket Write-Host ska göra.
try {
    wevtutil epl $logName $EvtxFile
    Write-Audit "Hämtar en logg MED Wevtutil från '$logName' och exporterar till Evtx-format"

}
catch {
    Write-Audit "Exporten misslyckades!: $($_.Exception.Message)"
    Write-Error "Varning! Kunde inte exportera logg!."
    exit 1
}

#Loggar att skriptet är klart. Write host har jag för att få en tom rad i terminalen 
Write-Audit "PowerShell-skriptet kördes klart, exporten lyckades!"
Write-Host " " 


