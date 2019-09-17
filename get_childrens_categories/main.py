from flask import Flask, escape, request, jsonify,Response
import pymongo
from json import dumps, loads
app = Flask(__name__)

conn = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = conn.kiero
collection = db.category

def get_childrens_categories(category):
    cursor = collection.find({"parent_id":category},{"_id":False,"path_from_root":False,"childrens_categories":False,"parent_id":False,"total_items_in_this_category":False})
    return cursor

@app.route('/category/<int:category>')
def build_categories(category):
    list_categories = []
    for category in get_childrens_categories(int(category)):
        list_categories.append(category)
    
    _json = {
        "code": 1,
        "result":{
            "message":"Proceso Exitoso",
            "return":list_categories
        }
    }
    __return = Response(dumps(_json),status=200, mimetype='application/json') 
    __return.headers['Access-Control-Allow-Origin'] = '*'
    __return.headers['Access-Control-Allow-Methods'] = 'GET'
    __return.headers['Allow'] = 'GET'
    return __return

if __name__ == "__main__":
    app.run()


