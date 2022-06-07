from flask import Flask

app = Flask(__name__)

@app.route("/")
def puntoEntrada():
    return "<p>Hello, World!</p>"

@app.route("/hyper")
def hyper():
    return "<p>Estás en hyper</p>"

@app.route("/hyper/indices")
def hyper_indices():
    return "<p>Estás en hyper_indices</p>"

@app.route("/hyper/evolucion")
def hyper_evolucion():
    return "<p>Estás en Hyper_evolucion</p>"

@app.route("/imagen")
def imagen():
    return "<p>Estás en imagen</p>"

@app.route("/imagen/timelapse")
def imagen_timelapse():
    return "<p>Estás en imagen_timelapse</p>"
    