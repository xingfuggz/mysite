from django.shortcuts import render

# Create your views here.
from .models import Topic

def index(request):
	return render(request, 'polls/index.html')


def topics(request):
	''' 显示所有的主题 '''
	topics = Topic.objects.order_by('date_added')
	context = {'topics':topics}
	return render(request, 'polls/topics.html', context)


def topic(request, topic_id):
	''' 显示特定主题列表页 '''
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'polls/topic.html', context)