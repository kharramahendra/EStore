from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from new_app import settings

urlpatterns = [
    path('',views.index,name='home'),
    path('shop/<str:slug>',views.shop,name='shop'),
    path('shop/',views.shop,name='shop'),
    path('product/<int:my_id>',views.product_view,name='Product_view'),
    path('viewcart/',views.ViewCart,name="viewcart"),
    path('checkout/',views.Checkout,name="checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('profile/',views.Profile,name="profile"),
    path('login/',views.Login,name="login"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('search/',views.Search,name="search"),
    path('comment/',views.postComment,name='postcomment'),
    path('clearcart/',views.Clear_cart,name="clear_cart"),
    path('contact/',views.Contact_,name="contact"),
    path('about/',views.About,name="about")
]