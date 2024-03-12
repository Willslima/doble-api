from data.data import usuario, olts
import paramiko
import time

def pesquisa_equipamento(olt,ip,vlan,user,password,equipamentos):
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

        channel.send('display ont autofind all\n\n')
        time.sleep(0.5)

        full_output = ""

        while channel.recv_ready():
            output = channel.recv(4096).decode()
            full_output += output

            if '---- More' in output:
                channel.send(' ')
                time.sleep(0.5)
            else:
                time.sleep(0.5)

        linhas_com_ont_sn = []
        linhas_com_fsp = []

        for line in full_output.split('\n'):
            if 'F/S/P'in line:
                linhas_com_fsp.append(line)
            if 'Ont SN' in line:
                linhas_com_ont_sn.append(line)

        for  idx, item in enumerate(linhas_com_ont_sn):
            equipamentos.append(f'{item[24:58].strip()} {linhas_com_fsp[idx].strip()[22:26]}{linhas_com_fsp[idx].strip()[26:]} {hostname} {vlan} {olt}')
        # equipamentos.append(olt)
        channel.close()
        client.close()

    except Exception as e:
        return 'Algo deu errado:',e
    
def pega_equipamento():
    user = usuario['user']
    password = usuario['password']
    equipamentos = []
    for i, olt in enumerate(olts):
        oltt, ip, vlan  = olt
        pesquisa_equipamento(oltt, ip, vlan, user, password, equipamentos)
    return equipamentos

if __name__ == "__main__":
    equipamentos = pega_equipamento()
    print("Equipamentos encontrados:")
    for equipamento in equipamentos:
        print(equipamento)