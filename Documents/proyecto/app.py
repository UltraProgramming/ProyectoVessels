from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://Ultrasea:Prefecturanaval@Ultrasea.mysql.pythonanywhere-services.com/Ultrasea$proyecto'
# URI de la BBDD                          driver de la BD  Ultrasea:Prefecturanaval@Ultrasea.mysqlpythonanywhere-services.com/Ultra$proyecto
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino la tabla
class Buque(db.Model):   # la clase Buque hereda de db.Model
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    matricula=db.Column(db.String(15))
    nombre=db.Column(db.String(100))
    tipo=db.Column(db.String(50))
    eslora=db.Column(db.Float(precision=2, asdecimal=True))
    tat=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    def __init__(self,matricula,nombre,tipo,eslora,tat,imagen):   #crea el  constructor de la clase
        self.matricula=matricula
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.tipo=tipo
        self.eslora=eslora
        self.tat=tat
        self.imagen=imagen





    #  si hay que crear mas tablas , se hace aqui




with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class BuqueSchema(ma.Schema):
    class Meta:
        fields=('id','matricula','nombre','tipo','eslora','tat','imagen')




buque_schema=BuqueSchema()            # El objeto buque_schema es para traer un buque
buques_schema=BuqueSchema(many=True)  # El objeto buques_schema es para traer multiples registros de buques




# crea los endpoint o rutas (json)
@app.route('/buques',methods=['GET'])
def get_Buques():
    all_buques=Buque.query.all()         # el metodo query.all() lo hereda de db.Model
    result=buques_schema.dump(all_buques)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/buques/<id>',methods=['GET'])
def get_buque(id):
    buque=Buque.query.get(id)
    return buque_schema.jsonify(buque)   # retorna el JSON de un buque recibido como parametro




@app.route('/buques/<id>',methods=['DELETE'])
def delete_buque(id):
    buque=Buque.query.get(id)
    db.session.delete(buque)
    db.session.commit()
    return buque_schema.jsonify(buque)   # me devuelve un json con el registro eliminado


@app.route('/buques', methods=['POST']) # crea ruta o endpoint
def create_buque():
    #print(request.json)  # request.json contiene el json que envio el cliente
    matricula=request.json['matricula']
    nombre=request.json['nombre']
    eslora=request.json['eslora']
    tipo=request.json['tipo']
    tat=request.json['tat']
    imagen=request.json['imagen']
    new_buque=Buque(matricula,nombre,eslora,tat,imagen)
    db.session.add(new_buque)
    db.session.commit()
    return buque_schema.jsonify(new_buque)


@app.route('/buques/<id>' ,methods=['PUT'])
def update_buque(id):
    buque=Buque.query.get(id)

    matricula=request.json['matricula']
    nombre=request.json['nombre']
    tipo=request.json['tipo']
    eslora=request.json['eslora']
    tat=request.json['tat']
    imagen=request.json['imagen']


    buque.matricula=matricula
    buque.nombre=nombre
    buque.tipo=tipo
    buque.eslora=eslora
    buque.tat=tat
    buque.imagen=imagen


    db.session.commit()
    return buque_schema.jsonify(buque)



# programa principal *******************************
'''
if __name__=='__main__':
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
'''

@app.route('/')
def hello_world():
     return 'Hello from Flask!'


