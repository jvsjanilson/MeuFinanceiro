django.jQuery().ready(function(){
    removeErrorElementos();

    setTimeout(function(){
        django.jQuery(".alert").fadeOut("slow", function(){
            $(this).alert("close");
        });
    },3000);
});

/**
 * Remove os erros dos elementos caso 
 * o usuario preencha com algum valor
 */
function removeErrorElementos() {

    django.jQuery("input, select").each((_, e)=> {
        django.jQuery(e).change((el) => {
            if (django.jQuery(el.target).hasClass('is-invalid'))
            {
                if (django.jQuery(el.target).val() != "" ) {
                    django.jQuery(el.target).removeClass('is-invalid');
                    django.jQuery(el.target).parent().find('.errorlist').remove();
                }
            }
        });
    });
}