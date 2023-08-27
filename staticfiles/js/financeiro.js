django.jQuery().ready(function(){
    checkAllEstorno();
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
