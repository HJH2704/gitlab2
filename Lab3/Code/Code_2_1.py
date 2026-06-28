import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# =========================
# OUTPUT
# =========================
OUT_DIR = "../Abbildungen/2/combined"
os.makedirs(OUT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUT_PATH = os.path.join(OUT_DIR, f"Theorie_Bessel_{TIMESTAMP}.pdf")


# =========================
# SIDE BAND LABELS
# =========================
def create_sideband_labels(x, carrier_label="Träger"):
    n = len(x)
    if n % 2 == 0:
        raise ValueError("x muss ungerade Länge haben")

    c = n // 2
    labels = []

    for i in range(n):
        if i == c:
            labels.append(carrier_label)
        else:
            labels.append(f"{abs(i-c)}.\nSF")

    return labels


# =========================
# SYMMETRISCHES WINDOW (RICHTIG!)
# =========================
def window_symmetric(x, y, sidebands):
    """
    sidebands = Anzahl pro Seite
    """
    c = len(y) // 2
    x_cut = x[c - sidebands : c + sidebands + 1]
    y_cut = y[c - sidebands : c + sidebands + 1]
    return x_cut, y_cut


# =========================
# BESSEL DATEN
# =========================
Amp = 1

besselval_05 = np.array([
    0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0002, 0.003, 0.031, 0.242,
    0.938, 0.242, 0.031, 0.003, 0.0002,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
])

besselval_24 = np.array([
    0.0, 0.0, 0.0, 0.001, 0.004,
    0.017, 0.064, 0.198, 0.431, 0.520,
    0.003, 0.520, 0.431, 0.198, 0.064,
    0.017, 0.004, 0.001, 0.0, 0.0, 0.0
])

besselval_100 = np.array([
    0.207, 0.292, 0.318, 0.216, 0.014,
    0.234, 0.220, 0.058, 0.255, 0.043,
    0.246, 0.043, 0.255, 0.058, 0.220,
    0.234, 0.014, 0.216, 0.318, 0.292,
    0.207
])


# =========================
# X ACHSE
# =========================
x = np.array([
     2.400, 2.410, 2.420, 2.430,
    2.440, 2.450, 2.460, 2.470, 2.480,
    2.490, 2.500, 2.510, 2.520, 2.530,
    2.540, 2.550, 2.560, 2.570, 2.580,
    2.590, 2.600
])


# =========================
# FARBEN (WICHTIG: FIXE SYMMETRIE)
# =========================
base_colors = plt.cm.tab20(np.linspace(0, 1, 11))
farben = np.vstack([base_colors, base_colors[:-1][::-1]])  # symmetrisch


# =========================
# PLOT FUNKTION
# =========================
def plot_bessel(ax, x, y, title):
    y = Amp * y

    ax.bar(x, y, color=farben, width=0.002)
    ax.axhline(0, color='black', linewidth=1)

    ax.set_title(title)
    ax.set_xlabel("Spektrallinien in MHz")
    ax.set_ylabel("Amplitude in V")
    ax.set_ylim(0,1)
    ax.grid(True)

    secax = ax.secondary_xaxis('top')
    secax.set_xticks(x)
    secax.set_xticklabels(create_sideband_labels(x))
    secax.tick_params(length=0)


# =========================
# FIGURE
# =========================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 11))

plot_bessel(ax1, x, besselval_05, "Theorie m = 0.5")
plot_bessel(ax2, x, besselval_24, "Theorie m = 2.4")
plot_bessel(ax3,x, besselval_100, "Theorie m = 10")

# =========================
# m = 10 KORREKT: 13 LINKS + TRÄGER + 13 RECHTS
# =========================
x_m10, y_m10 = window_symmetric(x, besselval_100, 13)

#plot_bessel(ax3, x_m10, y_m10,
#            "Theorie m = 10 (13 Seitenfrequenzen pro Seite)")


plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
plt.show()

print("Plot gespeichert als:", OUT_PATH)