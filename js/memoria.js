"use strict";

class Memoria {
    constructor(){
        this.tablero_bloqueado = true;
        this.primera_carta = null;
        this.segunda_carta = null;

        this.barajarCartas();
        
        this.tablero_bloqueado = false;

        this.cronometro = new Cronometro();
        this.cronometro.arrancar();
    }

    voltearCarta(carta){
        if (this.tablero_bloqueado) return;

        const estado = carta.dataset.estado;
        if (estado === "volteada" || estado === "revelada") return;
        
        carta.dataset.estado = "volteada";

        if (!this.primera_carta) {
            this.primera_carta = carta;
        } else {
            this.segunda_carta = carta;
            this.comprobarPareja();
        }
    }

    barajarCartas() {
        const tablero = document.getElementById("tablero");
        const cartas = Array.from(tablero.querySelectorAll(".carta"));        

        for (let i = cartas.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cartas[i], cartas[j]] = [cartas[j], cartas[i]];
        }

        for (let carta of cartas) {
            tablero.appendChild(carta);
        }
    }

    reiniciarAtributos() {
        this.tablero_bloqueado = false;
        this.primera_carta = null;
        this.segunda_carta = null;
    }

    deshabilitarCartas(){
        this.primera_carta.dataset.estado = "revelada";
        this.segunda_carta.dataset.estado = "revelada";

        this.primera_carta.onclick = null;
        this.segunda_carta.onclick = null;

        this.comprobarJuego();
        this.reiniciarAtributos();
    }

    comprobarJuego() {
        const cartas = document.querySelectorAll(".carta");
        let todasReveladas = true;

        for (let i = cartas.length - 1; i > 0; i--) {
            if (cartas[i].dataset.estado !== "revelada") {
                todasReveladas = false;
                break;
            }
        }

        if (todasReveladas) {
            this.cronometro.parar();
            setTimeout(() => {
            alert("¡Enhorabuena! Has encontrado todas las parejas");
            }, 300); 
        }
    }

    cubrirCartas(){
        this.tablero_bloqueado = true;
        setTimeout(() => {
            this.primera_carta.dataset.estado = null;
            this.segunda_carta.dataset.estado = null;
            this.reiniciarAtributos();
        }, 1000);
    }

    comprobarPareja(){
        const img1 = this.primera_carta.children[1];
        const src1 = img1.getAttribute("src");

        const img2 = this.segunda_carta.children[1];
        const src2 = img2.getAttribute("src");

        src1 == src2 ? this.deshabilitarCartas() : this.cubrirCartas();
    }

}

const juego = new Memoria();