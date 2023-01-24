from django.urls import path

from api.bot_app.views import (BotUserRetrieveView, BotUserCreateView, BotUserWithIdView,
                               JoinedGroupRetrieveView, JoinedGroupCreateView, JoinedGroupGetWithIdView,
                               BirthdayRetrieveView, BirthdayCreateView)

urlpatterns = [
    path('user/<int:chat_id>', BotUserRetrieveView.as_view(), name='get-user'),
    path('user/id/<int:pk>', BotUserWithIdView.as_view(), name='get-id-user'),
    path('user/add', BotUserCreateView.as_view(), name='create-user'),

    path('group/<int:chat_id>', JoinedGroupRetrieveView.as_view(), name='get-group'),
    path('group/id/<int:pk>', JoinedGroupGetWithIdView.as_view(), name='get-id-group'),
    path('group/add', JoinedGroupCreateView.as_view(), name='create-group'),

    path('birthday/<int:pk>', BirthdayRetrieveView.as_view(), name='get-birth'),
    path('birthday/add', BirthdayCreateView.as_view(), name='create-birth'),
]
