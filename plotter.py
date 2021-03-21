from flask import Flask
from flask import render_template, jsonify
from random import randrange
import matplotlib.pyplot as plt
import os
import io
import base64
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Markup

app = Flask(__name__ , static_url_path='/static', static_folder= str(os.getcwd()) + '/static',)

basedir = './db/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'soraia.db')
DATABASE = basedir + 'soraia.db'
db = SQLAlchemy(app)
app.config["DEBUG"] = True


x = [0,1,2,3,4,5,6]
y = [1,3,2,4,6,5,4]
tiempo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44]
ecg = [1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1,1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1,1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1]
ecg2 = [17,19,23,24.5,25,25.5,25.8,25.7,24,17,15.5,15,15.5,16,16.5,17,19,23,24.5,25,25.5,25.8,25.7,24,17,15.5,15,15.5,16,16.5,17,19,23,24.5,25,25.5,25.8,25.7,24,17,15.5,15,15.5,16,16.5,17,16,16.5,16,16,16]
ecgok = [1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1,1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1,1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1]
ecgbad = [1,1,2,1,1,0,12,0,1,3,2.5,2,1.5,1,1,1,1,2,1,1,0,12,0,1,3,2.5,2,1.5,1,1,1,1,2,1,1,0,12,0,1,3,2.5,2,1.5,1,1]
cbpm = 0
lbpm = 0
contador = 0

class PATIENTS(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    PATIENT = db.Column(db.Integer, unique=True)
    SPO2 = db.Column(db.Integer, unique=True)
    BPM = db.Column(db.Integer)
    PRESSLOW = db.Column(db.Integer)
    PRESSHIGH = db.Column(db.Integer)
    TEMP = db.Column(db.Integer)
    DATETIME = db.Column(db.Text)

class PATIENTSLIST(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    PATIENT = db.Column(db.Text)
    AGE = db.Column(db.Integer)
    BOX = db.Column(db.Integer)
    CHECKING = db.Column(db.Text)
    CHECKOUT = db.Column(db.Text)

def patient():
    patient_all = PATIENTS.query.order_by(PATIENTS.DATETIME).all()
    return patient_all

def patient_last():
    patient_last = PATIENTS.query.order_by(desc(PATIENTS.DATETIME)).first()
    return patient_last  

def get_alldata(db, mitable):
    """ query data from the table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM mitable ORDER BY id DESC LIMIT 1")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

@app.route("/patient", endpoint="patient", methods=["GET"])
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

@app.route('/VPC1')
def build_vpc():

    img = io.BytesIO()

    '''
    plt.plot(x,y)
    plt.title("Temperatura [°C]")
    plt.xlabel("Samples")
    plt.ylabel("Temperatura")
    plt.savefig(img, format='png')
    '''
    img.seek(0)
    rand = randrange(94,99,1)
    global lbpm
    global cbpm
    global contador
    texto = ''
    lbpm = cbpm
    cbpm = randrange(65,70,1)
    pmax = randrange(70, 140, 2)
    pmin = randrange(30,80, 2)

    #tiempo.append((len(tiempo) - 1) + 1)
    ecg = []
    y = 0
    while y < 45:
        if(contador > 8):
            ecg.append(ecgbad[y])
            texto = 'El paciente esta sufriendo un estado cardíaco anomalo compatible con un infarto.'
        else:
            ecg.append(ecgok[y])
        y = y + 1

    plot_url = base64.b64encode(img.getvalue()).decode()
    pagina = '<html><head><meta http-equiv="refresh" content="3"></head><body><img src="data:image/png;base64,{}"></body></html>'
    contador = contador + 1

    return render_template("VPC1.html", x = tiempo, y = ecg, cbpm = cbpm, lbpm = lbpm, spo2 = rand, pmax = pmax, pmin = pmin, alarma = texto)

@app.route('/', methods=['GET'])
def indexroute():
    return render_template("index.html")

@app.route('/index.html', methods=['GET'])
def vpc2():
    return render_template("index.html", nombre = "Isabel Zendal", Cargo = "Enfermera")

@app.route('/register.html', methods=['GET'])
def registeroute():
    return render_template("register.html", nombre = "Isabel Zendal", Cargo = "Enfermera")

@app.route('/box1.html', methods=['GET'])
def boxroute():

    #img.seek(0)
    spo = randrange(94,99,1)
    global lbpm
    global cbpm
    global contador
    texto = ''
    lbpm = cbpm
    cbpm = randrange(65,70,1)
    bpmax = randrange(70, 140, 2)
    bpmin = randrange(30,80, 2)
    bpress = str(bpmax) + '/' + str(bpmin)
    
    return render_template("box1.html", nombre = "Isabel Zendal", Cargo = "Enfermera", bp = bpress, hr = cbpm, spo2 = spo, glucose = "100", bt = "36", x = tiempo, y = ecg, z = ecg2)

@app.route('/alertas.html', methods=['GET'])
def alertroute():
    return render_template("alertas.html", nombre = "Isabel Zendal", Cargo = "Enfermera")

@app.route('/patient_medical_data.html', methods=['GET'])
def medicalroute():
    return render_template("patient_medical_data.html", nombre = "Isabel Zendal", Cargo = "Enfermera")

@app.route('/patient_list.html', methods=['GET'])
def listroute():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from PATIENTSLIST")
    pacientes = cur.fetchall()

    return render_template("patient_list.html", nombre = "Isabel Zendal", Cargo = "Enfermera", patients = pacientes)

@app.route('/VPC1_3.html', methods=['GET'])
def vpc3():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from PATIENTSLIST")
                    
    pacientes = cur.fetchall()
    return render_template("VPC1_3.html", patients = pacientes)

@app.route('/VPC1_3_all.html', methods=['GET'])
def vpc3all():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from PATIENTS")
                    
    pacientes = cur.fetchall()
    return render_template("VPC1_3_all.html", patients = pacientes)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>VirtualPatientCare. The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, host='0.0.0.0')