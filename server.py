from flask import Flask
from flask import render_template
from flask import url_for
import os
import numpy as np
from PIL import Image
import cv2
app = Flask(__name__)

def aplicarEcualizacion(foto):
    fotoEcualizada = np.array(foto)
    fotoEcualizada = cv2.cvtColor(fotoEcualizada, cv2.COLOR_RGB2YUV)
    fotoEcualizada[:,:,0] = cv2.equalizeHist(fotoEcualizada[:,:,0])
    fotoEcualizada = cv2.cvtColor(fotoEcualizada, cv2.COLOR_YUV2RGB)
    return Image.fromarray(fotoEcualizada)

def agruparPorTimestamp(fotos):
    tandaFotos = []
    fotosAgrupadas = []
    grupos = 0
    tamGrupo = 0    
    tandaFotos.append(fotos[0])
    for foto in fotos[1:]:
        if (foto[:26] == tandaFotos[0][:26]):
            tandaFotos.append(foto)
        else:
            fotosAgrupadas.append(tandaFotos)
            tandaFotos = []
            tandaFotos.append(foto)
    [print(len(fotos), "de 7 fotos\n", fotos, "\n\n") for fotos in np.array(fotosAgrupadas)]
    return fotosAgrupadas

#Se realiza el solapamiento
def solaparFotos(fotosAgrupadas):
    for grupoFotos in fotosAgrupadas:
        fotosSolapadas = Image.new('RGB',(len(grupoFotos)*1080, 1920), (250,250,250))
        for iteracion,foto in enumerate(grupoFotos):    
            with Image.open("./dirFotos/green_visor_imgs/"+foto) as ficheroFoto:
                fotosSolapadas.paste(ficheroFoto, (1080*int(foto[33]),0))
        fotosSolapadas = aplicarEcualizacion(fotosSolapadas)
        fotosSolapadas.save("./static/" + foto[:26] + ".jpg","JPEG")

@app.route('/')
def httpGET():
    fotos = sorted(os.listdir("./dirFotos/green_visor_imgs"))
    
    fotos = agruparPorTimestamp(fotos)

    solaparFotos(fotos)
        
    fotosDefinitivas = sorted(os.listdir("./static"), reverse=True)    

    return render_template('pageTemplate', fotos=fotosDefinitivas, fotosSize=len(fotosDefinitivas))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
