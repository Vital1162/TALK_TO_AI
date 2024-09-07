from django.forms import ModelForm
from .models import Prompt

class PromptForm(ModelForm):
    class Meta:
        model = Prompt
        fields = ['prompt']

class Config(ModelForm):
    class Meta:
        fields = ['temperature','top_p','top_k','max_output_tokens']
        
# class ConversationForm(ModelForm):
#     class Meta:
#         fields = ['response','start_time','end_time']