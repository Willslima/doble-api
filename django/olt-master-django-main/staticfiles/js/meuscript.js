document.getElementById("inputNome").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-provisionar").click();
  }
});
document.getElementById("inputCB").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-provisionar").click();
  }
});
document.getElementById("inputFP").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-provisionar").click();
  }
});
document.getElementById("inputCX").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-provisionar").click();
  }
});
document.getElementById("inputFS").addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("btn-provisionar").click();
  }
});

function getEquipamentos() {
  // Fazer a requisição HTTP usando o Axios
  let select = document.getElementById('equipamentos')
  
  // Limpa todas as opções existentes
  select.innerHTML = ''

  function chamada(oltID){

    axios
      .get(`http://127.0.0.1:5000/equipamentos/${oltID}`)
      .then(function (response) {
        // Exibir parte do resultado no HTML
        console.log(response)
  
        function preencherSelect(data) {
          let select = document.getElementById('equipamentos')
  
          // Limpa todas as opções existentes
          //select.innerHTML = ''
  
          // Itera sobre os dados recebidos e adiciona as opções ao select
          for (let i = 0; i < data.length; i++) {
            let option = document.createElement('option')
            option.setAttribute('value', data[i])
  
            partes = data[i].split(")", 1)
            resultado = partes[0]
            option.text = resultado + ")"
            select.add(option)
          }
        }
  
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

function provisiona(){
    let nomeDoCliente = document.getElementById('inputNome').value

    function converterParaNormal(nome) {
      return nome.normalize('NFD')
                 .replace(/[\u0300-\u036f]/g, "")  // Remove acentos
                 .replace(/Ø/g, "O")              // Substitui 'Ø' por 'O'
                 // Adicione mais substituições aqui, se necessário
  }
  
  let nomeOriginal = nomeDoCliente
  let nomeConvertido = converterParaNormal(nomeOriginal)

    let equipamentos = document.getElementById('equipamentos').value
    let cabo = document.getElementById('inputCB').value
    let fibraPri = document.getElementById('inputFP').value
    let caixa = document.getElementById('inputCX').value
    let fibraSec = document.getElementById('inputFS').value

    let tipoEquipamento = document.getElementById('ont-onu').value
    

    let confirmacao = confirm("Provisionando equipamento, por favor aguarde")
    

    let data = {
        "nome": nomeConvertido,
        "equipamento":equipamentos,
        "cto":[cabo,fibraPri,caixa,fibraSec],
        "tipo-equipamento": tipoEquipamento
        }

        if(confirmacao){

        let retornoSpan = document.querySelector('textarea')
        retornoSpan.innerHTML = 'Provisionando'

        axios.post("http://127.0.0.1:5000/provisionamento", data)
        .then(function(response) {
            console.log("Resposta do servidor:", response.data);
            // Faça algo com a resposta do servidor, se necessário
            let retornoSpan = document.querySelector('textarea')
            retornoSpan.innerHTML = response.data
            let equipamentos = document.getElementById('equipamentos')
            equipamentos.innerHTML = '' 
            
        })
        .catch(function(error) {
            console.error("Erro:", error);
        });
      } else {
        let retornoSpan = document.querySelector('textarea')
        retornoSpan.innerHTML = 'Provisionamento cancelado'
      }
}

