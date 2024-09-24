from django.urls import include, path, re_path
from auctionapp import views, api
from auctionapp.views import spa_view
app_name = "auctionapp"
urlpatterns = [
    path('', spa_view, name='app'),
    path('login/',views.login_view,name='login'),
    path('signup/', views.sign_up, name= 'signup'),
    #path('profile/', views.profile_view, name='profile')
    path('logout/', views.logout, name='logout'),
    path('api/items/',views.Item_api, name='items'),
    path('api/messages/',views.messages_api, name='messages'),
    path('getuser/',views.GET_User, name='getuser'),
    path('changeprofile/', views.Change_User_Profile, name="changeprofile"),
    path('api/getimage/', views.fetch_profile_image, name="getimage"),



    path('api/change_image/', api.change_image, name = 'uploading api'),
    path('api/item_image/<int:item_id>/', api.addItemImage, name = 'uploading image'),

]

urlpatterns += [
    re_path('^(?!media).*$', spa_view, name='app'),
]
