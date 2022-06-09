from pymongo import MongoClient
import gridfs
import numpy as np
from PIL import Image
import cv2
from io import BytesIO

client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.fotosAgro, "fotosRGB")
numeroCamaras = 7
def aplicarEcualizacion(foto):
    fotoEcualizada = np.array(foto)
    fotoEcualizada = cv2.cvtColor(fotoEcualizada, cv2.COLOR_RGB2YUV)
    fotoEcualizada[:,:,0] = cv2.equalizeHist(fotoEcualizada[:,:,0])
    fotoEcualizada = cv2.cvtColor(fotoEcualizada, cv2.COLOR_YUV2RGB)
    return Image.fromarray(fotoEcualizada)

#Consume una lista de {oid, timestamp}
def agruparPorTimestamp(fotos):
    tandaFotos = []
    fotosAgrupadas = []
    grupos = 0
    tamGrupo = 0
    tandaFotos.append(fotos[0])
    for foto in fotos[1:]:
        if (foto["timestamp"][:26] == tandaFotos[0]["timestamp"][:26]):
            tandaFotos.append(foto)
        else:
            fotosAgrupadas.append(tandaFotos)
            tandaFotos = []
            tandaFotos.append(foto)
    [print(len(fotos), "de 7 fotos\n\n") for fotos in np.array(fotosAgrupadas)]
    return fotosAgrupadas

#Se realiza el solapamiento. Consume una lista de listas de {oid, timestamp}
#agrupadas por timestamp
def solaparFotos(fotosAgrupadas): 
    for grupoFotos in fotosAgrupadas:
        fotosSolapadas = Image.new('RGB',(numeroCamaras*1080, 1920), (250,250,250))
        for iteracion,foto in enumerate(grupoFotos):
            buffer = fs.find_one({"filename": foto["filename"]}).read()
            numPixeles = len(buffer) //(1920*1080)
            #imagen =  Image.frombuffer("RGB", (1080,1920), buffer)
            imagen = Image.open(BytesIO(buffer))
            fotosSolapadas.paste(imagen, (1080*int(foto["pos"]),0))
        fotosSolapadas = aplicarEcualizacion(fotosSolapadas)
        fotosSolapadas.save("./static/" + foto["filename"][:26] + ".jpg","JPEG")

def obtenerCursorFotos():
    cursorImagenes = client["fotosAgro"]["fotosRGB.files"].find({}, {"filename":1, "metadata.timestamp":1, "metadata.pos":1})
    elementos = list([{"filename":documento["filename"], "timestamp":documento["metadata"]["timestamp"], "pos":documento["metadata"]["pos"]} for documento in cursorImagenes])
    return elementos
