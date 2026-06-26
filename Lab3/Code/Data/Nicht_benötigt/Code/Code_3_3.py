
import os
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Optional: falls du scipy-Funktionen nutzen willst (z.B. glätten/interpolieren)
# from scipy import interpolate, signal

# --- Konfiguration ---
# --- Konfiguration ---
INPUT_PATH1 = "./Data/tabelle_3_3.txt"     # Eingabedatei mit LaTeX-Tabellenzeilen
OUT_DIR = "../Abbildungen/3/3"           # Ausgabeordner
os.makedirs(OUT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PNG_PATH1 = os.path.join(OUT_DIR, f"Messspektrum_f1_30kHz_{TIMESTAMP}.pdf")
PNG_PATH2 = os.path.join(OUT_DIR, f"Messspektrum_f1_50kHz_{TIMESTAMP}.pdf")
PNG_PATH3 = os.path.join(OUT_DIR, f"Messspektrm_f1_70kHz_{TIMESTAMP}.pdf")
PNG_PATH4 = os.path.join(OUT_DIR, f"Messspektrm_f1_100kHz_{TIMESTAMP}.pdf")

def clean_line(line: str) -> str:
    """Entfernt LaTeX-Enden, \hline, Kommentare und Leerraum; wandelt ','->'.'."""
    line = line.split('%', 1)[0]

    line = re.sub(r'\\\\\s*\\hline', '', line)
    line = re.sub(r'\\\\', '', line)
    line = re.sub(r'\\hline', '', line)

    line = line.replace('{', '').replace('}', '')
    line = line.replace(',', '.')

    return line.strip()


def parse_table_file(path: str):
    """
    Liest eine LaTeX-Tabelle ein und gibt ein 2D-numpy-array zurück.

    Jede LaTeX-Spalte wird dabei zu einem eigenen Array:
        mat[0] -> 1. Spalte
        mat[1] -> 2. Spalte
        ...
    """
    rows = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"Eingabedatei nicht gefunden: {path}")

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = clean_line(raw)

            if not line or '&' not in line:
                continue

            parts = [p.strip() for p in line.split("&")]

            try:
                nums = [float(p) for p in parts if p != ""]
            except ValueError:
                continue

            rows.append(nums)

    if not rows:
        raise ValueError("Keine gültigen Datenzeilen gefunden.")

    # Matrix erzeugen
    mat = np.array(rows, dtype=float)

    # Zeilen <-> Spalten tauschen
    return mat.T

def create_plot(x, y, title, outfile):
    plt.figure(figsize=(8, 5))

    valid = ~np.isnan(y)

    base_colors = plt.cm.tab20(np.linspace(0, 1, len(x[valid])))
    farben = np.vstack([base_colors[:11], base_colors[:10][::-1]])

    plt.bar(x[valid], y[valid], color=farben[:len(x[valid])], width=0.02)

    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Spektrallinien in MHz")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(outfile, dpi=300, bbox_inches="tight")
    plt.close()

    print("Plot gespeichert:", outfile)


if __name__ == "__main__":

    print("Lese Datei:", INPUT_PATH1)

    data = parse_table_file(INPUT_PATH1)

    print("Form:", data.shape)

    plots = [
        (0, 1, "Messspektrum f1 = 30kHz", PNG_PATH1),
        (2, 3, "Messspektrum f1 = 50kHz", PNG_PATH2),
        (4, 5, "Messspektrum f1 = 70kHz", PNG_PATH3),
        (6, 7, "Messspektrum f1 = 100kHz", PNG_PATH4),
    ]

    for x_idx, y_idx, title, outfile in plots:
        x = data[x_idx]
        y = data[y_idx]

        sort_idx = np.argsort(x)

        x = x[sort_idx]
        y = y[sort_idx]

        create_plot(x, y, title, outfile)