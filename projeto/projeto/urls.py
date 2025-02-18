"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from quadra_facil.views import QuadraView, HorarioView, ReservaView

urlpatterns = [
    path('admin/', admin.site.urls),
    
     # Endpoint para listar e criar quadras
    path('quadras/', QuadraView.as_view(), name='quadras'),

    # Endpoint para listar horários disponíveis e criar novos horários
    path('quadras/<int:quadra_id>/horarios/', HorarioView.as_view(), name='horarios'),

    # Endpoint para listar e criar reservas
    path('reservas/', ReservaView.as_view(), name='reservas'),
    
    # Endpoint para listar as reservas de um horário específico
    path('reservas/<int:horario_id>/', ReservaView.as_view(), name='reservas_por_horario'),
]
