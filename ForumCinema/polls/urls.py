from django.urls import path
from . import views


app_name = "polls"

urlpatterns = [
    path('add/<int:group>/', views.polls_add, name='createpoll'),
    path('edit/<pk>/<int:group>/', views.polls_edit, name='editpoll'),
    path('delete/<pk>/<int:group>/', views.polls_delete, name='deletepoll'),
    path('edit/<pk>/<int:group>/choice/add/', views.add_choice, name='addchoice'),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name='choice_edit'),
    path('delete/choice/<int:choice_id>/',views.choice_delete, name='choice_delete'),
    path('detailpoll/<pk>/<int:group>/', views.poll_detail, name='detailpoll'),
    path('vote/<pk>/<int:group>', views.poll_vote, name='vote'),
]