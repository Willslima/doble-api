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

  function chamada(oltID){
    axios
      .post(`http://127.0.0.1:5000/verifica-caixa/${oltID}`, { nome: cliente })
      .then(function (response) {

        response.data.forEach(grupo => {
          grupo.forEach(el => {
            let elementoPai = document.getElementById('retorno')
            // elementoPai.innerHTML = ''
            let elemento = document.createElement('p')
            elemento.textContent = el
            if (elemento.textContent.includes('online')) {
              elemento.className = 'bg-success text-white'
            } else if (elemento.textContent.includes('offline')) {
              elemento.className = 'bg-danger text-white'
            } 

            //the total of ONTs are
            elementoPai.appendChild(elemento)
          })
                    
      })

      })
      .catch(function (err) {
        console.log(err)
      })

  }

  chamada(0)
  chamada(1)
  chamada(2)
  chamada(3)

}
