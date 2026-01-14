#
# Syfte: 
# Syftet med detta skript är att bygga vidare på logginsamlingen jag skapat i bash och powershell. Istället för att köra varje skript för sig, vill jag att
# Python skall starta bash-skriptet och powershell-skriptet för att slippa köra 3 skript för en aktivitet. 
# Logginsamling: Python startar hämtning av loggar i Linux via Bash och i Windows via Powershell
# Bash och Powershell hämtar ner filerna i JSON och Evtx -format. Python skall analysera dessa och hämta ut en rapport från filerna. 
# JAG HAR AVSIKTLIGT GJORT FEL SÖKVÄG TILL BASH OCH POWERSHELL FÖR ATT MEDDELA ANÄNDAREN ATT DET INTE GICK 
# Nu några viktiga importer för att få allt att fungera
# Jag har installerat en Evtx för att få detta fungera. 
import subprocess
import os
import json
import xml.etree.ElementTree as ET
from Evtx.Evtx import Evtx

#-------------------------------------------------------------------------------------
#-------------------------------DEFINITIONER------------------------------------------
#-------------------------------------------------------------------------------------

# Några Definitioner på säkvägarna, bashskript, powershellskript samt vart logg skall sparas och en Clownrapport jag ska skapa
Bash_Script = "./Bash___automation.sh"
PowerShell_Script = "./Powershell___Automation.ps1"
AuditLogg_Directory ="./json_logs/audit.log"
ClownReport = "./Chaos_in_universe.txt"
JsonLog_Directory = "./json_logs"
Evtx_Directory = "./evtx_logs"
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
    print("Startar Powershell-Skriptet för Windows loggar...")
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File",PowerShell_Script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Du har misslyckats här med, du kanske ska be din mamma om hjälp!")
        print(result.stderr)
    else: 
        print("Klockrent! PowerShell skriptet har körts klart och du har fått en guldmedalj!")  
        
#-------------------------------------------------------------------------------------
#---------------------------------RapportAnalys---------------------------------------
#-------------------------------------------------------------------------------------
# Börjar med Analysen för JSON.. 
def analyze_json_logs():
    results = []

    json_files = [
        f for f in os.listdir(JsonLog_Directory)
        if f.lower().endswith(".json")
    ]

    if not json_files:
        results.append(
            "Linux har varit tyst som en mus. Ingen JSON-logg hittades eller så har någon raderat dem med onda avsikter."
        )
        return results

    for filename in json_files:
        path = os.path.join(JsonLog_Directory, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            results.append(
                f"{filename}: JSON-loggen är oläsbar. Clownen fick panik! Fel: {e}"
            )
            continue

        # Räkna antal loggrader
        if isinstance(data, list):
            count = len(data)
            results.append(
                f"{filename}: {count} loggrader hittade. Linux verkar ha haft en riktig pratstund!"
            )
        else:
            results.append(
                f"{filename}: Vad hände nu? Antagligen har en Alien försökt skriva loggar."
            )

    return results

# Dags för analysen för Evtx... 
def analyze_evtx_logs():
    results = []

    evt_files = [
        f for f in os.listdir(Evtx_Directory)
        if f.lower().endswith(".evtx")
    ]

    if not evt_files:
        results.append(
            "Nu är du ute på hal is! Börja om från början, gör om och gör rätt..."
        )
        return results

    for filename in evt_files:
        path = os.path.join(Evtx_Directory, filename)
        try:
            with Evtx(path) as log:
                event_count = 0
                for record in log.records():
                    xml_str = record.xml()
                    root = ET.fromstring(xml_str)
                    event_id = root.find(".//EventID")
                    if event_id is not None:
                        event_count += 1

                results.append(
                    f"{filename}: {event_count} Intressant! Det finns mycket att läsa av här! Du är inte så dum ändå"
                )
        except Exception as e:
            results.append(
                f"{filename}: Nope! Detta blev inte rätt.. Vart har du gått skola någonstans? Fel: {e}"
            )

    return results
#-------------------------------------------------------------------------------------
#---------------------------------Trouble in paradise --------------------------------
#-------------------------------------------------------------------------------------
# Här skriver vi rapporten 
def write_clown_report(json_results, evtx_results):
    with open(ClownReport, "w", encoding="utf-8") as f:
        f.write(" --- CHAOS IN THE UNIVERSE REPORT --- \n\n")
        f.write("JSON-loggar\n")
        for line in json_results:
            f.write(line + "\n")
        f.write("\nEVTX-loggar (Windows)\n")
        for line in evtx_results:
            f.write(line + "\n")
        f.write("\n💥 Slut på rapporten. Clownen har lämnat cirkusen.\n")
        
#-------------------------------------------------------------------------------------
#---------------------------------Trouble in paradise --------------------------------
#-------------------------------------------------------------------------------------        
# Förenklad version av main som jag haft tidigare
def main():
    run_bash_script()
    run_powershell_script()
    json_results = analyze_json_logs()
    evtx_results = analyze_evtx_logs()
    write_clown_report(json_results, evtx_results)

if __name__ == "__main__":
    main()
