from django.contrib.auth.views import LoginView
from django.urls import reverse

class LoginView(LoginView):

    def get_success_url(self):
        return reverse('blog-post-user', kwargs={'username':self.request.user.username})