#!/usr/bin/python3
#-*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import pymongo 
from bson.objectid import ObjectId
import json
import time
import urllib3.request
import datetime

client = MongoClient('db')
db = client['dexter']

app = Flask(__name__)
cors = CORS(app)


@app.route("/api/geral/")
def filme_geral():    
    filmes = db.filmes.find({})
    dic = {'filmes': []}

    for f in filmes:
        f['id'] = str(f['_id'])
        f.pop('_id', None)
        if 'comentarios' in f.keys():
            f['comentarios'] = [str(i) for i in f['comentarios']]
           
        dic['filmes'].append(f)
    
    return jsonify(dic)


@app.route("/api/geral/<id>")
def filme_especifico(id):
    info = db.filmes.aggregate([
        {"$match": {'_id': ObjectId(id)}},
        {"$lookup": {
            "from": "comentarios",
            "localField": "comentarios",
            "foreignField": "_id",
            "as": "comentarios"
        }}
    ])

    dic = {'info': []}
    for i in info:
        i['id'] = str(i['_id'])
        i.pop('_id', None)
        if 'comentarios' in i.keys():
            i['comentarios'] = [ {"nome": c.get("nome"),
                "comentario": c.get("comentario")}
                for c in i['comentarios']]
        dic['info'].append(i)

    return jsonify(dic)


@app.route("/api/filme/filtro",methods=["POST"])
def categorias():    
    filtro = request.get_json()
    k = list(filtro.keys())[0]
    filtro[k] = {"$regex": ".*%s*." % filtro[k], "$options":"i"}
    filmes = db.filmes.find(filtro)

    dic = {'filmes': []}
    for f in filmes:
        f['id'] = str(f['_id'])
        f.pop('_id', None)
        k = [k for k in f.keys() if "arquivo" == k]
        if not k:
            f['arquivo'] = "static/img/ghost-in-the-shell.jpg"
        if 'comentarios' in f.keys():
            f['comentarios'] = [str(i) for i in f['comentarios']]
        dic['filmes'].append(f)

    return jsonify(dic)


@app.route("/api/filme/<id>", methods=["PUT"])
def ver_filme(id):
    info = db.filmes.update({"_id":ObjectId(id)}, {"$set":
        {"visto": datetime.datetime.now()}})
    return jsonify({"message": "Assistindo filme"})

        
@app.route("/api/filme/<id>/comentarios", methods=['POST'])
def comentario(id):
    comment = db.comentarios.insert_one(request.get_json())
    info = db.filmes.update(
        {'_id': ObjectId(id)},
        {'$addToSet': {
            'comentarios': comment.inserted_id
        }}
    )

    return jsonify({"message": "Comentario enviado!"})


@app.route("/api/filme/<id>/avaliacao", methods=['POST'])
def nota(id):  
    nota = request.get_json().get("nome")
    result = db.filmes.update({"_id": ObjectId(id)}, {"$inc": {"avaliacao.%s"%nota:1}})
    return jsonify({"message":"Comentario enviado"})


@app.route("/api/geral/",methods=["POST"])
def novo_filme_geral():
    filme = request.get_json()
    filme['avaliacao'] = {
            'bom': 0,
            'medio': 0,
            'ruim': 0}
    filme['arquivo'] = 'static/img/ghost-in-the-shell.jpg'
    filme = db.filmes.insert(filme)

    return jsonify({"message":"filmes cadastrado com sucesso"})

        
@app.route("/api/filme/recentes")
def ver_recentes():
    filmes = db.filmes.find({}, 
        {"titulo":1, "visto":1, "_id":0}
    ).sort([('visto', pymongo.DESCENDING)]).limit(4)
    
    dic = {'filmes': [f for f in filmes]}
    return jsonify(dic)

        
@app.route("/api/filme/recomendados")
def ver_recomendados():
    filmes = db.filmes.find({}, 
        {"titulo":1, "avaliacao":1, "_id":0}
    ).sort([('avaliacao.bom', pymongo.DESCENDING)]).limit(4)

    dic = {'filmes': [f for f in filmes]}
    print dic
    return jsonify(dic)


@app.route("/api/geral/<id>",methods=["DELETE"])
def filme_remover(id):
    result = db.filmes.delete_one({"_id": ObjectId(id)})
    return jsonify({"message":"Filme removido com sucesso"})


if __name__ == '__main__':
     app.run(host="0.0.0.0",port=5000,debug=True,threaded=True)
