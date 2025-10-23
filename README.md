# HealthDataAnalyzer
TIDS

# 🩺 Tržnica zdravja – Naloga XML in JSON

## Opis projekta
Projekt **Tržnica zdravja (naloga 1: XML in JSON)** je nadaljevanje ideje iz prejšnje naloge – spremljanje zdravstvenih kazalnikov po slovenskih regijah.  
Aplikacija prikazuje, kako lahko s pomočjo **XML in JSON struktur** predstavimo, povežemo in filtriramo podatke iz več povezanih virov.

Podatki so organizirani v **tri XML datoteke**:
- `regions.xml` – seznam slovenskih regij (z imenom, glavnim mestom, površino, številom prebivalcev …),
- `indicators.xml` – seznam zdravstvenih kazalnikov (npr. delež oseb z dobrim zdravjem, debelost, pričakovana življenjska doba …),
- `measurements.xml` – meritve (povezava med regijo in kazalnikom, datum meritve, vrednost).

Program vse tri datoteke prebere, poveže podatke prek ID-jev (`regionId`, `indicatorId`), omogoča **filtriranje po različnih pogojih**, ter izvoz rezultatov v formatu **JSON in XML**.

---

## Funkcionalnosti aplikacije
- **Branje XML datotek** in pretvorba v Python objekte (deserializacija).  
- **Združevanje podatkov** prek atributov `id`, `regionId`, `indicatorId`.  
- **Filtriranje** po različnih kriterijih (regija, kazalnik, datum, vrednost).  
- **Izpis v pregledni tabeli** v konzoli.  
- **Izvoz filtriranih rezultatov** v datoteki `filtrirano.json` in `filtrirano.xml`.

---

## Struktura projekta
data/
├── regions.xml
│   └── Regions
│       ├── Region (id="RE01")
│       │   ├── name
│       │   ├── capital
│       │   ├── nutsCode
│       │   ├── areaKm2
│       │   ├── population
│       │   ├── note
│       │   └── createdAt
│       ├── Region (id="RE02")
│       ├── ...
│       └── Region (id="RE12")
│
├── indicators.xml
│   └── Indicators
│       ├── Indicator (id="IN01")
│       │   ├── code
│       │   ├── name
│       │   ├── unit
│       │   ├── source
│       │   └── createdAt
│       ├── Indicator (id="IN02")
│       ├── ...
│       └── Indicator (id="IN10")
│
└── measurements.xml
    └── Measurements
        ├── Observation (id="OB001", regionId="RE02", indicatorId="IN01")
        │   ├── date
        │   ├── value
        │   ├── quality
        │   └── comment
        ├── Observation (id="OB002", regionId="RE08", indicatorId="IN01")
        ├── ...
        └── Observation (id="OB015", regionId="RE04", indicatorId="IN05")


![alt text](image.png)
![alt text](image-1.png)