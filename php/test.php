<?php
require_once __DIR__ . "/../cronometro.php";
session_start();

// --- REINICIO CONTROLADO DE SESIÓN ---
if (!isset($_GET["continuar"])) {
    session_unset();
}

// ===== CONFIG BD =====
$conexion = new mysqli("localhost", "DBUSER2025", "DBPSWD2025", "UO300568_DB");
if ($conexion->connect_errno) {
    die("Error de conexión con la base de datos");
}

/* ---------- FASE ---------- */
if (!isset($_SESSION["fase"])) {
    $_SESSION["fase"] = "datos";
}

/* ---------- GUARDAR USUARIO ---------- */
if (isset($_POST["guardar_usuario"])) {

    $stmt = $conexion->prepare(
        "INSERT INTO usuarios (id_usuario, profesion, edad, genero, pericia)
         VALUES (?, ?, ?, ?, ?)
         ON DUPLICATE KEY UPDATE
           profesion=VALUES(profesion),
           edad=VALUES(edad),
           genero=VALUES(genero),
           pericia=VALUES(pericia)"
    );

    $stmt->bind_param(
        "isisi",
        $_POST["id_usuario"],
        $_POST["profesion"],
        $_POST["edad"],
        $_POST["genero"],
        $_POST["pericia"]
    );
    $stmt->execute();

    $_SESSION["id_usuario"] = $_POST["id_usuario"];
    $_SESSION["dispositivo"] = $_POST["dispositivo"];
    $_SESSION["fase"] = "inicio";
}

// ===== INICIAR PRUEBA =====
if (isset($_POST["iniciar"])) {
    $_SESSION["cronometro"] = new Cronometro();
    $_SESSION["cronometro"]->arrancar();
    $_SESSION["fase"] = "prueba";
}

// ===== TERMINAR PRUEBA =====
if (isset($_POST["terminar"])) {

    $_SESSION["cronometro"]->parar();
    $textoTiempo  = $_SESSION["cronometro"]->mostrar();

    sscanf($textoTiempo, "%d:%d.%d", $m, $s, $d);
    $tiempo_segundos = $m * 60 + $s + ($d / 10);

    // Guardar prueba
    $stmt = $conexion->prepare(
        "INSERT INTO pruebas 
        (id_usuario, dispositivo, tiempo_segundos, completado, comentarios_usuario, mejoras, valoracion)
        VALUES (?, ?, ?, ?, ?, ?, ?)"
    );

    $completado = 1;
    $comentarios_usuario = $_POST["comentarios_usuario"] ?? "";
    $mejoras = $_POST["mejoras"] ?? "";
    $valoracion = 8;

    $stmt->bind_param(
        "isidssi",
        $_SESSION["id_usuario"],
        $_SESSION["dispositivo"],
        $tiempo_segundos,
        $completado,
        $comentarios_usuario,
        $mejoras,
        $valoracion
    );
    $stmt->execute();
/*
    // Guardar comentario observador
    if (!empty($_POST["comentario_observador"])) {
        $stmt2 = $conexion->prepare(
            "INSERT INTO observaciones (id_usuario, comentario) VALUES (?, ?)"
        );
        $stmt2->bind_param("is", $id_usuario, $_POST["comentario_observador"]);
        $stmt2->execute();
    }

    $_SESSION["fase"] = "fin";*/
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Test de Usabilidad</title>
    <link rel="stylesheet" href="../estilo/estilo.css">
    <link rel="stylesheet" href="../estilo/layout.css">
</head>

<body>
<h2>Test de Usabilidad – MotoGP Desktop</h2>

<?php if ($_SESSION["fase"] === "datos"): ?>

<form method="post">
    <p>ID Usuario (1–12): <input type="number" name="id_usuario" min="1" max="12" required></p>
    <p>Profesión: <input type="text" name="profesion" required></p>
    <p>Edad: <input type="number" name="edad" required></p>

    <p>Género:
        <select name="genero" required>
            <option>Hombre</option>
            <option>Mujer</option>
            <option>Otro</option>
        </select>
    </p>

    <p>Pericia informática (0–10):
        <input type="number" name="pericia" min="0" max="10" required>
    </p>

    <p>Dispositivo:
        <select name="dispositivo" required>
            <option>ordenador</option>
            <option>tableta</option>
            <option>telefono</option>
        </select>
    </p>

    <button type="submit" name="guardar_usuario">Continuar</button>
</form>

<?php elseif ($_SESSION["fase"] === "inicio"): ?>

<form method="post">
    <button type="submit" name="iniciar">Iniciar prueba</button>
</form>

<?php elseif ($_SESSION["fase"] === "prueba"): ?>

<form method="post">

<p>1. ¿En qué apartado de la web encontrarías la información del piloto?</p>
<input type="text" name="p1" required>

<p>2. ¿Dónde irías para consultar los datos del circuito?</p>
<input type="text" name="p2" required>

<p>3. ¿Qué acción te permite visualizar el circuito sobre un mapa?</p>
<input type="text" name="p3" required>

<p>4. ¿Te resulta fácil encontrar la información meteorológica? ¿Dónde está?</p>
<input type="text" name="p4" required>

<p>5. ¿Qué página muestra el ganador de la carrera?</p>
<input type="text" name="p5" required>

<p>6. ¿Qué acción te permite visualizar la clasificación de la carrera?</p>
<input type="text" name="p6" required>

<p>7. ¿Te ha resultado intuitivo el juego de cartas?</p>
<input type="text" name="p7" required>

<p>8. ¿Consideras que la sección de noticias en el apartado inicio es clara, 
    considerando el pequeño resumen que se proporciona, los links a la noticia completa y sus respectivas fuente? </p>
<input type="text" name="p8" required>

<p>9. ¿Consideras que la ayuda proporciona información suficiente?</p>
<input type="text" name="p9" required>

<p>10. Si has usado la sección de ayuda, ¿crees que podrías volver a usar la aplicación sin ella?</p>
<input type="text" name="p10" required>

<p>Propuestas de mejora:</p>
<textarea name="mejoras"></textarea>

<p>Comentarios:</p>
<textarea name="comentarios_usuario"></textarea>

<p><button type="submit" name="terminar">Terminar prueba</button></p>
</form>

<?php else: ?>

<p><strong>Prueba finalizada correctamente ✅</strong></p>

<?php endif; ?>

</body>
</html>
