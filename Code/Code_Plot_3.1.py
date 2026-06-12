import matplotlib.pyplot as plt
import os
import matplotlib
from datetime import datetime

# Daten einlesen
x = []
y = []

with open("./Daten/tabelle_3_1.txt", "r", encoding="utf-8") as file:
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

plt.figure(figsize=(10, 5))
plt.xlabel("Frequenz $f$ [kHz]")
plt.ylabel("Ausgangsspannung $U_A$ [mV]")
plt.title("Frequenzgang $U_a(f_0)$")
plt.plot(x, y, marker="o")
plt.axhline(y=721.847, color = 'green', label = '3dB Grenze')
plt.xlim(400,600)
plt.ylim(0,1100)
plt.vlines(x=462.18, ymin = 0, ymax =1200, color = 'orange', label = 'Grenzfrequenzen')
plt.vlines(x=497.12, ymin = 0, ymax =1200, color = 'orange')
plt.vlines(x=480, ymin = 0, ymax =1200, color = 'red', label = 'Mittenfrequenz')
plt.grid(which= 'both')
plt.legend()

plt.savefig("../Abbildungen/3/3.1/Frequenzgang.png", dpi=300, bbox_inches="tight")

plt.show(block=True)