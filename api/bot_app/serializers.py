from rest_framework.serializers import ModelSerializer

from api.bot_app.models import BotUser, Birthday, JoinedGroup


class BirthdaySerializer(ModelSerializer):

    class Meta:
        model = Birthday
        fields = ['id', 'name', 'image_id', 'congrat', 'date', 'user', 'groups']


class BirthdayForUserSerializer(ModelSerializer):

    class Meta:
        model = Birthday
        fields = ['id', 'name', 'date']


class BotUserSerializer(ModelSerializer):
    birthdays = BirthdayForUserSerializer(many=True, read_only=True)

    class Meta:
        model = BotUser
        fields = ['chat_id', 'joined', 'birthdays']


class JoinedGroupSerializer(ModelSerializer):

    class Meta:
        model = JoinedGroup
        fields = ['chat_id', 'joined']
