from django.urls import path
from . import views,user_views,customer_views
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('add_property_owner',views.add_property_owner,name='add_property_owner'),
    path('View_property_owner',views.view_property_owner,name='View_property_owner'),
    path('property_owner/edit/<int:id>/', views.edit_property_owner, name='edit_property_owner'),
    path('delete_property_owner/<int:id>/', views.delete_property_owner, name='delete_property_owner'),
    path('add_question',views.add_question,name='add_question'),
    path('View_question',views.view_question,name='View_question'),
    path('Edit_question/<int:id>/',views.edit_question,name='Edit_question'),
    path('Delete_question/<int:id>/', views.delete_question, name='Delete_question'),

    # path('Delete_question',views.delete_question,name='Delete_question'),
    path('add_manage_property',views.add_manage_property,name='add_manage_property'),
    path('View_manage_property',views.view_manage_property,name='View_manage_property'),
    path('notification',views.notification,name='notification'),
    path('Privacy_Policy',views.privacy,name='Privacy_Policy'),
    path('terms_condition',views.terms_condition,name='terms_condition'),
    path('profile',views.profile,name='profile'),
    path('manage_user_admin/', views.manage_user_admin, name='manage_user_admin'),
    path('index/', views.index, name='index'),
    path('save_question_answer', views.save_question_answer, name='save_question_answer'),
    # path('import_excel', views.import_excel, name='import_excel'),
    path('notifications/edit/<int:id>/', views.edit_notification, name='edit_notification'),
    path('delete_notification/<int:id>/', views.delete_notification, name='delete_notification'),
 #  path('import_data/', views.import_data, name='import_data'),
    path('update_personal_details/', views.update_personal_details, name='update_personal_details'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_terms_condition/<int:id>/', views.delete_terms_condition, name='delete_terms_condition'),
    path('delete_privacy_policy/<int:id>/', views.delete_privacy_policy, name='delete_privacy_policy'),
    path('get_answer/', views.get_answer, name='get_answer'),
    #path('', views.index, name='index'),
    path('chat', views.chat, name='chatbot_page'),
    path('import-csv/', views.import_csv, name='import_csv'),
  
    ################  USER VIEWS ###################

    path('user_dashboard',user_views.user_dashboard,name='user_dashboard'),
    path('login_user',user_views.login_user,name='login_user'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('logout_user',user_views.logout_view_user,name='logout_user'),
    path('Add_hotel_management',user_views.add_hotel_management,name='Add_hotel_management'),
    path('view_hotel_management',user_views.view_hotel_management,name='view_hotel_management'),
    path('delete_hotel/<int:id>',user_views.delete_hotel,name='delete_hotel'),
    path('edit_hotel/<int:id>',user_views.edit_hotel,name='edit_hotel'),
    path('add_property_management',user_views.add_property_management,name='add_property_management'),
    path('view_property_management',user_views.view_property_management,name='view_property_management'),
    path('edit_room/<int:id>',user_views.edit_room,name='edit_room'),
    path('delete_property_management/<int:id>/',user_views.delete_property_management,name='delete_property_management'),
    path('Add_user_management',user_views.add_user_management,name='Add_user_management'),
    path('View_user_management',user_views.view_user_management,name='View_user_management'),
    path('Add_room',user_views.add_room,name='Add_room'),
    path('View_room',user_views.view_room,name='View_room'),
    path('Edit_user/<int:id>',user_views.edit_user,name='edit_user'),
    path('Delete_user/<int:id>',user_views.delete_user,name='delete_user'),
    path('edit_items/<int:id>',user_views.edit_items,name='edit_items'),
    path('delete_items/<int:id>/',user_views.delete_items,name='delete_items'),
    path('Faq',user_views.faq_view,name='Faq'),
    path('edit_faq/<int:id>',user_views.edit_faq,name='edit_faq'),
    path('delete_faq/<int:id>',user_views.delete_faq,name='delete_faq'),
    path('Terms_condition_user',user_views.terms_condition_user,name='Terms_condition_user'),
    path('Notification_user',user_views.Notification_user,name='Notification_user'),
    path('Privacy_policy_user',user_views.privacy_policy_user,name='Privacy_policy_user'),
    path('Profile_user',user_views.profile_user,name='Profile_user'),
    path('update_personal_details_user',user_views.update_personal_details_user,name='update_personal_details_user'),
    path('change_password_user',user_views.change_password_user,name='change_password_user'),

       ################  CUSTOMER VIEWS ###################
    path('customer_dashboard',customer_views.customer_dashboard,name='customer_dashboard'),
    path('login_customer',customer_views.login_customer,name='login_customer'),
    # path('chat_customer',customer_views.chat_customer,name='chat_customer'),
    path('get_answer_cutomer/',customer_views.get_answer_cutomer,name='get_answer_cutomer'),
    path('logout_customer',customer_views.logout_view_customer,name='logout_customer'),

]