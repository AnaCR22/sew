<?php
class Cronometro {

    private $inicio;   
    private $tiempo;   

    public function __construct() {
        $this->tiempo = 0;
        $this->inicio = null;
    }

    public function arrancar() {
        $this->inicio = microtime(true);
    }

    public function parar() {
        if ($this->inicio !== null) {
            $fin = microtime(true);
            $this->tiempo = $fin - $this->inicio;
            $this->inicio = null;
        }
    }

    public function mostrar() {
        $total = $this->tiempo;

        $min = floor($total / 60);
        $seg = floor($total % 60);
        $decimas = floor(($total - floor($total)) * 10);

        return sprintf("%02d:%02d.%d", $min, $seg, $decimas);
    }
}

?>

