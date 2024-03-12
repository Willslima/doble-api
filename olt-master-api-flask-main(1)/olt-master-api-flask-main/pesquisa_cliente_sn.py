from data.data import usuario, olts
import time
import paramiko

def pesquisa(olt,ip,vlan,user,password, clientes, sn_equipamento):
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

        channel.send(f'display ont info by-sn {sn_equipamento}\n\n')
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

        fsp = []
        ont_id = []
        description = []
        sn = []
        control_flag = []
        run_state = []
        config_state = []
        match_state = []
        no = 'no'
        

        for line in full_output.split('\n'):
            if 'F/S/P                   :'in line:
                fsp.append(line)
            if 'ONT-ID                  :'in line:
                ont_id.append(line)
            if 'Description             :'in line:
                description.append(line)
            if 'SN                      :'in line:
                sn.append(line)
            if 'Control flag            :'in line:
                control_flag.append(line)
            if 'Run state               :'in line:
                run_state.append(line)
            if 'Config state            :'in line:
                config_state.append(line)
            if 'Match state             :'in line:
                match_state.append(line)
        

        dados = f'{fsp[0][25:].strip()} {ont_id[0][25:].strip()} {description[0][25:].strip()} {fsp[0][25:].strip()} {ont_id[0][25:].strip()} {sn[0][25:43].strip()} {control_flag[0][25:].strip()} {run_state[0][25:].strip()} {config_state[0][25:].strip()} {match_state[0][25:].strip()} {no} {hostname}'
        dados_tratados = dados.replace(':','')

        clientes.append(dados_tratados)
        
        channel.close()
        client.close()

    except Exception as e:
        return 'Algo deu errado:',e

def pesquisa_cliente_sn(sn_equipamento):
    user = usuario['user']
    password = usuario['password']
    clientes = []
    for i, olt in enumerate(olts):
        oltt, ip, vlan  = olt
        pesquisa(oltt, ip, vlan, user, password, clientes, sn_equipamento)

    if len(clientes) != 0:
        return clientes
    else:
        return []

if __name__ == '__main__':
    pesquisa_cliente_sn('')