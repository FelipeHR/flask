from ctypes import sizeof
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo import InsertOne
from pymongo import MongoClient
from flask import request
import json

import flask

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://Checho:2laSw16x9MUf2rAv@serverlessinstance0.wkk1z.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient('mongodb+srv://Checho:2laSw16x9MUf2rAv@serverlessinstance0.wkk1z.mongodb.net/?retryWrites=true&w=majority')

db = client['MaxSave']

col = db['gastos']

mongo = PyMongo(app)

@app.route('/insertGasto', methods=['POST'])
def insert_gasto():
    
    monto = request.json['monto']
    fecha = request.json['fecha']
    categoria = request.json['categoria']
    descripcion = request.json['descripcion']
    
    if monto and fecha and categoria:

        col.insert_one( {

            "monto": monto,
            "fecha": fecha,
            "categoria": categoria,
            "descripcion": descripcion
        })

    else:
        return {'message': 'Gasto no Insertado'}

    print(request.json)
    return {'message': 'Gasto Insertado'}


@app.route('/getGastosFecha/<inicio>/<final>', methods=['POST'])
def getGastosFecha(inicio, final):
    
    fechaInicio = inicio
    fechaFinal = final

    res = []
    datos = {}

    if fechaInicio and fechaFinal:

        for documento in col.find({ 

            "fecha": {"$gte": fechaInicio, "$lte": fechaFinal}

        }):

            aux = {
                "monto": documento["monto"],
                "fecha": documento["fecha"],
                "categoria": documento["categoria"],
                "descripcion": documento["descripcion"]
            }
            res.append(aux)

    else:
        return jsonify({'message': 'ERROR!'})

    return jsonify({"message": res})


@app.route('/getGastosDia/<diaFecha>', methods=['GET'])
def get_gastos_dia(diaFecha):
    
    fecha = diaFecha

    res = []
    categorias = []
    maxCategorias = []
    montosCategorias = []

    total = 0

    if fecha:

        #encuentra todas las categorias de los gastos de ese dia
        for documento in col.find({ 

            "fecha": fecha

        }).distinct("categoria"):
            print(documento)
            categorias.append(documento)

        #crea lista de totales para cada categoria del dia
        totalesCategorias = [*range(len(categorias))]

        for i in range(len(totalesCategorias)):
            totalesCategorias[i] = 0

        #encuentra todos los gastos del dia y suma los montos
        for documento in col.find({ 

            "fecha": fecha

        }):
            print (documento)
            res.append(documento)
            total = total + int(documento["monto"])

            cat = documento["categoria"]
            index = categorias.index(cat)
            totalesCategorias[index] = totalesCategorias[index] + int(documento["monto"])

        #z = [x for _, x in sorted(zip(totalesCategorias, categorias))]

        zipped_lists = zip(totalesCategorias, categorias)
        sorted_pairs = sorted(zipped_lists)

        tuples = zip(*sorted_pairs)
        totalesCategorias, categorias = [ list(tuple) for tuple in  tuples]  

        datos = {}

        if(len(categorias) <= 4):
            #z tiene las 4 max categorias
            maxCategorias = categorias
            montosCategorias = totalesCategorias

            for i in range(len(maxCategorias)):
                
                datos[maxCategorias[i]] = montosCategorias[i]

        else:
            #se necesitan las ultimas 4 posiciones de z 
            maxCategorias = categorias[-4:]
            montosCategorias = totalesCategorias[-4:]
            suma = 0
            for i in range(len(totalesCategorias)):
                 if(i < len(totalesCategorias) - 4):
                    suma = suma + totalesCategorias[i]

            print(categorias)
            print(totalesCategorias)

            maxCategorias.append("Varios")
            montosCategorias.append(suma)

            print(maxCategorias)
            print(montosCategorias)
            for i in range(len(maxCategorias)):

                datos[maxCategorias[i]] = montosCategorias[i]

        y = json.dumps(datos)

    else:
        return {'message': 'ERROR!'}

    print(y)
    return y

'''
if __name__ == "__main__":
    app.run(debug=True)

'''
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080) 
