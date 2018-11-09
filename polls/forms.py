# from django import forms
from django.forms import ModelForm, Textarea
from .models import Topic, Entry

class TopicForm(ModelForm):
	class Meta:
		model = Topic
		fields = ['text']
		labels = {'text':'提交'}

class EntryForm(ModelForm):
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text':'修改笔记'}
		widgets = {
			'text':Textarea(attrs={'cols':80, 'rows':20}),
		}