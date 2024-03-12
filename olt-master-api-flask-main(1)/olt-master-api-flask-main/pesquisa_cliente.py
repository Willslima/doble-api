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

        linhas_com_nome = []
        linhas_com_active = []

        for line in full_output.split('\n'):
            if nome in line:
                if 'display ont info by-desc' not in line:
                    linhas_com_nome.append(line)
            if 'active'in line:
                linhas_com_active.append(line)

        for idx, item in enumerate(linhas_com_nome):
            item = item.replace("---- More ( Press 'Q' to break ) ----","")
            item = item.replace("[37D                                     ","")
            item = item.replace('[37D','')
            item = item.replace("  "," ")
            clientes.append(f'{item + linhas_com_active[idx].replace("  "," ") + hostname}')
        
        channel.close()
        client.close()

    except Exception as e:
        return 'Algo deu errado:',e

def pesquisa_cliente(nome):
    user = usuario['user']
    password = usuario['password']
    clientes = []
    for i, olt in enumerate(olts):
        oltt, ip, vlan  = olt
        pesquisa(oltt, ip, vlan, user, password, clientes, nome)

    if len(clientes) != 0:
        return clientes
    else:
        return []

if __name__ == '__main__':
    pesquisa_cliente('WILLIAN')