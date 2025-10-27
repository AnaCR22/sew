"use strict";

class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = 0;
        this.coordenadas = { lat: 0, lon: 0 };
    }

    rellenarDatos(poblacion, coordenadas) {
        this.poblacion = poblacion;
        this.coordenadas = coordenadas; // {lat: número, lon: número}
    }

    // Método que devuelve el nombre de la ciudad en texto
    getNombre() {
        return this.nombre;
    }

    // Método que devuelve el nombre del país
    getPais() {
        return this.pais;
    }

    // Método que devuelve una lista HTML con el gentilicio y la población
    getInfoSecundaria() {
        return `
            <ul>
                <li>Gentilicio: ${this.gentilicio}</li>
                <li>Población: ${this.poblacion.toLocaleString()} habitantes</li>
            </ul>
        `;
    }

    // Método que escribe en el documento las coordenadas usando document.write()
    escribirCoordenadas() {
        const p = document.createElement("p");
        p.textContent = `Coordenadas: Latitud ${this.coordenadas.lat}, Longitud ${this.coordenadas.lon}`;
        document.body.appendChild(p);
    }
}

// Ejemplo: Jerez de la Frontera (España)
const ciudadJerez = new Ciudad(
    "Jerez de la Frontera",
    "España",
    "jerezano/a"
);

ciudadJerez.rellenarDatos(213105, { lat: 36.6850, lon: -6.1263 });