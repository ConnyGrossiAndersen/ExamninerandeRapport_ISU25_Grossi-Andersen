#!/usr/bin/env bash  
#Har läst att detta alternativ är bättre för att hitta bash via användarens PATH

#Syfte: 
# Syftet är att skriptet ska sampla in systemloggar och konvertera dem till JSON filer för vidare ananlys i Python.
# Detta skript vill jag hämta systemfiler, som Auth.log/syslog samt kern.log och konvertera till JSON-format
# För detta måste jag börja med att definiera Variabeln för mappen där filerna ska sparas och skapa mappen.

#-------------------------------------------------------------------------------------
#-------------------------------DEFINITIONER------------------------------------------
#-------------------------------------------------------------------------------------

# Jag börjar med att definiera sökvägen till en mapp där loggarna i JSON format kommer att sparas. 
Directory_for_Jsonlogs="./json_logs"

#Jag definierar loggfilerna som ska konverteras
Log_files=(
    "/var/log/syslog"
    "/var/log/auth.log"
    "/var/log/kern.log"
)
#Jag definiera sökvägen till en logg för spårbarhet och revision (Vem kör skriptet och datumstämpel.). 
Audit_log="$Directory_for_Jsonlogs/audit.log"

#-------------------------------------------------------------------------------------
#-------------------------------INITSIERING-------------------------------------------
#-------------------------------------------------------------------------------------

#Direktory för loggarna i JSON-format och för Run-loggen
mkdir -p "$Directory_for_Jsonlogs"

#Revision på körloggen: 
echo "$(date '+%Y-%m-%d %H:%M:%S') Skriptet $(basename "$0") startades av: $USER via host: $(hostname)" \
    >> "$Audit_log"

for input_file in /var/log/syslog /var/log/auth.log /var/log/kern.log; do
    output_file="./json_logs/$(basename "$input_file").json"

    echo "$(date '+%Y-%m-%d %H:%M:%S')  Bearbetar filer och konverterar till JSON $input_file → $output_file" \
        >> "$Audit_log"

done
echo "$(date '+%Y-%m-%d %H:%M:%S') Konvertering klart! Programmet avslutas..." >> "$Audit_log"    

#-------------------------------------------------------------------------------------
#---------------------------------FUNKTIONER Test------------------------------------------
#-------------------------------------------------------------------------------------
#Jag skapar en funktion som hanterar en loggfil  Den ska ta input från en fil (ex syslog) och sedan 
#ta output från en annan (ex.json_logs) och konvertera till JSON

# Log funktion med tidstämpel till terminalen 
log() {
    local msg="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S')  $msg"
}

# Funktion som konverterar en loggfil till JSON fil. 
process_log_file() {
    local input_file="$1"
    local output_file="$2"
    local first=true

    # Kontrollerar att filen finns och hoppar över om den inte gör det. 
    if [[ ! -f "$input_file" ]]; then
        log "VARNING: $input_file finns inte, hoppar över."
        return 1
    fi

    # Visar ett meddelande i terminalen att filen konverteras.
    log "Bearbetar filer och konverterar till JSON $input_file → $output_file"

    # Skriver över till output filen och strukturerar till en tydlig JSON
    # Läser loggfilen rad för rad hanterar backslashes och whitespaces citattecken och mer.
    # Gör JSON filen läsbar
    {
        echo "["

        while IFS= read -r line; do
            # Escape specialtecken för JSON
            safe_line="${line//\\/\\\\}"   # backslash
            safe_line="${safe_line//\"/\\\"}" # dubbla citattecken
            safe_line="${safe_line//$'\b'/\\b}"  # backspace
            safe_line="${safe_line//$'\f'/\\f}"  # form feed
            safe_line="${safe_line//$'\n'/\\n}"  # newline
            safe_line="${safe_line//$'\r'/\\r}"  # carriage return
            safe_line="${safe_line//$'\t'/\\t}"  # tab

            if [[ "$first" == true ]]; then
                first=false
            else
                echo ","
            fi

            # Skriv snyggt med indentering
            echo -n "  {\"line\": \"$safe_line\"}"
        done < "$input_file"

        echo
        echo "]"
    } > "$output_file"
}

#-------------------------------------------------------------------------------------
#---------------------------------HUVUDPROGRAM----------------------------------------
#-------------------------------------------------------------------------------------
# Loopar över loggfilerna 
for file in "${Log_files[@]}"; do
    base_name=$(basename "$file")          # t.ex. syslog/ auth.log eller vidare
    output_file="$Directory_for_Jsonlogs/${base_name}.json"

    process_log_file "$file" "$output_file"
done

# Avslutar med ett meddelande i terminalen att konverteringen är klar. Finns också med i audit filen. 
log "Konvertering klart! Programmet avslutas..."