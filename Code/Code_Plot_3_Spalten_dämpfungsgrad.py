import matplotlib.pyplot as plt
import os
import matplotlib
from datetime import datetime

dateiname = datetime.now().strftime("../Abbildungen/plot_%Y%m%d_%H%M%S.png")
matplotlib.use('QtAgg')
print("Skript gestartet")
print("Arbeitsverzeichnis:", os.getcwd())


# Daten einlesen
x = []
y1 = []
y2 = []

with open("tabelle.txt", "r", encoding="utf-8") as file:
    for line in file:

        # LaTeX-Reste entfernen
        line = line.replace("\\\\ \\hline", "").strip()

        # Zeile aufteilen
        parts = [p.strip() for p in line.split("&")]

        # Nur gültige Zeilen verarbeiten
        if len(parts) != 3:
            continue

        x.append(float(parts[0]))
        y1.append(float(parts[1]))
        y2.append(float(parts[2]))
M=[]
for i in range(len(y1)):
    U = (y2[i]-y1[i])/(y2[i]+y1[i])
    M.append(U)
    
# Plot erzeugen
plt.figure(figsize=(8, 5))
#(max-min)/(max+min)
plt.loglog(x, M, marker="o", label="Spalte 2")
#plt.plot(x, y2, marker="s", label="Spalte 3")

plt.xlabel("Spalte 1")
plt.ylabel("Wert")
plt.title("Plot der Messdaten")

plt.grid(True)
plt.legend()

plt.tight_layout()
#plt.savefig("../Abbildungen/plot.png", dpi=300, bbox_inches="tight")
plt.savefig(dateiname, dpi=300, bbox_inches="tight")

#print("x =", x)
#print("y1 =", y1)
#print("y2 =", y2)

plt.show(block=True)