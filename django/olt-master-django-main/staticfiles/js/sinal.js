document.getElementById("inputNome").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-buscar").click();
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
    
    chamada(0)// Fazer a requisição HTTP usando o Axios
    chamada(1)// Fazer a requisição HTTP usando o Axios
    chamada(2)// Fazer a requisição HTTP usando o Axios
    chamada(3)// Fazer a requisição HTTP usando o Axios
  }getClientes(data)

  function getSinal() {
    const select = document.getElementById('btn-verificar-sinal')
    select.addEventListener('click', function () {
      const cliente = document.getElementById('clientes')
      let opcaoSelecionada = cliente.value
      let retorno = document.getElementById('retorno')
      retorno.innerHTML = ''
      opcaoSelecionada = opcaoSelecionada.replace(/\/\s(\d)/g, '/$1')
      // retorno.innerHTML = opcaoSelecionada
      let data = {
        nome: 'NOME_TESTE',
        cliente_selecinado: opcaoSelecionada
      }
      let verificacao = confirm('Deseja verificar o Sinal?')
      if(verificacao){
      axios
        .post('http://127.0.0.1:5000/verificar_sinal', data)
        .then(function (response) {
          // Exibir parte do resultado no HTML
          console.log(response)
          document.getElementById('retorno').innerHTML = response.data
        })
        .catch(function (error) {
          console.error(error)
        })
      } else {
        alert('A verificação foi cancelada !')
      }
    })
  }

  getSinal()

}
