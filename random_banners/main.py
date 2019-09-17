# importamos las librerias necesarias para flask  
from flask import Flask, escape, request, jsonify, Response
import pymongo
import random
from random import sample
from json import dumps

# cargamos flask en el entorno 
app = Flask(__name__)

bebes = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-bebes.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-bebes.webp"},"permalink": "https://listado.kiero.co/listcategory/?id-26137/#Entretenimiento%20para%20Beb%C3%A9s"}

camaras = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-camaras.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-camaras.webp"},'permalink':"https://listado.kiero.co/listcategory/?id-28543/#Camaras"}

computadoras = {"link_banner": {"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-computacion.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-computacion.webp"},'permalink':'https://listado.kiero.co/listcategory/?id-26761/#Computadoras'}

futbol =  {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-deportes.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-deportes.webp"} ,'permalink':"https://listado.kiero.co/listcategory/?id-30014/#F%C3%BAtbol"}

com_electronicos = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-electronica.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-electronica.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-50122/#Componentes-electronicos'}

oficinas = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-oficina.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/banner-oficina.webp"},"permalink":"https://listado.kiero.co/listcategory/?id-26336/#Equipamiento-para-oficinas"}


# =====================================================================================================================================================#

banner_bebe = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/baby.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/baby.webp"},"permalink":"https://listado.kiero.co/listcategory/?id-26137/#Entretenimiento%20para%20Beb%C3%A9s"}
   
banner_camaras = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/cameras.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/cameras.webp"},'permalink':"https://listado.kiero.co/listcategory/?id-28543/#Camaras"}

banner_computadoras = {"link_banner": {"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/computer.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/computer.webp"},'permalink':'https://listado.kiero.co/listcategory/?id-26761/#Computadoras'}

banner_electronicos = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/electronics.jpg","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/electronics.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-50122/#Componentes-electronicos'}

banner_videojuegos = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/videojuegos.png","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/videojuegos.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-24119/#PlayStation-4'}

banner_instrumentos = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/instrumentos.png","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/instrumentos.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-25320/#Accesorios-para-instrumentos'}

banner_electrodomesticos = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/electrodomesticos.png","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/electrodomesticos.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-27594/#Electrodom%C3%A9sticos-de-cocina'}

banner_belleza = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/dispositivos+belleza.png","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/dispositivos+belleza.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-14675/#Electrodomesticos-de-Belleza'}

banner_bicicletas = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/bicicletas+y+ciclismo.png","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/bicicletas+y+ciclismo.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-29395/#Bicicletas'}

banner_audio_hogar = {"link_banner":{"jpg":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/audio+para+el+hogar.png","webp":"https://resourcekiero.s3-us-west-2.amazonaws.com/banner-3/audio+para+el+hogar.webp"},"permalink":'https://listado.kiero.co/listcategory/?id-50059/#Audio-para-el-hogar'}


# array de links para las imagenes JPG
_json_minibanner = [bebes,camaras,computadoras,futbol,com_electronicos,oficinas]
# array de links para las imagenes WEBP

_json_banners = [banner_bebe,banner_camaras,banner_computadoras,banner_electronicos,banner_videojuegos,banner_instrumentos,banner_electrodomesticos,banner_belleza,banner_bicicletas,banner_audio_hogar]


# Creamos las rutas de acceso web, la uri
@app.route('/')
def build_products():
    
    # Creamos el aleatorio de las imagenes
    RANDOM1, RANDOM2, RANDOM3 = random.sample(_json_minibanner, 3)
    BANNER1, BANNER2, BANNER3, BANNER4 = random.sample(_json_banners,4)
    # Creamos el objeto json
    _json = {
        "code": 1,
        "result_mini_banner":[RANDOM1,RANDOM2,RANDOM3],
        "result_banners":[BANNER1,BANNER2,BANNER3, BANNER4]
    }
    __return = Response(dumps(_json),status=200, mimetype='application/json') 
    __return.headers['Access-Control-Allow-Origin'] = '*'
    __return.headers['Access-Control-Allow-Methods'] = 'GET'
    __return.headers['Allow'] = 'GET'
    return __return


if __name__ == "__main__":
    app.run()
