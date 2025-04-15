# Nástroj pro Analýzu Akciového Trhu 📈

Moderní desktopová aplikace pro analýzu akciového trhu s daty v reálném čase a technickými indikátory.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![DearPyGui](https://img.shields.io/badge/DearPyGui-1.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Funkce 🚀

- **Data v Reálném Čase**: Získávání aktuálních informací o akciích pomocí Yahoo Finance API
- **Vyhledávání Společností**: Najděte burzovní symboly pro jakoukoliv společnost
- **Cenová Analýza**: Sledujte nejvyšší a nejnižší ceny v různých časových obdobích
- **Technická Analýza**: Generování interaktivních grafů s různými indikátory
  - Jednoduché Klouzavé Průměry (SMA20, SMA50)
  - Index Relativní Síly (RSI)
  - Svíčkové grafy
- **Informace o Společnosti**: Získejte klíčové finanční metriky jako výnosy, dluh a ziskové marže
- **Moderní Rozhraní**: Čisté, tmavé téma s intuitivním ovládáním

## Instalace 🔧

1. Klonování repozitáře:
   ```bash
   git clone https://github.com/yourusername/StockMarketProject.git
   cd StockMarketProject
   ```

2. Vytvoření a aktivace virtuálního prostředí (doporučeno):
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalace závislostí:
   ```bash
   pip install -r requirements.txt
   ```

## Použití 💡

1. Spuštění aplikace:
   ```bash
   python src/UserGui.py
   ```

2. Dostupné funkce v postranním panelu:
   - **Cenová Analýza**: Zobrazení nejvyšších/nejnižších cen akcií
   - **Vyhledávání Tickerů**: Najděte burzovní symboly společností
   - **Info o Společnosti**: Získejte základní finanční informace
   - **Technický Graf**: Generujte interaktivní grafy technické analýzy

3. Pro technickou analýzu:
   - Zadejte název společnosti nebo ticker
   - Vyberte časové období (1d až 5y)
   - Zvolte technické indikátory (SMA20, SMA50, RSI)
   - Klikněte na "Generovat Graf" pro vytvoření a zobrazení analýzy

## Struktura Projektu 📁

```
StockMarketProject/
├── src/
│   ├── UserGui.py           # Hlavní GUI aplikace
│   └── Stocks/
│       ├── StockDataHandler.py    # Správa dat akcií
│       └── TechnicalAnalysis.py   # Technické indikátory a grafy
├── charts/                  # Úložiště generovaných grafů
├── requirements.txt         # Závislosti projektu
└── README.md
```

## Závislosti 📚

- `dearpygui`: Framework pro moderní GUI
- `yfinance`: Wrapper pro Yahoo Finance API
- `yahooquery`: Rozšířená funkcionalita Yahoo Finance API
- `plotly`: Generování interaktivních grafů
- `pandas`: Manipulace a analýza dat
- `numpy`: Numerické výpočty

## Logování 📝

Aplikace udržuje logy v `app.log`, sleduje:
- Vyhledávání akcií
- Generování grafů
- Chyby a výjimky
- Operace načítání dat

