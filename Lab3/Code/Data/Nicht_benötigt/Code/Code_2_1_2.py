
import os
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Optional: falls du scipy-Funktionen nutzen willst (z.B. glätten/interpolieren)
# from scipy import interpolate, signal

# --- Konfiguration ---
INPUT_PATH1 = "./Data/tabelle_2_11.txt"  
INPUT_PATH2 = "./Data/tabelle_2_12.txt"
INPUT_PATH3 = "./Data/tabelle_2_13.txt"   # Eingabedatei mit LaTeX-Tabellenzeilen
OUT_DIR = "../Abbildungen/2/2.1.2"           # Ausgabeordner
os.makedirs(OUT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PNG_PATH1 = os.path.join(OUT_DIR, f"Messspektrum_m05_{TIMESTAMP}.pdf")
PNG_PATH2 = os.path.join(OUT_DIR, f"Messspektrum_m24_{TIMESTAMP}.pdf")
PNG_PATH3 = os.path.join(OUT_DIR, f"Messspektrm_m100_{TIMESTAMP}.pdf")




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

if __name__ == "__main__":
    print("Lese Datei:", INPUT_PATH1)
    data = parse_table_file(INPUT_PATH1)   # shape (n_rows, n_cols)
    # Erste Spalte als x, restliche als y1, y2, ...
    x = data[:, 0]
    ys = data[:, 1:]

    # Sortiere nach x (falls nicht sortiert)
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    ys = ys[sort_idx, :]

    print("Gelesene Form:", data.shape)
    print("x (erste 10):", x[:10])
    print("y-Spaltenanzahl:", ys.shape[1])

    # --- Plot ---
    plt.figure(figsize=(8, 5))
    for col in range(ys.shape[1]):
        y =  ys[:, col] # hier umwandlung in \omega möglich
        # Ignoriere Spalten, die komplett NaN sind
        if np.all(np.isnan(y)):
            continue
        # Entferne NaN-Reihen für Plot
        valid = ~np.isnan(y)
        label = f"$y_{col+1}$"
        farben = plt.cm.rainbow(np.linspace(0, 1, len(y)))
        
        plt.bar(x[valid],y[valid], color=farben, width=0.2)
        plt.bar(-x[valid], y[valid], color=farben, width=0.2)
        plt.axhline(0, color='black', linewidth=1)
        plt.xlabel("Spektrallinien in 10 kHz")
        plt.ylabel("Amplitude")
        plt.title("Messspektrum m = 0,5")       
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(PNG_PATH1, dpi=300, bbox_inches="tight")
        print("Plot gespeichert als:", PNG_PATH1)

if __name__ == "__main__":
    print("Lese Datei:", INPUT_PATH2)
    data = parse_table_file(INPUT_PATH2)   # shape (n_rows, n_cols)
    # Erste Spalte als x, restliche als y1, y2, ...
    x = data[:, 0]
    ys = data[:, 1:]

    # Sortiere nach x (falls nicht sortiert)
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    ys = ys[sort_idx, :]

    print("Gelesene Form:", data.shape)
    print("x (erste 10):", x[:10])
    print("y-Spaltenanzahl:", ys.shape[1])


    # --- Plot ---
    plt.figure(figsize=(8, 5))
    for col in range(ys.shape[1]):
        y = ys[:, col] # hier umwandlung in \omega möglich
        # Ignoriere Spalten, die komplett NaN sind
        if np.all(np.isnan(y)):
            continue
        # Entferne NaN-Reihen für Plot
        valid = ~np.isnan(y)
        label = f"$y_{col+1}$"
        farben = plt.cm.rainbow(np.linspace(0, 1, len(y)))
        plt.bar(x[valid],y[valid], color=farben, width=0.2)
        plt.bar(-x[valid], y[valid], color=farben, width=0.2)
        plt.axhline(0, color='black', linewidth=1)
        plt.xlabel("Spektrallinien in 10 kHz")
        plt.ylabel("Amplitude")
        plt.title("Messspektrum m = 2,4")       
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(PNG_PATH2, dpi=300, bbox_inches="tight")
        print("Plot gespeichert als:", PNG_PATH2)

if __name__ == "__main__":
    print("Lese Datei:", INPUT_PATH3)
    data = parse_table_file(INPUT_PATH3)   # shape (n_rows, n_cols)
    # Erste Spalte als x, restliche als y1, y2, ...
    x = data[:, 0]
    ys = data[:, 1:]

    # Sortiere nach x (falls nicht sortiert)
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    ys = ys[sort_idx, :]

    print("Gelesene Form:", data.shape)
    print("x (erste 10):", x[:10])
    print("y-Spaltenanzahl:", ys.shape[1])


    # --- Plot ---
    plt.figure(figsize=(8, 5))
    for col in range(ys.shape[1]):
        y = ys[:, col] # hier umwandlung in \omega möglich
        # Ignoriere Spalten, die komplett NaN sind
        if np.all(np.isnan(y)):
            continue
        # Entferne NaN-Reihen für Plot
        valid = ~np.isnan(y)
        label = f"$y_{col+1}$"
        farben = plt.cm.rainbow(np.linspace(0, 1, len(y)))
        plt.bar(x[valid],y[valid], color=farben, width=0.2)
        plt.bar(-x[valid], y[valid], color=farben, width=0.2)
        plt.axhline(0, color='black', linewidth=1)
        plt.xlabel("Spektrallinien in 10 kHz")
        plt.ylabel("Amplitude")
        plt.title("Messspektrum m = 10")       
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(PNG_PATH3, dpi=300, bbox_inches="tight")
        print("Plot gespeichert als:", PNG_PATH3)

