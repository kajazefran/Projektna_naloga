import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def poberi_html_za_vse_letalske_nesrece(od_leto=1919, do_leto=2024, mapa="nesrece"):
    """ S to funkcijo, se sprehodimo po straneh vseh let nesrec v ASN bazi, prenesemo
    html za vsako letalsko nesreco posebej in jih shranimo v mapo: nesrece"""

    pot_do_brskalnika = os.path.join(os.getcwd(), "msedgedriver.exe") # pot v isti mapi kot skripta
    storitev = Service(executable_path=pot_do_brskalnika)

    moznosti = Options()
    moznosti.add_argument("user-agent=Mozilla/5.0")
    moznosti.add_argument("--headless")

    brskalnik = webdriver.Edge(service=storitev, options=moznosti)
    cakanje = WebDriverWait(brskalnik, 3)

    os.makedirs(mapa, exist_ok=True) # ce mapa kamor bomo shranjevali htmlje se ne obstaja, jo ustvarimo

    zaporedna_stevilka_nesrec = 1

    for leto in range(od_leto, do_leto + 1):
        print(f"Leto {leto}")
        stevilka_strani = 1

        while True:
            print(stevilka_strani)

            povezava = f"https://asn.flightsafety.org/database/year/{leto}/{stevilka_strani}"
            brskalnik.get(povezava)
            cakanje.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            vrstice_nesrec = brskalnik.find_elements(By.CSS_SELECTOR, "tr.list")
            vse_povezave = []

            for vrstica in vrstice_nesrec:
                povezave_nesrec = vrstica.find_elements(By.CSS_SELECTOR, "a[href*=\"wikibase\"]")
                for povezava in povezave_nesrec:
                    href = povezava.get_attribute("href")
                    if href:
                        vse_povezave.append(href)
            
            if not vse_povezave:
                print(f"Na strani {stevilka_strani} ni vec nesrec za leto {leto}.")
                break

            for povezava_nesrece in vse_povezave:
                brskalnik.get(povezava_nesrece)
                cakanje.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
                html = brskalnik.page_source

                ime_html = os.path.join(mapa, f"nesreca_{zaporedna_stevilka_nesrec}.html")
                with open(ime_html, "w", encoding="utf-8") as dat:
                    dat.write(html)
                zaporedna_stevilka_nesrec += 1
                
            stevilka_strani += 1

    brskalnik.quit()
    print("Vse nesrece so bile prenesene.")

poberi_html_za_vse_letalske_nesrece()