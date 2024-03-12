from data.data import usuario, olts

import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from flask_migrate import Migrate

from scripts_olt.alterar_dados_cliente import alterar_dados
from scripts_olt.excluir_cliente import excluir_cliente
from scripts_olt.provisionamento import provisionamento
from scripts_olt.status_cliente import status_cliente
from scripts_olt.troca_equipamento import troca_equipamento
from scripts_olt.upper_limit import upper_limit
from scripts_olt.verifica_caixa import pesquisa_caixa, pesquisa as pesq_cx
from scripts_olt.verificar_sinal import verificar_sinal
from scripts_olt.motivo_queda import motivo_da_queda

from pesquisa_cliente_sn import pesquisa as pesq_sn, pesquisa_cliente_sn
from pega_nome import pega_nome, pega_sn
from pega_cto import pega_cto
from pega_equipamento import pega_equipamento, pesquisa_equipamento   
from pesquisa_cliente import pesquisa, pesquisa_cliente

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class RouteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(100))
    response = db.Column(db.Text)  # Ajuste o tamanho conforme necessário
    timestamp = db.Column(db.DateTime)

    def __init__(self, route, response):
        self.route = route
        self.response = response
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))

class provisionamentoLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    nome_cliente = db.Column(db.String(160))
    equipamento = db.Column(db.String(150))
    ont_onu = db.Column(db.String(4))
    cb = db.Column(db.String(6))
    fp = db.Column(db.String(6))
    cx = db.Column(db.String(6))
    fs = db.Column(db.String(6)) 

    def __init__(self, usuario_logado, rota_link, nome_cliente, equipamento, ont_onu, cb, fp, cx, fs):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.nome_cliente = nome_cliente
        self.equipamento = equipamento
        self.ont_onu = ont_onu
        self.cb = cb
        self.fp = fp
        self.cx = cx
        self.fs = fs

class statusLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    nome_cliente = db.Column(db.String(160))
    cliente_selecionado = db.Column(db.String(160)) 

    def __init__(self, usuario_logado, rota_link, nome_cliente, cliente_selecionado):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.nome_cliente = nome_cliente
        self.cliente_selecionado = cliente_selecionado

class sinalLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    nome_cliente = db.Column(db.String(160))
    cliente_selecionado = db.Column(db.String(160)) 

    def __init__(self, usuario_logado, rota_link, nome_cliente, cliente_selecionado):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.nome_cliente = nome_cliente
        self.cliente_selecionado = cliente_selecionado

class alteraDadosLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    nome_cliente = db.Column(db.String(160))
    cliente_selecionado = db.Column(db.String(150))
    nova_desc = db.Column(db.String(160))
    cb = db.Column(db.String(6))
    fp = db.Column(db.String(6))
    cx = db.Column(db.String(6))
    fs = db.Column(db.String(6)) 

    def __init__(self, usuario_logado, rota_link, nome_cliente, cliente_selecionado, nova_desc, cb, fp, cx, fs):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.nome_cliente = nome_cliente
        self.cliente_selecionado = cliente_selecionado
        self.nova_desc = nova_desc
        self.cb = cb
        self.fp = fp
        self.cx = cx
        self.fs = fs

class exclusaoLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    nome_cliente = db.Column(db.String(160))
    cliente_selecionado = db.Column(db.String(160)) 

    def __init__(self, usuario_logado, rota_link, nome_cliente, cliente_selecionado):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.nome_cliente = nome_cliente
        self.cliente_selecionado = cliente_selecionado

class trocaEquipamentoLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    nome_cliente = db.Column(db.String(160))
    cliente_selecionado = db.Column(db.String(160)) 
    equipamento_selecionado = db.Column(db.String(50)) 
    tipo_equipamento = db.Column(db.String(5)) 

    def __init__(self, usuario_logado, rota_link, nome_cliente, cliente_selecionado,equipamento_selecionado,tipo_equipamento):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.nome_cliente = nome_cliente
        self.cliente_selecionado = cliente_selecionado
        self.equipamento_selecionado = equipamento_selecionado
        self.tipo_equipamento = tipo_equipamento

class pesquisaEquipLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_logado = db.Column(db.String(100))
    rota_link = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    cto_pesquisada = db.Column(db.String(160))

    def __init__(self, usuario_logado, rota_link, cto_pesquisada):
        self.usuario_logado = usuario_logado
        self.rota_link = rota_link
        self.timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        self.cto_pesquisada = cto_pesquisada


with app.app_context():
    db.create_all()

# Rotas
@app.route('/clientes', methods=['POST'])
def clientes_route():    
    data = request.json
    nome = data.get('nome')
    nome_formatado = pega_nome(nome)
    resposta = pesquisa_cliente(nome_formatado)
    resposta_json = jsonify(resposta)
    resposta_str = json.dumps(resposta)
    novo_registro = RouteLog(route='/clientes', response=resposta_str)
    db.session.add(novo_registro)
    db.session.commit()
    
    return resposta_json

################################################
################################################

@app.route('/clientes/<int:index>', methods=['POST'])
def cliente_route(index):
    clientes = []
    if index < len(olts):
        data = request.json
        nome = data.get('nome')
        nome_formatado = pega_nome(nome)
        resposta = pesquisa(olts[index][0],
                            olts[index][1],
                            olts[index][2],
                            'tecnico',
                            "Spac3@2023",
                            clientes,
                            nome_formatado)
        resposta_json = jsonify(resposta)
        resposta_str = json.dumps(clientes)
        novo_registro = RouteLog(route=f'/clientes/{index}', response=resposta_str)
        db.session.add(novo_registro)
        db.session.commit()
        
        return clientes    
    else:
        return jsonify({"Error":"Page not found : 404"})

################################################
################################################

@app.route('/clientes-sn/<int:index>', methods=['POST'])
def cliente_sn_route(index):
    clientes = []
    if index < len(olts):
        data = request.json
        sn = data.get('sn')
        sn_formatado = pega_sn(sn)
        resposta = pesq_sn(olts[index][0],
                            olts[index][1],
                            olts[index][2],
                            'tecnico',
                            "Spac3@2023",
                            clientes,
                            sn_formatado)
        # resposta_json = jsonify(resposta)
        resposta_str = json.dumps(clientes)
        novo_registro = RouteLog(route=f'/clientes-sn/{index}', response=resposta_str)
        db.session.add(novo_registro)
        db.session.commit()
        
        return clientes    
    else:
        return jsonify({"Error":"Page not found : 404"})

################################################
################################################

@app.route('/clientes-sn', methods=['POST'])
def clientes_sn_route():    
    data = request.json
    sn = data.get('sn')
    sn_formatado = pega_sn(sn)

    resposta = pesquisa_cliente_sn(sn_formatado)
    resposta_json = jsonify(resposta)
    resposta_str = json.dumps(resposta)
    novo_registro = RouteLog(route='/clientes-sn', response=resposta_str)
    db.session.add(novo_registro)
    db.session.commit()

    return resposta_json

################################################
################################################
@app.route('/equipamentos', methods=['GET'])
def equipamentos_route():
    equipamentos = pega_equipamento()
    equipamento_escolhido = equipamentos
    return jsonify(equipamento_escolhido)
################################################
################################################

@app.route('/equipamentos/<int:index>')
def equipamento_route(index):
    equipamentos = []
    if index < len(olts):
        retorno = pesquisa_equipamento(olts[index][0],olts[index][1],olts[index][2],'tecnico',"Spac3@2023",equipamentos)
        return jsonify(equipamentos)
    else:
        return jsonify({"Error":"Page not found : 404"})

@app.route('/provisionamento', methods=['POST'])
def provisionamento_route():
    data = request.json
    nome = data.get('nome')
    nome_formatado = pega_nome(nome)
    equipamento = data.get('equipamento')
    ontOnu = data.get('tipo-equipamento')
    cabo,fibra_primaria,caixa,fibra_secundaria = data.get('cto') #list []
    cto_formatado = pega_cto(cabo,fibra_primaria,caixa,fibra_secundaria)

    resposta = provisionamento(nome_formatado,equipamento,cto_formatado,ontOnu)
    resposta_json = jsonify(resposta)
    resposta_str = json.dumps(resposta)
    novo_registro = RouteLog(route='/provisionamento', response=resposta_str)
    db.session.add(novo_registro)
    db.session.commit()

    return resposta_json

@app.route('/verifica-caixa/<int:index>', methods=['POST'])
def verifica_caixa_route(index):  
    clientes = []
    if index < len(olts):  
        data = request.json
        nome = data.get('nome')
        caixa_formatada = pega_nome(nome)
        resposta = pesq_cx(olts[index][0],
                            olts[index][1],
                            olts[index][2],
                            'tecnico',
                            "Spac3@2023",
                            clientes,
                            caixa_formatada)
        resposta_json = jsonify(resposta)
        resposta_str = json.dumps(resposta)
        novo_registro = RouteLog(route=f'/verifica-caixa/{index}', response=resposta_str)
        db.session.add(novo_registro)
        db.session.commit()
        
        return resposta_json
    else:
        return jsonify({"Error":"Page not found : 404"})

@app.route('/troca-equipamento', methods=['POST'])
def troca_equipamento_route():
    data = request.json
    interface = data.get('interface')
    ontId = data.get('ont_id')
    ontOnu = data.get('tipo-equipamento')
    novoEquipamento = data.get('novo_equip') #list []
    ip = data.get('ip')

    resposta = troca_equipamento(interface, ontId, novoEquipamento, ontOnu, ip)
    resposta_json = jsonify(resposta)
    resposta_str = json.dumps(resposta)
    novo_registro = RouteLog(route='/troca-equipamento', response=resposta_str)
    db.session.add(novo_registro)
    db.session.commit()

    return resposta_json

@app.route('/status_cliente', methods=['POST'])
def status_cliente_route():
    data = request.json
    nome = data.get('nome')
    nome_formatado = pega_nome(nome)
    resultado = status_cliente(nome_formatado)
    clientes = []
    
    for item in resultado:
        x = item.split(',')
        clientes.append(x)

    resposta = clientes 
    resposta_json = jsonify(resposta)
    resposta_str =  json.dumps(resposta)
    novo_registro = RouteLog(route='/status_cliente', response=resposta_str)
    db.session.add(novo_registro)
    db.session.commit()

    return resposta_json

@app.route('/verificar_sinal', methods=['POST'])
def verificar_sinal_route():
    data = request.json
    nome = data.get('nome')
    nome_formatado = pega_nome(nome)
    cliente_selecionado = data.get('cliente_selecinado')

    resposta =  verificar_sinal(nome_formatado, cliente_selecionado)
    resposta_json = jsonify(resposta)
    resposta_str = json.dumps(resposta)
    novo_registro = RouteLog(route='/verificar_sinal', response=resposta_str)
    db.session.add(novo_registro) 
    db.session.commit()     

    return resposta_json

@app.route('/motivo_da_queda', methods=['POST'])
def motivo_da_queda_route():
    
    data = request.json
    nome = data.get('nome')
    nome_formatado = pega_nome(nome)
    cliente_selecionado = data.get('cliente_selecinado')

    resposta =  motivo_da_queda(nome_formatado, cliente_selecionado)
    resposta_json = jsonify(resposta) 
    resposta_str = json.dumps(resposta) 
    novo_registro = RouteLog(route='/motivo_da_queda', response=resposta_str) 
    db.session.add(novo_registro) 
    db.session.commit()        
    
    return resposta_json

@app.route('/alterar_dados', methods=['POST'])
def alterar_dados_route():
    data = request.json
    nome = data.get('nome')
    nome_formatado = pega_nome(nome)
    cliente_selecionado = data.get('cliente_selecinado')
    cabo,fibra_primaria,caixa,fibra_secundaria = data.get('cto') #list []
    cto_formatado = pega_cto(cabo,fibra_primaria,caixa,fibra_secundaria)

    resposta = alterar_dados(nome_formatado, cliente_selecionado, cto_formatado) 
    resposta_json = jsonify(resposta) 
    resposta_str = json.dumps(resposta)  
    novo_registro = RouteLog(route='/alterar_dados', response=resposta_str) 
    db.session.add(novo_registro)  
    db.session.commit()     

    return resposta_json

@app.route('/excluir_cliente', methods=['POST'])
def excluir_cliente_route():
    data = request.json
    cliente_selecionado = data.get('cliente_selecinado')

    resposta = excluir_cliente(cliente_selecionado) 
    resposta_json = jsonify(resposta) 
    resposta_str = json.dumps(resposta)  
    novo_registro = RouteLog(route='/excluir_cliente', response=resposta_str) 
    db.session.add(novo_registro)  
    db.session.commit()     

    return resposta_json

@app.route('/upper_limit', methods=['POST'])
def upper_limit_route():
    data = request.json
    interface = data.get('itfc') #list []
    hostname = data.get('hostname')

    resposta = upper_limit(interface,hostname) 
    resposta_json = jsonify(resposta) 
    resposta_str = json.dumps(resposta)  
    novo_registro = RouteLog(route='/upper_limit', response=resposta_str) 
    db.session.add(novo_registro)  
    db.session.commit()     

    return resposta_json    

@app.route('/logs-admin/post')
def view_logs():
    logs = RouteLog.query.all()
    logs_list = [{'route': log.route, 'response': log.response, 'timestamp': log.timestamp} for log in logs]
    return jsonify(logs_list)

@app.route('/logs-admin/reg-provisionamento', methods=['POST'])
def reg_provisionamento():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    nome_cliente = data.get('nome_cliente')
    equipamento = data.get('equipamento')
    ont_onu = data.get('ont_onu')
    cb = data.get('cb')
    fp = data.get('fp')
    cx = data.get('cx')
    fs = data.get('fs')

    registra_db = provisionamentoLog(usuario_logado=usuario_logado,  rota_link=rota_link, nome_cliente=nome_cliente, equipamento=equipamento, ont_onu=ont_onu, cb=cb, fp=fp, cx=cx, fs=fs)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-provisionamento-get')
def view_logs_reg_provisionamento():
    logs = provisionamentoLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'nome_cliente': log.nome_cliente,'equipamento': log.equipamento,'ont_onu': log.ont_onu,'cb': log.cb,'fp': log.fp,'cx': log.cx,'fs': log.fs} for log in logs]

    return jsonify(logs_list)

@app.route('/logs-admin/reg-status', methods=['POST'])
def reg_status():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    nome_cliente = data.get('nome_cliente')
    cliente_selecionado = data.get('cliente_selecionado')

    registra_db = statusLog(usuario_logado=usuario_logado,  rota_link=rota_link, nome_cliente=nome_cliente, cliente_selecionado=cliente_selecionado)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-status-get')
def view_logs_reg_status():
    logs = statusLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'nome_cliente': log.nome_cliente,'cliente_selecionado': log.cliente_selecionado} for log in logs]

    return jsonify(logs_list)

@app.route('/logs-admin/reg-sinal', methods=['POST'])
def reg_sinal():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    nome_cliente = data.get('nome_cliente')
    cliente_selecionado = data.get('cliente_selecionado')

    registra_db = sinalLog(usuario_logado=usuario_logado,  rota_link=rota_link, nome_cliente=nome_cliente, cliente_selecionado=cliente_selecionado)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-sinal-get')
def view_logs_reg_sinal():
    logs = sinalLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'nome_cliente': log.nome_cliente,'cliente_selecionado': log.cliente_selecionado} for log in logs]

    return jsonify(logs_list)

@app.route('/logs-admin/reg-altera-dados', methods=['POST'])
def reg_altera_dados():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    nome_cliente = data.get('nome_cliente')
    cliente_selecionado = data.get('cliente_selecionado')
    nova_desc = data.get('nova_desc')
    cb = data.get('cb')
    fp = data.get('fp')
    cx = data.get('cx')
    fs = data.get('fs')

    registra_db = alteraDadosLog(usuario_logado=usuario_logado,  rota_link=rota_link, nome_cliente=nome_cliente, cliente_selecionado=cliente_selecionado, nova_desc=nova_desc, cb=cb, fp=fp, cx=cx, fs=fs)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-altera-dados-get')
def view_logs_reg_altera_dados():
    logs = alteraDadosLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'nome_cliente': log.nome_cliente,'cliente_selecionado': log.cliente_selecionado,'nova_desc': log.nova_desc,'cb': log.cb,'fp': log.fp,'cx': log.cx,'fs': log.fs} for log in logs]

    return jsonify(logs_list)

@app.route('/logs-admin/reg-exclusao', methods=['POST'])
def reg_exclusao():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    nome_cliente = data.get('nome_cliente')
    cliente_selecionado = data.get('cliente_selecionado')

    registra_db = exclusaoLog(usuario_logado=usuario_logado,  rota_link=rota_link, nome_cliente=nome_cliente, cliente_selecionado=cliente_selecionado)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-exclusao-get')
def view_logs_reg_exclusao():
    logs = exclusaoLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'nome_cliente': log.nome_cliente,'cliente_selecionado': log.cliente_selecionado} for log in logs]

    return jsonify(logs_list)

@app.route('/logs-admin/reg-troca-equip', methods=['POST'])
def reg_troca_equip():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    nome_cliente = data.get('nome_cliente')
    cliente_selecionado = data.get('cliente_selecionado')
    equipamento_selecionado = data.get('equipamento_selecionado')
    tipo_equipamento = data.get('tipo_equipamento')

    registra_db = trocaEquipamentoLog(usuario_logado=usuario_logado,  rota_link=rota_link, nome_cliente=nome_cliente, cliente_selecionado=cliente_selecionado,equipamento_selecionado=equipamento_selecionado,tipo_equipamento=tipo_equipamento)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-troca-equip-get')
def view_logs_troca_equip():
    logs = trocaEquipamentoLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'nome_cliente': log.nome_cliente,'cliente_selecionado': log.cliente_selecionado,'equipamento_selecionado': log.equipamento_selecionado,'tipo_equipamento': log.tipo_equipamento} for log in logs]

    return jsonify(logs_list)

@app.route('/logs-admin/reg-pesquisa-cto', methods=['POST'])
def reg_pesquisa_cto():
    data = request.json
    usuario_logado = data.get('usuario_logado')
    rota_link = data.get('rota_link')
    cto_pesquisada = data.get('cto_pesquisada')

    registra_db = pesquisaEquipLog(usuario_logado=usuario_logado,  rota_link=rota_link, cto_pesquisada=cto_pesquisada)
    db.session.add(registra_db)
    db.session.commit()

    return "Registro feito com sucesso"

@app.route('/logs-admin/reg-pesquisa-cto-get')
def view_logs_reg_pesquisa_cto():
    logs = pesquisaEquipLog.query.all()
    logs_list = [{'usuario_logado': log.usuario_logado, 'rota_link': log.rota_link, 'timestamp': log.timestamp,'cto_pesquisada': log.cto_pesquisada} for log in logs]

    return jsonify(logs_list)


if __name__ == '__main__':
    app.run(debug=True)