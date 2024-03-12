from data.data import usuario
import time
import paramiko

def motivo_da_queda(nome, dados):
    interface, porta, nome, itfc2, pt2, sn, active, status, normal, match, no, ip = dados.split()
    user = usuario['user']
    password = usuario['password']

    def verificar(interface, porta, ip, user, password):
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

            channel.send(f'display ont info {itfc[2]} {porta}\n\n')
            time.sleep(0.5)

            down_cause = ''
            sinal = []
            posicao = 0
            
        # Lista das frases que queremos encontrar
            required_phrases = [
                'Last down cause         :',
                'Last up time            :',
                'Last down time          :',
                'Last dying gasp time    :',
                'ONT online duration     :'
            ]

            while True:
                if channel.recv_ready():
                    output = channel.recv(4096).decode()
                    down_cause += output
                    
                    # Verifique cada frase na saída
                    for phrase in required_phrases:
                        if phrase in output:
                            sinal.append(output)
                            required_phrases.remove(phrase)  # Remove a frase da lista

                    # Se "---- More" estiver na saída, envie um espaço para continuar
                    if '---- More' in output:
                        channel.send(' ')
                        time.sleep(1)
                    elif not required_phrases:
                        break
                    else:
                        channel.send(f'interface gpon {itfc[0]}/{itfc[1]}\n\n')
                        channel.send(f'display ont info {itfc[2]} {porta}\n\n')
                else:
                    time.sleep(1)  # Pode adicionar um sleep aqui para evitar sobrecarga

            down_c = sinal[0].find('Last down cause         :')
            up_time = sinal[1].find('Last up time            :')
            down_time = sinal[1].find('Last down time          :')
            cause_time = sinal[1].find('Last dying gasp time    :')
            online_duration = sinal[1].find('ONT online duration     :')

            dc = sinal[0][down_c:down_c + 36]
            upt = sinal[1][up_time:up_time + 51]
            dt = sinal[1][down_time:down_time + 51]
            ct = sinal[1][cause_time:cause_time + 51]
            od = sinal[1][online_duration:online_duration + 74]
            
            channel.close()
            client.close()

            return [dc, upt, dt, ct, od]

        except Exception as e:
            return 'Algo deu errado (verificação info cliente):',e
        
    resultado = verificar( interface, porta, ip,user, password)
    
    # print(resultado)
 
    return resultado

if __name__ == '__main__':
    motivo_da_queda()