import matplotlib.pyplot as plt
import os
import matplotlib
from datetime import datetime
import numpy as np

dateiname = datetime.now().strftime("../Abbildungen/plot_%Y%m%d_%H%M%S.png")
matplotlib.use('QtAgg')
print("Skript gestartet")
print("Arbeitsverzeichnis:", os.getcwd())


# Daten einlesen
x = []
y1 = []
y2 = []

with open("./Daten/tabelle_3_2.txt", "r", encoding="utf-8") as file:
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
plt.loglog(x, M, marker="o", label="")


plt.xlabel("Frequenz $f$ [kHz]")
plt.ylabel("Modulationsgrad $m$")
plt.title("Modulationskennlinie")
plt.axhline(y=.7, color = 'orange', linestyle = '-', label = '-3dB Grenze')
plt.vlines(x = 45.16,ymax=2, ymin = 0, color = 'red', linestyle = '-', label = 'Untere Grenzfrequenz (45Hz)')
plt.vlines(x = 17394,ymax=2, ymin = 0,color = 'green', linestyle = '-', label = 'Obere Grenzfrequenz (17,4kHz)')
plt.xlim(10,40000)
plt.ylim(0,1)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("../Abbildungen/3/3.2/Modulationskennlinie.png", dpi=300, bbox_inches="tight")

#print("x =", x)
#print("y1 =", y1)
#print("y2 =", y2)
print(np.round(M,2))
plt.show(block=True)
