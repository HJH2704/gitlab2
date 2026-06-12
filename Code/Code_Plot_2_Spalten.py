import matplotlib.pyplot as plt
import os
import matplotlib
from datetime import datetime

# Daten einlesen
x = []
y = []

with open("tabelle.txt", "r", encoding="utf-8") as file:
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

plt.plot(x, y, marker="o", label="Spalte 2")
plt.axhline(y=721.847)
plt.vlines(x=462.18, ymin = 0, ymax =1200)
plt.vlines(x=497.12, ymin = 0, ymax =1200)
plt.vlines(x=480, ymin = 0, ymax =1200, color = 'red')
plt.grid(which= 'both')