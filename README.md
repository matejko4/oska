# Aplikace pro správu fotbalistů

Webová aplikace ve Flasku s přihlášením a možností vytvářet kartičky fotbalistů.

## Funkce

- **Registrace a přihlášení uživatelů** - zabezpečené hesla pomocí hash
- **Vytváření kartiček fotbalistů** - formulář s informacemi jako jméno, věk, pozice, klub, číslo dresu, národnost
- **Přehled fotbalistů** - zobrazení všech fotbalistů vytvořených přihlášeným uživatelem
- **Mazání fotbalistů** - možnost smazat karticku fotbalisty
- **SQLite databáze** - dvě propojené tabulky (uživatelé a fotbalisté)

## Instalace

1. Naklonujte repozitář:
```bash
git clone <url-repozitare>
cd oska
```

2. Vytvořte virtuální prostředí:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate  # Windows
```

3. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

## Spuštění

```bash
python app.py
```

Aplikace bude dostupná na adrese: `http://127.0.0.1:5000`

## Použití

1. Zaregistrujte se na stránce `/registrace`
2. Přihlaste se pomocí svého uživatelského jména a hesla
3. Klikněte na "Přidat fotbalistu" a vyplňte formulář
4. Prohlížejte si své fotbalisty v přehledu
5. Můžete je také mazat pomocí tlačítka "Smazat"

## Struktura projektu

```
oska/
├── app.py                 # Hlavní aplikace Flask
├── requirements.txt       # Python závislosti
├── .gitignore            # Git ignore soubor
├── README.md             # Tento soubor
└── templates/            # HTML šablony
    ├── base.html         # Základní šablona
    ├── prihlaseni.html   # Přihlášení
    ├── registrace.html   # Registrace
    ├── prehled.html      # Přehled fotbalistů
    └── pridat_fotbalistu.html  # Formulář pro přidání
```

## Technologie

- **Flask** - Python web framework
- **SQLAlchemy** - ORM pro práci s databází
- **Bootstrap 5** - CSS framework pro design
- **SQLite** - Databáze

## Připraveno pro GitHub

Projekt obsahuje `.gitignore` soubor, který ignoruje:
- Databázové soubory (*.db)
- Virtuální prostředí
- Python cache soubory
- IDE konfigurace

Před nahráním na GitHub změňte `SECRET_KEY` v `app.py` na bezpečnější hodnotu!