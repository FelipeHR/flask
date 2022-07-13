from flask import Flask
from flask_pymongo import PyMongo
from pymongo import InsertOne
from pymongo import MongoClient
from flask import request

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
'''
@app.route('/getGastosFecha', methods=['GET'])
def get_gasto_fecha(data):
    
    if data:
    else:
        return {'message': 'ERROR!'}
    print(request.json)
    return {'message': 'Gastos Encontrados'}
'''
'''
if __name__ == "__main__":
    app.run(debug=True)
'''

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
