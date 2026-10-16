"""Chargement et préparation de base des données NASA C-MAPSS."""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

SETTINGS = ["setting_1", "setting_2", "setting_3"]
SENSORS = [f"s_{i}" for i in range(1, 22)]
COLUMNS = ["unit", "cycle"] + SETTINGS + SENSORS

# Signification des capteurs (Saxena et al., 2008)
SENSOR_NAMES = {
    "s_1": "T2 - Température entrée soufflante (°R)",
    "s_2": "T24 - Température sortie LPC (°R)",
    "s_3": "T30 - Température sortie HPC (°R)",
    "s_4": "T50 - Température sortie LPT (°R)",
    "s_5": "P2 - Pression entrée soufflante (psia)",
    "s_6": "P15 - Pression conduit bypass (psia)",
    "s_7": "P30 - Pression totale sortie HPC (psia)",
    "s_8": "Nf - Vitesse physique soufflante (rpm)",
    "s_9": "Nc - Vitesse physique cœur (rpm)",
    "s_10": "epr - Rapport de pression moteur",
    "s_11": "Ps30 - Pression statique sortie HPC (psia)",
    "s_12": "phi - Ratio débit carburant / Ps30",
    "s_13": "NRf - Vitesse corrigée soufflante (rpm)",
    "s_14": "NRc - Vitesse corrigée cœur (rpm)",
    "s_15": "BPR - Taux de dilution",
    "s_16": "farB - Ratio carburant/air brûleur",
    "s_17": "htBleed - Enthalpie de prélèvement",
    "s_18": "Nf_dmd - Vitesse soufflante demandée (rpm)",
    "s_19": "PCNfR_dmd - Vitesse corrigée demandée (rpm)",
    "s_20": "W31 - Débit air refroidissement HPT",
    "s_21": "W32 - Débit air refroidissement LPT",
}


def load_split(subset: str = "FD001", split: str = "train", data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Charge train_FDxxx.txt ou test_FDxxx.txt sous forme de DataFrame."""
    path = Path(data_dir) / f"{split}_{subset}.txt"
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLUMNS)


def load_test_rul(subset: str = "FD001", data_dir: Path = DATA_DIR) -> pd.Series:
    """RUL réelle de chaque moteur de test, à son dernier cycle observé."""
    path = Path(data_dir) / f"RUL_{subset}.txt"
    rul = pd.read_csv(path, header=None, names=["RUL"])["RUL"]
    rul.index = range(1, len(rul) + 1)
    rul.index.name = "unit"
    return rul


def add_rul(df: pd.DataFrame, cap: int | None = None) -> pd.DataFrame:
    """Ajoute la colonne RUL = dernier cycle du moteur - cycle courant.

    Avec `cap`, la RUL est plafonnée (ex. 125) : un moteur neuf ne montre
    pas encore de signe d'usure, inutile de chercher à prédire au-delà.
    """
    out = df.copy()
    last_cycle = out.groupby("unit")["cycle"].transform("max")
    out["RUL"] = last_cycle - out["cycle"]
    if cap is not None:
        out["RUL"] = out["RUL"].clip(upper=cap)
    return out


def constant_columns(df: pd.DataFrame, cols: list[str], tol: float = 1e-3) -> list[str]:
    """Colonnes dont l'écart-type est quasi nul : elles n'apportent aucune information."""
    std = df[cols].std()
    return std[std < tol].index.tolist()
