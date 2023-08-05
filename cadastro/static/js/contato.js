django.jQuery().ready(function(){
    loadMunicipios(django.jQuery("#id_estado").val());
    django.jQuery("#id_estado").on('change', function(e) {
        loadMunicipios(e.target.value);
    });
   
});

/**
 * Carrega os municipios conforme
 * o estado informado por parametro
 * @param {int} estado 
 */
function loadMunicipios(estado) {
    let municipioSelected = django.jQuery("#id_municipio").val();
     django.jQuery("#id_municipio option").remove();
    if (estado != "" && estado != undefined) {
        django.jQuery.ajax({
            method: 'get',
            url: '/api/municipios/'+estado,
            success: (res) => {
                data = JSON.parse(res);
                data.forEach(m => {
                    if (municipioSelected == "")
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