from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.db.models.deletion import RestrictedError
from django.contrib import messages


class UserAccessMixin(PermissionRequiredMixin):
    fail_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            if self.fail_url is None:
                return redirect('/')
            else:
                return redirect(self.fail_url)
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class InvalidFormMixin:
    """
        Autor: Janilson Varela
        Mixin para preencher os input com a class is-invalid 
        do bootstrap quando houver error
    """
    def form_invalid(self, form):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return self.render_to_response(self.get_context_data(form=form))


class DeleteExceptionMixin:
    """
        Autor: Janilson Varela
        Data: 19/08/2023
        Mixim para tratar a deleçao do registro, em caso de ter algum
        vinculo com outra tabela e que o cascade seja restric
    """

    def __init__(self):
        self.object = None

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        self.object = self.get_object()
        try:
            res = super().post(request, *args, **kwargs)
        except RestrictedError:
            messages.add_message(request, messages.ERROR, f'Não é possível excluir {self.model._meta.verbose_name}')
            return self.render_to_response(context)

        return res
    