from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView

from api.bot_app.serializers import BotUserSerializer, BirthdaySerializer, JoinedGroupSerializer
from api.bot_app.models import BotUser, Birthday, JoinedGroup

"""
    C - Create
    U - Update
    R - Retrieve
    L - List
"""

class BotUserRUView(RetrieveUpdateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    lookup_field = 'chat_id'


class BotUserCLView(ListCreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class JoinedGroupRUView(RetrieveUpdateAPIView):
    queryset = JoinedGroup.objects.all()
    serializer_class = JoinedGroupSerializer
    lookup_field = 'chat_id'


class JoinedGroupCLView(ListCreateAPIView):
    queryset = JoinedGroup.objects.all()
    serializer_class = JoinedGroupSerializer


class BirthdayRUView(RetrieveUpdateAPIView):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer


class BirthdayCLView(ListCreateAPIView):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer
