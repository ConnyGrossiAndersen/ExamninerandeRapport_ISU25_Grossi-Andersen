<#
Syfte: 
Syftet med detta skript är att jag vill hämta ut loggar med wevtutil från security-loggen. och exportera dem till .\securitylogs i en evtx fil. 
Sedan ska python analysera dessa. 
#> 

<# Definitioner
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


<# Funktioner
1. Skapar en mapp/katalog  om den inte redan finns, och undviker fel om den redan skulle vara skapad. 

#>
if (-not (Test-Path $Directory_for_securitylog)) {
    New-Item -ItemType Directory -Path $Directory_for_securitylog | Out-Null
}

<#   Jag har itnte kommit hit ännu, men epl exporterarhela loggen utan att rensa den  detta ska 
wevtutil epl $logName $EvtxFile
#>


#
#Write-Host "Hej från PowerShell-Scriptet fungerar!"
