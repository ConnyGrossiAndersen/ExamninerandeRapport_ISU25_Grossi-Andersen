#
# Syfte: 
# Syftet med detta skript är att bygga vidare på logginsamlingen jag skapat i bash och powershell. Istället för att köra varje skript för sig, vill jag att
# Python skall starta bash-skriptet och powershell-skriptet för att slippa köra 3 skript för en aktivitet. 
# Logginsamling: Python startar hämtning av loggar i Linux via Bash och i Windows via Powershell
# Bash och Powershell hämtar ner filerna i JSON och Evtx -format. Python skall analysera dessa och hämta ut en rapport från filerna. 
#
# Nu några viktiga importer för att få allt att fungera
import subprocess
import os
import json
import xml.etre.ElementTree as ET
from datetime import datetime 

#-------------------------------------------------------------------------------------
#-------------------------------DEFINITIONER------------------------------------------
#-------------------------------------------------------------------------------------

# Några Definitioner på säkvägarna, bashskript, powershellskript samt vart logg skall sparas och en Clownrapport jag ska skapa
Bash_Script = "./Bash_automation.sh"
PowerShell_Script = "./Powershell_Automation.ps1"
AuditLogg_Directory ="./json_logs/audit.log"
ClownReport = "./Chaos_in_universe.txt"
JsonLog_Directory = "./json_logs"
#-------------------------------------------------------------------------------------
#---------------------------------FUNKTIONER------------------------------------------
#-------------------------------------------------------------------------------------

# Börjar med Bash-Skriptet 
def run_bash_script():
    print("Startar Bash-Skriptet för Linux-loggar...")
    
    result = subprocess.run(
        ["bash", Bash_Script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Bash-Skriptet har misslyckats, har du testat IT-for dummies?")
        print(result.stderr)
    else:
        print("Bash-skriptet har kört klart! Grattis din dumme fan!")

# Dags för Powershell-Skriptet 
def run_powershell_script():
    print("Startar Powershell-Skriptet för Windows loggar... Tro fan du lyckades här med")
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File",PowerShell_Script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Du har fan inte lyckats med detta heller, be din mamma om hjälp!")
        print(result.stderr)
    else: 
        print("Klockrent! PowerShell skriptet har körts klart och du har fått en guldmedalj!")    

#-------------------------------------------------------------------------------------
#---------------------------------ANALYSERNA------------------------------------------
#-------------------------------------------------------------------------------------

# Börjar med att hitta alla json filer i mappen 
def analyze_json_logs():
    results = []

    json_files = [
        f for f in os.listdir(JsonLog_Directory)
        if f.lower().endswith(".json")
    ]

    if not json_files: 
        results.append(
            "Du får gräva djupare, Linux säger inget eller så har en dumbom raderat dem"
        )
        return results

    for filename in json_files:
        path = os.path.join(JsonLog_Directory, filename)

        try: 
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        except Exception as e:
            results.append(
                f"{filename}: är helt oläsbar. JSON ger upp, GÅ HEM! Fel: {e}"
            ) 
            continue
           
# Ska räkna loggrader och är där ett antal, så skall det skrivas ut    
        if isinstance(data, list):
            count = len(data)
            results.append(
                f"{filename}: {count} loggrader hittade. Linux har varit riktigt pratglad."
            )
        else: 
            results.append(
                f"{filename}: Vad hände nu? Antagligen har vi en Ailen som snackar."
            )

    return results     