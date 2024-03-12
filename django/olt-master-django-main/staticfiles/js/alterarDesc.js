document.getElementById("inputNome").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-buscar").click();
  }
});
document.getElementById("inputNovaDesc").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-alterar").click();
  }
});
document.getElementById("inputCB").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-alterar").click();
  }
});
document.getElementById("inputFP").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-alterar").click();
  }
});
document.getElementById("inputCX").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-alterar").click();
  }
});
document.getElementById("inputFS").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-alterar").click();
  }
});


function getNome() {
    let nome = document.getElementById('inputNome').value
    let select = document.getElementById('clientes')
  
    // Limpa todas as opções existentes
    select.innerHTML = ''
    let option = document.createElement('option')
    option.text = 'Pesquisando ... '
    select.add(option)
  
    let data = {
      nome: nome
    }
  
    function getClientes(data) {
      let select = document.getElementById('clientes')
  
      // Limpa todas as opções existentes
      select.innerHTML = 'Pesquisando ... '
  
      function chamada(oltId){
        axios
          .post(`http://127.0.0.1:5000/clientes/${oltId}`, data)
          .then(function (response) {
            // Exibir parte do resultado no HTML
            console.log(response)
            
            function preencherSelect(data) {
              let select = document.getElementById('clientes')
    
              // Limpa todas as opções existentes
              // select.innerHTML = ''
              // let option = document.createElement('option')
              // option.text = '... Pesquisa concluída'
              // select.add(option)
              // Itera sobre os dados recebidos e adiciona as opções ao select
              for (let i = 0; i < data.length; i++) {
                let option = document.createElement('option')
                option.setAttribute('value', data[i])
                partes = data[i].split(' ')
                let dadosArray = []
    
                for (let item of partes) {
                  if (item.includes('_')) dadosArray.push(item)
                  if (item.includes('online')) dadosArray.push(item)
                  if (item.includes('offline')) dadosArray.push(item)
                }
                option.text = dadosArray[0] + ' ' + dadosArray[1]
                select.add(option)
              }
            }
    
            const select = document.getElementById('clientes')
            select.addEventListener('change', function () {
              const opcaoSelecionada = select.value
              let retorno = document.getElementById('retorno')
              retorno.innerHTML = ''
              opcaoSelecionada.includes('online')
                ? (retorno.innerHTML = 'Online')
                : (retorno.innerHTML = 'Offline')
            })
            preencherSelect(response.data)
          })
          .catch(function (error) {
            console.error(error)
          })
      }
      
      chamada(0)
      chamada(1)
      chamada(2)
      chamada(3)
    }
    getClientes(data)
  
  }
  
function fazAlteracao(){
    const select = document.getElementById('clientes')
    let opcaoSelecionada = select.value
    opcaoSelecionada = opcaoSelecionada.replace(/\/\s(\d)/g, '/$1')

    let novoNome = document.getElementById('inputNovaDesc').value
    let novoCabo = document.getElementById('inputCB').value
    let novaFpri = document.getElementById('inputFP').value
    let novaCaixa = document.getElementById('inputCX').value
    let novaFsec = document.getElementById('inputFS').value

    const data = {
        "nome": novoNome,
     "cliente_selecinado": opcaoSelecionada,
        "cto": [novoCabo,novaFpri,novaCaixa,novaFsec]
    }

    let retorno = document.getElementById('retorno')
    retorno.innerHTML = "Realizando alterações, por favor aguarde"

    axios
        .post("http://127.0.0.1:5000/alterar_dados", data)
        .then(function(response){

            retorno.innerHTML = ""
            retorno.innerHTML = response.data
        })
        .catch(function(err){
            console.log(err)
        })
    
}