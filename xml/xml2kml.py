# xml2kml.py
# -*- coding: utf-8 -*-
"""
Generación de etapa.kml a partir de etapaEsquema.xml
usando expresiones XPath (ElementTree)

@author: Ana Calleja Ramón
Universidad de Oviedo
"""

import xml.etree.ElementTree as ET


class GeneradorKML:

    colorRojo = "ff0000ff"
    colorVerde = "ff00ff00"
    colorAzul = "ffff0000"
    colorAmarillo = "ff00ffff"

    modoAltitud = "clampToGround"

    def __init__(self, nombreDocumento):
        self.raiz = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, "Document")
        ET.SubElement(self.doc, "name").text = nombreDocumento

    def addStyle(self, idEstilo, color):
        estilo = ET.SubElement(self.doc, "Style", id=idEstilo)
        iconoEstilo = ET.SubElement(estilo, "IconStyle")
        ET.SubElement(iconoEstilo, "color").text = color
        ET.SubElement(iconoEstilo, "scale").text = "1.0"

    def addPlacemark(self, nombre, descripcion, lon, lat, alt, idEstilo):
        pm = ET.SubElement(self.doc, "Placemark")
        if nombre is not None:
            ET.SubElement(pm, "name").text = nombre
        ET.SubElement(pm, "description").text = descripcion
        ET.SubElement(pm, "styleUrl").text = f"#{idEstilo}"
        punto = ET.SubElement(pm, "Point")
        ET.SubElement(punto, "coordinates").text = f"{lon},{lat},{alt}"
        ET.SubElement(punto, "altitudeMode").text = self.modoAltitud

    def addLineString(self, nombre, listaCoordenadas, color, ancho):
        pm = ET.SubElement(self.doc, "Placemark")
        ET.SubElement(pm, "name").text = nombre

        estilo = ET.SubElement(pm, "Style")
        linea = ET.SubElement(estilo, "LineStyle")
        ET.SubElement(linea, "color").text = color
        ET.SubElement(linea, "width").text = ancho

        ls = ET.SubElement(pm, "LineString")
        ET.SubElement(ls, "extrude").text = "0"
        ET.SubElement(ls, "tessellate").text = "1"
        ET.SubElement(ls, "altitudeMode").text = self.modoAltitud
        ET.SubElement(ls, "coordinates").text = listaCoordenadas

    def escribir(self, nombreArchivoKML):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding="utf-8", xml_declaration=True)


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

    def extraerCoordenadas(self, elementoPunto):
        lon = elementoPunto.findtext("u:longitudPunto", namespaces=self.ns)
        lat = elementoPunto.findtext("u:latitudPunto", namespaces=self.ns)
        alt = elementoPunto.findtext("u:altitudPunto", namespaces=self.ns)
        return lon, lat, alt

    def obtenerPuntoOrigenFinal(self):
        puntos = []

        origen = self.raiz.find("u:puntoOrigen/u:punto", self.ns)
        if origen is not None:
            lon, lat, alt = self.extraerCoordenadas(origen)
            puntos.append(("Salida", "Punto de salida de la etapa", lon, lat, alt))

        final = self.raiz.find("u:puntoFinal/u:punto", self.ns)
        if final is not None:
            lon, lat, alt = self.extraerCoordenadas(final)
            puntos.append(("Meta", "Punto de meta de la etapa", lon, lat, alt))

        return puntos

    def obtenerPuertos(self):
        puntos = []
        puertos = self.raiz.findall("u:hitos/u:puertoMontana", self.ns)

        for puerto in puertos:
            categoria = puerto.get("categoria")
            bonificado = puerto.get("bonificado")
            elementoPunto = puerto.find("u:punto", self.ns)
            lon, lat, alt = self.extraerCoordenadas(elementoPunto)
            distancia = puerto.findtext("u:distancia", namespaces=self.ns)
            descripcion = f"Puerto de categoría {categoria} (bonificado: {bonificado})"
            puntos.append((f"Puerto {categoria}", descripcion, lon, lat, alt, float(distancia)))

        return puntos

    def obtenerSprints(self):
        puntos = []
        sprints = self.raiz.findall("u:hitos/u:sprintIntermedio", self.ns)

        for sprint in sprints:
            bonificado = sprint.get("bonificado")
            elementoPunto = sprint.find("u:punto", self.ns)
            lon, lat, alt = self.extraerCoordenadas(elementoPunto)
            distancia = sprint.findtext("u:distancia", namespaces=self.ns)
            descripcion = f"Sprint intermedio (bonificado: {bonificado})"
            puntos.append(("Sprint intermedio", descripcion, lon, lat, alt, float(distancia)))

        return puntos

    def obtenerPuntosAnonimos(self):
        puntos = []
        anonimos = self.raiz.findall("u:puntosAnonimos/u:puntoAnonimo", self.ns)

        for anonimo in anonimos:
            nombre = anonimo.findtext("u:nombrePunto", default=None, namespaces=self.ns)
            distancia = anonimo.findtext("u:distancia", namespaces=self.ns)
            elementoPunto = anonimo.find("u:punto", self.ns)
            lon, lat, alt = self.extraerCoordenadas(elementoPunto)
            descripcion = f"Distancia desde el origen: {distancia} km"
            puntos.append((nombre, descripcion, lon, lat, alt, float(distancia)))

        return puntos


class ConversorKML:

    def __init__(self, rutaEntrada, rutaSalida):
        self.rutaEntrada = rutaEntrada
        self.rutaSalida = rutaSalida

    def construirPuntosLinea(self, lector):
            origen, final = lector.obtenerPuntoOrigenFinal()

            intermedios = lector.obtenerPuntosAnonimos() + lector.obtenerSprints() + lector.obtenerPuertos()
            intermedios.sort(key=lambda punto: punto[5])

            intermedios = [p[:5] for p in intermedios]

            return [origen] + intermedios + [final]
    
    def construirListaCoordenadas(self, puntos):
        return "\n".join(f"{lon},{lat},{alt}" for _, _, lon, lat, alt in puntos)

    def ejecutar(self):
        lector = LectorEtapaXML(self.rutaEntrada)
        if not lector.cargar():
            return

        nombreEtapa = lector.obtenerNombreEtapa()
        kml = GeneradorKML(nombreEtapa)

        kml.addStyle("estiloRojo", GeneradorKML.colorRojo)
        kml.addStyle("estiloVerde", GeneradorKML.colorVerde)
        kml.addStyle("estiloAzul", GeneradorKML.colorAzul)
        kml.addStyle("estiloAmarillo", GeneradorKML.colorAmarillo)

        puntosLinea = self.construirPuntosLinea(lector)

        kml.addLineString(
            f"Recorrido {nombreEtapa}",
            self.construirListaCoordenadas(puntosLinea),
            GeneradorKML.colorRojo,
            "4",
        )

        for nombre, descripcion, lon, lat, alt, _ in lector.obtenerPuntosAnonimos():
            kml.addPlacemark(nombre, descripcion, lon, lat, alt, "estiloAmarillo")

        for nombre, descripcion, lon, lat, alt, _ in lector.obtenerSprints():
            kml.addPlacemark(nombre, descripcion, lon, lat, alt, "estiloAzul")

        for nombre, descripcion, lon, lat, alt, _ in lector.obtenerPuertos():
            kml.addPlacemark(nombre, descripcion, lon, lat, alt, "estiloVerde")

        for nombre, descripcion, lon, lat, alt in lector.obtenerPuntoOrigenFinal():
            kml.addPlacemark(nombre, descripcion, lon, lat, alt, "estiloRojo")

        kml.escribir(self.rutaSalida)
        print(f"Creado el archivo: {self.rutaSalida}")


if __name__ == "__main__":
    ConversorKML("etapaEsquema.xml", "etapa.kml").ejecutar()
