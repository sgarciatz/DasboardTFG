from pymongo import MongoClient
import gridfs
import os
from datetime import datetime

parent_folder = os.path.dirname(os.path.realpath(__file__))
rgb_folder    = os.path.join(parent_folder, "sharedFolder", "imagenes_vera",  "rgb")
hyper_folder  = os.path.join(parent_folder, "sharedFolder", "imagenes_vera", "hyper")
rgb_images    = sorted(os.listdir(rgb_folder))
hyper_images  = sorted(os.listdir(hyper_folder))
client        = MongoClient('localhost', 27017)
fs            = gridfs.GridFS(client.fotosAgro, "fotosRGB")

for image in rgb_images:
    with open(rgb_folder + "/" + image, "rb") as image_file:
        try:
            image_timestamp = datetime.fromisoformat(imagen[:26])
            cam_pos         = int(image[33])
            cam_id          = int(image[41])
            fs.put(image_file, filename=image, metadata={"timestamp": image_timestamp, "pos": cam_pos, "idCam": cam_id})
        except:
            print("Se ha intentado insertar una imagen ya existente")
        print(imagen[:26], imagen[33], imagen[41], "\n")

fs = gridfs.GridFS(client.fotosAgro, "fotosHyper")

for image in hyper_images:
   with open(hyper_folder + "/" + image, "rb") as image_file:
        try:
            image_timestamp = datetime.fromisoformat(image[5:31])
            fs.put(image_file, filename=image, metadata={"timestamp": image_timestamp})
        except:
            print("Se ha intendao insertar una imagen ya existente")
        print(imagen, "\n")

client.close()
