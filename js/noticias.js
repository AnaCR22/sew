"use strict";

class Noticias {

    constructor(busqueda) {
        this.busqueda = busqueda;
        this.apiKey = "XDkwJE3TYCdDk9ppsyTUNTljIwC9ghqX01Jj0et8";
        this.url = "https://api.thenewsapi.com/v1/news/all";
        this.noticias = [];
    }

    buscar() {
        const urlCompleta =
            `${this.url}?api_token=${this.apiKey}` +
            `&search=${this.busqueda}` +
            `&language=es` +
            `&limit=5`;
            
        fetch(urlCompleta)
            .then(response => response.json())
            .then(json => this.procesarInformacion(json))
            .catch(() => alert("Error al obtener las noticias"));
    }

    procesarInformacion(json) {
        this.noticias = json.data;

        this.mostrarNoticias();
    }

    mostrarNoticias() {
        const seccion = $("<section></section>");
        const titulo = $("<h2>Noticias sobre MotoGP</h2>");
        seccion.append(titulo);

        // Crear un artículo por cada noticia
        this.noticias.forEach(n => {
            const art = $("<article></article>");

            const h3 = $("<h3></h3>").text(n.title);
            const p = $("<p></p>").text(n.description || "Sin descripción");
            const fuente = $("<p></p>").text("Fuente: " + n.source);
            const enlace = $("<a></a>")
                .attr("href", n.url)
                .attr("target", "_blank")
                .text("Leer noticia completa");

            art.append(h3);
            art.append(p);
            art.append(fuente);
            art.append(enlace);

            seccion.append(art);
        });

        $("main").append(seccion);
    }
}
