from data.data import usuario
import time
import paramiko
import re
from scripts_olt.sn_exists import sn_exists
from scripts_olt.upper_limit import upper_limit

def troca_equipamento(interface, ontId, novoEquipamento, tipoEquipamento, ip):
    user = usuario['user']
    password = usuario['password']
    
    def troca(interface, ontId, novoEquipamento, tipoEquipamento,user,password, ip):
        try:
            hostname = ip
            username = user
            password = password
            itfc = interface.split('/')

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

            if tipoEquipamento == 'onu':
                channel.send(f'ont port native-vlan 4 10 eth 1 vlan 10 priority 0\n\n')
                time.sleep(0.5)

            channel.send(f'ont modify {itfc[2]} {ontId} sn {novoEquipamento}\n\n')
            time.sleep(0.5)

            output_final = ''
            while channel.recv_ready():
                output_final += channel.recv(4096).decode()
                time.sleep(0.5)  # pequena pausa para evitar uso excessivo de CPU
                #print(output_final)

            channel.close()
            client.close()

            return 'Troca de equipamento realizada com sucesso!'

        except Exception as e:
            print(e)
            return e
        
    resultado = troca(interface, ontId, novoEquipamento, tipoEquipamento, user, password, ip)
    return resultado

if __name__ == '__main__':
    troca_equipamento()