from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home, name="home"),
    path('about', views.About, name="about"),
    path('contact', views.Contact, name="contact"),
    path('login', views.Login, name="login"),
    path('signup', views.Signup_User, name="signup"),
    path('admin_home', views.Admin_Home, name="admin_home"),
    path('predict', views.predict, name="predict"),
    path('profile', views.View_My_Detail, name="profile"),
    path('update_profile', views.Update_profile, name="update_profile"),
    path('consult', views.Consultation, name="consult"),
    path('add_article', views.Add_article, name="add_article"),
    path('add_doctor', views.Add_Doctor, name="add_doctor"),
    path('manage_article', views.Manage_article, name="manage_article"),
    path('manage_requests', views.Manage_requests, name="manage_requests"),
    path('manage_doctor', views.Manage_doctor, name="manage_doctor"),
    path('update_article<int:pid>', views.Update_article, name="update_article"),
    path('diagnose<int:pid>', views.Diagnosis, name="diagnose"),
    path('read_article<int:pid>', views.Read_Article, name="read_article"),
    path('past_report<int:pid>', views.Past_report, name="past_report"),
    path('report', views.Report, name="report"),
    path('update_doctor<int:pid>', views.Update_doctor, name="update_doctor"),
    path('manage_user', views.Manage_user, name="manage_user"),
    path('view_feedback', views.View_feedback, name="view_feedback"),
    path('send_feedback', views.Send_feedback, name="send_feedback"),
    path('view_requests', views.View_requests, name="view_requests"),
    path('change_password', views.Change_password, name="change_password"),
    path('logout', views.Logout, name="logout"),
    path('checkout', views.Checkout, name="checkout"),
    path('payment', views.Payments, name="payment"),
    path('payment_history', views.Payment_history, name="payment_history"),
    path(r'see_all/<cid>', views.See_all, name="see_all"),
    path('delete_user<int:pid>', views.delete_user, name="delete_user"),
    path('delete_news<int:pid>', views.delete_news, name="delete_news"),
    path('delete_doctor<int:pid>', views.Delete_doctor, name="delete_doctor"),
    path('delete_request<int:pid>', views.delete_request, name="delete_request"),
    path('delete_feedback<int:pid>', views.delete_feedback, name="delete_feedback"),


    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="passReset/password_reset.html"), name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="passReset/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="passReset/password_reset_confirm.html"), name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="passReset/password_reset_complete.html"), name="password_reset_complete"),

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)