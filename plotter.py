from flask import Flask
from flask import render_template, jsonify
from random import randrange
import matplotlib.pyplot as plt
import os
import io
import base64
from jinja2 import Markup
from pyecharts.charts import Line
from pyecharts import options as opts

app = Flask(__name__ , static_url_path='/static', static_folder= str(os.getcwd()) + '/static',)

x = [0,1,2,3,4,5,6]
y = [1,3,2,4,6,5,4]
# Estos arrays simulan un ECG en el tiempo
tiempo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
ecg = [1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1,1,1,2,1,1,0,12,0,1,3,1,1.5,1,1,1]
# Variables globales de pulso sanguineo
cbpm = 0
lbpm = 0

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
    cbpm = randrange(65,70,1)
    pmax = randrange(70, 140, 2)
    pmin = randrange(30,80, 2)

    tiempo.append((len(tiempo) - 1) + 1)
    ecg.append(randrange(0,12,2))

    plot_url = base64.b64encode(img.getvalue()).decode()
    pagina = '<html><head><meta http-equiv="refresh" content="3"></head><body><img src="data:image/png;base64,{}"></body></html>'

    #return pagina.format(plot_url)
    return render_template("VPC1.html", x = tiempo, y = ecg, cbpm = cbpm, lbpm = lbpm, spo2 = rand, pmax = pmax, pmin = pmin)

@app.route('/index.html', methods=['GET'])
def vpc2():
    return render_template("index.html")

@app.route('/VPC1_3.html', methods=['GET'])
def vpc3():
    return render_template("VPC1_3.html")

@app.route('/VPC1_3_all.html', methods=['GET'])
def vpc3all():
    return render_template("VPC1_3_all.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
