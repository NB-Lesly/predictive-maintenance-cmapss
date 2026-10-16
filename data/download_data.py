"""Télécharge le sous-ensemble FD001 de NASA C-MAPSS dans data/raw/.

Source officielle : NASA Prognostics Center of Excellence – Data Repository
("Turbofan Engine Degradation Simulation"). Ce script utilise une copie
publique hébergée sur GitHub pour un téléchargement direct.
"""
from pathlib import Path
from urllib.request import urlretrieve

BASE = "https://raw.githubusercontent.com/hankroark/Turbofan-Engine-Degradation/master/CMAPSSData"
FILES = ["train_FD001.txt", "test_FD001.txt", "RUL_FD001.txt"]
RAW = Path(__file__).resolve().parent / "raw"

if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        target = RAW / name
        if target.exists():
            print(f"déjà présent : {name}")
            continue
        print(f"téléchargement : {name}")
        urlretrieve(f"{BASE}/{name}", target)
    print("Terminé.")
