import pymongo
from tqdm import tqdm
from datetime import datetime
from json import dumps
from flask import Flask, escape, request,Response
from urllib.parse import urlparse
import json

app = Flask(__name__)
#nlp = spacy.load('en_core_web_sm')
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y%H%M%S")

def connect_category():
    try: 
        conn_mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        return conn_mongo
    except: 
        print("Could not connect to MongoDB") 

def connect_save():
    try: 
        conn_mongo = pymongo.MongoClient("mongodb://172.17.0.2:27017/")
        return conn_mongo
    except: 
        print("Could not connect to MongoDB") 


conn_category = connect_category()

db_category = conn_category.kiero
collection = db_category.random_category

# connect_save = connect_save()
# db_save = connect_save._kiero
# save = db_save.random_categories


def create(array):
    clear_data = []
    for row in array:
        imagen_W = ((urlparse(row['_L'])).path.rsplit('/', 1)[1]).splitlines()[0]
        build = {
            "Categoria_id": row['Categoria_id'],
            "Titulo": row['Titulo'],
            "Precio_cop": str(row['Precio_cop']).split('.')[0],
            "Producto_id": row['Producto_Id'],
            "Imagen": row['_L'] if row['_L'] else row['Imagenes_1'],
            "Imagen_W": 'https://images.kiero.co/images/_W/'+(imagen_W).split('.')[0]+'.webp'
        }
        clear_data.append(build)
    return clear_data

@app.route('/')
def hello():
    try:
        objectoJson = {}
        random_category = collection.aggregate([{'$match': {'Categoria_id':{'$exists':True}}},{ "$sample": { "size": 1 }}])
        for id in random_category:
            category = (id['Categoria_id'])
        products = db_category.products_sliders_6

        random_products=[]
        for i in products.aggregate([{'$match': {'Categoria_id':str(category)}},{ "$sample": { "size": 8 }}]):
            random_products.append(i)
        
        random_products = create(random_products)
        
        if random_products:
            
            buildJSON = {"code":1,"message":"productos encontrados satisfactoriamente",'random_products':random_products}
            __return = Response(json.dumps({"status":"success",'result':buildJSON}),status=200, mimetype='application/json') 
            __return.headers['Access-Control-Allow-Origin'] = '*'
            __return.headers['Access-Control-Allow-Methods'] = 'POST'
            __return.headers['Allow'] = 'POST'
            return __return

        else:
            buildJSON = {"code":0,"message":"Algo salio mal"}
            __return = Response(json.dumps({"status":"success",'result':buildJSON}),status=200, mimetype='application/json') 
            __return.headers['Access-Control-Allow-Origin'] = '*'
            __return.headers['Access-Control-Allow-Methods'] = 'POST'
            __return.headers['Allow'] = 'POST'
            return __return
        
    except Exception as err:
        print(err)
        objectoJson['Mensaje'] =  'Hubo un error'
        objectoJson['Resultados'] = str(category)
        _json = json.dumps(objectoJson)
        _Response = Response(_json,status=500, mimetype='application/json')
    
        _Response.headers['Access-Control-Allow-Origin'] = '*'
        return _Response

if __name__ == '__main__':
    app.run()






