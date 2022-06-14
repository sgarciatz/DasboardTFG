from pymongo import MongoClient
import gridfs
import numpy as np
from PIL import Image
import cv2
from io import BytesIO
import os
from datetime import datetime

client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.fotosAgro, "fotosRGB")
numeroCamaras = 7
parentFolder = os.path.dirname(os.path.abspath(__file__))
staticFolder = os.path.join(parentFolder, "static")

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
    [print(len(fotos), "de 7 fotos\n") for fotos in np.array(fotosAgrupadas)]
    return fotosAgrupadas

#Se realiza el solapamiento. Consume una lista de listas de {oid, timestamp}
#agrupadas por timestamp
def solaparFotos(fotosAgrupadas): 
    for grupoFotos in fotosAgrupadas:
        fotosSolapadas = Image.new('RGB',(numeroCamaras*1080, 1920), (250,250,250))
        for foto in grupoFotos:
            buffer = fs.find_one({"filename": foto["filename"]}).read()
            imagen = Image.open(BytesIO(buffer))
            fotosSolapadas.paste(imagen, (1080*int(foto["pos"]),0))
        fotosSolapadas = aplicarEcualizacion(fotosSolapadas)
        nombreImagen = foto["filename"][:26] + ".jpg"
        fotosSolapadas.save(os.path.join(staticFolder, nombreImagen))
        with open(os.path.join(parentFolder, "ultimoTimestamp"), "wt") as ultimoTimestamp:
            ultimoTimestamp.write(nombreImagen[:26])

def obtenerCursorFotos():
    projection = {"filename": 1, "metadata.timestamp":1, "metadata.pos":1 }
    try:
        ultimoTimestamp = datetime.fromisoformat(open(os.path.join(parentFolder, "ultimoTimestamp"), "rt").read())
        print(ultimoTimestamp)
        cursorImagenes = client["fotosAgro"]["fotosRGB.files"].find({"metadata.timestamp": {"$gt": ultimoTimestamp}}, projection)
    except:
        print("No se ha almacenado aun ningun timestamp de referencia, se deben generar todas las imagenes")
        cursorImagenes = client["fotosAgro"]["fotosRGB.files"].find({}, projection)

    elementos = list([{"filename":documento["filename"], "timestamp":documento["metadata"]["timestamp"], "pos":documento["metadata"]["pos"]} for documento in cursorImagenes])
    print(elementos)
    return elementos

def generarImagenes():
   #Se obtienen los metadatos de las imagenes que son necesarias generar
   listaMetadatos = obtenerCursorFotos()

   #Se hace una multilista agrupandolas por el campo timestamp
   listaMetadatos = agruparPorTimestamp(listaMetadatos)
   #Se crean las imagenes solapadas y se depositan el directorio  static
   solaparFotos(listaMetadatos)
