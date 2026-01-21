from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cotizador Pellet</title>
</head>
<body>
    <h1>🔥 Cotizador de Pellet</h1>
    <p>Servicio activo correctamente 🚀</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run()
