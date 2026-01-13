<#
Syfte: 
Syftet med detta skript är att jag vill hämta ut loggar med wevtutil från security-loggen. och exportera dem till .\securitylogs i en evtx fil. 
Sedan ska python analysera dessa. 
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
$AuditLog = Join-Path $PSScriptRoot "audit.log" 
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss" 



<# Funktioner-------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------Funktioner------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------
1. Skapar en mapp/katalog  om den inte redan finns, och undviker fel om den redan skulle vara skapad. 
2. Här är en funktion för att skriva ut Username, Datornamn och tidstämpel till Auditloggen Hämtad med hjälp av AI för att kunnna skriva ut den.
3. Try kör exporten , Lyckas exporten så skrivs den ut till Auditloggen.  Om det misslyckas, kommer ett felmeddelande och en exit kod.
4. Sist följer en utskrift att exporten är klar   
#>

if (-not (Test-Path $Directory_for_securitylog)) {
    New-Item -ItemType Directory -Path $Directory_for_securitylog | Out-Null
}

function Write-Audit {
    param([string]$Message)

    $User = $env:USERNAME
    $HostName = $env:COMPUTERNAME
    $Time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    "$Time | USER=$User | HOST=$HostName | $Message" |
        Out-File -FilePath $AuditLog -Append -Encoding utf8
}

try {
    wevtutil epl $logName $EvtxFile
    Write-Audit "Hämtar en logg MED Wevtutil från '$logName' och exporterar till Evtx: $EvtxFile"
}
catch {
    Write-Audit "Exporten misslyckades!: $($_.Exception.Message)"
    Write-Error "Varning! Kunde inte exportera logg!."
    exit 1
}

Write-Host "Export klar: $EvtxFile"
Write-Audit "PowerShell-skriptet kördes klart."

<#   Jag har itnte kommit hit ännu, men epl exporterarhela loggen utan att rensa den  detta ska 
wevtutil epl $logName $EvtxFile
#>


#
#Write-Host "Hej från PowerShell-Scriptet fungerar!"
