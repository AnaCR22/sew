# xml2altimetria.py
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class GeneradorSVG:
    """
    Genera archivos SVG con polilíneas, líneas y texto
    """

    def __init__(self, ancho, alto):
        self.raiz = ET.Element("svg", xmlns="http://www.w3.org/2000/svg")
        self.raiz.attrib["width"] = str(ancho)
        self.raiz.attrib["height"] = str(alto)
        self.raiz.attrib["viewBox"] = f"0 0 {ancho} {alto}"

    def addLine(self, x1, y1, x2, y2, stroke, strokeWidth):
        line = ET.SubElement(self.raiz, 'line', x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), stroke=stroke)
        line.set("stroke-width", str(strokeWidth))

    def addPolyline(self, points, stroke, strokeWidth, fill):
        polyline = ET.SubElement(self.raiz, 'polyline', points=points, stroke=stroke, fill=fill)
        polyline.set("stroke-width", str(strokeWidth))

    def addText(self, text, x, y, fontSize=14, style=""):
        attrs = {"x": str(x), "y": str(y), "font-size": str(fontSize)}
        if style:
            attrs["style"] = style
        ET.SubElement(self.raiz,'text', attrs).text = text

    def escribir(self, nombreArchivoSVG):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)

    def ver(self):
        print("\nElemento raiz =", self.raiz.tag)
        for hijo in self.raiz.findall('.//'):
            print("Elemento =", hijo.tag, "Atributos =", hijo.attrib)

class LectorEtapaXML:

    # Namespace del XML
    ns = {"u": "http://www.uniovi.es"}

    def __init__(self, rutaXml):
        self.rutaXml = rutaXml
        self.raiz = None

    def cargar(self):
        try:
            self.raiz = ET.parse(self.rutaXml).getroot()
            return True
        except (IOError, ET.ParseError) as error:
            print(f"Error procesando el archivo XML: {error}")
            return False

    def obtenerNombreEtapa(self):
        return self.raiz.findtext("u:nombreEtapa", default="Etapa", namespaces=self.ns)

    def obtenerLongitudEtapa(self):
        texto = self.raiz.findtext("u:longitudEtapa", namespaces=self.ns)
        return float(texto)

    def obtenerAltitudOrigen(self):
        texto = self.raiz.findtext("u:puntoOrigen/u:punto/u:altitudPunto", namespaces=self.ns)
        return float(texto)

    def obtenerAltitudFinal(self):
        texto = self.raiz.findtext("u:puntoFinal/u:punto/u:altitudPunto", namespaces=self.ns)
        return float(texto)
    
    def extraerDistanciaAltitud(self, elemento):
        distancia = elemento.findtext("u:distancia", namespaces=self.ns)
        altitud = elemento.findtext("u:punto/u:altitudPunto", namespaces=self.ns)
        return float(distancia), float(altitud)

    def obtenerPuntosAnonimos(self):
        anonimos = self.raiz.findall("u:puntosAnonimos/u:puntoAnonimo", self.ns)
        return [self.extraerDistanciaAltitud(a) for a in anonimos]

    def obtenerSprints(self):
        sprints = self.raiz.findall("u:hitos/u:sprintIntermedio", self.ns)
        return [self.extraerDistanciaAltitud(s) for s in sprints]

    def obtenerPuertos(self):
        puertos = self.raiz.findall("u:hitos/u:puertoMontana", self.ns)
        return [self.extraerDistanciaAltitud(p) for p in puertos]

    def obtenerPerfilCompleto(self):
        intermedios = self.obtenerPuntosAnonimos() + self.obtenerSprints() + self.obtenerPuertos()
        intermedios.sort(key=lambda punto: punto[0])

        origen = (0.0, self.obtenerAltitudOrigen())
        final = (self.obtenerLongitudEtapa(), self.obtenerAltitudFinal())

        return [origen] + intermedios + [final]
    
class ConversorAltimetria:
    margen = 50
    ancho = 1000
    alto = 600

    def __init__(self, rutaEntrada, rutaSalida):
        self.rutaEntrada = rutaEntrada
        self.rutaSalida = rutaSalida
        self.minDist = 0.0
        self.maxDist = 0.0
        self.minAlt = 0.0
        self.maxAlt = 0.0

    def escalarX(self, x):
        return self.margen + (x - self.minDist) / (self.maxDist - self.minDist) * (self.ancho - 2 * self.margen)

    def escalarY(self, y):
        return self.margen + (self.maxAlt - y) / (self.maxAlt - self.minAlt) * (self.alto - 2 * self.margen)
    
    def ejecutar(self):
        lector = LectorEtapaXML(self.rutaEntrada)
        if not lector.cargar():
            return

        perfil = lector.obtenerPerfilCompleto()
        distancias = [p[0] for p in perfil]
        altitudes = [p[1] for p in perfil]

        self.minDist = min(distancias)
        self.maxDist = max(distancias)
        self.minAlt = min(altitudes)
        self.maxAlt = max(altitudes)

        svg = GeneradorSVG(self.ancho, self.alto)

        puntos = [f"{self.escalarX(d):.2f},{self.escalarY(a):.2f}" for d, a in perfil]
        points_str = " ".join(puntos)

        svg.addPolyline(points_str, stroke="red", strokeWidth="3", fill="none")
        svg.addLine(self.escalarX(self.minDist), self.escalarY(self.minAlt),
                    self.escalarX(self.maxDist), self.escalarY(self.minAlt),
                    stroke="black", strokeWidth="2")
        svg.addLine(self.escalarX(self.minDist), self.escalarY(self.minAlt),
                    self.escalarX(self.minDist), self.escalarY(self.maxAlt),
                    stroke="black", strokeWidth="2")

        svg.addText("Distancia (km)", self.escalarX((self.minDist + self.maxDist) / 2),
                    self.escalarY(self.minAlt) + 30, fontSize=16, style="text-anchor: middle;")
        svg.addText("Altitud (m)", self.escalarX(self.minDist) - 40,
                    self.escalarY((self.minAlt + self.maxAlt) / 2), fontSize=16,
                    style="writing-mode: tb; glyph-orientation-vertical: 0;")

        svg.addText(f"{int(self.minDist)}", self.escalarX(self.minDist) - 5, self.escalarY(self.minAlt) + 15, fontSize=12)
        svg.addText(f"{int(self.maxDist)}", self.escalarX(self.maxDist) - 10, self.escalarY(self.minAlt) + 15, fontSize=12)
        svg.addText(f"{int(self.minAlt)}", self.escalarX(self.minDist) - 30, self.escalarY(self.minAlt), fontSize=12)
        svg.addText(f"{int(self.maxAlt)}", self.escalarX(self.minDist) - 30, self.escalarY(self.maxAlt), fontSize=12)


        svg.escribir(self.rutaSalida)
        print(f"Creado el archivo: {self.rutaSalida}")

if __name__ == "__main__":
    ConversorAltimetria("etapaEsquema.xml", "altimetria.svg").ejecutar()