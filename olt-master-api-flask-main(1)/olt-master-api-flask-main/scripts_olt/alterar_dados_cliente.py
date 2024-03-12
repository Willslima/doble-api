from data.data import usuario
import time
import paramiko

def alterar_dados(nome, dados, cto):
    interface, porta, nome_dados, itfc2, pt2, sn, active, status, normal, match, no, ip = dados.split()
    user = usuario['user']
    password = usuario['password']

    def alterando(interface, porta, nome, nome_dados, ip, user, password, cto):

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

            if len(nome) == 0:
                channel.send(f'ont modify {itfc[2]} {porta} desc {nome_dados+cto}\n\n')
                time.sleep(0.5)
            else:
                channel.send(f'ont modify {itfc[2]} {porta} desc {nome+cto}\n\n')
                time.sleep(0.5)

            full_output = ""
            prompt = f"(config-if-gpon-{itfc[0]}/{itfc[1]})#"

            while True:
                while channel.recv_ready():
                    time.sleep(1)
                    output = channel.recv(4096).decode()
                    full_output += output
                    # print(full_output)
                if full_output.strip().endswith(prompt):
                    break

            channel.close()
            client.close()

            return 'Alteração realizada com Sucesso !'

        except Exception as e:
            return 'Algo deu errado na alteração',e
        
    resultado = alterando( interface, porta, nome, nome_dados, ip,user, password, cto)
     
    return resultado

if __name__ == '__main__':
    alterar_dados()