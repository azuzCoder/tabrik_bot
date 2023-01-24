from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView

from api.bot_app.serializers import BotUserSerializer, BirthdaySerializer, JoinedGroupSerializer
from api.bot_app.models import BotUser, Birthday, JoinedGroup
from rest_framework import status


class BotUserRetrieveView(RetrieveUpdateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    lookup_field = 'chat_id'


class BotUserCreateView(ListCreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class BotUserWithIdView(RetrieveUpdateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class JoinedGroupRetrieveView(RetrieveUpdateAPIView):
    queryset = JoinedGroup.objects.all()
    serializer_class = JoinedGroupSerializer
    lookup_field = 'chat_id'


class JoinedGroupCreateView(ListCreateAPIView):
    queryset = JoinedGroup.objects.all()
    serializer_class = JoinedGroupSerializer


class JoinedGroupGetWithIdView(RetrieveUpdateAPIView):
    queryset = JoinedGroup.objects.all()
    serializer_class = JoinedGroupSerializer


class BirthdayRetrieveView(RetrieveUpdateAPIView):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer


class BirthdayCreateView(ListCreateAPIView):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer
