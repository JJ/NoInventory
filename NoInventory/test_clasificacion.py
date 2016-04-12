from bson.objectid import ObjectId

#from pymongo.objectid import ObjectId
from pymongo import *
import time
from catalogo import *
from item import *
from clasificacion import *
import os

def main():
    python_object = {'scaner':["{'clave':'valor'}"]}
    dic=dict(python_object)
    print dic
    aux3=json.JSONEncoder().encode(python_object)
    print aux3
    aux = json.loads(aux3)
    print aux
    #aux2=json.loads(str(aux["scaner"][0]))
    #print aux["scaner"][0]
    #print aux2
    #print dic
    #print
    #aux=dic["scaner"][0]
    #print aux["clave"]
    #aux = json.loads(str(dic["scaner"]))
    #print aux[0]
    #aux2=json.loads(str(aux[0]))
    #print aux2
    #data = json.loads(aux)
    #do = data['scaner'][0]
    #print do['clave']
    #print do['description']
    #aux = json.loads(str(dic["scaner"]))
    #aux2 = json.dumps(dic["scaner"])
    #print "claveee"
    #print aux2
    #print aux[0]
    #dic2=dict(aux[0])
    #print dic2



def main2():
    manejador = CatalogosDriver()
    manejadorItem = ItemsDriver()
    manejadorClasificacion=ClasificacionDriver()
    manejadorPruebas=ClasificacionPruebas(organizacion="nombre_prueba")

    print "\n#######################################################"
    print "LANZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#######################################################\n"

    manejadorClasificacion.destroyDriver("osl")
    manejadorClasificacion.createTag1("Codigo_Centro.csv","osl")
    #manejadorClasificacion.database.tag2.remove()
    manejadorClasificacion.createTag2("Tipo_Dispositivo.csv","osl")
    #manejadorClasificacion.database.tag3.remove()
    manejadorClasificacion.createTag3("default.csv","osl")
    #salida=manejadorClasificacion.read()
    #manejadorPruebas.prueba();
    #manejadorPruebas.destroyPrueba()
    #aux=manejadorPruebas.database[manejadorPruebas.organizacion].find()

    #for i in aux:
    #    print i
    salida=manejadorClasificacion.database.tag3.find()
    #salida=manejadorClasificacion.database.tag2.find({'organizacion':'osl','VALOR2':'CONSUMIBLE'})

    for s in salida:
        print s



    print "\n##########################################################"
    print "FINALIZANDO BATERIA DE TEST - OPERACIONES CRUD PARA CATALOGOS"
    print "#########################################################\n"

if __name__ == '__main__':
    main()
