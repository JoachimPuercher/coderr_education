
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserTypeChoices, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(max_length=100, write_only=True)
    type = serializers.ChoiceField(choices=UserTypeChoices.choices)
   

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password' : {
                'write_only' : True
            }
        }

    def save(self):
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            )
        user.set_password(self.validated_data["password"])
        user.save()
        user_profile = UserProfile(
            user=user,
            type=self.validated_data["type"]
        )
        user_profile.save()

        return user

    def validate_email(self, value):
        new_mail = value.lower()
        if User.objects.filter(email=new_mail).exists():
            raise serializers.ValidationError("Email already exists")
        else:
            return new_mail

    def validate(self, values):
        if values["password"] != values["repeated_password"]:
            raise serializers.ValidationError("Password do not match")
        else:
            return values