class Cronometro {
    #tiempo
    #inicio
    #corriendo
    #enMarcha

    constructor(){
        this.#tiempo = 0;
        this.#inicio = null;
        this.#corriendo = null;
        this.#enMarcha = false;
    }

    arrancar(){
        try{
            if(typeof Temporal === 'undefined'){
                throw new Error("Temporal no disponible");
            }
            this.#inicio = Temporal.Now.instant();

        }catch(error){
            this.#inicio = new Date();
        }

        this.#corriendo = setInterval(this.#actualizar.bind(this), 100);
        this.#enMarcha = true;
    }

    #actualizar(){
        try{
            if(typeof Temporal === 'undefined'){
                throw new Error("Temporal no disponible");
            }
            const ahora = Temporal.Now.instant();
            this.#tiempo = ahora.epochMilliseconds - this.#inicio.epochMilliseconds;
        }catch(error){
            const ahora = new Date();
            this.#tiempo = ahora.getTime() - this.#inicio.getTime();
        }
        this.#mostrar();
    }

    parar() {
        if (!this.#enMarcha) return;

        clearInterval(this.#corriendo);
        this.#enMarcha = false;
    }

    reiniciar() {
        clearInterval(this.#corriendo);
        this.#tiempo = 0;
        this.#inicio = null;
        this.#enMarcha = false;
        this.#mostrar();
    }

    #mostrar() {
        const minutos = parseInt(this.#tiempo / 60000);
        const segundos = parseInt((this.#tiempo % 60000) / 1000);
        const decimas = parseInt((this.#tiempo % 1000) / 100);

        const formato =
        String(minutos).padStart(2, "0") +
        ":" +
        String(segundos).padStart(2, "0") +
        "." +
        String(decimas);

        const parrafo = document.querySelector("main p");

        if (parrafo) {
            parrafo.textContent = formato;
        } else {
            console.warn("No se encontró ningún <p> dentro de <main>");
        }
    }

}

const c = new Cronometro();

const botones = document.querySelectorAll("main button");

function manejarClick(evento) {
    const texto = evento.target.textContent;
    if (texto === "Arrancar") c.arrancar();
    else if (texto === "Parar") c.parar();
    else if (texto === "Reiniciar") c.reiniciar();
}

for (let boton of botones) {
    boton.addEventListener("click", manejarClick);
}

