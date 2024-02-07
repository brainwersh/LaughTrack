from django.contrib import admin
from django.urls import include, path
from . import views
app_name = "laughtrack"

urlpatterns = [
    # path('', views.homestart, name='homestart'),  

    path('home' ,views.homepage, name='homepage'),
    path('home/<int:event_id>', views.homepage, name='homeevent'),
    path('comedian/<int:comedian_id>', views.comedianinfo, name="comedian"),
    path('comedian/<int:comedian_id>/<int:event_id>', views.comedianinfo, name="comedian"),
    path('signin', views.signin , name="signin" ),
    path('signup',views.signup,name='signup'),
    path('show-details/<int:event_id>', views.show_details, name='detail'),
    path('post-comment/<int:event_id>', views.post_comment, name='post_comment'),
    path('following',views.following,name='following'),
    path('following/<int:event_id>',views.following,name='followingevent'),
    path('follow/<int:comedian_id>',views.follow,name='follow'),
    path('unfollow/<int:comedian_id>',views.unfollow,name='unfollow'),
    path('logout',views.logout_view,name='logout_view')
]
