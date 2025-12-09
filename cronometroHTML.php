<?php
require_once "cronometro.php";
session_start();

if (!isset($_SESSION["cronometro"])) {
    $_SESSION["cronometro"] = new Cronometro();
}

$cronometro = $_SESSION["cronometro"];
$resultado = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    if (isset($_POST["arrancar"])) {
        $cronometro->arrancar();
        $resultado = "Cronómetro iniciado";
    }

    if (isset($_POST["parar"])) {
        $cronometro->parar();
        $resultado = "Cronómetro detenido";
    }

    if (isset($_POST["mostrar"])) {
        $resultado = "Tiempo: " . $cronometro->mostrar();
    }

    $_SESSION["cronometro"] = $cronometro;
}
?>

<!DOCTYPE HTML>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Cronómetro PHP</title>
    <link rel="stylesheet" href="estilo/estilo.css">
    <link rel="stylesheet" href="estilo/layout.css">
</head>

<body>
<header>
    <h1><a href="index.html">MotoGP Desktop</a></h1>
    <nav>
        <a href="index.html">Inicio</a>
        <a href="piloto.html">Piloto</a>
        <a href="circuito.html">Circuito</a>
        <a href="meteorologia.html">Meteorología</a>
        <a href="clasificaciones.html">Clasificaciones</a>
        <a href="juegos.html">Juegos</a>
        <a href="ayuda.html">Ayuda</a>
    </nav>
</header>

<p>Estás en: <a href="index.html">Inicio</a> >> <strong>Cronómetro PHP</strong></p>

<h2>Cronómetro en PHP</h2>

<form method="post">
    <button type="submit" name="arrancar">Arrancar</button>
    <button type="submit" name="parar">Parar</button>
    <button type="submit" name="mostrar">Mostrar</button>
</form>

<p><strong><?= htmlspecialchars($resultado) ?></strong></p>

</body>
</html>