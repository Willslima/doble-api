function verificaClientesOffline() {
  let equipamento = document.querySelector('select').value
  equipamento = equipamento.replace(/\/\s(\d)/g, '/$1')

  let dados_tratados = equipamento.split(' ')

  let dados = {
    itfc: dados_tratados[2].split('/'),
    hostname: dados_tratados[3]
  }

  axios
    .post('http://127.0.0.1:5000/upper_limit', dados)
    .then(function (response) {
      function preencherSelect(data) {
        let select = document.getElementById('cliente-lista')

        // Limpa todas as opções existentes
        select.innerHTML = ''

        // Itera sobre os dados recebidos e adiciona as opções ao select
        for (let i = 0; i < data.length; i++) {
          let option = document.createElement('option')
          option.setAttribute('value', data[i])
          let dadosSplitados = data[i].replace(/\/\s(\d)/g, '/$1')
          dadosSplitados = dadosSplitados.split(' ')

          let nomeDoCliente = dadosSplitados.filter(item => item.includes('_'))

          option.text = nomeDoCliente
          select.add(option)
        }
      }

      preencherSelect(response.data)
    })
    .catch(function (err) {
      console.log(err)
    })
}

function excluirCliente() {
  let confirmaAcao = confirm(
    'Tem certeza que deseja excluir o cliente selecionado ?'
  )
  let select = document.getElementById('cliente-lista')
  let opcaoSelecionada = select.value
  let retorno = document.getElementById('retorno-modal')
  retorno.innerHTML = ''
  opcaoSelecionada = opcaoSelecionada.replace(/\/\s(\d)/g, '/$1')
  
  let data = {
    nome: 'NOME_TESTE',
    cliente_selecinado: opcaoSelecionada
  }

  if (confirmaAcao) {
    document.getElementById('retorno-modal').innerHTML = 'Excluindo cliente...'
    console.log(data)
    axios
      .post('http://127.0.0.1:5000/excluir_cliente', data)
      .then(function (response) {
        // Exibir parte do resultado no HTML
        console.log(response)
        document.getElementById('retorno-modal').innerHTML = response.data
      })
      .catch(function (error) {
        document.getElementById('retorno-modal').innerHTML = error
      })
  }
}

function verificaUltimaQueda(){
  let select = document.getElementById('cliente-lista')
  let opcaoSelecionada = select.value
  let retorno = document.getElementById('retorno-modal')
  retorno.innerHTML = 'Verificando...'
  opcaoSelecionada = opcaoSelecionada.replace(/\/\s(\d)/g, '/$1')
  
  let data = {
    nome: 'NOME_TESTE',
    cliente_selecinado: opcaoSelecionada
  }

  axios 
  .post('http://127.0.0.1:5000/motivo_da_queda', data)
  .then(function (response) {
      let motivoQueda = document.getElementById('retorno-modal')
      motivoQueda.innerHTML = "" 
      for(item of response.data){
          let p = document.createElement('p')
          p.append(item)
          motivoQueda.append(p)
      } 
  })
  .catch(function (err) {
    console.log(err)
  })

}