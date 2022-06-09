from flask import Flask
from flask import render_template
from flask import url_for
import os


import funcionalidad

app = Flask(__name__)



@app.route('/')
def httpGET():
    fotos = sorted(os.listdir("/home/sgarciatz/carpetaCompartida/green_visor_imgss"))
    
    fotos = util.agruparPorTimestamp(fotos)

    util.solaparFotos(fotos)
        
    fotosDefinitivas = sorted(os.listdir("./static"), reverse=True)    

    return render_template('pageTemplate', fotos=fotosDefinitivas, fotosSize=len(fotosDefinitivas))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
