import numpy as np
import matplotlib.pyplot as plt

# Parameter
fc = 200e3          # Grenzfrequenz [Hz]
C = 15.9e-9         # Kapazität [F]
R = 1 / (2 * np.pi * fc * C)

print(f"R = {R:.2f} Ohm")

# Frequenzachse
f = np.logspace(3, 7, 1000)      # 1 kHz bis 10 MHz
w = 2 * np.pi * f

# Übertragungsfunktion RC-Tiefpass
H = (1j * w * R * C) / (1 + 1j * w * R * C)

# Betrag und Phase
A = 20 * np.log10(np.abs(H))
phi = np.angle(H, deg=True)

# ----------------------------
# Bode-Diagramm
# ----------------------------
plt.figure(figsize=(8, 6))

# Betrag
plt.semilogx(f, A, linewidth=2)
plt.axvline(fc, color='red', linestyle='--', label=f'$f_g={fc/1e3:.0f}$ kHz')
plt.axvline(10000, color='green', linestyle='--', label=f'10 kHz')
plt.axvline(20000, color='green', linestyle='--', label=f'20 kHz')
plt.fill_betweenx((-45, 5), 10000, 20000, color='green', alpha=.5)
plt.grid(True, which='both')
plt.ylim(-45,5)
plt.ylabel("Verstärkung [dB]")
plt.xlabel("Frequenz in Hz")
plt.title("Betragsfrequenzgang des RC-Hochpass")
plt.legend()
plt.show()