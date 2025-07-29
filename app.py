import os
import gspread
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- CONFIGURACIÓN DE GSPREAD ---
# Las credenciales se cargarán desde una variable de entorno en Render
try:
    creds_json = os.environ.get('GSPREAD_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    gc = gspread.service_account_from_dict(creds_dict)
    # Reemplaza "RegistrosAPI" con el nombre exacto de tu Hoja de Cálculo
    spreadsheet = gc.open("RegistrosAPI")
    worksheet = spreadsheet.sheet1
except Exception as e:
    print(f"Error al inicializar Google Sheets: {e}")
    gc = None
# --- FIN DE LA CONFIGURACIÓN ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    if not gc:
        return jsonify({'mensaje': 'Error de configuración del servidor con Google Sheets'}), 500
        
    datos = request.get_json()

    if not all(k in datos for k in ('correo', 'nombre_completo', 'sexo', 'edad')):
        return jsonify({'mensaje': 'Faltan datos en la solicitud'}), 400

    # Preparamos la fila en el orden que queremos en la hoja de cálculo
    nueva_fila = [
        datos['nombre_completo'],
        datos['correo'],
        datos['edad'],
        datos['sexo']
    ]

    try:
        # Añadimos la nueva fila a la hoja de cálculo
        worksheet.append_row(nueva_fila)
        return jsonify({'mensaje': 'Usuario registrado exitosamente en Google Sheets'}), 201
        
    except Exception as e:
        return jsonify({'mensaje': 'Ocurrió un error al registrar en Google Sheets', 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)