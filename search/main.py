from flask import Flask, escape, request, Response
from json import dumps
from elasticsearch import Elasticsearch
import pymongo
import sys, os
try: 
    conn = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
except: 
    print("Could not connect to MongoDB")

db = conn.kiero

# Created or Switched to collection names: my_gfg_collection 
collection = db.categorias16sep

app = Flask(__name__)

def _connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        return(_es)
    else:
        return('Awww it could not connect! in elasticsearch connection')
    return _es

def _replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString

def _buildArrayCategories(array):
    array_ids = []
    for item in array:
        array_ids.append(item['id'])
        if item['childrens_categories']:
            for children in item['childrens_categories']:                
                array_ids.append(children['id'])

    return array_ids

def finder(query):
    def match_category(query):
        # {"$text": {"$search": 'Accesorios'}},{"id":True,"name":True,"_id":False}
        # x = collection.find({"name":str(query)}).collation({'locale': "es", 'strength': 1})
        x = collection.find({"Fake2":{'$regex' : str(query), '$options' : 'i'}}).collation({'locale': "es", 'strength': 1})

        cursor = collection.find({"Fake2":{'$regex' : str(query), '$options' : 'i'}},{"id":True,"name":True,"_id":False,"childrens_categories":True}).collation({'locale': "es", 'strength': 1})

        array = [x for x in cursor]
        ids = _buildArrayCategories(array)
        # _json = {
        #     "id":array[0]['id'],
        #     "children":array[0]['childrens_categories']
        # }
        # _json = []
        return ids

    def match_product():
        return('hiii')

    _options = { 
        "match_category":match_category(query),
        "match_product": match_product()
    }
    return _options

def build_data(data):
    array = [data['id']]
    for item in data['children']:
        array.append(item['id'])
    return array

def build_json(data):
    return_json = []
    for row in data['hits']['hits']:
        build_json = {
            'Producto_Id' : row['_source']['Producto_Id'],
            'Categoria_id' : row['_source']['Categoria_id'],
            'Titulo' : row['_source']['Titulo'],
            #'Estado' : row['_source']['Estado'],
            'permalink' : 'https://articulo.kiero.co/product-details/?id-'+ row['_source']['Producto_Id']+'-'+(_replaceMultiple(row['_source']['Titulo'],["[","!","@","#",'"',"$",";","]","'",'(',')','/','?',',','.'],'')).replace(' ','-'),
            'Precio_cop' : row['_source']['Precio_cop'],
            'Imagenes_1' : row['_source']['Imagenes_1'],
            'Relevancia_cat' : row['_source']['Relevancia_cat'],
            'Relevancia_pro' : row['_source']['Relevancia_pro']
        }
        return_json.append(build_json)
    return return_json

def _suggestWords(query):
        ite = True;
        word = []
        correction = ''
        resultado= True;
        
        while ite:
            es = _connect_elasticsearch()
            res= es.search(index='productos_16septry3',body={
                    "suggest": {
                        "text" : query,
                        "my-suggest-1" : {
                            "term" : {
                                "field" : "Titulo"
                            }
                        }
                    }
                })

            for i in res['suggest']['my-suggest-1']:
                if i['options']:
                    
                    correction += i['options'][0]['text'] + ' '
                else:
                    correction += i['text'] + ' '

            ite = False 
                 
        return (correction)

def _search_categorys(correction):
    return_json = []
    _es = _connect_elasticsearch()
    res= _es.search(index='categorias', body={
            "query":{
                "match":{
                    "name": correction
                }
            },
            "sort":[
                "_score"
            ]
        },size=100)
    for row in res['hits']['hits']:
        build_json = {
            'id' : row['_source']['id'],
            'name' : row['_source']['name'],
            'linkcategory' : 'https://listado.kiero.co/listcategory/?id-'+ row['_source']['id']+'/#'+(_replaceMultiple(row['_source']['name'],["[","!","@","#",'"',"$",";","]","'",'(',')','/','?',',','.'],'')).replace(' ','%20')
        }
        return_json.append(build_json)
    return return_json

def search_elastic(correction):
    _es = _connect_elasticsearch()
    x = correction.split(' ')
    if len(x) > 2:
        print("Entro 2")
        res= _es.search(index='productos_16septry3', body={
        "query":{
            "match":{
                "Fake": correction
            }
        }
    },size=1000)
    else:
        res= _es.search(index='productos_16septry3',body={
            "query":{
                "match":{
                    "Fake": correction
                }
            },
            "sort":[
                {"Relevancia_cat.keyword":"asc"},
                {"Relevancia_pro.keyword":"asc"}
            ]
        },size=1000)

    return res

@app.route('/',methods=['POST','GET'])
def inicio():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            search_query=data['query']
            if "tetero" in search_query or "teteros" in search_query:
                correction = search_query
            else:
                correction = _suggestWords(search_query)
            json_categrias = _search_categorys(correction)
            retorno = finder(search_query)['match_category']
            _es = _connect_elasticsearch()
            rebuild = retorno
            res= _es.search(index='productos_16septry3',body={
                        "query":{
                            "match":{
                                "Categoria_id": (str(rebuild).replace('[','').replace(']','').replace(',',''))
                            }
                        },
                        "sort":[
                            {"Relevancia_cat.keyword":"asc"},
                            {"Relevancia_pro.keyword":"asc"}
                        ]
                    },size=1000)
            res2 = search_elastic(correction)
            if not res['hits']['hits']:
                res = search_elastic(correction)

            __return = Response(dumps({"status":1,'Total':res['hits']['total']['value'],'result':build_json(res)+build_json(res2),"Categorias_buscadas":json_categrias}),status=200, mimetype='application/json')
            __return.headers['Access-Control-Allow-Origin'] = '*'
            __return.headers['Access-Control-Allow-Methods'] = 'GET'
            __return.headers['Allow'] = 'GET'
            return __return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno,err)

    else:
        print('Hi, how are u')

if __name__ == "__main__":
    app.run(host='10.4.28.166',debug=True)
