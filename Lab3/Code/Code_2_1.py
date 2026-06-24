import numpy as np
import matplotlib.pyplot as plt
def Eingang_amp(a, f): 
    return f/a

dOmega1 = 31.41
dOmega2 = 150.79
dOmega3 = 628.31

steigung_aus_1 = 12.56

print('Eingangsamplitude für m = 0.5' + str(Eingang_amp(steigung_aus_1, dOmega1)))
print('Eingangsamplitude für m = 2.4' + str(Eingang_amp(steigung_aus_1, dOmega2)))
print('Eingangsamplitude für m = 10' + str(Eingang_amp(steigung_aus_1, dOmega3)))

Amp = 1 # Wert der amplitude des Trägersignals 

besselval_05 = np.array([0.938, 0.242, 0.031, 0.003,0,0,0,0,0,0,0 ])
besselval_24 =  np.array([0.003, 0.52, 0.431, 0.198,0.064,0.017,0.004,0,0,0,0])
besselval_100 =  np.array([0.246, 0.043, 0.255, 0.058,0.220 ,0.234,0.014,0.216 ,0.318,0.292, 0.207])

x = np.arange(len(besselval_05))

val_05 = Amp * besselval_05
val_24 = Amp * besselval_24
val_100 = Amp * besselval_100

farben = plt.cm.rainbow(np.linspace(0, 1, len(besselval_05)))

plt.figure(figsize=(10, 6))

# Positive Balken
plt.bar(x, val_05, color=farben, width=0.2)

# Negative Balken (gespiegelte Darstellung)
plt.bar(-x, val_05, color=farben, width=0.2)

plt.axhline(0, color='black', linewidth=1)

plt.xlabel("Spektrallinien in 10 kHz")
plt.ylabel("Amplitude")
plt.title("Spektrallinien (positiv und negativ dargestellt)")


plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Positive Balken
plt.bar(x, val_24, color=farben, width=0.2)

# Negative Balken (gespiegelte Darstellung)
plt.bar(-x, val_24, color=farben, width=0.2)

plt.axhline(0, color='black', linewidth=1)

plt.xlabel("Spektrallinien in 10 kHz")
plt.ylabel("Amplitude")
plt.title("Spektrallinien (positiv und negativ dargestellt)")


plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Positive Balken
plt.bar(x, val_100, color=farben, width=0.2)

# Negative Balken (gespiegelte Darstellung)
plt.bar(-x, val_100, color=farben, width=0.2)

plt.axhline(0, color='black', linewidth=1)

plt.xlabel("Spektrallinien in 10 kHz")
plt.ylabel("Amplitude")
plt.title("Spektrallinien (positiv und negativ dargestellt)")


plt.tight_layout()
plt.show()