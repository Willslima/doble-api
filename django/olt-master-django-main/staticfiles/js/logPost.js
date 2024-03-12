function logPost() {
  let p = document.getElementById('registros')
  p.innerHTML = ''
  axios
    .get('http://127.0.0.1:5000/logs-admin/post')
    .then(function (response) {
      let resposta = response.data
      console.log(resposta)
      let quantidadeItem = document.getElementById('qtds').value
      const tamanhoDaPagina = parseInt(quantidadeItem)
      const dadosInvertidos = [...resposta].reverse();
      let paginaAtual = 1

      function paginar(resposta, paginaAtual, tamanhoDaPagina) {
        const inicio = (paginaAtual - 1) * tamanhoDaPagina
        const fim = inicio + tamanhoDaPagina
        return resposta.slice(inicio, fim)
      }

      function exibirDados() {
        const dadosDaPagina = paginar(dadosInvertidos, paginaAtual, tamanhoDaPagina)
        let p = document.getElementById('registros')
        p.innerHTML = ''
        // Renderize dadosDaPagina no seu HTML
        dadosDaPagina.forEach(item => {
          var colDiv = document.createElement('div')
          colDiv.className = 'col-sm-12 mb-3 mb-sm-0 mt-1'

          var cardDiv = document.createElement('div')
          cardDiv.className = 'card'

          var cardBodyDiv = document.createElement('div')
          cardBodyDiv.className = 'card-body'

          var cardTitle = document.createElement('h5')
          cardTitle.className = 'card-title'
          cardTitle.textContent = item.route + ' ' + item.timestamp

          var cardText = document.createElement('p')
          cardText.className = 'card-text'
          cardText.textContent = item.response

          cardBodyDiv.appendChild(cardTitle)
          cardBodyDiv.appendChild(cardText)

          cardDiv.appendChild(cardBodyDiv)
          colDiv.appendChild(cardDiv)

          p.appendChild(colDiv)
        })
      }

      document.getElementById('proximo').addEventListener('click', () => {
        paginaAtual++
        exibirDados()
      })

      document.getElementById('anterior').addEventListener('click', () => {
        paginaAtual = Math.max(1, paginaAtual - 1)
        exibirDados()
      })

      // Inicialize a visualização
      exibirDados()
    })
    .catch(function (err) {
      console.log(err)
    })
}
