from rest_framework.serializers import ModelSerializer

from api.bot_app.models import BotUser, Birthday, JoinedGroup


class BotUserSerializer(ModelSerializer):

    class Meta:
        model = BotUser
        fields = ['id', 'chat_id', 'joined']


class BirthdaySerializer(ModelSerializer):

    class Meta:
        model = Birthday
        fields = ['id', 'name', 'image_path', 'congrat', 'date', 'user', 'groups']


class JoinedGroupSerializer(ModelSerializer):

    class Meta:
        model = JoinedGroup
        fields = ['id', 'chat_id', 'joined']
