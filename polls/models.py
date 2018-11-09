from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
	''' 文档主题 '''
	text = models.CharField('主题', max_length=200)
	date_added = models.DateTimeField('发布时间', auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['text']
		verbose_name_plural = "主题"

	def __str__(self):
		''' 返回模型的字符串表示 '''
		return self.text



class Entry(models.Model):
	''' 学到某主题有关的具体知识 '''
	topic = models.ForeignKey(
		Topic,
		on_delete=models.CASCADE,
		verbose_name = '主题'
		)
	text = models.TextField('具体知识')
	date_added = models.DateTimeField('发布日期',auto_now_add=True)

	class Meta:
		ordering = ['text']
		verbose_name_plural = "具体知识"

	def __str__(self):
		return self.text[:50] + '...'
