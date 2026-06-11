# Daten einlesen
x = []
y = []

with open("tabelle.txt", "r", encoding="utf-8") as file:
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