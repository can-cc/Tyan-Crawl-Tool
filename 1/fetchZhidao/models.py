from django.db import models



class ZhidaoQuestion(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    questiontitle = models.TextField()
    fulllquestion = models.TextField(blank=True,null=True)
    asktime = models.CharField(max_length=40)
    bestanster = models.TextField(blank=True,null=True)
    anster1 = models.TextField(blank=True,null=True)
    anster2 = models.TextField(blank=True,null=True)
    anster3 = models.TextField(blank=True,null=True)