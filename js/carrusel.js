"use strict";

class Carrusel {

    constructor(busqueda) {
        this.busqueda = busqueda;
        this.actual = 0;
        this.maximo = 4;
        this.fotos = [];
    }

    getFotografias() {
        window.jsonFlickrFeed = (json) => this.procesarJSONFotografias(json);

        $.ajax({
        url: "https://www.flickr.com/services/feeds/photos_public.gne",
        dataType: "jsonp",
        data: {
            format: "json",
            tags: this.busqueda,     // ej: "MotoGP, Jerez"
            tagmode: "all"
            }
        }); 
    }

    procesarJSONFotografias(json) {


        this.fotos = [];

        for (let i = 0; i < 5; i++) {

            let url = json.items[i].media.m;

            url = url.replace("_m.jpg", "_z.jpg");
            this.fotos.push(url);
        }

        this.mostrarFotografias();
    }

    mostrarFotografias() {

        let articulo = $("<article></article>");
        let titulo = $("<h2></h2>").text("Imágenes del circuito de " + this.busqueda);
        let imagen = $("<img>").attr("src", this.fotos[0]);

        articulo.append(titulo);
        articulo.append(imagen);

        $("main").append(articulo);

        setInterval(this.cambiarFotografia.bind(this), 3000);
    }

    cambiarFotografia() {

        this.actual++;

        if (this.actual > this.maximo) {
            this.actual = 0;
        }

        $("article img").attr("src", this.fotos[this.actual]);
    }
}

