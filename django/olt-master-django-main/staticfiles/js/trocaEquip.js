document.getElementById("inputNome").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-troca-eqp").click();
  }
});

function trocaEquip() {
  let cliente = document.getElementById('clientes').value
  cliente = cliente.replace(/\/\s(\d)/g, '/$1')
  cliente = cliente.replace(/\s{2,}/g, ' ')
  cliente = cliente.split(' ')

  let interface = cliente[1]
  let ontId = cliente[2]
  let ip = cliente[12]
  let equipamento = document.getElementById('equipamentos').value
  equipamento = equipamento.split(' ')
  let tipoEquipamento = document.getElementById('ont-onu').value

  const data = {
    interface: interface,
    ont_id: ontId,
    'tipo-equipamento': tipoEquipamento,
    novo_equip: equipamento[0],
    ip: ip
  }
  let retorno = (document.getElementById('retorno').innerHTML =
    'Realizando a troca do equipamento')

  axios
    .post('http://127.0.0.1:5000/troca-equipamento', data)
    .then(function (response) {
      let retorno = (document.getElementById('retorno').innerHTML =
        response.data)
    })
    .catch(function (err) {
      console.log(err)
    })
  // console.log(data)
}
