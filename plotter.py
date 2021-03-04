from flask import Flask
from flask import render_template, jsonify
from random import randrange
import matplotlib.pyplot as plt
import os
import io
import base64
from jinja2 import Markup
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__ , static_url_path='/static', static_folder= str(os.getcwd()) + '/static',)

# Database instancia
basedir = './'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'soraia.db')
db = SQLAlchemy(app)

class PATIENTS(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    PATIENT = db.Column(db.Integer, unique=True)
    SPO2 = db.Column(db.Integer, unique=True)
    BPM = db.Column(db.Integer)
    PRESSLOW = db.Column(db.Integer)
    PRESSHIGH = db.Column(db.Integer)
    TEMP = db.Column(db.Integer)
    DATETIME = db.Column(db.Text)

x = [0,1,2,3,4,5,6]
y = [1,3,2,4,6,5,4]
# Estos arrays simulan un ECG en el tiempo
tiempo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
ecg = [1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1,1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1]
# Variables globales de pulso sanguineo
cbpm = 0
lbpm = 0

@app.route('/patient', endpoint="patient", methods=["GET"])
def patient():
    values = PATIENTS.query.order_by(PATIENTS.DATETIME).all()

    return jsonify({
        "items": [{
            "id": x.ID, 
            "Paciente": x.PATIENT, 
            "SpO2": x.SPO2,
            "Pulsaciones": x.BPM,
            "Presion low": x.PRESSLOW,
            "Presion alta": x.PRESSHIGH,
            "Fecha-hora": x.DATETIME,
            } for x in values]
    })

@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    #y = [1,2,3,4,5]
    #x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.title("Temperatura [°C]")
    plt.xlabel("Samples")
    plt.ylabel("Temperatura")
    plt.savefig(img, format='png')
    img.seek(0)
    rand = randrange(5)

    x.append((len(x) - 1) + 1)
    y.append(rand)

    plot_url = base64.b64encode(img.getvalue()).decode()
    pagina = '<html><head><meta http-equiv="refresh" content="3"></head><body><img src="data:image/png;base64,{}"></body></html>'

    #return pagina.format(plot_url)
    return render_template("VPC1.html", plot = plot_url)

@app.route('/vpc')
def build_vpc():

    img = io.BytesIO()
    img.seek(0)
    rand = randrange(90,99,2)
    global lbpm
    global cbpm
    lbpm = cbpm
    ecgnor = [1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1]
    ecgmio = [1,1,2,1,1,0,12,1,3,5,2,1.5,1,1,1]
    
    cbpm = randrange(65,70,1)
    pmax = randrange(70, 140, 2)
    pmin = randrange(30,80, 2)

    tiempo.append((len(tiempo) - 1) + 1)
    valorecg = randrange(0,12,1)
    if (valorecg > 4) and (valorecg < 8):
       alarma = 'Detectado un posible problema de miocardio. Revisar ECG'
    else:
       alarma = ''
    ecg.append(randrange(0,12,1))

    plot_url = base64.b64encode(img.getvalue()).decode()
    pagina = '<html><head><meta http-equiv="refresh" content="3"></head><body><img src="data:image/png;base64,{}"></body></html>'

    #return pagina.format(plot_url)
    return render_template("VPC1.html", x = tiempo, y = ecg, cbpm = cbpm, lbpm = lbpm, spo2 = rand, pmax = pmax, pmin = pmin, alarma = alarma)

@app.route('/index.html', methods=['GET'])
def vpc2():
    return render_template("index.html")

@app.route('/VPC1_3.html', methods=['GET'])
def vpc3():
    return render_template("VPC1_3.html")

@app.route('/VPC1_3_all.html', methods=['GET'])
def vpc3all():
    return render_template("VPC1_3_all.html")

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>VirtualPatientCare. The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.debug = True
    app.run()
