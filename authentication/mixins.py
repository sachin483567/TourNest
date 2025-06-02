from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class HostRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'host')
    
    def handle_no_permission(self):
        return redirect('host_login')