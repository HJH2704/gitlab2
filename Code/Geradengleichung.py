x = [-11.0, -10.5, -10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0, -6.5, -6.0, -5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0]
y1 = [110.0, 203.0, 297.0, 392.0, 486.0, 580.0, 675.0, 770.0, 864.0, 958.0, 1051.0, 1145.0, 1238.0, 1331.0, 1423.0, 1517.0, 1609.0, 1700.0, 1791.0, 1882.0, 1973.0, 2065.0, 1852.0]




steigungen = []

x_min = -10
x_max = -2

# Punkte im gewünschten Bereich auswählen
x_bereich = []
y_bereich = []

for xi, yi in zip(x, y1):
    if x_min <= xi <= x_max:
        x_bereich.append(xi)
        y_bereich.append(yi)

# durchschnittliche Steigung zwischen Anfangs- und Endpunkt
m = (y_bereich[-1] - y_bereich[0]) / (x_bereich[-1] - x_bereich[0])

# Achsenabschnitt berechnen: y = m*x + b  ->  b = y - m*x
b = y_bereich[0] - m * x_bereich[0]

print("Steigung m:", m)
print("Achsenabschnitt b:", b)
print(f"Geradengleichung: y = {m:.3f} * x + {b:.3f}")



x_k = -6-1.414
x_m = -6+1.414


y_x = m*x_k + b
y_m = m*x_m + b



print("Wert",y_x)

Modulationswert = (y_m-y_x)/(y_m+y_x)