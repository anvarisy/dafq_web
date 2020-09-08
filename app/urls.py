from django.urls import path
from app.views import  *

urlpatterns = [
    path('', ViewHomePage.as_view(), name='home'),
    path('about',ViewAbout.as_view(),name='about'),
    path('our-team',ViewTeam.as_view(),name='our-team'),
    path('misi', ViewMisi.as_view(), name='misi'),
    path('detail/<str:mis_id>', DetailMisi.as_view(), name='detail'),
    path('register', ViewRegister.as_view(), name='register'),
    path('news', ViewNews.as_view(), name='news'),
    path('new-detail/<str:news_id>', DetailNews.as_view(), name='new'),
    path('proposal', ViewProposal.as_view(),name='proposal'),
    path('login', ViewLogin.as_view(),name='login'),
    path('post-login', PostLogin.as_view(),name='post-login'),
    path('post-register',PostRegister.as_view(),name='post-register'),
    path('logout',Logout.as_view(),name='logout'),
    path('post-proposal',PostProposal.as_view(),name='post-proposal'),
    path('donate',HandlePayment.as_view(),name='donate'),
    path('record',HandleRecord.as_view(),name='record')
    # path('ok',ViewSuccess.as_view(),name='ok')
    ]