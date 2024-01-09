from django.urls import path
from . import views,owner_views,user_views
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    path('logout',views.logout_view,name='logout'),

    path('add_property_owner',views.add_property_owner,name='add_property_owner'),
    path('View_property_owner',views.view_property_owner,name='View_property_owner'),
    path('edit_property_owner/edit/<int:id>/', views.edit_property_owner, name='edit_property_owner'),
    path('delete_property_owner/<int:id>/', views.delete_property_owner, name='delete_property_owner'),
   
    path('get_rooms1/', views.get_rooms1, name='get_rooms1'),
    path('add_question',views.add_question,name='add_question'),
    path('save_question_answer', views.save_question_answer, name='save_question_answer'),
    path('View_question',views.view_question,name='View_question'),
    path('Edit_question/<int:id>/',views.edit_question,name='Edit_question'),
    path('Delete_question/<int:id>/', views.delete_question, name='Delete_question'),

   
   
    path('View_manage_property',views.view_manage_property,name='View_manage_property'),
    
    path('notification',views.notification,name='notification'),
    path('edit_notification/edit/<int:id>/', views.edit_notification, name='edit_notification'),
    path('delete_notification/<int:id>/', views.delete_notification, name='delete_notification'),

    path('Privacy_Policy',views.privacy,name='Privacy_Policy'),
    path('delete_privacy_policy/<int:id>/', views.delete_privacy_policy, name='delete_privacy_policy'),

    path('terms_condition',views.terms_condition,name='terms_condition'),
    path('delete_terms_condition/<int:id>/', views.delete_terms_condition, name='delete_terms_condition'),
   
    path('profile',views.profile,name='profile'),
    path('update_personal_details/', views.update_personal_details, name='update_personal_details'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('Faq_admin',views.faq_view_admin,name='Faq_admin'),
    path('edit_faq_admin/<int:id>',views.edit_faq_admin,name='edit_faq_admin'),
    path('delete_faq_admin/<int:id>/',views.delete_faq_admin,name='delete_faq_admin'),



    path('manage_user_admin/', views.manage_user_admin, name='manage_user_admin'),
    path('index/', views.index, name='index'),
   
    path('import-csv/', views.import_csv, name='import_csv'),
    
    path('chat', views.chat, name='chatbot_page'),
    path('get_answer/', views.get_answer, name='get_answer'),
   
  
    
     
    ################  Owner VIEWS ###################

    path('owner_dashboard',owner_views.owner_dashboard,name='owner_dashboard'),
    path('login_owner',owner_views.login_owner,name='login_owner'),
    path('logout_owner',owner_views.logout_view_owner,name='logout_owner'),

    path('Add_property_management',owner_views.add_property_management,name='Add_property_management'),
    path('view_property_management',owner_views.view_property_management,name='view_property_management'),
    path('edit_property/<int:id>',owner_views.edit_property,name='edit_property'),
    path('delete_property/<int:id>/',owner_views.delete_property,name='delete_property'),

    path('add_room_management',owner_views.add_room_management,name='add_room_management'),
    path('view_room_management',owner_views.view_room_management,name='view_room_management'),
    path('edit_room/<int:id>',owner_views.edit_room,name='edit_room'),
    path('delete_room/<int:id>/',owner_views.delete_room,name='delete_room'),

    path('Add_user_management',owner_views.add_user_management,name='Add_user_management'),
    path('View_user_management',owner_views.view_user_management,name='View_user_management'),
    path('edit_user/<int:id>',owner_views.edit_user,name='edit_user'),
    path('delete_user/<int:id>/',owner_views.delete_user,name='delete_user'),
    
    path('Add_equipment',owner_views.add_equipments,name='Add_equipment'),
    path('View_equipment',owner_views.view_equipments,name='View_equipment'),
    path('edit_equipment/<int:id>',owner_views.edit_equipments,name='edit_equipment'),
    path('delete_equipment/<int:id>/',owner_views.delete_equipments,name='delete_equipment'),

    path('Add_items',owner_views.add_items,name='Add_items'),
    path('View_items',owner_views.view_items,name='View_items'),
    path('edit_items/<int:id>',owner_views.edit_items,name='edit_items'),
    path('delete_items/<int:id>/',owner_views.delete_items,name='delete_items'),
   
    path('get_rooms/', owner_views.get_rooms, name='get_rooms'),
    path('Add_question_answer',owner_views.Add_question_answer,name='Add_question_answer'),
    #path('save_question_answer1', owner_views.save_question_answer1, name='save_question_answer1'),
    path('View_question_answer',owner_views.view_question_answer,name='View_question_answer'),
    path('Edit_question_answer/<int:id>/',owner_views.edit_question_answer,name='Edit_question_answer'),
    path('Delete_question_answer/<int:id>/', owner_views.delete_question_answer, name='Delete_question_answer'),




    path('Faq',owner_views.faq_view,name='Faq'),
    path('edit_faq/<int:id>',owner_views.edit_faq,name='edit_faq'),
    path('delete_faq/<int:id>/',owner_views.delete_faq,name='delete_faq'),

    path('Notification_owner',owner_views.Notification_owner1,name='Notification_owner'),
    path('edit_notification_owner/<int:id>',owner_views.edit_notification_owner,name='edit_notification_owner'),
    path('delete_notification_owner/<int:id>/', owner_views.delete_notification_owner, name='delete_notification_owner'),

    path('Terms_condition_owner',owner_views.terms_condition_owner,name='Terms_condition_owner'),
    path('Privacy_policy_owner',owner_views.privacy_policy_owner,name='Privacy_policy_owner'),
    path('Profile_owner',owner_views.profile_owner,name='Profile_owner'),
    path('update_personal_details_owner',owner_views.update_personal_details_owner,name='update_personal_details_owner'),
    path('change_password_owner',owner_views.change_password_owner,name='change_password_owner'),
    
    path('owner_chat', owner_views.owner_chat, name='owner_chat'),
    path('get_answer_owner/', owner_views.get_answer_owner, name='get_answer_owner'),
   
  
    



     ################  USER VIEWS ###################

    path('user_dashboard',user_views.user_dashboard,name='user_dashboard'),
    path('login_user',user_views.login_user,name='login_user'),
    path('logout_user',user_views.logout_view_user,name='logout_user'),
    path('get_answer_user/', user_views.get_answer_user, name='get_answer_user'),

     

]