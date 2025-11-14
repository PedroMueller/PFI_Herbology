from flask import Flask, jsonify, request
from flask_cors import CORS
import controller as ctrl

app = Flask(__name__)
CORS(app)

# =============================
# HOME
# =============================
@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "API Herbology funcionando!"})


# =============================
# PLANTAS
# =============================
@app.route('/plantas', methods=['GET'])
def get_plantas():
    #termo = request.args.get("termo")
    try:
        plantas = ctrl.get_plantas()
        #? print(plantas) em caso de teste no terminal mostra todas as plantas cadastradas
        return jsonify({"status": "ok", "data": plantas})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/detalhes/<int:planta_id>', methods=['GET'])
def get_detalhes(planta_id):
    try:
        planta_completa = ctrl.get_planta_completa(planta_id)
        if planta_completa:
            return jsonify({"status": "ok", "data": planta_completa})
        else:
            return jsonify({"status": "not_found", "message": "Planta não encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


        
# =============================
# BUSCA DE PLANTAS
# =============================
@app.route('/busca_planta', methods=['GET'])
def buscar_planta():
    try:
        # 1️⃣ Recebe o texto enviado pelo front-end via query string
        termo = request.args.get('termo', '').strip()

        # 2️⃣ Chama o controller responsável pela busca
        resultados = ctrl.buscar_planta(termo)

        print(">> termo recebido:", termo)
        print(">> resultados:", resultados)


        return jsonify({"status": "ok", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#!---------------------------------------------------------------------------------------------
"""
@app.route('/plantas/<int:planta_id>', methods=['GET'])
def get_planta(planta_id):
    try:
        planta = ctrl.get_planta(planta_id)
        if planta:
            return jsonify({"status": "ok", "data": planta})
        return jsonify({"status": "not_found", "message": "Planta não encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/plantas/<int:planta_id>/completa', methods=['GET'])
def get_planta_completa(planta_id):
    try:
        planta = ctrl.get_planta_completa(planta_id)
        if planta:
            return jsonify({"status": "ok", "data": planta})
        return jsonify({"status": "not_found", "message": "Planta não encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500 
"""
#!---------------------------------------------------------------------------------------------





if __name__ == '__main__':
    app.run(debug=True)




# =============================
# CATEGORIAS
# =============================
