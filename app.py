import os
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
ARCHIVO_EXCEL = 'registros.xlsx'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    datos = request.get_json()

    # Se elimina 'password' de los campos requeridos
    if not all(k in datos for k in ('correo', 'nombre_completo', 'sexo', 'edad')):
        return jsonify({'mensaje': 'Faltan datos en la solicitud'}), 400

    nuevo_usuario = {
        'correo': datos['correo'],
        'nombre_completo': datos['nombre_completo'],
        'sexo': datos['sexo'],
        'edad': datos['edad']
    }

    try:
        # Se elimina 'password' de las columnas
        columnas = ['correo', 'nombre_completo', 'sexo', 'edad']
        if os.path.exists(ARCHIVO_EXCEL):
            df = pd.read_excel(ARCHIVO_EXCEL)
            if nuevo_usuario['correo'] in df['correo'].values:
                return jsonify({'mensaje': 'El correo ya está registrado'}), 409
        else:
            df = pd.DataFrame(columns=columnas)

        nuevo_df = pd.DataFrame([nuevo_usuario])
        df_actualizado = pd.concat([df, nuevo_df], ignore_index=True)

        df_actualizado = df_actualizado[columnas]
        df_actualizado.to_excel(ARCHIVO_EXCEL, index=False)
        
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

    except Exception as e:
        return jsonify({'mensaje': 'Ocurrió un error al registrar', 'error': str(e)}), 500

# El endpoint de login ha sido eliminado
# ...

if __name__ == '__main__':
    # Código listo para el despliegue
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)