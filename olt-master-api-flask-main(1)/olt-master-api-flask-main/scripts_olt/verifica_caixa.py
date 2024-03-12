import re
from data.data import usuario, olts
import time
import paramiko

def pesquisa(olt,ip,vlan,user,password, clientes, nome):
    try:
        hostname = ip
        username = user
        password = password
        vlan = vlan

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password,allow_agent=False,look_for_keys=False)

        channel = client.invoke_shell()

        channel.send('enable\n\n')  
        time.sleep(0.5)

        channel.send('config\n\n')
        time.sleep(0.5)

        channel.send(f'display ont info by-desc {nome}\n\n')
        time.sleep(0.5)

        # Inicia a variável output como string vazia
        full_output = ""
        prompt = "(config)#"

        while True:
            while channel.recv_ready():
                time.sleep(1)
                output = channel.recv(4096).decode()
                full_output += output

                if '---- More' in output:  
                    channel.send(' ')
                    time.sleep(1)

            if full_output.strip().endswith(prompt):
                break
        
        clientes_sn = []
        clientes_nome = []
        total_clientes = []
       
        for linha in full_output.split('\n'):
            
            if 'active' in linha:
                if 'display ont info by-desc ' not in linha :
                    linha = linha.replace("---- More ( Press 'Q' to break ) ----","")
                    linha = linha.replace("[37D","")
                    linha = linha.replace("","")
                    linha = linha.replace("                                      ","")
                    clientes_sn.append(linha.strip())
            if '_' in linha:
                if 'display ont info by-desc ' not in linha :
                    linha = linha.replace("---- More ( Press 'Q' to break ) ----","")
                    linha = linha.replace("[37D","")
                    linha = linha.replace("","")
                    linha = linha.replace("                                      ","")

                    clientes_nome.append(linha.strip())
            if 'the total of ONTs are:' in linha:
                if 'display ont info by-desc ' not in linha :
                    linha = linha.replace("---- More ( Press 'Q' to break ) ----","")
                    linha = linha.replace("[37D","")
                    linha = linha.replace("","")
                    linha = linha.replace("                                      ","")

                    total_clientes.append(linha.strip())
        
        channel.close()
        client.close()

        return clientes_sn,clientes_nome,total_clientes 

    except Exception as e:
        return 'Algo deu errado:',e

def pesquisa_caixa(nome):
    user = usuario['user']
    password = usuario['password']
    clientes = []
    for i, olt in enumerate(olts):
        oltt, ip, vlan  = olt
        resultado = pesquisa(oltt, ip, vlan, user, password, clientes, nome)
        clientes.append(resultado)

    if len(clientes) != 0:
        return clientes
    else:
        return 'Nenhum cliente localizado'

if __name__ == '__main__':
    pesquisa_caixa()