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
            image_timestamp = datetime.fromisoformat(image[:26])
            cam_pos         = int(image[33])
            cam_id          = int(image[41])
            fs.put(image_file, filename=image, metadata={"timestamp": image_timestamp, "pos": cam_pos, "idCam": cam_id})
            print(f"Imagen insertada -> {image_timestamp} || {cam_pos} || {cam_id}")
        except Exception as e:
            print(f"Se ha intentado insertar una imagen ya existente {image}")
            print(e)

fs = gridfs.GridFS(client.fotosAgro, "fotosHyper")

for image in hyper_images:
   with open(hyper_folder + "/" + image, "rb") as image_file:
        try:
            image_timestamp = datetime.fromisoformat(image[5:31])
            fs.put(image_file, filename=image, metadata={"timestamp": image_timestamp})
            print(f"Imagen HIM insertada -> {image_timestamp}")
        except:
            print(f"Se ha intendao insertar una imagen ya existente {image}")
            print(e)
client.close()
