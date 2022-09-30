from django.urls import path

from .views import AdvertView, AdvertCreate, AdvertEdit, AdvertDetail, AdvertDelete, RespCreate, \
    UserAdvert, RespList, resp_change_status, delete_response

app_name = 'bill_board'
urlpatterns = [
    path('', AdvertView.as_view(), name='advert'),
    path('<int:pk>/', AdvertDetail.as_view(), name='detail'),
    path('create/', AdvertCreate.as_view(), name='create'),
    path('edit/<int:pk>/', AdvertEdit.as_view(), name='edit'),
    path('delete/<int:pk>/', AdvertDelete.as_view(), name='delete'),
    path('add_resp/', RespCreate.as_view(), name='add_response'),
    path('user_advert/', UserAdvert.as_view(), name='user_advert'),
    path('resp_list/', RespList.as_view(), name='resp_list'),
    path('resp_status/', resp_change_status, name='resp_status'),
    path('delete_response/', delete_response, name='resp_delete'),
]
