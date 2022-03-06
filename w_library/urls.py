"""w_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('catalog/', include('catalog.urls')),
                  path('', RedirectView.as_view(url='catalog/')),
                  path('accounts/', include('django.contrib.auth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# from menu.views import MySignupView, MyLoginView, MyLogoutView, home_view
# path('signup', MySignupView.as_view()),
# path('login/', RedirectView.as_view(url='/login')),
# path('signup/', RedirectView.as_view(url='/signup')),
# class MyLogoutView(LogoutView):
#     form_class = AuthenticationForm
#     redirect_authenticated_user = True
#     template_name = 'menu/logout.html'
#
#
# class MySignupView(CreateView):
#     form_class = UserCreationForm
#     success_url = 'login'
#     template_name = 'menu/signup.html'
