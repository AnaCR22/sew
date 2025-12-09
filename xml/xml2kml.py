import xml.etree.ElementTree as ET

# Namespace del XML
NS = "{http://www.uniovi.es}"

def leer_coordenadas(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    coordenadas = []

    # 1. Obtener punto origen (uso obligatorio de XPath)
    origen = root.findall(f".//{NS}puntoOrigen/{NS}punto")
    for p in origen:
        lon = p.get("longitud")
        lat = p.get("latitud")
        alt = p.get("altitud")
        coordenadas.append(f"{lon},{lat},{alt}")

    # 2. Obtener los puntos de los tramos (XPath obligatorio)
    tramos = root.findall(f".//{NS}tramos/{NS}tramo/{NS}punto")
    for p in tramos:
        lon = p.get("longitud")
        lat = p.get("latitud")
        alt = p.get("altitud")
        coordenadas.append(f"{lon},{lat},{alt}")

    return coordenadas


def generar_kml(coordenadas, outfile):
    with open(outfile, "w", encoding="utf-8") as f:
        # 1. ENCABEZADO
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        f.write('    <name>Circuito MotoGP</name>\n')

        # 2. MARCADOR DEL PUNTO ORIGEN
        origen = coordenadas[0]
        f.write('    <Placemark>\n')
        f.write('      <name>Punto Origen</name>\n')
        f.write('      <Point>\n')
        f.write(f'        <coordinates>{origen}</coordinates>\n')
        f.write('      </Point>\n')
        f.write('    </Placemark>\n')

        # 3. POLILÍNEA DEL CIRCUITO
        f.write('    <Placemark>\n')
        f.write('      <name>Recorrido del Circuito</name>\n')
        f.write('      <LineString>\n')
        f.write('        <tessellate>1</tessellate>\n')
        f.write('        <coordinates>\n')

        for c in coordenadas:
            f.write(f'          {c}\n')

        f.write('        </coordinates>\n')
        f.write('      </LineString>\n')
        f.write('    </Placemark>\n')

        # 4. CIERRE DEL DOCUMENTO
        f.write('  </Document>\n')
        f.write('</kml>')


# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
if __name__ == "__main__":
    coords = leer_coordenadas("circuitoEsquema.xml")
    generar_kml(coords, "circuito.kml")
    print("Archivo circuito.kml generado correctamente.")
