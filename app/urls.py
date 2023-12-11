from django.urls import path
from . import views,user_views
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
   
    path('login',views.login,name='login'),
    path('Logout',views.logout_view,name='logout'),
    path('Add_property_owner',views.add_property_owner,name='add_property_owner'),
    path('View_property_owner',views.view_property_owner,name='view_property_owner'),
    path('property_owner/edit/<int:id>/', views.edit_property_owner, name='edit_property_owner'),
    path('property_owner/delete/<int:id>/', views.delete_property_owner, name='delete_property_owner'),
    path('Add_question',views.add_question,name='add_question'),
    path('View_question',views.view_question,name='view_question'),
    path('Edit_question/<int:id>/',views.edit_question,name='Edit_question'),
    path('Delete_question/<int:id>/',views.delete_question,name='Delete_question'),
    path('Add_manage_property',views.add_manage_property,name='add_manage_property'),
    path('View_manage_property',views.view_manage_property,name='view_manage_property'),
    path('Notification',views.notification,name='notification'),
    path('Privacy_Policy',views.privacy,name='privacy_policy'),
    path('Terms_Condition',views.terms_condition,name='terms_condition'),
    path('profile',views.profile,name='profile'),
    path('manage_user_admin/', views.manage_user_admin, name='manage_user_admin'),
    path('index/', views.index, name='index'),
    path('save_question_answer', views.save_question_answer, name='save_question_answer'),
    path('import_excel', views.import_excel, name='import_excel'),
    path('notifications/edit/<int:id>/', views.edit_notification, name='edit_notification'),
    path('notifications/delete/<int:id>/', views.delete_notification, name='delete_notification'),
 #  path('import_data/', views.import_data, name='import_data'),
    path('update_personal_details/', views.update_personal_details, name='update_personal_details'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_terms_condition/<int:id>/', views.delete_terms_condition, name='delete_terms_condition'),
    path('delete_privacy_policy/<int:id>/', views.delete_privacy_policy, name='delete_privacy_policy'),


################  USER VIEWS ###################

 path('user_dashboard',user_views.user_dashboard,name='user_dashboard'),
 path('logout',user_views.logout_view_user,name='logout'),
 path('Add_user_management',user_views.add_user_management,name='Add_user_management'),
 path('View_user_management',user_views.view_user_management,name='View_user_management'),
 path('Add_room',user_views.add_room,name='Add_room'),
 path('View_room',user_views.view_room,name='View_room'),
 path('Faq',user_views.faq_view,name='Faq'),
 path('Terms_condition_user',user_views.terms_condition_user,name='Terms_condition_user'),
 path('Notification_user',user_views.Notification_user,name='Notification_user'),
 path('Privacy_policy_user',user_views.privacy_policy_user,name='Privacy_policy_user'),
 path('Profile_user',user_views.profile_user,name='Profile_user'),




]