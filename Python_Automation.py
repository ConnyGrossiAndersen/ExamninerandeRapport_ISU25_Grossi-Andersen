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
import xml.etree.ElementTree as ET
from Evtx.Evtx import Evtx

#-------------------------------------------------------------------------------------
#-------------------------------DEFINITIONER------------------------------------------
#-------------------------------------------------------------------------------------

# Några Definitioner på säkvägarna, bashskript, powershellskript samt vart logg skall sparas och en Clownrapport jag ska skapa
Bash_Script = "./Bash_automation.sh"
PowerShell_Script = "./Powershell_Automation.ps1"
AuditLogg_Directory ="./json_logs/audit.log"
ClownReport = "./Chaos_in_universe.txt"
JsonLog_Directory = "./json_logs"
Evtx_Directory = "./evtx_logs"
#-------------------------------------------------------------------------------------
#---------------------------------FUNKTIONER-------------------------------------------
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



# Powershell Evtx-filer 
def analyze_evtx_files():
    results = []

    # Hitta alla evtx-filer
    evtx_files = [f for f in os.listdir(Evtx_Directory) if f.lower().endswith(".evtx")]

    if not evtx_files:
        results.append("Nu blev det fel! Har du testat IT-for dummies?")
        return results

    for filename in evtx_files:
        path = os.path.join(Evtx_Directory, filename)

        try:
            with Evtx(path) as log:
                event_count = 0
                for record in log.records():
                    xml_str = record.xml()  
                    root = ET.fromstring(xml_str)

                    
                    event_id = root.find(".//EventID")
                    time_created = root.find(".//TimeCreated")
                    if event_id is not None:
                        event_count += 1

                results.append(
                    f"{filename}: {event_count} här händer det grejer! Som tuppen i en hönsgård!"
                )

        except Exception as e:
            results.append(
                f"{filename}: Du kan inte göra någonting rätt, be din mamma om hjälp!. Fel: {e}"
            )

    return results
#-------------------------------------------------------------------------------------
#---------------------------------Rapportering----------------------------------------
#-------------------------------------------------------------------------------------
#
def write_clown_report(json_results, evtx_results):
    with open(ClownReport, "w", encoding="utf-8") as f:
        f.write("========== CHAOS IN THE UNIVERSE ==========\n")
        f.write("En clownanalys av loggarnas mörka hemligheter\n\n")

        f.write("----- JSON (Linux) -----\n")
        for line in json_results:
            f.write(line + "\n")

        f.write("\n----- EVTX (Windows) -----\n")
        for line in evtx_results:
            f.write(line + "\n")

        f.write("\n========== SLUT PÅ RAPPORT ==========\n")
#        


def main():
    print("==========================================")
    print("   Startar hela logg-cirkusen i Python")
    print("==========================================\n")

    # 1. Kör Bash-skriptet
    print("[1] Kör Bash-skriptet...")
    run_bash_script()
    print()

    # 2. Kör PowerShell-skriptet
    print("[2] Kör PowerShell-skriptet...")
    run_powershell_script()
    print()

    # 3. Analysera JSON-loggar
    print("[3] Analyserar JSON-loggar...")
    json_results = analyze_json_logs()
    for r in json_results:
        print("JSON:", r)
    print()

    # 4. Analysera EVTX-loggar
    print("[4] Analyserar EVTX-loggar...")
    evtx_results = analyze_evtx_files()
    for r in evtx_results:
        print("EVTX:", r)
    print()

    # 5. Skriv clownrapporten
    print("[5] Skriver clownrapporten...")
    write_clown_report(json_results, evtx_results)
    print(f"Clownrapport skapad: {ClownReport}")

    print("\n==========================================")
    print("   Allt klart! Cirkusen är officiellt över")
    print("==========================================")

# Kör main om skriptet körs direkt
if __name__ == "__main__":
    main()
