import xml.etree.ElementTree as ET

NS = {"u": "http://www.uniovi.es"}  # namespace del XML


class Html:
    def __init__(self, filename):
        self.f = open(filename, "w", encoding="utf-8")

    def writeln(self, text=""):
        self.f.write(text + "\n")

    def start_tag(self, tag, attrs=None):
        if attrs is None:
            attrs = {}
        attr_text = "".join(f' {k}="{v}"' for k, v in attrs.items())
        self.writeln(f"<{tag}{attr_text}>")

    def end_tag(self, tag):
        self.writeln(f"</{tag}>")

    def full_tag(self, tag, content, attrs=None):
        if attrs is None:
            attrs = {}
        attr_text = "".join(f' {k}="{v}"' for k, v in attrs.items())
        self.writeln(f"<{tag}{attr_text}>{content}</{tag}>")

    def close(self):
        self.f.close()


def generar_html(xmlfile, htmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    # Atributos del circuito
    nombre = root.get("nombre", "Circuito")
    localidad = root.get("localidad", "")
    pais = root.get("pais", "")

    # Dimensiones
    dim = root.find("u:dimensiones", NS)
    longitud = dim.get("longitud") if dim is not None else ""
    anchura = dim.get("anchura") if dim is not None else ""
    unidad = dim.get("unidad") if dim is not None else ""

    # Carrera
    carrera = root.find("u:carrera", NS)
    fecha = carrera.get("fecha") if carrera is not None else ""
    hora = carrera.get("horaInicio") if carrera is not None else ""
    vueltas = carrera.get("vueltas") if carrera is not None else ""

    # Patrocinador
    patrocinador_elem = root.find("u:patrocinador", NS)
    patrocinador = patrocinador_elem.text.strip() if patrocinador_elem is not None and patrocinador_elem.text else ""

    # Referencias
    referencias = root.findall("u:referencias/u:referencia", NS)

    # Fotos
    fotos = root.findall("u:fotos/u:foto", NS)

    # Videos
    videos = root.findall("u:videos/u:video", NS)

    # Vencedor
    vencedor = root.find("u:vencedor", NS)
    nombre_vencedor = vencedor.get("nombre") if vencedor is not None else ""
    tiempo_vencedor = vencedor.get("tiempo") if vencedor is not None else ""

    # Clasificación
    clasificados = root.findall("u:clasificacion/u:clasificado", NS)

    # --------- Generación del HTML ---------
    h = Html(htmlfile)

    # DOCTYPE y <html>
    h.writeln("<!DOCTYPE html>")
    h.start_tag("html", {"lang": "es"})

    # HEAD
    h.start_tag("head")
    h.full_tag("meta", "", {"charset": "UTF-8"})
    h.full_tag("meta", "", {"name": "viewport", "content": "width=device-width, initial-scale=1.0"})
    h.full_tag("title", f"Información del circuito: {nombre}")
    h.writeln('<link rel="stylesheet" href="estilo.css">')
    h.end_tag("head")

    # BODY
    h.start_tag("body")

    # Header principal
    h.start_tag("header")
    h.full_tag("h1", nombre)
    if localidad or pais:
        h.full_tag("p", f"{localidad} ({pais})")
    h.end_tag("header")

    # Contenido principal
    h.start_tag("main")

    # Sección dimensiones
    h.start_tag("section")
    h.full_tag("h2", "Dimensiones del circuito")
    h.start_tag("ul")
    if longitud:
        h.full_tag("li", f"Longitud: {longitud} {unidad}")
    if anchura:
        h.full_tag("li", f"Anchura: {anchura} {unidad}")
    h.end_tag("ul")
    h.end_tag("section")

    # Sección carrera
    h.start_tag("section")
    h.full_tag("h2", "Datos de la carrera")
    h.start_tag("ul")
    if fecha:
        h.full_tag("li", f"Fecha: {fecha}")
    if hora:
        h.full_tag("li", f"Hora de inicio: {hora}")
    if vueltas:
        h.full_tag("li", f"Número de vueltas: {vueltas}")
    h.end_tag("ul")
    h.end_tag("section")

    # Sección patrocinador
    if patrocinador:
        h.start_tag("section")
        h.full_tag("h2", "Patrocinador principal")
        h.full_tag("p", patrocinador)
        h.end_tag("section")

    # Sección referencias
    if referencias:
        h.start_tag("section")
        h.full_tag("h2", "Referencias")
        h.start_tag("ul")
        for ref in referencias:
            url = ref.get("url", "")
            if url:
                h.writeln(f'<li><a href="{url}">{url}</a></li>')
        h.end_tag("ul")
        h.end_tag("section")

    # Sección fotos
    if fotos:
        h.start_tag("section")
        h.full_tag("h2", "Galería de fotos")
        h.start_tag("ul")
        for foto in fotos:
            archivo = foto.get("archivo", "")
            if archivo:
                h.full_tag("li", archivo)
        h.end_tag("ul")
        h.end_tag("section")

    # Sección vídeos
    if videos:
        h.start_tag("section")
        h.full_tag("h2", "Vídeos del circuito")
        h.start_tag("ul")
        for video in videos:
            archivo = video.get("archivo", "")
            if archivo:
                h.full_tag("li", archivo)
        h.end_tag("ul")
        h.end_tag("section")

    # Sección vencedor
    if nombre_vencedor or tiempo_vencedor:
        h.start_tag("section")
        h.full_tag("h2", "Vencedor de la carrera")
        h.start_tag("p")
        texto_v = nombre_vencedor
        if tiempo_vencedor:
            texto_v += f" — Tiempo: {tiempo_vencedor}"
        h.writeln(texto_v)
        h.end_tag("p")
        h.end_tag("section")

    # Sección clasificación
    if clasificados:
        h.start_tag("section")
        h.full_tag("h2", "Clasificación general")
        h.start_tag("table")
        h.writeln("<caption>Clasificación del campeonato</caption>")
        h.start_tag("thead")
        h.writeln("<tr><th scope=\"col\">Piloto</th><th scope=\"col\">Puntos</th></tr>")
        h.end_tag("thead")
        h.start_tag("tbody")
        for c in clasificados:
            nom = c.get("nombre", "")
            pts = c.get("puntos", "")
            h.writeln(f"<tr><td>{nom}</td><td>{pts}</td></tr>")
        h.end_tag("tbody")
        h.end_tag("table")
        h.end_tag("section")

    h.end_tag("main")

    # Footer
    h.start_tag("footer")
    h.full_tag("p", "Información generada automáticamente a partir de circuitoEsquema.xml")
    h.end_tag("footer")

    # Cierre body y html
    h.end_tag("body")
    h.end_tag("html")

    h.close()


if __name__ == "__main__":
    generar_html("circuitoEsquema.xml", "InfoCircuito.html")
    print("Archivo InfoCircuito.html generado correctamente.")
