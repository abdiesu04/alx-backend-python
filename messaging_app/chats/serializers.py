from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    extra_field = serializers.CharField(required=False)
    method_field = serializers.SerializerMethodField()

    def get_method_field(self, obj):
        return "example"

    def validate_email(self, value):
        # Custom validation for email
        if not value.endswith("@example.com"):
            raise serializers.ValidationError("Email must end with '@example.com'.")
        return value

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'extra_field', 'method_field']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    def validate_message_body(self, value):
        # Custom validation for message body
        if len(value) < 10:
            raise serializers.ValidationError("Message body must be at least 10 characters long.")
        return value

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, data):
        # Custom validation for conversation
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
