from pymongo import MongoClient
import gridfs
import os
from pymongo import MongoClient
import gridfs
from datetime import datetime
imagenes = sorted(os.listdir("/home/sgarciatz/carpetaCompartida/green_visor_imgs"))

client = MongoClient('localhost', 27017)
fs = gridfs.GridFS(client.fotosAgro, "fotosRGB")

for imagen in imagenes:
	with open("/home/sgarciatz/carpetaCompartida/green_visor_imgs/"+imagen, "rb") as ficheroImagen:
		try:
			fs.put(ficheroImagen, filename=imagen, metadata={"timestamp": imagen[:26], "pos": imagen[33], "idCam": imagen[41]})
		except:
			print("Se ha intentado insertar una imagen ya existente")
		print(imagen[:26], imagen[33], imagen[41], "\n")
client.close()
