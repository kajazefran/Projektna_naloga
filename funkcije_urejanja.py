import re

def poisci(vzorec, vsebina):
    najdba = re.search(vzorec, vsebina, re.DOTALL)
    if not najdba:
        return "Ni podatka"
    vrednost = najdba.group(1).strip()
    if vrednost.strip() == "" or vrednost.lower() in ["unknown", "-"]:
        return "Ni podatka"
    return vrednost

def pocisti_kraj(surovi_kraj):
    # Vzemi samo del pred " - "
    kraj = surovi_kraj.split(" - ")[0]

    # Združeni vzorci za odstranjevanje neželenih delov
    vzorec = re.compile(
        r'\b(off|en route|in|about|area|degrees|from|over|near|within|north|northern|eastern|south|east|west|location|km|m|mi|nautical|miles|mls|nm|nr|ca|stn|unk|unknown|W|S|N|E|NE|NW|SE|SW|ENE|ESE|SSE|SSW|WSW|WNW|NNW|NNE|LG)\b'
        r'|\d+'
        r'|\s*\(.*?\)'
        r'|^\s*of\s+'
        r'|[?]',
        flags=re.IGNORECASE
    )

    kraj = vzorec.sub('', kraj)         # Uporabi en sam sub
    kraj = kraj.split(",")[0]           # Odstrani po vejici
    kraj = re.sub(r',[ ]*[A-Z]{2}$', '', kraj)  # Odstrani kratice držav
    kraj = re.sub(r'\s+', ' ', kraj).strip(" -").strip()
    return kraj if kraj else "Ni podatka"

def pocisti_besedilo(besedilo):
    # Odstrani vprašaje, oklepaje, vejice na koncu, "of" na začetku, ipd.
    if not besedilo or besedilo.lower() in ["unknown", "-"]:
        return "Ni podatka"
    besedilo = re.sub(r'[?()]', '', besedilo)
    besedilo = re.sub(r'^\s*of\s+', '', besedilo, flags=re.IGNORECASE)
    besedilo = re.sub(r',[ ]*[A-Z]{2,4}$', '', besedilo)
    besedilo = re.sub(r'\s*\(.*?\)', '', besedilo)
    besedilo = besedilo.replace(",", "").strip()
    return besedilo if besedilo else "Ni podatka"