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
