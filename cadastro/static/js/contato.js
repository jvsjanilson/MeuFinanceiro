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

     django.jQuery("#cpfcnpj-search").on('click', function(e) {

        let cnpj = django.jQuery("#id_cpf_cnpj").val()
        if (cnpj) {
            ( cnpj != "" && cnpj.length == 14) ?  consultaCnpj(cnpj) : alert('Informe um cnpj');

        } else {
            alert('Informe um cnpj');
        }
    });
  
});

function consultaCnpj(cnpj) {
    django.jQuery.ajax({
        method: 'get',
        url: '/api/consulta/cnpj/'+cnpj,
        success: (res) => {

            if (res) {
                django.jQuery("#id_razao_social").val(res.razao_social);
                django.jQuery("#id_bairro").val(res.estabelecimento.bairro);
                django.jQuery("#id_cep").val(res.estabelecimento.cep);
                django.jQuery("#id_endereco").val(`${res.estabelecimento.tipo_logradouro} ${res.estabelecimento.logradouro}`);
                django.jQuery("#id_numero").val(res.estabelecimento.numero);
                django.jQuery("#id_nome_fantasia").val(res.estabelecimento.nome_fantasia);
                django.jQuery("#id_email").val(res.estabelecimento.email);
                if (res.estabelecimento.ddd1 != null && res.estabelecimento.telefone1 != null)
                    django.jQuery("#id_fone").val(`(${res.estabelecimento.ddd1}) ${res.estabelecimento.telefone1}`);
                django.jQuery("#id_municipio").val(res.estabelecimento.cidade.cidade_pk);
                django.jQuery("#id_estado option").each((_, e) =>  {
                    if (e.innerText == res.estabelecimento.estado.sigla)
                        django.jQuery(e).prop("selected","selected");
                });
                loadMunicipios(django.jQuery("#id_estado").val(), res.estabelecimento.cidade.cidade_pk);


            }
        }
    })
}

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
async function loadMunicipios(estado, municipio = undefined) {

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
                        if (municipio == undefined) {
                            django.jQuery("#id_municipio").append(`
                               <option ${m.fields.capital ? 'selected' : ''}
                                    value=${m.pk}>${m.fields.nome}
                                </option>
                            `);
                        } else {
                            if (Number.isInteger(municipio)) {
                                 django.jQuery("#id_municipio").append(`
                                    <option ${municipio == m.pk ? 'selected' : ''}
                                        value=${m.pk}>${m.fields.nome}
                                    </option>
                                `);
                            }
                        }

                    }
                    else {
                        console.log(municipio)
                        if (municipio == undefined) {
                             django.jQuery("#id_municipio").append(`
                               <option ${m.fields.capital ? 'selected' : ''}
                                    value=${m.pk}>${m.fields.nome}
                                </option>
                            `);
                        }
                        else {
                            django.jQuery("#id_municipio").append(`
                                <option ${municipio == m.pk ? 'selected' : ''}
                                    value=${m.pk}>${m.fields.nome}
                                </option>
                            `);
                        }
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
