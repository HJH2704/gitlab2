import numpy as np
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime

def Eingang_amp(a, f): 
    return f/a


OUT_DIR = "../Abbildungen/2/2.1" 
os.makedirs(OUT_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PNG_PATH = os.path.join(OUT_DIR, f"Frequenzspektren_{TIMESTAMP}.pdf")


dOmega1 = 31.41
dOmega2 = 150.79
dOmega3 = 628.31

steigung_aus_1 = 12.56

print('Eingangsamplitude für m = 0.5' + str(Eingang_amp(steigung_aus_1, dOmega1)))
print('Eingangsamplitude für m = 2.4' + str(Eingang_amp(steigung_aus_1, dOmega2)))
print('Eingangsamplitude für m = 10' + str(Eingang_amp(steigung_aus_1, dOmega3)))

Amp = 1 # Wert der amplitude des Trägersignals 

besselval_05 = np.array([0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0002, 0.003, 0.031, 0.242,
    0.938, 0.242, 0.031, 0.003, 0.0002,
    0.0, 0.0, 0.0, 0.0, 0.0,
    0.0])
besselval_24 =  np.array([0.0, 0.0, 0.0, 0.001, 0.004,
    0.017, 0.064, 0.198, 0.431, 0.520,
    0.003, 0.520, 0.431, 0.198, 0.064,
    0.017, 0.004, 0.001, 0.0, 0.0,
    0.0])
besselval_100 =  np.array([ 0.207, 0.292, 0.318, 0.216, 0.014,
    0.234, 0.220, 0.058, 0.255, 0.043,
    0.246, 0.043, 0.255, 0.058, 0.220,
    0.234, 0.014, 0.216, 0.318, 0.292,
    0.207])

import numpy as np

x = np.array([
    2.900, 2.910, 2.920, 2.930, 2.940,
    2.950, 2.960, 2.970, 2.980, 2.990,
    3.000, 3.010, 3.020, 3.030, 3.040,
    3.050, 3.060, 3.070, 3.080, 3.090,
    3.100
])


val_05 = Amp * besselval_05
val_24 = Amp * besselval_24
val_100 = Amp * besselval_100

base_colors = plt.cm.tab20(np.linspace(0, 1, 11))
farben = np.vstack([base_colors, base_colors[:-1][::-1]])

fig, (ax1, ax2, ax3 ) = plt.subplots(3,1, figsize = (8,10))
plt.grid()
# Positive Balken
ax1.bar(x, val_05, color=farben, width=0.002)
# Negative Balken (gespiegelte Darstellung)
#ax1.bar(-x, val_05, color=farben, width=0.2)
ax1.axhline(0, color='black', linewidth=1)
ax1.set_xlabel("Spektrallinien in MHz")
ax1.set_ylabel("Amplitude")
ax1.set_title("Spektrum m = 0,5")
ax1.grid(True)
# Positive Balken
ax2.bar(x, val_24, color=farben, width=0.002)
# Negative Balken (gespiegelte Darstellung)
#ax2.bar(-x, val_24, color=farben, width=0.2)
ax2.axhline(0, color='black', linewidth=1)
ax2.set_xlabel("Spektrallinien in MHz")
ax2.set_ylabel("Amplitude")
ax2.set_title("Spektrum m = 2,4")
ax2.grid(True)
# Positive Balken
ax3.bar(x, val_100, color=farben, width=0.002)
# Negative Balken (gespiegelte Darstellung)
#ax3.bar(-x, val_100, color=farben, width=0.2)
ax3.axhline(0, color='black', linewidth=1)
ax3.set_xlabel("Spektrallinien in MHz")
ax3.set_ylabel("Amplitude")
ax3.set_title("Spektrum m = 10")
ax3.grid(True)
plt.subplots_adjust(hspace=0.45)
plt.savefig(PNG_PATH, dpi=300)
plt.show()
print("Plot gespeichert als:", PNG_PATH)