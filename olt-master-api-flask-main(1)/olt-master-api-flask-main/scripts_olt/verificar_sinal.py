from data.data import usuario
import time
import paramiko

def verificar_sinal(nome, dados):
    interface, porta, nome, itfc2, pt2, sn, active, status, normal, match, no, ip = dados.split()
    user = usuario['user']
    password = usuario['password']

    def verificar(interface, porta, nome, itfc2, pt2, sn, active, status, normal, match, no, ip, user, password):
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

            channel.send(f'display ont optical-info {itfc[2]} {porta}\n\n')
            time.sleep(0.5)

            output_sinal = ''
            sinal = []
            posicao = 0

            while channel.recv_ready():
                output_sinal += channel.recv(4096).decode()
                time.sleep(1)
                
                if 'Rx optical power(dBm)                  :' in output_sinal: 
                    sinal.append(output_sinal)
                else:
                    channel.send(f'interface gpon {itfc[0]}/{itfc[1]}\n\n')
                    channel.send(f'display ont optical-info {itfc[2]} {porta}\n\n')
            
            posicao = sinal[0].find('Rx optical power(dBm)                  :')
            
            sinal_final = sinal[0][posicao:posicao + 47]

            channel.close()
            client.close()

            return sinal_final,  interface

        except Exception as e:
            return 'Algo deu errado na verificação de sinal:',e
        0
    resultado = verificar( interface, porta, nome, itfc2, pt2, sn, active, status, normal, match, no, ip,user, password)
    
    resultado = list(resultado)
    # print(type(resultado))
 

    return resultado[0]

if __name__ == '__main__':
    verificar_sinal()