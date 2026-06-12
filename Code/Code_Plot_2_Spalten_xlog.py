import matplotlib.pyplot as plt
import os
import matplotlib
from datetime import datetime
import numpy as np


# Daten einlesen
x = []
y = []


with open("./Daten/tabelle_3_2.txt", "r", encoding="utf-8") as file:
    for line in file:

        # LaTeX-Reste entfernen
        line = line.replace("\\\\ \\hline", "").strip()

        # Zeile aufteilen
        parts = [p.strip() for p in line.split("&")]

        # Nur gültige Zeilen verarbeiten
        if len(parts) != 2:
            continue

        x.append(float(parts[0]))
        y.append(float(parts[1]))
        
plt.figure(figsize=(8, 5))
xlog= 20*np.log10(x)
plt.plot(x, y, marker="o", label="Spalte 2")
plt.xlabel("Spalte 1")
plt.ylabel("Wert")
plt.title("Plot der Messdaten")

plt.grid(True)
plt.legend()