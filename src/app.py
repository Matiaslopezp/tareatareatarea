"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users=User.query.all()
    new_users=[]
    for i in range(len(all_users)):
        print(all_users[i].serialize())
        new_users.append(all_users[i].serialize())

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(new_users), 200

@app.route('/user/favoritos', methods=['GET'])
def user_fav():
     return jsonify({
         "lista de usuarios favoritos":"ahahahhaha"
          })


@app.route("/people", methods=["GET"])
def get_all_people():
        return jsonify({
         "menasaje":"Lista de los personajes"
          })


@app.route("/people/<int:id>", methods=["GET"])
def get_one_people(id):
        return jsonify({
         "menasaje":"El personaje selecciondo es:  "+str(id)
          })



@app.route("/planets", methods=["GET"])
def get_all_planets():
        return jsonify({
         "menasaje":"Lista de Planetas"
          })

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_one_planets(planet_id):
        return jsonify({
         "menasaje":"aca esta el planeta seleccionado:  "+ str(planet_id)
          })



@app.route("/favorite/planet/<int:planet_id>", methods=['POST',"DELETE"])
def modify_fav_planet(planet_id):
    if request.method=="POST":
        return jsonify({
        "mensaje": "El planeta con id "+ str(planet_id) + " ha sido agregado"
    })
    else:
         return jsonify({
        "mensaje": "El planeta con id "+ str(planet_id) + " ha sido eliminado"
    })

@app.route("/favorite/person/<int:person_id>", methods=['POST',"DELETE"])
def modify_fav_person(person_id):
    if request.method=="POST":
        return jsonify({
        "mensaje": "El personaje con id "+ str(person_id) + " ha sido agregado"
      })
    else:
         return jsonify({
        "mensaje": "El personaje con id "+ str(person_id) + " ha sido eliminado"
    })



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
