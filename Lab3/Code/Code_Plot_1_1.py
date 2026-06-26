#!/usr/bin/env python3
"""
Liest eine LaTeX-Tabelle (Zeilen mit '&' und evtl. '\\\\ \\hline'), wandelt
die Werte in numpy-Arrays um, speichert diese und erzeugt einen Plot.

Benötigte Pakete:
- numpy
- matplotlib
- scipy (optional)

Installation:
pip install numpy matplotlib scipy
"""

import os
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Optional: falls du scipy-Funktionen nutzen willst (z.B. glätten/interpolieren)
# from scipy import interpolate, signal

# --- Konfiguration ---
INPUT_PATH = "./Data/tabelle_1.txt"       # Eingabedatei mit LaTeX-Tabellenzeilen
OUT_DIR = "../Abbildungen/1/1.1"           # Ausgabeordner
os.makedirs(OUT_DIR, exist_ok=True)

ymaxval = 4
Xbottom = 1.0
Xtop = 1.5
clip_front = 4  # Anzahl der ersten Werte, die entfernt werden sollen
clip_back = 4  # Anzahl der letzten Werte, die entfernt werden sollen
mittelwert = 12 #index des mittlerster Wert aus linerarem Bereich

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PNG_PATH = os.path.join(OUT_DIR, f"Modulationskennlinie_{TIMESTAMP}.pdf")


# --- Hilfsfunktionen ---
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


# --- Hauptprogramm ---
if __name__ == "__main__":
    print("Lese Datei:", INPUT_PATH)
    data = parse_table_file(INPUT_PATH)   # shape (n_rows, n_cols)
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
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'd', '^', 'v']
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

 

    for col in range(ys.shape[1]):
        y =  ys[:, col]
        # Ignoriere Spalten, die komplett NaN sind
        if np.all(np.isnan(y)):
            continue
        # Entferne NaN-Reihen für Plot
        valid = ~np.isnan(y)
        label = f"$y_{col+1}$"
        style = linestyles[col % len(linestyles)]
        marker = markers[col % len(markers)]
        color = colors[col % len(colors)]
        x_neu = x[clip_front:len(x)-clip_back]
        y_neu = y[clip_front:len(y)-clip_back]
        coeffs= np.polyfit(x_neu,y_neu,1)
        a_s = coeffs[0]
        b = coeffs[1]
        plt.plot(x[valid], y[valid], linestyle=style, marker=marker, color=color, label='Geradengleichung: f(x) = '+ str(a_s)+ ' $\cdot$ x + '+ str(b))

    plt.xlabel("Eingangsgleichspannung $U_e$ [V]")
    plt.ylabel("Momentfrequenz $\omega$ [rad/s]")
    plt.title("Statische Modulationskennlinie $\omega = f(U_e)$ ")
    plt.xlim(-4.5, 4.5)
    plt.ylim(1.5, ymaxval)
    plt.vlines(x = Xbottom,ymax=ymaxval, ymin = 0, color = 'red', linestyle = '--', label = 'Unterer Grenzwert $U_{e,min}= '+ str(Xbottom)+'$V')
    plt.vlines(x = Xtop,ymax=ymaxval, ymin = 0,color = 'red', linestyle = '-.', label = 'Oberer Grenzwert $U_{e,max}= '+ str(Xtop)+'$V')
    #plt.axhline(y=896.31, color = 'orange', linestyle = '-', label = 'Hüllkurven-Minima $U_{min}=896$mV')
    #plt.axhline(y=1423, color = 'green', linestyle = '-', label = 'Hüllkurven-Maxima $U_{max}=1423$mV')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PNG_PATH, dpi=300, bbox_inches="tight")
    print("Plot gespeichert als:", PNG_PATH)
  
# Kürzen der Arrays

