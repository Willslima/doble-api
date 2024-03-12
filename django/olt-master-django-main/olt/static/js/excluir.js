document.getElementById("inputNome").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-buscar").click();
  }
});

function getNome() {
  let nome = document.getElementById('inputNome').value

  function converterParaNormal(nome) {
    return nome.normalize('NFD')
      .replace(/[\u0300-\u036f]/g, "")  // Remove acentos
      .replace(/Ø/g, "O")              // Substitui 'Ø' por 'O'
      // Adicione mais substituições aqui, se necessário
}

let nomeOriginal = nome
let nomeConvertido = converterParaNormal(nomeOriginal)

  let select = document.getElementById('clientes')

  // Limpa todas as opções existentes
  select.innerHTML = ''
  let option = document.createElement('option')
  option.text = 'Pesquisando ... '
  select.add(option)

  let data = {
    nome: nomeConvertido
  }

  function getClientes(data) {
    let select = document.getElementById('clientes')

    // Limpa todas as opções existentes
    select.innerHTML = 'Pesquisando ... '
    let option = document.createElement('option')
    option.textContent = 'Clique para ver os clientes'
    select.add(option)

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

  function excluirCliente() {
    const select = document.getElementById('clientes')
    select.addEventListener('change', function () {
      let opcaoSelecionada = select.value
      let retorno = document.getElementById('retorno')
      retorno.innerHTML = ''
      opcaoSelecionada = opcaoSelecionada.replace(/\/\s(\d)/g, '/$1')
      // retorno.innerHTML = opcaoSelecionada
      let data = {
        nome: 'NOME_TESTE',
        cliente_selecinado: opcaoSelecionada
      }
      
      const buttonSim = document.getElementById('btn-sim')
      buttonSim.addEventListener('click',function(){
        let opcao = confirm("Tem certeza que deseja excluir o cliente selecionado?")
        if(opcao){
          document.getElementById('retorno').innerHTML = 'Excluindo equipamento'
        axios
        .post('http://127.0.0.1:5000/excluir_cliente', data)
        .then(function (response) {
          // Exibir parte do resultado no HTML
          console.log(response)
          document.getElementById('retorno').innerHTML = response.data
        })
        .catch(function (error) {
          document.getElementById('retorno').innerHTML = error
        })
      }
      })
    })
  }

  excluirCliente()

}
