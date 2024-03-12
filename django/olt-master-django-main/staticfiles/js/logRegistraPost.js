function registraProvisionamento() {
  let rota = '/provisionamento'
  let usuario = document.getElementById('nome_usuario').innerHTML
  let inputNome = document.getElementById('inputNome').value
  let equipSelecionado = document.getElementById('equipamentos').value
  let ontOnu = document.getElementById('ont-onu').value
  let cb = document.getElementById('inputCB').value
  let fp = document.getElementById('inputFP').value
  let cx = document.getElementById('inputCX').value
  let fs = document.getElementById('inputFS').value

  let data = {
    usuario_logado: usuario,
    rota_link: rota,
    nome_cliente: inputNome,
    equipamento: equipSelecionado,
    ont_onu: ontOnu,
    cb: cb,
    fp: fp,
    cx: cx,
    fs: fs
  }

  axios
    .post('http://127.0.0.1:5000/logs-admin/reg-provisionamento', data)
    .then(function (response) {
      console.log(response.data)
    })
    .catch(function (err) {
      console.log(err)
    })
}

function getRegistraProvisionamento() {
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-provisionamento-get')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'Nome do cliente: ' + item.nome_cliente

        let cardText1 = document.createElement('p')
        cardText1.className = 'card-text'
        cardText1.textContent =
          'CB: ' +
          item.cb +
          ' FP: ' +
          item.fp +
          ' CX: ' +
          item.cx +
          ' FS: ' +
          item.fs

        let cardText2 = document.createElement('p')
        cardText2.className = 'card-text'
        cardText2.textContent = 'Equipamento: ' + item.equipamento

        let cardText3 = document.createElement('p')
        cardText3.className = 'card-text'
        cardText3.textContent = 'Tipo de equipamento: ' + item.ont_onu

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText1)
        cardBodyDiv.appendChild(cardText2)
        cardBodyDiv.appendChild(cardText3)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}

function registraStatusDoCliente() {
  let rota = '/status'
  let usuario = document.getElementById('nome_usuario').innerHTML
  let inputNome = document.getElementById('inputNome').value
  let clientes = document.getElementById('clientes').value

  let data = {
    usuario_logado: usuario,
    rota_link: rota,
    nome_cliente: inputNome,
    cliente_selecionado: clientes
  }

  axios
    .post('http://127.0.0.1:5000/logs-admin/reg-status', data)
    .then(function (response) {
      console.log(response.data)
    })
    .catch(function (err) {
      console.log(err)
    })
}

function getRegistraStatusDoCliente() {
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-status-get')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'Cliente pesquisado: ' + item.nome_cliente

        let cardText2 = document.createElement('p')
        cardText2.className = 'card-text'
        cardText2.textContent =
          'Cliente Selecionado: ' + item.cliente_selecionado

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText2)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}

function registraVerificacaoSinal() {
  let rota = '/sinal'
  let usuario = document.getElementById('nome_usuario').innerHTML

  let inputNome = document.getElementById('inputNome').value
  let clientes = document.getElementById('clientes').value

  let data = {
    usuario_logado: usuario,
    rota_link: rota,
    nome_cliente: inputNome,
    cliente_selecionado: clientes
  }

  console.log(data)
  axios
    .post('http://127.0.0.1:5000/logs-admin/reg-sinal', data)
    .then(function (response) {
      console.log(response.data)
    })
    .catch(function (err) {
      console.log(err)
    })
}

function getRegistraVerificacaoSinal(){
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-sinal-get')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'Cliente pesquisado: ' + item.nome_cliente

        let cardText2 = document.createElement('p')
        cardText2.className = 'card-text'
        cardText2.textContent =
          'Cliente Selecionado: ' + item.cliente_selecionado

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText2)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}

function registraAlteracaoDados() {
  let rota = '/alterar-dados'
  let usuario = document.getElementById('nome_usuario').innerHTML

  let inputNome = document.getElementById('inputNome').value
  let clienteSelecionado = document.getElementById('clientes').value
  let novaDesc = document.getElementById('inputNovaDesc').value
  let cb = document.getElementById('inputCB').value
  let fp = document.getElementById('inputFP').value
  let cx = document.getElementById('inputCX').value
  let fs = document.getElementById('inputFS').value

  let data = {
    usuario_logado: usuario,
    rota_link: rota,
    nome_cliente: inputNome,
    cliente_selecionado: clienteSelecionado,
    nova_desc: novaDesc,
    cb: cb,
    fp: fp,
    cx: cx,
    fs: fs
  }

  axios
    .post('http://127.0.0.1:5000/logs-admin/reg-altera-dados', data)
    .then(function (response) {
      console.log(response.data)
    })
    .catch(function (err) {
      console.log(err)
    })
}

function getRegistraAlteracaoDados(){
  let p = document.getElementById('registros')
  p.innerHTML = ''

  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-altera-dados-get')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'Nome do cliente: ' + item.nome_cliente

        let cardText1 = document.createElement('p')
        cardText1.className = 'card-text'
        cardText1.textContent =
          'CB: ' +
          item.cb +
          ' FP: ' +
          item.fp +
          ' CX: ' +
          item.cx +
          ' FS: ' +
          item.fs

        let cardText2 = document.createElement('p')
        cardText2.className = 'card-text'
        cardText2.textContent = 'Cliente selecionado: ' + item.cliente_selecionado

        let cardText3 = document.createElement('p')
        cardText3.className = 'card-text'
        cardText3.textContent = 'Nova descrição: ' + item.nova_desc

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText2)
        cardBodyDiv.appendChild(cardText3)
        cardBodyDiv.appendChild(cardText1)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}

function registraDeletarCliente() {
  let rota = '/excluir'
  let usuario = document.getElementById('nome_usuario').innerHTML
  let inputNome = document.getElementById('inputNome').value
  let clientes = document.getElementById('clientes').value

  let data = {
    "usuario_logado":usuario,
    "rota_link":rota,
    "nome_cliente":inputNome,
    "cliente_selecionado":clientes
  }

  axios.post('http://127.0.0.1:5000/logs-admin/reg-exclusao',data).then(function(response){
    console.log(response.data)
  }).catch(function(err){
    console.log(err)
  })
}

function getRegistraDeletarCliente(){
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-exclusao-get')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'Cliente pesquisado: ' + item.nome_cliente

        let cardText2 = document.createElement('p')
        cardText2.className = 'card-text'
        cardText2.textContent =
          'Cliente Selecionado: ' + item.cliente_selecionado

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText2)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}

function registraTrocaEquipamento() {
  let rota = '/troca-equipamento'
  let usuario = document.getElementById('nome_usuario').innerHTML
  let inputNome = document.getElementById('inputNome').value
  let clientes = document.getElementById('clientes').value
  let equipamentos = document.getElementById('equipamentos').value
  let tipoEquipamento = document.getElementById('ont-onu').value

  let data =
    {
      "usuario_logado":usuario,
      "rota_link":rota,
      "nome_cliente":inputNome,
      "cliente_selecionado":clientes,
      "equipamento_selecionado":equipamentos,
      "tipo_equipamento":tipoEquipamento
    }
  

  axios.post('http://127.0.0.1:5000/logs-admin/reg-troca-equip',data).then(function(response){
    console.log(response.data)
  }).catch(function(err){
    console.log(err)
  })
}

function getRegistraTrocaEquipamento(){
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-troca-equip-get')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'Cliente pesquisado: ' + item.nome_cliente

        let cardText1 = document.createElement('p')
        cardText1.className = 'card-text'
        cardText1.textContent = 'Equipamento selecionado: ' + item.equipamento_selecionado

        let cardText3 = document.createElement('p')
        cardText3.className = 'card-text'
        cardText3.textContent = 'Tipo do equipamento: ' + item.tipo_equipamento

        let cardText2 = document.createElement('p')
        cardText2.className = 'card-text'
        cardText2.textContent =
          'Cliente Selecionado: ' + item.cliente_selecionado

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText1)
        cardBodyDiv.appendChild(cardText3)
        cardBodyDiv.appendChild(cardText2)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}

function registraBuscaCto() {
  let rota = '/verificar-caixa'
  let usuario = document.getElementById('nome_usuario').innerHTML
  let cb = document.getElementById('inputCB').value
  let fp = document.getElementById('inputFP').value
  let cx = document.getElementById('inputCX').value

  let cliente = `CB${cb}_FP${fp}_CX${cx}`


  let data = {
    "usuario_logado":usuario,
    "rota_link":rota,
    "cto_pesquisada":cliente,
  }

  axios.post('http://127.0.0.1:5000/logs-admin/reg-pesquisa-cto',data).then(function(response){
    console.log(response.data)
  }).catch(function(err){
    console.log(err)
  })
}

function getRegistraBuscaCto(){
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/reg-pesquisa-cto-get')
    .then(function (response) {
      let resposta = response.data
      // console.log(resposta)

      resposta.forEach(item => {
        let colDiv = document.createElement('div')
        colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

        let cardDiv = document.createElement('div')
        cardDiv.className = 'card'

        let cardBodyDiv = document.createElement('div')
        cardBodyDiv.className = 'card-body'

        let cardTitle = document.createElement('h5')
        cardTitle.className = 'card-title'
        cardTitle.textContent = item.rota_link + ' - ' + item.timestamp

        let cardText0 = document.createElement('p')
        cardText0.className = 'card-text'
        cardText0.textContent = 'CTO pesquisada: ' + item.cto_pesquisada

        let cardText4 = document.createElement('p')
        cardText4.className = 'card-text'
        cardText4.textContent = 'Usuário: ' + item.usuario_logado

        cardBodyDiv.appendChild(cardTitle)
        cardBodyDiv.appendChild(cardText0)
        cardBodyDiv.appendChild(cardText4)

        cardDiv.appendChild(cardBodyDiv)
        colDiv.appendChild(cardDiv)

        p.appendChild(colDiv)
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}