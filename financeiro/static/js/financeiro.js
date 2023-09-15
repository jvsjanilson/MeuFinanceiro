django.jQuery().ready(function(){
    checkAllEstorno();
    django.jQuery("#id_valor_juros, #id_valor_multa, #id_valor_desconto").bind('change click',(e) => {
        comp = ['id_valor_juros','id_valor_multa', 'id_valor_desconto'].filter((i) => i != e.target.id)
        
        if (e.target.value == "") {
            e.target.value = 0.0
        }
        let soma = 0;
        soma = somaValores(comp)
        if (e.target.value > 0 || soma > 0)
        {
            django.jQuery("#id_valor_pago").prop("readonly", true)
            django.jQuery("#id_valor_pago").css("background-color", "#e9ecef")
            django.jQuery("#id_valor_pago").val(
                
            parseFloat( django.jQuery("#id_saldo_pagar").val())+
            parseFloat( django.jQuery("#id_valor_juros").val()) +
            parseFloat( django.jQuery("#id_valor_multa").val()) -
            parseFloat( django.jQuery("#id_valor_desconto").val()) 
            )

        } else {
            e.target.value = 0.0
            django.jQuery("#id_valor_pago").css("background-color", "white")
            django.jQuery("#id_valor_pago").val(
                
                parseFloat( django.jQuery("#id_saldo_pagar").val())+
                parseFloat( django.jQuery("#id_valor_juros").val()) +
                parseFloat( django.jQuery("#id_valor_multa").val()) -
                parseFloat( django.jQuery("#id_valor_desconto").val()) 
                )
            django.jQuery("#id_valor_pago").prop("readonly", false)
        }
    })
});

/**
 * No estorno add um click no check-total, para marcar ou
 * desmarcar os titulos que serao estornados 
 */
function checkAllEstorno() {
    django.jQuery("#ckeck-total").click((e) => {
        django.jQuery("input[name=check]").prop("checked", e.target.checked);
    });
}

function somaValores(listaValores) {
    return listaValores.reduce((a,b) => {
        let valor = parseFloat(django.jQuery(`#${b}`).val())
        if (isNaN(valor)) {
            valor = 0
        }
        return a + valor
    },0)
}



