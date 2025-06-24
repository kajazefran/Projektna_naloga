import re

def poisci(vzorec, vsebina):
    """Poišče prvo ujemanje vzorca v besedilu. Če ni najdeno ali je neveljavno, vrne 'Ni podatka'."""

    najdba = re.search(vzorec, vsebina, re.DOTALL)

    if not najdba:
        return "Ni podatka"
    vrednost = najdba.group(1).strip()

    if vrednost.strip() == "" or vrednost.lower() in ["unknown", "-"]:
        return "Ni podatka"
    
    return vrednost

def pocisti_kraj(surovi_kraj):
    """ Očisti neurejene zapise o krajih nesreč."""
    kraj = surovi_kraj.split(" - ")[0] # vzamemo samo del pred -

    vzorec = re.compile(
        r'\b(off|en route|in|about|area|degrees|from|over|near|within|north|northern|'
        r'eastern|south|east|west|location|km|m|mi|nautical|miles|mls|nm|nr|ca|stn|'
        r'unk|unknown|W|S|N|E|NE|NW|SE|SW|ENE|ESE|SSE|SSW|WSW|WNW|NNW|NNE|LG)\b'
        r'|\d+'
        r'|\s*\(.*?\)'
        r'|^\s*of\s+'
        r'|[?]',
        flags=re.IGNORECASE
    )

    kraj = vzorec.sub("", kraj)        
    kraj = kraj.split(",")[0]           # odstrani po vejici
    kraj = re.sub(r',[ ]*[A-Z]{2}$', "", kraj)  # odstrani kratice držav
    kraj = re.sub(r'\s+', ' ', kraj).strip(" -").strip()

    return kraj if kraj else "Ni podatka"

def pocisti_besedilo(besedilo):
    """ Očisti neurejene zapise."""

    if not besedilo or besedilo.lower() in ["unknown", "-"]:
        return "Ni podatka"
    
    besedilo = re.sub(r'[?()]', "", besedilo)
    besedilo = re.sub(r'^\s*of\s+', "", besedilo, flags=re.IGNORECASE)
    besedilo = re.sub(r',[ ]*[A-Z]{2,4}$', "", besedilo)
    besedilo = re.sub(r'\s*\(.*?\)', "", besedilo)
    besedilo = besedilo.replace(",", "").strip()
    
    return besedilo if besedilo else "Ni podatka"