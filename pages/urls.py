from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('start',views.start,name='start'),
    path('Review',views.Review,name='Review'),
    path('Category',views.Category,name='Category'),
    path('add_rating',views.add_rating,name='add_rating'),
    path('showUser',views.showUser,name='showUser'),
    path('Drugs', views.Drugs, name='Drugs'),
    path('Drugs/Add', views.AddDrugs, name='AddDrugs'),
    path('AddCategory/Add', views.AddCategory, name='AddCategory'),
    path('result', views.check, name='qrcode_view'),
    path('add-Drugs', views.add_drugs, name='add-drugs'),
    path('add-Category', views.add_Category, name='add-Category'),
    path('medication/delete/<int:medication_id>', views.delete_medication, name='delete_medication'),
    path('Category/delete/<int:Category_id>', views.delete_Category, name='delete_Category'),
    path('toggle-activation/<int:user_id>/',views.toggle_user_activation, name='toggle_activation'),

    
]