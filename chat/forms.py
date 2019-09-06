from django import forms
from .models import Chatrooms

class ChatroomForm(forms.ModelForm):
    class Meta:
        model = Chatrooms
        fields = "__all__"