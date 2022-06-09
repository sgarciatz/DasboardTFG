#from pymongo import MongoClient
#import gridfs
import numpy as np
from PIL import Image
import cv2

#client = MongoClient('localhost', 27017)
#fs = gridfs.GridFS(client.fotosAgro, "fotosRGB")

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
            with Image.open("/home/sgarciatz/carpetaCompartida/green_visor_imgs"+foto) as ficheroFoto:
                fotosSolapadas.paste(ficheroFoto, (1080*int(foto[33]),0))
        fotosSolapadas = aplicarEcualizacion(fotosSolapadas)
        fotosSolapadas.save("./static/" + foto[:26] + ".jpg","JPEG")

