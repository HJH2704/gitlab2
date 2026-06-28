
import os
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Optional: falls du scipy-Funktionen nutzen willst (z.B. glätten/interpolieren)
# from scipy import interpolate, signal

# --- Konfiguration ---
# --- Konfiguration ---
INPUT_PATH1 = "./Data/tabelle_3_21.txt"  
INPUT_PATH2 = "./Data/tabelle_3_22.txt"
   # Eingabedatei mit LaTeX-Tabellenzeilen
OUT_DIR = "../Abbildungen/3/2"           # Ausgabeordner
os.makedirs(OUT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PNG_PATH1 = os.path.join(OUT_DIR, f"Messspektrum_Rechteck_m05_{TIMESTAMP}.pdf")
PNG_PATH2 = os.path.join(OUT_DIR, f"Messspektrum_Rechteck_m1{TIMESTAMP}.pdf")





def clean_line(line: str) -> str:
    """Entfernt LaTeX-Enden, \hline, Kommentare und Leerraum; wandelt ','->'.'."""
    # Kommentare nach '%' entfernen
    line = line.split('%', 1)[0]
    # LaTeX-Endevarianten entfernen
    line = re.sub(r'\\\\\s*\\hline', '', line)  # "\\ \hline"
    line = re.sub(r'\\\\', '', line)             # "\\"
    line = re.sub(r'\\hline', '', line)          # "\hline"
    # Entferne überflüssige Backslashes oder geschweifte Klammern
    line = line.replace('{', '').replace('}', '')
    # Dezimalkomma zu Dezimalpunkt
    line = line.replace(',', '.')
    return line.strip()

def parse_table_file(path: str):
    """
    Liest die Datei und gibt ein 2D-numpy-array zurück mit shape (n_rows, n_cols).
    Erwartet Zeilen mit & als Spaltentrenner. Ignoriert ungültige Zeilen.
    """
    rows = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"Eingabedatei nicht gefunden: {path}")
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = clean_line(raw)
            if not line:
                continue
            # Nur Zeilen mit '&' auswerten
            if '&' not in line:
                continue
            parts = [p.strip() for p in line.split("&")]
            # Versuche, alle Teile in float zu konvertieren; bei Fehler Zeile überspringen
            try:
                nums = [float(p) for p in parts if p != '']
            except ValueError:
                # Falls Zeile Text enthält, überspringen
                continue
            if len(nums) >= 2:
                rows.append(nums)
    if not rows:
        raise ValueError("Keine gültigen Datenzeilen gefunden.")
    # Vereinheitliche Spaltenanzahl (fülle fehlende Spalten mit np.nan)
    max_cols = max(len(r) for r in rows)
    mat = np.full((len(rows), max_cols), np.nan, dtype=float)
    for i, r in enumerate(rows):
        mat[i, :len(r)] = r
    return mat

def create_sideband_labels(x, carrier_label="Träger"):
    """
    Erstellt zweizeilige xticklabels für ein symmetrisches Spektrum.

    Beispiel:
        3.
        SF

        2.
        SF

        1.
        SF

        Träger
    """

    n = len(x)

    if n % 2 == 0:
        raise ValueError("Das Array muss eine ungerade Anzahl an Frequenzen besitzen.")

    center = n // 2
    labels = []

    for i in range(n):
        if i == center:
            labels.append(carrier_label)
        else:
            order = abs(i - center)
            labels.append(f"{order}.\nSB")

    return labels

if __name__ == "__main__":
    print("Lese Datei:", INPUT_PATH1)
    data = parse_table_file(INPUT_PATH1)   # shape (n_rows, n_cols)
#   Erste Spalte als x, restliche als y1, y2, ...
    x = data[:, 0]
    ys = data[:, 1:]
 
#   Sortiere nach x (falls nicht sortiert)
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    ys = ys[sort_idx, :]
 
    print("Gelesene Form:", data.shape)
    print("x (erste 21):", x[:21])
    print("y-Spaltenanzahl:", ys.shape[1])
    #y_bessel05 = np.array([0.031, 0.242, 0.938, 0.242, 0.031])
   
    #--- Plot ---
    fig, ax = plt.subplots(figsize=(8, 5))
    for col in range(ys.shape[1]):
        y =  ys[:, col] # hier umwandlung in \omega möglich
        # Ignoriere Spalten, die komplett NaN sind
        if np.all(np.isnan(y)):
            continue
        # Entferne NaN-Reihen für Plot
        valid = ~np.isnan(y)
        label = f"$y_{col+1}$"
        base_colors = plt.cm.tab20(np.linspace(0, 1, 4))
        farben = np.vstack([base_colors, base_colors[:-1][::-1]])
        y_neu = y/1.13
        ax.bar(x[valid],y_neu[valid], color=farben, label= "Messwerte", width=0.001)
        #ax.bar(x, y_bessel05,color='black',label = "Theoriewerte des Besselfunktion", width=0.00035)
        ax.axhline(0, color='black', linewidth=1)
        ax.set_ylim(0,1)
        ax.set_xlabel("Frequenz in MHz")
        secax = ax.secondary_xaxis('top')
        secax.set_xticks(x)
        secax.set_xticklabels(create_sideband_labels(x))
# Abstand zwischen den beiden Achsen
       # secax.spines['top'].set_position(('outward', 40))
        secax.tick_params(length=0)
        ax.set_ylabel("Amplitude in V")
        ax.set_title("Messspektrum m = 0,5")       
        plt.grid(True)
        plt.tight_layout()
        fig.text(0.98, 0.02, "SB = Seitenband", ha="right", fontsize=10)
        ax.legend(loc="upper right")
        plt.savefig(PNG_PATH1, dpi=300, bbox_inches="tight")
        print("Plot gespeichert als:", PNG_PATH1)


if __name__ == "__main__":
    print("Lese Datei:", INPUT_PATH2)
    data = parse_table_file(INPUT_PATH2)   # shape (n_rows, n_cols)
#   Erste Spalte als x, restliche als y1, y2, ...
    x = data[:, 0]
    ys = data[:, 1:]
 
#   Sortiere nach x (falls nicht sortiert)
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    ys = ys[sort_idx, :]
 
    print("Gelesene Form:", data.shape)
    print("x (erste 21):", x[:21])
    print("y-Spaltenanzahl:", ys.shape[1])
    #y_bessel05 = np.array([0.031, 0.242, 0.938, 0.242, 0.031])
   
    #--- Plot ---
    fig, ax = plt.subplots(figsize=(8, 5))
    for col in range(ys.shape[1]):
        y =  ys[:, col] # hier umwandlung in \omega möglich
        # Ignoriere Spalten, die komplett NaN sind
        if np.all(np.isnan(y)):
            continue
        # Entferne NaN-Reihen für Plot
        valid = ~np.isnan(y)
        label = f"$y_{col+1}$"
        base_colors = plt.cm.tab20(np.linspace(0, 1, 5))
        farben = np.vstack([base_colors, base_colors[:-1][::-1]])
        y_neu = y/1.13
        ax.bar(x[valid],y_neu[valid], color=farben, label= "Messwerte", width=0.001)
        #ax.bar(x, y_bessel05,color='black',label = "Theoriewerte des Besselfunktion", width=0.00035)
        ax.axhline(0, color='black', linewidth=1)
        ax.set_ylim(0,1)
        ax.set_xlabel("Frequenz in MHz")
        secax = ax.secondary_xaxis('top')
        secax.set_xticks(x)
        secax.set_xticklabels(create_sideband_labels(x))
# Abstand zwischen den beiden Achsen
       # secax.spines['top'].set_position(('outward', 40))
        secax.tick_params(length=0)
        ax.set_ylabel("Amplitude in V")
        ax.set_title("Messspektrum Phasenmodulator m = 1")       
        plt.grid(True)
        plt.tight_layout()
        fig.text(0.98, 0.02, "SB = Seitenband", ha="right", fontsize=10)
        ax.legend(loc="upper right")
        plt.savefig(PNG_PATH2, dpi=300, bbox_inches="tight")
        print("Plot gespeichert als:", PNG_PATH2)
