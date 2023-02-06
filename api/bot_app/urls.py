from django.urls import path

from api.bot_app.views import (BotUserRUView, BotUserCLView,
                               JoinedGroupRUView, JoinedGroupCLView,
                               BirthdayRUView, BirthdayCLView)

urlpatterns = [
    path('users/<int:chat_id>', BotUserRUView.as_view()),
    path('users', BotUserCLView.as_view(),),

    path('groups/<int:chat_id>', JoinedGroupRUView.as_view()),
    path('groups', JoinedGroupCLView.as_view()),

    path('birthdays/<int:pk>', BirthdayRUView.as_view()),
    path('birthdays', BirthdayCLView.as_view()),
]

