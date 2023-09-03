django.jQuery().ready(function(){
    loadMunicipios(django.jQuery("#id_estado").val());
    django.jQuery("#id_estado").on('change', function(e) {
        loadMunicipios(e.target.value);
    });
    
    django.jQuery("#cep-search").on('click', function(e) {
        let cep = django.jQuery("#id_cep").val()
        if (cep) {
            consultaCep(cep)
        }
    });
  
});

async function consultaCep(cep) {
    await django.jQuery.ajax({
        method: 'get',
        url: '/api/consulta/cep/'+cep,
        success: (res) => {
            if (res) {
                django.jQuery("#id_endereco").val(res.logradouro);
                django.jQuery("#id_bairro").val(res.bairro);
                django.jQuery("#id_complemento").val(res.complemento);
                django.jQuery("#id_estado option").filter((_, a) => { 
                    return django.jQuery(a).text() == res.uf 
                }).prop("selected", true);

                django.jQuery("#id_municipio option").remove();
                res.municipios.forEach((e) => {
                    django.jQuery("#id_municipio").append(`
                        <option ${e.selected ? 'selected' : ''}
                            value=${e.id}>${e.nome}
                        </option>
                    `);
                })

                django.jQuery("#id_numero").focus();
            }

        }
    })
}


/**
 * Carrega os municipios conforme
 * o estado informado por parametro
 * @param {int} estado 
 */
async function loadMunicipios(estado) {
    let municipioSelected = django.jQuery("#id_municipio").val();
    let pk = django.jQuery("#id").val();
     django.jQuery("#id_municipio option").remove();
    if (estado != "" && estado != undefined) {
       await django.jQuery.ajax({
            method: 'get',
            url: '/api/municipios/'+estado,
            success: (res) => {
                data = JSON.parse(res);
                data.forEach(m => {
                    if (pk == "")
                    {
                        django.jQuery("#id_municipio").append(`
                            <option ${m.fields.capital ? 'selected' : ''}
                                value=${m.pk}>${m.fields.nome}
                            </option>
                        `);
                    }
                    else {
                        django.jQuery("#id_municipio").append(`
                            <option ${municipioSelected == m.pk ? 'selected' : ''}
                                value=${m.pk}>${m.fields.nome}
                            </option>
                        `);
                    }
                });

                if (data.length == 0){
                    django.jQuery("#id_municipio").append("<option value>---------</option>");
                }
            }
        });
    } else {
        django.jQuery("#id_municipio").append("<option value>---------</option>");
    }
}
