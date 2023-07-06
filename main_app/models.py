from django.db import models


class Mapproject(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    complete = models.BooleanField(default=False)
    tag = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Miniproject(models.Model):
    name = models.CharField(max_length=100)
    description= models.TextField(max_length=1000)
    complete= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    mapproject = models.ForeignKey(Mapproject, on_delete = models.CASCADE,related_name='miniprojects' )
    def __str__(self):
        return self.name

# Create your models here.

class Task(models.Model):
    description=models.TextField(max_length=1000)
    project= models.ForeignKey(Miniproject, on_delete=models.CASCADE, related_name="task")

    def __str__(self):
        return self.name
    
class Group(models.Model):
    title = models.CharField(max_length=150)
    projects = models.ManyToManyField(Mapproject)

    def __str__(self):
        return self.title