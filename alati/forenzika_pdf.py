import os
from pypdf import PdfReader

def forenzicki_pregled_pdfa(putanja_fajla):
    """
    Funkcija koja otvara PDF i izvlači sve skrivene metapodatke o autoru i sistemu.
    """
    if not os.path.exists(putanja_fajla):
        print("❌ Greška: Fajl ne postoji na navedenoj putanji.")
        return

    try:
        # Otvaranje PDF dokumenta
        reader = PdfReader(putanja_fajla)
        meta = reader.metadata
        broj_stranica = len(reader.pages)
        
        print("\n" + "="*50)
        print("🔍 FORENZIČKI IZVJEŠTAJ METAPODATAKA DOKUMENTA")
        print("="*50)
        print(f"📁 Naziv fajla: {os.path.basename(putanja_fajla)}")
        print(f"📄 Broj stranica u dokumentu: {broj_stranica}")
        print("-"*50)

        if not meta:
            print("⚠️ Upozorenje: Ovaj dokument nema sačuvane metapodatke (fajl je očišćen ili je sirov sken).")
            return

        # Mapiranje standardnih PDF metapodataka
        standardni_podaci = {
            "Naslov (Title)": meta.title,
            "Autor (Author/Korisnik računara)": meta.author,
            "Tema (Subject)": meta.subject,
            "Kreator (Aplikacija koja je pisala tekst)": meta.creator,
            "Producenat (Softver koji je napravio PDF)": meta.producer,
            "Datum kreiranja (Creation Date)": meta.creation_date,
            "Datum izmjene (Modification Date)": meta.modification_date
        }

        # Ispis standardnih metapodataka
        nadjeni_podaci = False
        for oznaka, vrijednost in standardni_podaci.items():
            if vrijednost:
                print(f"📌 {oznaka}: {vrijednost}")
                nadjeni_podaci = True

        # Ispis dodatnih ili prilagođenih metapodataka koje institucije nekad unesu
        print("-"*50)
        print("⚙️ Ostali skriveni sistemski tagovi:")
        for kljuc, vrijednost in meta.items():
            # Preskačemo standardne jer smo ih već ispisali
            if kljuc not in ['/Title', '/Author', '/Subject', '/Creator', '/Producer', '/CreationDate', '/ModDate']:
                print(f"  🔹 {kljuc}: {vrijednost}")
                nadjeni_podaci = True

        if not nadjeni_podaci:
            print("   Nema dodatnih skrivenih tagova.")
            
        print("="*50)
        print("💡 Savjet za građansku forenziku:")
        print("Ukoliko se ime autora (Author) razlikuje od osobe koja je potpisala rješenje,")
        print("to može ukazivati na to da je nacrt dokumenta pisalo treće lice ili spoljni saradnik.")
        print("="*50 + "\n")

    except Exception as e:
        print(f"❌ Došlo je do greške prilikom analize PDF-a: {e}")

if __name__ == "__main__":
    print("--- Alat za građansku forenziku: Ekstraktor PDF Metapodataka ---")
    putanja = input("Unesite putanju do PDF dokumenta (ili ga prevucite ovdje): ").strip("'\" ")
    forenzicki_pregled_pdfa(putanja)
