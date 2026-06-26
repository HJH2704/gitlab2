import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv

# Definitionsbereich
m = np.linspace(0, 20, 2000)

# Abbildungsstil
plt.rcParams.update({
    "font.size": 14,
    "mathtext.fontset": "stix",
    "font.family": "STIXGeneral"
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), dpi=150)

# -----------------------------
# Linkes Diagramm: ν = 0 ... 4
# -----------------------------
for nu in range(5):
    ax1.plot(m, jv(nu, m), lw=2)

ax1.set_xlim(0, 20)
ax1.set_ylim(-0.5, 1.0)
ax1.set_xlabel(r"$m$")
ax1.set_ylabel(r"$J_\nu(m)$")
ax1.grid(True, alpha=0.4)

# Beschriftungen ähnlich der Vorlage
ax1.text(2.1, 0.88, r"$\nu=0$")
ax1.text(3.2, 0.67, "1")
ax1.text(4.4, 0.60, "2")
ax1.text(5.6, 0.52, "3")
ax1.text(6.8, 0.50, "4")

# -----------------------------
# Rechtes Diagramm: ν = 5 ... 10
# -----------------------------
for nu in range(5, 11):
    ax2.plot(m, jv(nu, m), lw=2)

ax2.set_xlim(0, 20)
ax2.set_ylim(-0.4, 0.6)
ax2.set_xlabel(r"$m$")
ax2.set_ylabel(r"$J_\nu(m)$")
ax2.grid(True, alpha=0.4)

ax2.text(7.5, 0.50, r"$\nu=5$")
ax2.text(9.0, 0.42, "6")
ax2.text(10.1, 0.40, "7")
ax2.text(11.1, 0.38, "8")
ax2.text(12.2, 0.36, "9")
ax2.text(13.2, 0.34, "10")

plt.tight_layout()
plt.show()