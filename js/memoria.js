"use strict";

class Memoria {
    #tableroBloqueado;
    #primeraCarta;
    #segundaCarta;
    #cronometro;

    constructor(){
        this.#tableroBloqueado = true;
        this.#primeraCarta = null;
        this.#segundaCarta = null;

        this.#barajarCartas();
        
        this.#tableroBloqueado = false;

        this.#cronometro = new Cronometro();
        this.#cronometro.arrancar();
    }

    voltearCarta(carta){
        if (this.#tableroBloqueado) return;

        const estado = carta.dataset.estado;
        if (estado === "volteada" || estado === "revelada") return;
        
        carta.dataset.estado = "volteada";

        if (!this.#primeraCarta) {
            this.#primeraCarta = carta;
        } else {
            this.#segundaCarta = carta;
            this.#comprobarPareja();
        }
    }

    #barajarCartas() {
        const tablero = document.querySelector("main");
        const cartas = Array.from(tablero.querySelectorAll(".carta"));        

        for (const child of cartas.children) {
            cartas.appendChild(child);
        }
        for (let i = cartas.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cartas[i], cartas[j]] = [cartas[j], cartas[i]];
        }

        for (let carta of cartas) {
            tablero.appendChild(carta);
        }
    }

    #reiniciarAtributos() {
        this.#tableroBloqueado = false;
        this.#primeraCarta = null;
        this.#segundaCarta = null;
    }

    #deshabilitarCartas(){
        this.#primeraCarta.dataset.estado = "revelada";
        this.#segundaCarta.dataset.estado = "revelada";

        this.#primeraCarta.onclick = null;
        this.#segundaCarta.onclick = null;

        this.#comprobarJuego();
        this.#reiniciarAtributos();
    }

    #comprobarJuego() {
        const cartas = document.querySelectorAll(".carta");
        let todasReveladas = true;

        for (let i = cartas.length - 1; i > 0; i--) {
            if (cartas[i].dataset.estado !== "revelada") {
                todasReveladas = false;
                break;
            }
        }

        if (todasReveladas) {
            this.#cronometro.parar();
        }
    }

    #cubrirCartas(){
        this.#tableroBloqueado = true;
        setTimeout(() => {
            this.#primeraCarta.dataset.estado = null;
            this.#segundaCarta.dataset.estado = null;
            this.#reiniciarAtributos();
        }, 1000);
    }

    #comprobarPareja(){
        const img1 = this.#primeraCarta.children[1];
        const src1 = img1.getAttribute("src");

        const img2 = this.#segundaCarta.children[1];
        const src2 = img2.getAttribute("src");

        src1 == src2 ? this.#deshabilitarCartas() : this.#cubrirCartas();
    }

}

const juego = new Memoria();

const cartas = document.querySelectorAll(".carta");

for (let carta of cartas) {
    carta.addEventListener("click", () => juego.voltearCarta(carta));
}

