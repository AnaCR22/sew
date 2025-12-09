import xml.etree.ElementTree as ET

NS = {"u": "http://www.uniovi.es"}  # namespace de circuitoEsquema.xml


def leer_distancias_y_alturas(xmlfile):
    """Lee circuitoEsquema.xml y devuelve listas de distancias acumuladas y altitudes."""
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    distancias = []
    altitudes = []

    # 1. Punto de origen (distancia 0)
    origen = root.findall(".//u:puntoOrigen/u:punto", NS)
    if not origen:
        raise ValueError("No se encontró el punto de origen en el XML.")

    p0 = origen[0]
    alt0 = float(p0.get("altitud"))
    distancias.append(0.0)
    altitudes.append(alt0)

    # 2. Tramos: acumulamos distancia y tomamos altitud de cada punto
    tramos = root.findall(".//u:tramos/u:tramo", NS)
    distancia_acumulada = 0.0

    for tramo in tramos:
        d = float(tramo.get("distancia"))
        distancia_acumulada += d

        punto = tramo.find("u:punto", NS)
        if punto is None:
            continue

        alt = float(punto.get("altitud"))

        distancias.append(distancia_acumulada)
        altitudes.append(alt)

    return distancias, altitudes


def escalar_a_svg(distancias, altitudes, width, height, margin):
    """Devuelve una lista de puntos (x,y) escalados al sistema de coordenadas SVG."""
    max_dist = max(distancias) if distancias else 1.0
    min_alt = min(altitudes) if altitudes else 0.0
    max_alt = max(altitudes) if altitudes else 1.0

    # Evitar división por cero
    if max_alt == min_alt:
        max_alt = min_alt + 1.0

    svg_points = []

    for d, a in zip(distancias, altitudes):
        # Escalar distancia en X
        x = margin + (d / max_dist) * (width - 2 * margin)
        # Escalar altitud en Y (invertido, porque en SVG y aumenta hacia abajo)
        y = height - margin - ((a - min_alt) / (max_alt - min_alt)) * (height - 2 * margin)
        svg_points.append((x, y))

    return svg_points


def generar_svg(distancias, altitudes, outfile):
    """Genera el archivo altimetria.svg con un perfil de altitud vs distancia."""
    width = 800
    height = 400
    margin = 50

    puntos_svg = escalar_a_svg(distancias, altitudes, width, height, margin)

    with open(outfile, "w", encoding="utf-8") as f:
        # Prólogo SVG
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write(f'width="{width}" height="{height}" ')
        f.write(f'viewBox="0 0 {width} {height}">\n')

        # Fondo blanco
        f.write('  <rect x="0" y="0" width="100%" height="100%" fill="white"/>\n')

        # Ejes
        eje_x_y = height - margin
        eje_y_x = margin

        # Eje X (distancia)
        f.write(f'  <line x1="{margin}" y1="{eje_x_y}" x2="{width - margin}" y2="{eje_x_y}" ')
        f.write('stroke="black" stroke-width="1"/>\n')

        # Eje Y (altitud)
        f.write(f'  <line x1="{eje_y_x}" y1="{margin}" x2="{eje_y_x}" y2="{height - margin}" ')
        f.write('stroke="black" stroke-width="1"/>\n')

        # Etiquetas de ejes
        f.write(f'  <text x="{width/2}" y="{height - margin/3}" text-anchor="middle" font-size="14">Distancia (m)</text>\n')
        f.write(f'  <text x="{margin/3}" y="{height/2}" text-anchor="middle" font-size="14" transform="rotate(-90 {margin/3},{height/2})">Altitud (m)</text>\n')

        # Construir la polilínea de altimetría
        if puntos_svg:
            puntos_attr = " ".join(f"{x:.2f},{y:.2f}" for x, y in puntos_svg)

            # Opcional: cerrar polilínea hacia el "suelo" para rellenar
            x_last, _ = puntos_svg[-1]
            x_first, _ = puntos_svg[0]
            suelo_y = eje_x_y

            puntos_attr_suelo = puntos_attr + f" {x_last:.2f},{suelo_y:.2f} {x_first:.2f},{suelo_y:.2f}"

            # Relleno bajo la curva
            f.write(f'  <polyline points="{puntos_attr_suelo}" fill="lightblue" stroke="blue" stroke-width="2" fill-opacity="0.4"/>\n')

            # Línea de perfil (solo la curva, sin cierre)
            f.write(f'  <polyline points="{puntos_attr}" fill="none" stroke="blue" stroke-width="2"/>\n')

        # Cierre SVG
        f.write('</svg>\n')


if __name__ == "__main__":
    dist, alt = leer_distancias_y_alturas("circuitoEsquema.xml")
    generar_svg(dist, alt, "altimetria.svg")
    print("Archivo altimetria.svg generado correctamente.")
