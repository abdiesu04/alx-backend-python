from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with custom email validation."""

    def validate_email(self, value):
        """Custom validation to ensure email has a valid domain."""
        if not value.endswith("@example.com"):  # Replace with a domain relevant to your app
            raise serializers.ValidationError("Email must end with '@example.com'.")
        return value

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
            'is_online',
            'last_seen',
            'profile_picture',
            'status_message',
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with custom validations."""
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_message_body(self, value):
        """Ensure message body length is appropriate."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message body must be at least 10 characters long.")
        return value

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at',
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with participants and messages."""
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )  # Allow writable participants
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, data):
        """Ensure a conversation has at least two participants."""
        participants = data.get('participants', [])
        if len(participants) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]
