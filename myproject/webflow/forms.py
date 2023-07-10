from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm): # class RoomForm inherits from ModelForm
    class Meta:      #this is our meta data for the form we are creating for the room
        model = Room  # am specifying the model am creating a form for, wich is the room model the we specify the fields below
        fields = '__all__'  #this creates the form based on the meta data of my room model
