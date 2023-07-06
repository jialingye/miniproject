from django.contrib import admin
from .models import Mapproject, Miniproject, Task, Group
# Register your models here.

admin.site.register(Mapproject)
admin.site.register(Miniproject)
admin.site.register(Task)
admin.site.register(Group)