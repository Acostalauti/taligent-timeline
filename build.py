import csv
import json
import re
import os

CSV_FILE = 'Taligent_Hitos_Historicos.xlsx - Hitos Taligent.csv'
HTML_FILE = 'index.html'

def main():
    hitos_data = []
    
    if not os.path.exists(CSV_FILE):
        print(f"Error: No se encontró el archivo '{CSV_FILE}'")
        return

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header_found = False
        
        for row in reader:
            if not row or len(row) < 5:
                continue
                
            if not header_found:
                # Buscar encabezado
                if row[0] == '#' or row[1] == 'Fecha':
                    header_found = True
                continue
            
            # Estamos en datos
            # El CSV termina con un footer: "Taligent LLC · Última actualización..."
            if "Taligent LLC" in row[0]:
                break
                
            year = row[1].strip()
            hito = row[2].strip()
            cat = row[3].strip()
            desc = row[4].strip()
            
            # Si el hito esta vacio, ignoramos
            if not hito:
                continue
                
            # Agregamos al JSON structure
            hitos_data.append({
                "year": year,
                "hito": hito,
                "cat": cat,
                "desc": desc
            })

    if not hitos_data:
        print("No se encontraron hitos en el CSV.")
        return

    # Formateo manual para que quede lindo en el HTML
    json_str = "[\n"
    for item in hitos_data:
        # escapes basicos
        desc_escaped = item['desc'].replace('"', '\\"')
        hito_escaped = item['hito'].replace('"', '\\"')
        
        json_str += f'  {{ year:"{item["year"]}", hito:"{hito_escaped}", cat:"{item["cat"]}", desc:"{desc_escaped}" }},\n'
    json_str += "]"

    print(f"Se encontraron {len(hitos_data)} hitos en el CSV.")

    if not os.path.exists(HTML_FILE):
        print(f"Error: No se encontró el archivo '{HTML_FILE}'")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Reemplazar la lista hitos con REGEX
    pattern = r"const hitos = \[.*?\];"
    replacement = f"const hitos = {json_str};"
    
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("Success: El archivo HTML se actualizó correctamente con los nuevos hitos.")

if __name__ == '__main__':
    main()
