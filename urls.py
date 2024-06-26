from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("admin", views.admin, name="admin"),
    path("register", views.register, name="register"),
    path("appointment_reg", views.appointment_reg, name="appointment_reg"),
    path("appointment", views.appointment, name="appointment"),
    path("appointmentAdmin", views.appointmentAdmin, name="appointmentAdmin"),
    path("meetTest/<int:meetID>", views.meetTest, name="meetTest"),
    path("calling/", views.calling, name="calling"),
    path("schedule/", views.schedule, name="schedule"),
    path("sms", views.sms, name="sms"),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path("logout", views.logout, name="logout"),
    path("prediction", views.prediction, name="prediction"),
    path('linkupload/<str:link>', views.linkupload, name='linkupload'),
]