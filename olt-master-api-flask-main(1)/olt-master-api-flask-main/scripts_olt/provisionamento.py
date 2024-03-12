from data.data import usuario
import time
import paramiko
import re
from scripts_olt.sn_exists import sn_exists
from scripts_olt.upper_limit import upper_limit

def provisionamento(nome, equipamento, cto, tipoEquipamento):
    eqp, modelo, interface, ip, vlan, olt, olt_desc = equipamento.split(' ')
    user = usuario['user']
    password = usuario['password']
    olt = f'{olt} {olt_desc}'
    ontOuOnu = tipoEquipamento

    def provisiona(olt,ip,vlan,user,password,eqp,interface, nome, cto,ontOuOnu):
        try:
            hostname = ip
            username = user
            password = password
            vlan = vlan
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

            channel.send(f'ont add {itfc[2]}   sn-auth {eqp} omci ont-lineprofile-id 101 ont-srvprofile-id 101 desc\n{nome}{cto}\n\n')
            time.sleep(0.5)
            
            channel.send('\n\n')
            time.sleep(0.5)

        except Exception as e:
            print('ERRO DETALHADO',e)
            return 'Algo deu errado no provisionamento:',e

        # Ler a saída
        output_provisionamento = ''

        ONTID = []
        # print(olt)
        try:
            while channel.recv_ready():
                output_provisionamento += channel.recv(4096).decode()
                time.sleep(0.5)  # pequena pausa para evitar uso excessivo de CPU
                #print(output_provisionamento)
            for line in output_provisionamento.split('\n'):
                if 'SN already exists' in line:
                    sn_exists(eqp)
                    return ['Equipamento localizado em outro cliente, o mesmo foi apagado, clique para provisionar novamente']
                if 'reach upper limit' in line:
                    channel.close()
                    client.close()

                    return ['Limite da primária excedido, verifique os clientes offline e remova 1 inativo']
                    
                if 'ONTID'in line:
                    ONTID.append(line)
                    #print(line)

        except Exception as e:            
            print('Algo deu errado "while/for"' ,e)

        try:

            match = re.search(r'ONTID\s*:\s*(\d+)', ONTID[0])
            if match:
                last_id = match.group(1)
                #print(f'O último ID é: {last_id}')
                
                if ontOuOnu == 'onu':
                    channel.send(f'ont port native-vlan {itfc[2]} {last_id} eth 1 vlan 10 priority 0\n\n')
                    time.sleep(0.5)

                channel.send('quit\n\n')
                time.sleep(0.5)

                channel.send(f'service-port vlan {vlan} gpon {itfc[0]}/{itfc[1]}/{itfc[2]} ONT {last_id}  gemport 1 multi-service user-vlan 10\n\n')
                time.sleep(0.5)

            output_final = ''
            while channel.recv_ready():
                output_final += channel.recv(4096).decode()
                time.sleep(0.5)  # pequena pausa para evitar uso excessivo de CPU
                # print(output_final)
            
            channel.close()
            client.close()

            return [f'Provisionamento concluido com sucesso! {eqp} {itfc[0]}/{itfc[1]}/{itfc[2]} {olt} {nome}{cto}', olt, interface]
        except Exception as e:
            print('Erro service-port', e)
        
    resultado = provisiona(olt, ip, vlan, user, password, eqp, interface,nome, cto, ontOuOnu)
    return resultado[0]

if __name__ == '__main__':
    provisionamento()