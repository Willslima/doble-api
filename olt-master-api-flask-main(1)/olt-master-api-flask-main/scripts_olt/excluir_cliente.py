from data.data import usuario
import time
import paramiko
import re

def excluir_cliente(dados):
    interface, porta, nome_dados, itfc2, pt2, sn, active, status, normal, match, no, ip = dados.split()
    user = usuario['user']
    password = usuario['password']

    def exluindo(interface, porta, ip, user, password, nome_dados, sn):

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

            channel.send(f'display service-port port {itfc[0]}/{itfc[1]}/{itfc[2]} ont {porta}\n\n')
            time.sleep(0.5)

            output_index = ''
            index_linha = []
            common = 0
            
            while True:
                if channel.recv_ready():
                    output_index += channel.recv(4096).decode()
                    time.sleep(2)
                    # print(output_index)
                    if 'common' in output_index:
                        match = re.search(r'(\d+)\s+\d{1,3}\s+common', output_index)
                        if match:
                            index_id = match.group(1)
                            print(f'O index ID é: {index_id}')
                            index_linha.append(index_id)
                            break  # Saia do loop quando a string desejada for encontrada
                    elif 'No service virtual port can be operated' in output_index:
                        channel.send(f'interface gpon {itfc[0]}/{itfc[1]}\n\n')
                        time.sleep(0.5)
                        channel.send(f'ONT DELETE {itfc[2]} {porta}\n\n')
                        time.sleep(0.5)
                        return 'Equipamento excluido com sucesso !'
                else:
                    time.sleep(0.5)  # Pode adicionar um sleep aqui para evitar sobrecarga
            
            common = index_linha[0]
            index_num = common


            channel.send(f'UNDO SERVICE-PORT {index_num}\n\n')
            time.sleep(1)

            channel.send(f'INTERFACE GPON {itfc[0]}/{itfc[1]}\n\n')
            time.sleep(1)

            channel.send(f'ONT DELETE {itfc[2]} {porta}\n\n')
            time.sleep(1)

            output_delete = ''

            while True:
                if channel.recv_ready():
                    output_delete += channel.recv(4096).decode()
                    time.sleep(1)
                    # print(output_delete)
                    if 'Number of ONTs that can be deleted: 1, success: 1' in output_delete:
                        print('Equipamento excluido com sucesso')
                        break  # Saia do loop quando a string desejada for encontrada
                    
                    else:
                        print('Algo deu errado, iremos tentar novamente...')
                        time.sleep(1)
                else:
                    time.sleep(1)

            channel.close()
            client.close()

            return f'Equipamento excluido com sucesso ! {nome_dados} {sn}'

        except Exception as e:
            print(f'Erro: {e}')
            return 'Algo deu errado na exclusão',e
        
    resultado = exluindo( interface, porta, ip,user, password, nome_dados, sn)
     
    return resultado


if __name__ == '__main__':
    excluir_cliente()