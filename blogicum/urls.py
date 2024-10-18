from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import path, include, reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('pages/', include(('pages.urls', 'pages'), namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    re_path(r'^.*$', lambda request: redirect('/')),

]


handler403 = 'blog.views.csrf_failure'
handler404 = 'blog.views.page_not_found'
handler500 = 'blog.views.server_error'
