import csv

def zapisi_rezultate_v_csv(seznam_podatkov, ime_csv):
    if not seznam_podatkov:
        print("Ni podatkov za zapis.")
        return

    kljuci = list(seznam_podatkov[0].keys())

    with open(ime_csv, mode="w", encoding="utf-8", newline="") as f:
        pisec = csv.DictWriter(f, fieldnames=kljuci)
        pisec.writeheader()
        pisec.writerows(seznam_podatkov)

    print(f"Podatki shranjeni.")