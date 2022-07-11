from flask import Flask
from flask import render_template
from flask import url_for
import os


import funcionalidad

app = Flask(__name__)

parentFolder = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    #Se llama a este metodo por si hace falte generar nuevas imagenes
    funcionalidad.generarImagenes()

    fotosDefinitivas = sorted(os.listdir(os.path.join(parentFolder, "static", "vera_images")), reverse=True)
    print(len(fotosDefinitivas), fotosDefinitivas)
    return render_template('indexV2.html', fotos=fotosDefinitivas, fotosSize=len(fotosDefinitivas))

@app.route('/timeLapse')
def timeLapse():
    #Se llama a este metodo por si hace falte generar nuevas imagenes
    funcionalidad.generarImagenes()
    fotosDefinitivas = sorted(os.listdir(os.path.join(parentFolder, "static", "vera_images")), reverse=True)
    return render_template('index.html', fotos=fotosDefinitivas, fotosSize=len(fotosDefinitivas))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
