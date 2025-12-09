"use strict";

class Circuito {

    constructor() {
        this.comprobarApiFile();
        this.leerArchivoHTML();
    }

    comprobarApiFile() {
        if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
            const p = document.createElement("p");
            p.textContent = "Este navegador no soporta la API File de HTML5.";
            document.body.appendChild(p);
        }
    }

    leerArchivoHTML() {
        const body = document.querySelector("body");
        const input = body.querySelector("input");
        
        input.addEventListener("change", () => {
            const archivo = input.files[0];
            if (!archivo) return;

            const lector = new FileReader();

            lector.onload = () => {
                const contenido = lector.result;
                this.mostrarContenidoHTML(contenido);
            };

            lector.readAsText(archivo);
        });
    }

    mostrarContenidoHTML(texto) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(texto, "text/html");

        const bodyArchivo = doc.querySelector("body");

        const body = document.querySelector("body");

        const h3 = document.createElement("h3");
        h3.textContent = "Información del Circuito (Archivo cargado)";
        document.body.appendChild(h3);

        const contenedor = document.createElement("section");
        const elementos = Array.from(bodyArchivo.children);

        for (let elem of elementos) {
            const clon = elem.cloneNode(true);
            contenedor.appendChild(clon);
        }

        document.body.appendChild(contenedor);
    }
}

const circuito = new Circuito();
//body>div

class CargadorSVG {

    constructor() {
        this.configurarInput();
    }

    configurarInput() {
        const body = document.querySelector("body");
        const inputs = body.querySelectorAll("input");

        const inputSVG = inputs[1]; 

        inputSVG.addEventListener("change", () => {
            const archivo = inputSVG.files[0];
            if (archivo) {
                this.leerArchivoSVG(archivo);
            }
        });
    }

    leerArchivoSVG(archivo) {
        const lector = new FileReader();

        lector.onload = () => {
            const svgTexto = lector.result;
            this.insertarSVG(svgTexto);
        };

        lector.readAsText(archivo);
    }

    insertarSVG(svgTexto) {
        const parser = new DOMParser();
        const docSVG = parser.parseFromString(svgTexto, "image/svg+xml");

        const svg = docSVG.documentElement;

        const h3 = document.createElement("h3");
        h3.textContent = "Altimetría del Circuito (Archivo SVG)";

        const contenedor = document.createElement("section");

        const svgClon = svg.cloneNode(true);
        contenedor.appendChild(svgClon);

        const body = document.querySelector("body");
        body.appendChild(h3);
        body.appendChild(contenedor);
    }
}
const cargadorSVG = new CargadorSVG();

class CargadorKML {

    constructor() {
        this.configurarInput();
        this.inicializarMapa();
    }

    configurarInput() {
        const body = document.querySelector("body");
        const inputs = body.querySelectorAll("input");

        // El TERCER input es el de KML (HTML → [HTML, SVG, KML])
        const inputKML = inputs[2];

        inputKML.addEventListener("change", () => {
            const archivo = inputKML.files[0];
            if (archivo) {
                this.leerArchivoKML(archivo);
            }
        });
    }


    inicializarMapa() {
        const body = document.querySelector("body");
        const divs = body.querySelectorAll("div");

        // Primer <div> para el mapa dinámico
        this.divMapa = divs[0];

        this.mapa = new google.maps.Map(this.divMapa, {
            center: { lat: 0, lng: 0 },
            zoom: 2
        });
    }

    // TAREA 4: leer archivo KML
    leerArchivoKML(archivo) {
        const lector = new FileReader();

        lector.onload = () => {
            const textoKML = lector.result;

            // Procesar el KML como XML
            const parser = new DOMParser();
            const xml = parser.parseFromString(textoKML, "text/xml");
            console.log("Texto KML leído:");
            console.log(textoKML);

            console.log("XML parseado:");
            console.log(xml);

            console.log("Coordenadas encontradas:");
            console.log(xml.querySelectorAll("coordinates"));
            console.log(xml.querySelectorAll("coordinates").length);

                const coordsXML = xml.querySelectorAll("coordinates");
            this.coordenadas = [];

            for (let nodo of coordsXML) {
                const texto = nodo.textContent.trim();
                const puntos = texto.split(/\s+/);

                for (let p of puntos) {
                    const [lon, lat] = p.split(",").map(Number);

                    // Guardamos lat/lon de cada punto
                    this.coordenadas.push({ lat: lat, lon: lon });
                }
            }

            // Una vez extraídas las coordenadas → Tarea 5
            this.insertarCapaKML();
        };
        lector.readAsText(archivo);
    }

    insertarCapaKML() {
        if (!this.coordenadas || this.coordenadas.length === 0) {
            console.error("No hay coordenadas para representar.");
            return;
        }

        // 1. ORIGEN DEL CIRCUITO (primer punto)
        const origen = this.coordenadas[0];

        // Crear el marcador del origen
        new google.maps.Marker({
            position: { lat: origen.lat, lng: origen.lon },
            map: this.mapa,
            title: "Punto de origen del circuito"
        });

        // 2. CREAR LA POLILÍNEA (todos los tramos del circuito)
        const ruta = this.coordenadas.map(p => ({ lat: p.lat, lng: p.lon }));

        const polilinea = new google.maps.Polyline({
            path: ruta,
            geodesic: true,
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 3
        });

        polilinea.setMap(this.mapa);

        // 3. AJUSTAR EL MAPA PARA MOSTRAR TODO EL CIRCUITO
        const bounds = new google.maps.LatLngBounds();

        for (let punto of ruta) {
            bounds.extend(punto);
        }

        this.mapa.fitBounds(bounds);
    }

}
function iniciarMapa() {
    new CargadorKML();
}