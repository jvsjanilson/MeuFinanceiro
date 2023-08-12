from django.shortcuts import redirect
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/')

        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class InvalidFormMixin:
    """
        Autor: Janilson Varele
        Mixin para preencher os input com a class is-invalid 
        do bootstrap quando houver error
    """
    def form_invalid(self, form):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return self.render_to_response(self.get_context_data(form=form))