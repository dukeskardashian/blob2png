from PIL import Image
from io import BytesIO
import mysql.connector

# Verbindung zur Datenbank herstellen
#blob zu png umwandeln
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database=""
)

# SQL-Abfrage zum Abrufen der Blob-Daten aus der Tabelle "bilder"
cursor = mydb.cursor()
sql = "SELECT police, nonpolice, mix, v1 FROM bilder"
cursor.execute(sql)
results = cursor.fetchall()

# Durch die Ergebnisse iterieren, Bilder konvertieren und als PNG in der Datenbank speichern
update_sql = "UPDATE bilder SET police_png = %s, nonpolice_png = %s, mix_png = %s, v1_png = %s WHERE id = %s"
for result in results:
    id = result[0]
    police_data = result[1] if len(result) > 1 else None
    nonpolice_data = result[2] if len(result) > 2 else None
    mix_data = result[3] if len(result) > 3 else None

    # Prüfen, ob die Spaltenwerte vorhanden sind
    if police_data is None or nonpolice_data is None or mix_data is None:
        continue

    # Blob-Daten als PIL-Image öffnen
    police_image = Image.open(BytesIO(police_data))
    nonpolice_image = Image.open(BytesIO(nonpolice_data))
    mix_image = Image.open(BytesIO(mix_data))

    # Bilder als PNG konvertieren und als Blob-Daten aktualisieren
    police_buffer = BytesIO()
    nonpolice_buffer = BytesIO()
    mix_buffer = BytesIO()

    police_image.save(police_buffer, format='PNG')
    nonpolice_image.save(nonpolice_buffer, format='PNG')
    mix_image.save(mix_buffer, format='PNG')

    # Blob-Daten abrufen
    police_png_data = police_buffer.getvalue()
    nonpolice_png_data = nonpolice_buffer.getvalue()
    mix_png_data = mix_buffer.getvalue()

    # SQL-Abfrage zum Aktualisieren der Datensätze mit den PNG-Bilddaten
    update_values = (police_png_data, nonpolice_png_data, mix_png_data, id)
    cursor.execute(update_sql, update_values)
    mydb.commit()

print("Bilder erfolgreich konvertiert und in der Datenbank aktualisiert.")

# Verbindung zur Datenbank schließen
cursor.close()
mydb.close()
