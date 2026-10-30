# Para las aplicaciones web creadas con Flask, debemos importar siempre el modulo 
from flask import Flask    

# Para poder servir plantillas HTML desde archivos, es necesario importar el modulo render_template
from flask import render_template, request

import sys
sys.path.append( "src" )

from model.tarjeta import Tarjeta
from controller.tarjetas_controller import TarjetasController

# Flask constructor: crea una variable que nos servirá para comunicarle a Flask
# la configuración que queremos para nuestra aplicación
app = Flask(__name__)     

# decorator: se usa para indicar el URL Path por el que se va a invocar nuestra función
@app.route('/')      
def hello():
    return render_template("crear_tarjeta.html")

@app.route('/guardar_tarjeta')
def guardar_tarjeta():
    
    # Crear una tarjeta de credito
    tarjeta = Tarjeta( numero_tarjeta="",
                            cedula="", franquicia="", codigo_banco="", fecha_vencimiento="", cupo=0, tasa_interes=0, cuota_manejo=0)
    tarjeta.numero_tarjeta = request.args["numero_tarjeta"]
    tarjeta.cedula = request.args["cedula"]
    tarjeta.cupo = request.args["cupo"]
    tarjeta.franquicia = request.args["franquicia"]
    tarjeta.fecha_vencimiento = request.args["fecha_vencimiento"]
    tarjeta.tasa_interes = request.args["tasa_interes"]
    tarjeta.cuota_manejo = request.args["cuota_manejo"]
    
    # Guardarla en la BD
    TarjetasController.insertar( tarjeta )

    return "Tarjeta insertada exitosamente"

@app.route('/crear_tablas')
def crear_tablas():
    TarjetasController.crear_tabla()
    return "Tablas creadas exitosamente"

@app.route("/buscar_tarjeta")
def buscar_tarjeta():
    try:
        tarjeta_encontrada = TarjetasController.buscar_tarjeta( request.args["tarjeta_buscada"] )
        return render_template("tarjeta_buscada.html", tarjeta=tarjeta_encontrada)
    except Exception as error:
        return f"No es posible buscar la tarjeta: { error }"


@app.route('/compra')
def compra():
    return render_template('compra.html'  )

@app.route('/guardar_compra')
def guardar():
        
    # Armar una instancia de la clase compra
    compra = Compra( id_compra= str(uuid.uuid4() ) , 
                    numero_tarjeta= request.args["numero_tarjeta"] ,         
                    fecha=datetime.date.today(),   
                    valor_compra= float( request.args["compra"] ),        
                    tasa_interes= float(request.args["tasa"]),        
                    cuotas= int( request.args["cuotas"] ),  cuota_mensual=0  )
    compra.cuota_mensual = logica_tarjeta.calcular_cuota( compra=compra.valor_compra, tasa=compra.tasa_interes/100, plazo=compra.cuotas )
    # Guardarla en la BD
    ComprasController.insertar( compra )    

    return render_template("mostrar_compra.html", compra=compra)

# Esta linea permite que nuestra aplicación se ejecute individualmente
if __name__=='__main__':
   app.run( debug=True)