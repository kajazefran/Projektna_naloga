import re
import os

import funkcije_urejanja

def obdelaj_datum(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev datuma."""

    datum = funkcije_urejanja.poisci(r'<td class="caption">Date:</td><td class="caption">(.*?)</td>', vsebina)
    meseci = {
        "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
        "May": "May", "Jun": "June", "Jul": "July", "Aug": "August", 
        "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"
    }

    if "unk. date" in datum:
        podatki_nesrece["mesec"] = "Ni podatka"
        podatki_nesrece["leto"] = datum[-4:]

    else:
        datum = datum.split()
        mesec = datum[-2]
        podatki_nesrece["mesec"] = meseci.get(mesec, mesec)
        podatki_nesrece["leto"] = datum[-1]

def obdelaj_model_letala(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev modela letala."""

    # najprej poisci celoten <td class="desc"> za Type:
    vse = funkcije_urejanja.poisci(
        r'<td class="caption" valign="bottom">Type:</td>\s*<td class="desc">(.*?)</td>', 
        vsebina
    )

    if vse == "Ni podatka":
        podatki_nesrece["model_letala"] = "Ni podatka"
        return

    # poskusi najti <a> in vzeti tekst znotraj
    model_letala = funkcije_urejanja.poisci(r'<a[^>]*>(.*?)</a>', vse)

    if model_letala == "Ni podatka":
        model_letala = re.sub(r'<.*?>', '', vse).strip()

    model_letala = funkcije_urejanja.pocisti_besedilo(model_letala)
    podatki_nesrece["model_letala"] = model_letala

def obdelaj_operaterja(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev operaterja."""

    operater = funkcije_urejanja.poisci(r'<td class="caption">Owner/operator:</td><td class="desc">(.*?)</td>', vsebina)
    operater = funkcije_urejanja.pocisti_besedilo(operater)
    podatki_nesrece["operater"] = operater

def obdelaj_starost_letala(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev starosti letala."""

    leto_proizvodnje = funkcije_urejanja.poisci(r'<td class="caption">Year of manufacture:</td><td class="desc">(.*?)</td>', vsebina)

    if leto_proizvodnje != "Ni podatka":
        leto_nesrece = podatki_nesrece["leto"]

        if leto_nesrece != "Ni podatka":
            starost_letala = int(leto_nesrece) - int(leto_proizvodnje)
            podatki_nesrece["starost_letala"] = starost_letala
        else:
           podatki_nesrece["starost_letala"] = "Ni podatka" 

    else:
        podatki_nesrece["starost_letala"] = leto_proizvodnje

def obdelaj_posadka_in_smrti(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev števila posadke in smrtnih žrtev."""

    posadka_in_smrtne_zrtve = re.search(r'Fatalities: (.*?) / Occupants: (.*?)</td>', vsebina)

    if posadka_in_smrtne_zrtve:
        smrtne_zrtve = posadka_in_smrtne_zrtve.group(1).strip()
        posadka = posadka_in_smrtne_zrtve.group(2).strip()

        if posadka == "0":
            posadka = "Ni podatka"

        if posadka == "":
            posadka = "Ni podatka"

        if smrtne_zrtve == "":
            smrtne_zrtve = "Ni podatka"   

        podatki_nesrece["smrtne_zrtve"] = smrtne_zrtve
        podatki_nesrece["posadka"] = posadka

        if posadka != "Ni podatka" and smrtne_zrtve != "Ni podatka":
            try:
                preziveli = int(posadka) - int(smrtne_zrtve)
                razmerje_prezivelih = round((preziveli / int(posadka)) * 100)
                podatki_nesrece["razmerje_prezivelih"] = razmerje_prezivelih
            except (ValueError, ZeroDivisionError):
                podatki_nesrece["razmerje_prezivelih"] = "Ni podatka"

        else:
            podatki_nesrece["razmerje_prezivelih"] = "Ni podatka"

    else:
        podatki_nesrece["smrtne_zrtve"] = "Ni podatka"
        podatki_nesrece["posadka"] = "Ni podatka"
        podatki_nesrece["razmerje_prezivelih"] = "Ni podatka"

def obdelaj_skoda_letala(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev škode letala."""

    skoda_letala = funkcije_urejanja.poisci(r'<td class="caption">Aircraft damage:</td><td class="desc">(.*?)</td>', vsebina)
    skoda_letala = funkcije_urejanja.pocisti_besedilo(skoda_letala.replace(", ", " & "))
    podatki_nesrece["skoda_letala"] = skoda_letala

def obdelaj_vrsto_nesrece(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev vrste nesreče."""

    vrsta_nesrece = funkcije_urejanja.poisci(r'<td class="caption">Category:</td><td class="desc">(.*?)</td>', vsebina)
    podatki_nesrece["vrsta_nesrece"] = vrsta_nesrece

def obdelaj_faza_leta(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev faze leta ob nesreči."""

    faza_leta = funkcije_urejanja.poisci(r'<td class="caption">Phase:</td><td class="desc">(.*?)</td>', vsebina)

    if "Manoeuvring" in faza_leta:
        faza_leta = "Manoeuvring"

    podatki_nesrece["faza_leta"] = faza_leta

def obdelaj_narava_leta(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev narave leta."""

    narava_leta = funkcije_urejanja.poisci(r'<td class="caption">Nature:</td><td class="desc">(.*?)</td>', vsebina)
    podatki_nesrece["narava_leta"] = narava_leta

def obdelaj_kraj_nesrece(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev kraja nesreče."""

    ujemanja = re.search(
        r'<td[^>]*>Location:</td><td class="desc">(.*?)<img[^>]*>\s*&nbsp;\s*<a[^>]*>(.*?)</a>',
        vsebina, re.DOTALL)

    if ujemanja:
        surovi_kraj = ujemanja.group(1).strip()
        drzava = ujemanja.group(2).strip()
        kraj = funkcije_urejanja.pocisti_kraj(surovi_kraj)
        kraj = re.sub(r'^\s*of\s+', '', kraj, flags=re.IGNORECASE)

        if drzava.lower() == "unknown country":
            drzava = "Ni podatka"

    else:
        kraj = "Ni podatka"
        drzava = "Ni podatka"

    podatki_nesrece["kraj_nesrece"] = kraj
    podatki_nesrece["drzava_nesrece"] = drzava

def obdelaj_odhodno_letalisce(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev odhodnega letališča."""

    odhodno_letalisce = funkcije_urejanja.poisci(r'<td class="caption">Departure airport:</td><td class="desc">(.*?)</td>', vsebina)

    if odhodno_letalisce != "Ni podatka":
        odhodno_letalisce = funkcije_urejanja.pocisti_besedilo(odhodno_letalisce)

    podatki_nesrece["odhodno_letalisce"] = odhodno_letalisce

def obdelaj_ciljno_letalisce(vsebina, podatki_nesrece):
    """ Funkcija za pridobitev ciljnega letališča."""

    ciljno_letalisce = funkcije_urejanja.poisci(r'<td class="caption"><nobr>Destination airport:</nobr></td><td class="desc">(.*?)</td></tr>', vsebina)

    if ciljno_letalisce != "Ni podatka":
        ciljno_letalisce = funkcije_urejanja.pocisti_besedilo(ciljno_letalisce)

    podatki_nesrece["ciljno_letalisce"] = ciljno_letalisce

obdelovalci = {
        "Date": obdelaj_datum, "Type": obdelaj_model_letala, "Owner/operator": obdelaj_operaterja, "Year of manufacture": obdelaj_starost_letala,
        "Fatalities": obdelaj_posadka_in_smrti, "Aircraft damage": obdelaj_skoda_letala, "Category": obdelaj_vrsto_nesrece, "Phase": obdelaj_faza_leta,
        "Nature": obdelaj_narava_leta, "Location": obdelaj_kraj_nesrece, "Departure airport": obdelaj_odhodno_letalisce, "Destination airport": obdelaj_ciljno_letalisce,
} 

def preberi_vsebino_iz_datoteke(ime_datoteke):
    with open(ime_datoteke, "r", encoding="utf-8") as f:
        return f.read()
    
def obdelaj_nesreco(vsebina):
    podatki_nesrece = {}
    for kljuc, funkcija in obdelovalci.items():
        funkcija(vsebina, podatki_nesrece)

    return podatki_nesrece

def obdelaj_vse_datoteke(v_mapi):
    rezultati = []
    for ime_datoteke in os.listdir(v_mapi):
        if ime_datoteke.endswith(".html"):
            pot = os.path.join(v_mapi, ime_datoteke)
            vsebina = preberi_vsebino_iz_datoteke(pot)
            podatki = obdelaj_nesreco(vsebina)
            rezultati.append(podatki)

    return rezultati