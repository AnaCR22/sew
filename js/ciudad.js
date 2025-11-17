"use strict";

class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = 0;
        this.coordenadas = { lat: 0, lon: 0 };
        this.dia = "2025-11-15"; // cambiar segun el dia de la carrera
    }

    rellenarDatos(poblacion, coordenadas) {
        this.poblacion = poblacion;
        this.coordenadas = coordenadas;
    }

    getNombre() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInfoSecundaria() {
        return `
            <ul>
                <li>Gentilicio: ${this.gentilicio}</li>
                <li>Población: ${this.poblacion.toLocaleString()} habitantes</li>
            </ul>
        `;
    }

    escribirCoordenadas() {
        const p = document.createElement("p");
        p.textContent = `Coordenadas: Latitud ${this.coordenadas.lat}, Longitud ${this.coordenadas.lon}`;
        document.querySelector("main").appendChild(p);
    }

    getMeteorologiaCarrera() {

        $.ajax({
            url: "https://api.open-meteo.com/v1/forecast",
            data: {
                latitude: this.coordenadas.lat,
                longitude: this.coordenadas.lon,
                start_date: this.dia,
                end_date: this.dia,
                hourly: "temperature_2m,apparent_temperature,relative_humidity_2m,rain,wind_speed_10m,wind_direction_10m",
                daily: "sunrise,sunset",
                timezone: "auto"
            },
            dataType: "json",
            method: "GET",
            success: (json) => this.procesarJSONCarrera(json),
            error: () => alert("Error al obtener los datos meteorológicos")
        });

    }

    procesarJSONCarrera(json) {
        this.datos = {
            sunrise: json.daily.sunrise[0],
            sunset: json.daily.sunset[0],

            horas: json.hourly.time,
            temperatura: json.hourly.temperature_2m,
            sensacion: json.hourly.apparent_temperature,
            humedad: json.hourly.relative_humidity_2m,
            lluvia: json.hourly.rain,
            vientoVel: json.hourly.wind_speed_10m,
            vientoDir: json.hourly.wind_direction_10m
        };

        this.mostrarDatosCarrera();
    }

    mostrarDatosCarrera() {

        let art = $("<article></article>");
        let h3 = $("<h3></h3>").text("Meteorología del circuito: " + this.nombre);
        art.append(h3);
        let ul = $("<ul></ul>");

        ul.append("<li>Amanecer: " + this.datos.sunrise + "</li>");
        ul.append("<li>Anochecer: " + this.datos.sunset + "</li>");
        ul.append("<li>Temperatura (12:00): " + this.datos.temperatura[12] + " °C</li>");
        ul.append("<li>Sensación térmica (12:00): " + this.datos.sensacion[12] + " °C</li>");
        ul.append("<li>Lluvia (12:00): " + this.datos.lluvia[12] + " mm</li>");
        ul.append("<li>Humedad (12:00): " + this.datos.humedad[12] + " %</li>");
        ul.append("<li>Viento (12:00): " + this.datos.vientoVel[12] + " km/h</li>");
        ul.append("<li>Dirección del viento (12:00): " + this.datos.vientoDir[12] + "°</li>");

        art.append(ul);
        $("main").append(art);
    }

    getMeteorologiaEntrenos() {

    let fechaCarrera = new Date(this.dia);

    // tres días antes
    let d1 = new Date(fechaCarrera);
    d1.setDate(d1.getDate() - 3);

    let d2 = new Date(fechaCarrera);
    d2.setDate(d2.getDate() - 2);

    let d3 = new Date(fechaCarrera);
    d3.setDate(d3.getDate() - 1);

    let start = d1.toISOString().substring(0, 10);
    let end = d3.toISOString().substring(0, 10);

    $.ajax({
        url: "https://api.open-meteo.com/v1/forecast",
        data: {
            latitude: this.coordenadas.lat,
            longitude: this.coordenadas.lon,
            start_date: start,
            end_date: end,
            hourly: "temperature_2m,rain,wind_speed_10m,relative_humidity_2m",
            timezone: "auto"
        },
        dataType: "json",
        method: "GET",
        success: (json) => this.procesarJSONEntrenos(json),
        error: () => alert("Error al obtener los datos meteorológicos de entrenamientos")
    });

}
procesarJSONEntrenos(json) {

    let horas = json.hourly.time;
    let temp = json.hourly.temperature_2m;
    let lluvia = json.hourly.rain;
    let viento = json.hourly.wind_speed_10m;
    let humedad = json.hourly.relative_humidity_2m;

    // Identificar los cambios de día
    let dias = {};

    for (let i = 0; i < horas.length; i++) {
        let dia = horas[i].substring(0, 10);

        if (!dias[dia]) {
            dias[dia] = {
                temperatura: [],
                lluvia: [],
                viento: [],
                humedad: []
            };
        }

        dias[dia].temperatura.push(temp[i]);
        dias[dia].lluvia.push(lluvia[i]);
        dias[dia].viento.push(viento[i]);
        dias[dia].humedad.push(humedad[i]);
    }

    // Calcular medias por día
    this.mediasEntrenos = [];

    for (let dia in dias) {
        let datos = dias[dia];
        let calcularMedia = arr => (arr.reduce((a,b)=>a+b,0) / arr.length).toFixed(2);

        this.mediasEntrenos.push({
            dia: dia,
            temperatura: calcularMedia(datos.temperatura),
            lluvia: calcularMedia(datos.lluvia),
            viento: calcularMedia(datos.viento),
            humedad: calcularMedia(datos.humedad)
        });
    }

    this.mostrarDatosEntrenos();
}
mostrarDatosEntrenos() {

    let art = $("<article></article>");
    let h3 = $("<h3></h3>").text("Meteorología – Entrenamientos (3 días previos)");
    art.append(h3);

    this.mediasEntrenos.forEach(dia => {

        let ul = $("<ul></ul>");
        ul.append(`<li><strong>Día:</strong> ${dia.dia}</li>`);
        ul.append(`<li>Temperatura media: ${dia.temperatura} °C</li>`);
        ul.append(`<li>Lluvia media: ${dia.lluvia} mm</li>`);
        ul.append(`<li>Viento medio: ${dia.viento} km/h</li>`);
        ul.append(`<li>Humedad media: ${dia.humedad} %</li>`);

        art.append(ul);
    });

    $("main").append(art);
}

}

const ciudadJerez = new Ciudad(
    "Jerez de la Frontera",
    "España",
    "jerezano/a"
);

ciudadJerez.rellenarDatos(213105, { lat: 36.6850, lon: -6.1263 });
