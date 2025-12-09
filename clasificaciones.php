<?php
class Clasificacion {

    private $documento;  
    private $xml;

    public function __construct() {
        $this->documento = "xml/circuitoEsquema.xml";  
    }

    public function consultar() {
        if (!file_exists($this->documento)) {
            return false;
        }

        $this->xml = simplexml_load_file($this->documento);
        return $this->xml !== false;
    }

    public function getGanador() {
        return [
            "nombre" => (string)$this->xml->vencedor['nombre'],
            "tiempo" => (string)$this->xml->vencedor['tiempo']
        ];
    }

    public function getClasificacion() {
        $lista = [];
        foreach ($this->xml->clasificacion->clasificado as $piloto) {
            $lista[] = [
                "nombre" => (string)$piloto['nombre'],
                "puntos" => (string)$piloto['puntos']
            ];
        }
        return $lista;
    }
}

$cls = new Clasificacion();
$cls->consultar();
$ganador = $cls->getGanador();
$clasificacion = $cls->getClasificacion();
?>

<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Clasificaciones</title>
    <meta name ="author" content="Ana" />
    <meta name="description" content="La clasificación de la carrera de MotoGP" />
    <meta name="keywords" content="MotoGP, clasificaciones, resultados, mundial, carreras" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="estilo/estilo.css">
    <link rel="stylesheet" href="estilo/layout.css">
    <link rel ="icon" href="multimedia/favicon.ico">
</head>

<body>
    <header>
        <!-- Datos con el contenidos que aparece en el navegador -->
        <h1><a href="index.html">MotoGP Desktop</a></h1>
        <nav>
            <a href="index.html" title="Página de inicio">Inicio</a> 
            <a href="piloto.html" title="Información del piloto">Piloto</a> 
            <a href="circuito.html" title="Información del circuito">Circuito</a> 
            <a href="meteorologia.html" title="Datos meteorológicos">Meteorología</a> 
            <a href="clasificaciones.php" class="active" title="Resultados y clasificaciones">Clasificaciones</a> 
            <a href="juegos.html" title="Juegos de MotoGP">Juegos</a> 
            <a href="ayuda.html" title="Información de ayuda del proyecto">Ayuda</a>
        </nav>
    </header>

    <p>Estás en: <a href="index.html">Inicio</a> >> <strong>Clasificaciones</strong></p>

    <h2>Clasificaciones de MotoGP-Desktop</h2>
    
    <h3>Ganador de la Carrera</h3>
    <p><strong><?php echo $ganador["nombre"]; ?></strong> — Tiempo: <?php echo $ganador["tiempo"]; ?></p>

    <h3>Clasificación del Mundial</h3>
    <ul>
    <?php foreach ($clasificacion as $piloto): ?>
        <li><?= $piloto["nombre"] ?> — <?= $piloto["puntos"] ?> puntos</li>
    <?php endforeach; ?>    
    </ul>
</body>
</html>