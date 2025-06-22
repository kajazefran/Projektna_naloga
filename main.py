import os
import uvozi
import obdelaj
import napisi_csv

mapa = "nesrece"
csv_ime = "rezultati.csv"

def main():
    # 1. Če mapa z nesrečami ne obstaja, jo ustvari in prenesi html-je
    if not os.path.exists(mapa):
        print(f"Mapa '{mapa}' ne obstaja. Ustvarjam in prenašam HTML datoteke...")
        os.makedirs(mapa)
        uvozi.poberi_html_za_vse_letalske_nesrece(mapa=mapa)
    else:
        # Preverimo, če v mapi že obstajajo .html datoteke
        html_datoteke = [f for f in os.listdir(mapa) if f.endswith(".html")]
        if not html_datoteke:
            print(f"Mapa '{mapa}' je prazna. Prenašam HTML datoteke...")
            uvozi.poberi_html_za_vse_letalske_nesrece(mapa=mapa)
        else:
            print(f"HTML datoteke že obstajajo v '{mapa}'. Preskočim prenos.")

    # 2. Če CSV še ni narejen, ga naredimo
    if not os.path.exists(csv_ime):
        print("CSV datoteka še ne obstaja. Obdelujem HTML datoteke in ustvarjam CSV...")
        podatki = obdelaj.obdelaj_vse_datoteke(mapa)
        napisi_csv.zapisi_rezultate_v_csv(podatki, csv_ime)
        print(f"CSV datoteka ustvarjena.")
    else:
        print("CSV datoteka že obstaja. Ne obdelujem ponovno.")

if __name__ == "__main__":
    main()