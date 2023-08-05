django.jQuery().ready(function(){
    django.jQuery("input, select").each((_, e)=> {
        django.jQuery(e).change((el) => {
            if (django.jQuery(el.target).hasClass('is-invalid'))
            {
                if (django.jQuery(el.target).val() != "" ) {
                    django.jQuery(el.target).removeClass('is-invalid');
                    //remove mensagem com a classe errorlist
                    django.jQuery(el.target).next().each((_, span) => {
                        if (django.jQuery(span).hasClass('errorlist'))
                        {
                            django.jQuery(span).remove();
                        }
                    })
                }
            }
        });
    })
});