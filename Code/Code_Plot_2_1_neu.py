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

with open("./Daten/tabelle_1.txt", "r", encoding="utf-8") as file:
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
        #y2.append(float(parts[2]))

# Plot erzeugen
plt.figure(figsize=(8, 5))

plt.plot(x, y1, marker="o")
#plt.plot(x, y2, marker="s")

plt.xlabel("Eingangsgleichspannung $U_2$ [V]")
plt.ylabel("Ausgangsamplitude $U_A$ [mV]")
plt.title("Statische Modulationskennlinie $U_A = f(U_2)$ ($U_0 =2$V)")
plt.xlim(-12,0)
plt.ylim(0,2150)
plt.vlines(x = -4.5857,ymax=2500, ymin = 0, color = 'red', linestyle = '-', label = 'Bandbreite')
plt.vlines(x = -7.41421,ymax=2500, ymin = 0,color = 'red', linestyle = '-')
plt.axhline(y=786.12, color = 'orange', linestyle = '-', label = 'Hüllkurven-Minima $U_{min}=786$mV')
plt.axhline(y=1315, color = 'green', linestyle = '-', label = 'Hüllkurven-Maxima $U_{max}=1315$mV')
plt.grid(True)
plt.legend()

plt.tight_layout()
#plt.savefig("../Abbildungen/plot.png", dpi=300, bbox_inches="tight")
plt.savefig("../Abbildungen/2/2.1/Modulationskennlinie_V2.png", dpi=300, bbox_inches="tight")

print("x =", x)
print("y1 =", y1)
print("y2 =", y2)

plt.show(block=True)