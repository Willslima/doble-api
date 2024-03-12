import time
import paramiko
from data.data import usuario

def upper_limit(itfc, hostname):
    username = usuario['user']
    password = usuario['password']

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password,allow_agent=False,look_for_keys=False)

    channel = client.invoke_shell()

    channel.send('enable\n\n')  
    time.sleep(0.5)

    channel.send('config\n\n')  
    time.sleep(0.5)

    channel.send(f'interface gpon {itfc[0]}/{itfc[1]}\n\n')  
    time.sleep(0.5)

    channel.send(f'display ont info {itfc[2]} all\n\n')  
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

    linhas_com_sn = []
    linhas_com_nome = []

    for line in full_output.split('\n'):
        if '_'in line:
            linhas_com_nome.append(line)
        if 'active' in line:
            linhas_com_sn.append(line)

    clientes_full = []

    for i, linha in enumerate(linhas_com_sn):
        lcn = linhas_com_nome[i].strip()
        lcn = lcn.replace("---- More ( Press 'Q' to break ) ----","")
        lcn = lcn.replace("[37D","")
        lcn = lcn.replace("","")
        lcn = lcn.replace("                                      ","")

        lnh = linha.strip()
        lnh = lnh.replace("---- More ( Press 'Q' to break ) ----","")
        lnh = lnh.replace("[37D","")
        lnh = lnh.replace("","")
        lnh = lnh.replace("                                      ","")

        clientes_full.append(f'{lcn} {lnh} {hostname}')

    clientes_off = []
    
    for cliente in clientes_full:
        if 'offline' in cliente:
            clientes_off.append(cliente)

    channel.close()
    client.close()

    return clientes_off

if __name__ == '__main__':
    upper_limit()