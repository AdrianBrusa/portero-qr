from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

DEPARTAMENTOS = {
    "1": {"nombre": "Depto 1A", "canal": "portero-edificio-1a"},
    "2": {"nombre": "Depto 1B", "canal": "portero-edificio-1b"},
    "3": {"nombre": "Depto 2A", "canal": "portero-edificio-2a"},
    "4": {"nombre": "Depto 2B", "canal": "portero-edificio-2b"},
    "5": {"nombre": "Depto 3A", "canal": "portero-edificio-3a"},
    "6": {"nombre": "Depto 3B", "canal": "portero-edificio-3b"},
    "7": {"nombre": "Depto 4A", "canal": "portero-edificio-4a"},
    "8": {"nombre": "Depto 4B", "canal": "portero-edificio-4b"},
}

HTML_INTEGRADO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portero Digital</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f9; margin: 0; padding: 20px; }
        h1 { color: #333; margin-bottom: 5px; }
        p { color: #666; margin-bottom: 25px; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; max-width: 400px; margin: 0 auto; }
        button { background-color: #007bff; color: white; border: none; padding: 25px 10px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: background 0.2s; -webkit-tap-highlight-color: transparent; }
        button:active { background-color: #0056b3; }
        #status { margin-top: 25px; font-size: 16px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Portero Digital</h1>
    <p>Seleccione el departamento para tocar el timbre</p>
    <div class="grid">
"""

for idx, info in DEPARTAMENTOS.items():
    HTML_INTEGRADO += f'<button onclick="tocarTimbre(\'{idx}\')">{info["nombre"]}</button>\n'

HTML_INTEGRADO += """
    </div>
    <div id="status"></div>
    <script>
        function tocarTimbre(id) {
            const statusDiv = document.getElementById('status');
            statusDiv.style.color = '#666'; 
            statusDiv.innerText = 'Llamando...';
            
            fetch('/llamar/' + id, { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    if(data.status === 'success') {
                        statusDiv.style.color = '#28a745'; 
                        statusDiv.innerText = data.message + ' ✔';
                    } else {
                        statusDiv.style.color = '#dc3545'; 
                        statusDiv.innerText = 'Error al llamar';
                    }
                })
                .catch(() => {
                    statusDiv.style.color = '#dc3545'; 
                    statusDiv.innerText = 'Error de conexión';
                });
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML_INTEGRADO


@app.route("/llamar/<id_depto>", methods=["POST"])
def llamar(id_depto):
    if id_depto in DEPARTAMENTOS:
        depto = DEPARTAMENTOS[id_depto]
        # CORRECCIÓN: Agregada la barra '/' entre el dominio y el canal
        url = f"https://ntfy.sh/{depto['canal']}"
        headers = {
            "Title": "Portero Digital",
            "Priority": "high",
            "Tags": "bell",
        }
        try:
            res = requests.post(
                url,
                data=f"Están tocando el timbre en el {depto['nombre']}".encode(
                    "utf-8"
                ),
                headers=headers,
                timeout=5,
            )
            if res.status_code == 200:
                return jsonify(
                    {
                        "status": "success",
                        "message": f"Llamando al {depto['nombre']}",
                    }
                )
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "No encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)