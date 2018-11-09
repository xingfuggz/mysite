from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
# Create your views here.
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request, 'polls/index.html')

@login_required
def topics(request):
	''' 显示所有的主题 '''
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics':topics}
	return render(request, 'polls/topics.html', context)

@login_required
def topic(request, topic_id):
	''' 显示特定主题列表页 '''
	topic = Topic.objects.get(id=topic_id)

	# 确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'polls/topic.html', context)

@login_required
def new_topic(request):
	''' 添加新主题 '''
	if request.method != 'POST':
		# 如果不是POST请求，我们需要创建一个空表单
		form = TopicForm()
	else:
		# 创建一个表单实例并使用请求中的数据填充它：
		form = TopicForm(request.POST)
		# 检查他是否有效
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('polls:topics'))
	
	form = TopicForm()
	return render(request, 'polls/new_topic.html', {'form':form})

@login_required
def new_entry(request, topic_id):
	'''在特定主题中添加新笔记'''
	topic = Topic.objects.get(id=topic_id)
	# 添加新笔记
	if request.method != 'POST':
		# 创建空表单
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		# 检查是否有效
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('polls:topic', args=[topic_id]))

	context = {'topic':topic, 'form':form}
	return render(request, 'polls/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# 使用当前条目填充表单
		form = EntryForm(instance=entry)
	else:
		# 对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('polls:topic',args=[topic.id]))

	context = {'entry':entry, 'topic':topic, 'form':form}
	return render(request, 'polls/edit_entry.html', context)
