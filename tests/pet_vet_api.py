from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dados fictícios de veterinários e pets (você deve usar um banco de dados real)
veterinarios = {
    1: {"nome": "Dr. João", "especialidade": "Clínica Geral"},
    2: {"nome": "Dra. Maria", "especialidade": "Dermatologia"},
}

pets = {
    1: {"nome": "Rex", "raca": "Golden Retriever"},
    2: {"nome": "Luna", "raca": "Siamese"},
}

# Rota para agendar uma consulta
@app.route("/agendar_consulta", methods=["POST"])
def agendar_consulta():
    data = request.json
    pet_id = data["pet_id"]
    veterinario_id = data["veterinario_id"]
    # Aqui você pode adicionar lógica para verificar disponibilidade, pré-diagnóstico, etc.
    return jsonify({"mensagem": "Consulta agendada com sucesso!"})

# Rota para obter informações sobre veterinários e pets
@app.route("/veterinarios")
def listar_veterinarios():
    return jsonify(veterinarios)

@app.route("/pets")
def listar_pets():
    return jsonify(pets)

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para agendamento
@app.route('/agendar.html')
def agendar():
    return render_template('consultas.html')

if __name__ == "__main__":
    app.run(debug=True)
