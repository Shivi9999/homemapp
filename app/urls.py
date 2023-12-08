from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    # path('Logout',views.logout,name='logout'),
    path('Add_property_owner',views.add_property_owner,name='add_property_owner'),
    path('View_property_owner',views.view_property_owner,name='view_property_owner'),
    path('property_owner/edit/<int:id>/', views.edit_property_owner, name='edit_property_owner'),
    path('property_owner/delete/<int:id>/', views.delete_property_owner, name='delete_property_owner'),
    path('Add_question',views.add_question,name='add_question'),
    path('View_question',views.view_question,name='view_question'),
    path('Add_manage_property',views.add_manage_property,name='add_manage_property'),
    path('View_manage_property',views.view_manage_property,name='view_manage_property'),
    path('Notification',views.notification,name='notification'),
    path('Privacy_Policy',views.privacy,name='privacy_policy'),
    path('Terms_Condition',views.terms_condition,name='terms_condition'),
    path('profile',views.profile,name='profile'),
    path('manage_user_admin/', views.manage_user_admin, name='manage_user_admin'),
    path('index/', views.index, name='index'),
    path('delete_terms_condition/<int:id>/', views.delete_terms_condition, name='delete_terms_condition'),
    path('delete_privacy_policy/<int:id>/', views.delete_privacy_policy, name='delete_privacy_policy'),
]