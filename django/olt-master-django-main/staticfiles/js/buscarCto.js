document.getElementById("inputCB").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-queda").click();
  }
});
document.getElementById("inputFP").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-queda").click();
  }
});
document.getElementById("inputCX").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-queda").click();
  }
});

function buscarCto() {
  let cb = document.getElementById('inputCB').value
  let fp = document.getElementById('inputFP').value
  let cx = document.getElementById('inputCX').value

  let cliente = `CB${cb}_FP${fp}_CX${cx}`
  let retorno = document.getElementById('retorno')
  retorno.innerHTML = 'Buscando cto... Por favor, aguarde...'

  axios
    .post('http://127.0.0.1:5000/verifica-caixa', { nome: cliente })
    .then(function (response) {
      let elementoPai = document.getElementById('retorno')
      elementoPai.innerHTML = ''
      response.data.forEach(grupo => {
        // Agora, lidar com as outras linhas
        for (let i = 0; i < grupo[0].length; i++) {
          let linha1 = grupo[0][i] // Linha do primeiro subarray
          let linha2 = grupo[1][i] // Linha do segundo subarray

          // Criar um elemento p
          let elemento = document.createElement('p')
          elemento.textContent = linha1 + ' | ' + linha2 // Combinar as duas linhas

          // Adicionar classes com base no status
          if (elemento.textContent.includes('online')) {
            elemento.className = 'bg-success text-white'
          } else if (elemento.textContent.includes('offline')) {
            elemento.className = 'bg-danger text-white'
          }

          // Adicionar o elemento ao elemento pai
          elementoPai.appendChild(elemento)
        }

        // Primeiro, lidar com a linha 'In port'
        if (grupo[2].length > 0) {
          let linhaInPort = grupo[2][0]
          let elementoInPort = document.createElement('p')
          elementoInPort.textContent = linhaInPort
          elementoPai.appendChild(elementoInPort)
        }
      })
    })
    .catch(function (err) {
      console.log(err)
    })
}
