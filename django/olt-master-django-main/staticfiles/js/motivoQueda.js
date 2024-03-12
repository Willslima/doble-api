document.getElementById("inputNome").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-buscar").click();
  }
});


function motivoDaQueda() {
  alert('Aguarde enquanto verificamos')
  let selecionado = document.querySelector('select').value
  selecionado = selecionado.replace(/\/\s(\d)/g, '/$1')

  let dados = {
    nome: 'CLIENTE_TESTE',
    cliente_selecinado: selecionado
  }

  axios
    .post('http://127.0.0.1:5000/motivo_da_queda', dados)
    .then(function (response) {
        let motivoQueda = document.getElementById('retorno-mtv-queda')
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
