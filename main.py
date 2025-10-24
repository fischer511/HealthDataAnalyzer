import argparse, json
from dataclasses import dataclass
from datetime import date
from xml.etree import ElementTree as ET
from pathlib import Path

DATA_DIR = Path("data")

#Pretvorba XML podatkov v objekte, npr. razrede ali sezname.
@dataclass 
class Region:
    id: str; name: str; capital: str

@dataclass
class Indicator:
    id: str; code: str; name: str; unit: str

@dataclass
class Observation:
    id: str; regionId: str; indicatorId: str; date: str; value: str

def load_regions():
    root = ET.parse(DATA_DIR/"regions.xml").getroot() #branje XML datotek
    out = {}
    for r in root.findall("Region"):
        out[r.get("id")] = Region(
            id=r.get("id"),
            name=r.findtext("name"),
            capital=r.findtext("capital")
        )
    return out

def load_indicators():
    root = ET.parse(DATA_DIR/"indicators.xml").getroot()
    out = {}
    for i in root.findall("Indicator"):
        out[i.get("id")] = Indicator(
            id=i.get("id"),
            code=i.findtext("code"),
            name=i.findtext("name"),
            unit=i.findtext("unit")
        )
    return out

def load_measurements():
    root = ET.parse(DATA_DIR/"measurements.xml").getroot()
    obs = []
    for o in root.findall("Observation"):
        obs.append(Observation(
            id=o.get("id"),
            regionId=o.get("regionId"),
            indicatorId=o.get("indicatorId"),
            date=o.findtext("date"),
            value=(o.findtext("value") or "").strip()
        ))
    return obs

#Združite podatke prek ID-jev (npr. naročilo vsebuje artikelId in dobaviteljId).
def join_data(obs, regions, indicators):
    rows = []
    for o in obs:
        r = regions.get(o.regionId)
        ind = indicators.get(o.indicatorId)
        rows.append({
            "obsId": o.id,
            "date": o.date,
            "regionId": o.regionId,
            "region": r.name if r else None,
            "indicatorId": o.indicatorId,
            "indicator": ind.code if ind else None,
            "indicatorName": ind.name if ind else None,
            "unit": ind.unit if ind else None,
            "value": None if o.value=="" else (float(o.value) if o.value.replace('.','',1).isdigit() else o.value),
        })
    return rows

#pogoji glede na argumente, ki jih uporabnik vnese v terminal
def filter_rows(rows, args):
    def after(d, cutoff): return d and d >= cutoff
    out = []
    for row in rows:
        if args.region and (row["region"] or "").lower() != args.region.lower():
            continue
        if args.indicator and (row["indicator"] or "").lower() != args.indicator.lower():
            continue
        if args.after and not after(row["date"], args.after):
            continue
        if args.max_value is not None and isinstance(row["value"], (int,float)) and row["value"] >= args.max_value:
            continue
        if args.min_value is not None and isinstance(row["value"], (int,float)) and row["value"] < args.min_value:
            continue
        out.append(row)
    return out

def print_table(rows):
    if not rows:
        print("Ni rezultatov.")
        return
    cols = ["date","region","indicator","value","unit","obsId"]
    widths = {c:max(len(c),*(len(str(r.get(c,""))) for r in rows)) for c in cols}
    line = " | ".join(c.ljust(widths[c]) for c in cols)
    print(line); print("-"*len(line))
    for r in rows:
        print(" | ".join(str(r.get(c,"")).ljust(widths[c]) for c in cols))

#“Shranite filtrirane rezultate v datoteko filtrirano.json.”
def export_json(rows, path="filtrirano.json"):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(rows,f,ensure_ascii=False,indent=2)
#“Iz istih podatkov ustvarite nov XML (filtrirano.xml).”
def export_xml(rows, path="filtrirano.xml"):
    root = ET.Element("Filtered")
    for r in rows:
        e = ET.SubElement(root, "Record", id=r["obsId"])
        for k in ["date","regionId","region","indicatorId","indicator","indicatorName","unit","value"]:
            child = ET.SubElement(e, k)
            if r[k] is None:  # manjkajoče
                continue
            child.text = str(r[k])
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

#… izpišite filtrirane rezultate
def main():
    parser = argparse.ArgumentParser(description="XML → povezava → filter → JSON/XML")
    parser.add_argument("--region", help="npr. Podravska")
    parser.add_argument("--indicator", help="npr. good_health_pct")
    parser.add_argument("--after", help="npr. 2024-01-01")
    parser.add_argument("--min-value", type=float)
    parser.add_argument("--max-value", type=float)
    args = parser.parse_args()

    regions = load_regions()
    indicators = load_indicators()
    obs = load_measurements()
    rows = join_data(obs, regions, indicators)
    
    #funkcija za filtriranje:
    filtered = filter_rows(rows, args)

#Filtrirane rezultate izpišite v konzolo v pregledni obliki (tabela, seznam …)
    print_table(filtered)
    export_json(filtered)
    export_xml(filtered)
    print("\nShranjeno: filtrirano.json, filtrirano.xml")

if __name__ == "__main__":
    main()
