<?php

class Configuracion {

    private $conexion;
    private $host = "localhost";
    private $usuario = "DBUSER2025";
    private $password = "DBPSWD2025";
    private $bd = "UO300568_DB";

    public function __construct() {
        $this->conexion = new mysqli(
            $this->host,
            $this->usuario,
            $this->password,
            $this->bd
        );

        if ($this->conexion->connect_error) {
            die("Error de conexión");
        }
    }

    // 🔄 Vaciar tablas
    public function reiniciarBD() {
        $this->conexion->query("DELETE FROM observaciones");
        $this->conexion->query("DELETE FROM pruebas");
        $this->conexion->query("DELETE FROM usuarios");
    }

    // ❌ Eliminar base de datos
    public function eliminarBD() {
        $this->conexion->query("DROP DATABASE {$this->bd}");
    }

    // 📄 Exportar datos a CSV
    public function exportarCSV() {
        $resultado = $this->conexion->query("SELECT * FROM pruebas");

        $archivo = fopen("export_pruebas.csv", "w");
        fputcsv($archivo, [
            "id_prueba","id_usuario","dispositivo","tiempo",
            "completado","comentarios_usuario","mejoras","valoracion"
        ]);

        while ($fila = $resultado->fetch_assoc()) {
            fputcsv($archivo, $fila);
        }
        fclose($archivo);
    }

    public function __destruct() {
        $this->conexion->close();
    }
}

// ─── CONTROL DE ACCIONES ─────────────────────────
$config = new Configuracion();
$mensaje = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    if (isset($_POST["reiniciar"])) {
        $config->reiniciarBD();
        $mensaje = "Base de datos reiniciada correctamente";
    }

    if (isset($_POST["exportar"])) {
        $config->exportarCSV();
        $mensaje = "Datos exportados a CSV";
    }

    if (isset($_POST["eliminar"])) {
        $config->eliminarBD();
        $mensaje = "Base de datos eliminada";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Configuración Test</title>
    <link rel="stylesheet" href="../estilo/estilo.css">
    <link rel="stylesheet" href="../estilo/layout.css">
</head>

<body>

<h1>Configuración del Test de Usabilidad</h1>

<form method="post">
    <button name="reiniciar">Reiniciar Base de Datos</button>
    <button name="exportar">Exportar datos (CSV)</button>
    <button name="eliminar"
            onclick="return confirm('¿Seguro que deseas eliminar la base de datos?')">
        Eliminar Base de Datos
    </button>
</form>

<p><strong><?= $mensaje ?></strong></p>

</body>
</html>
