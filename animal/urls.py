from django.urls import path

from animal import views as animal_view


urlpatterns = [
    #path('', animal_view.define_model, name='homepage'),
    path('', animal_view.predict_anim, name='predict_anim'),
    path('animal/', animal_view.create_animal, name="create_animal"),

    
]