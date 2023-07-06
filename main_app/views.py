from django.shortcuts import render
from typing import Any, Dict
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.http import HttpResponse
from .models import Mapproject, Miniproject, Task, Group
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.

class Home(TemplateView):
        template_name = "home.html"

        def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
                context= super().get_context_data(**kwargs)
                context['group'] = Group.objects.all()
                return context



class ProjectList(TemplateView):
         template_name= "project_list.html"

         def get_context_data(self, **kwargs):
                 context = super().get_context_data(**kwargs)
                 title = self.request.GET.get("title")
                 if title != None:
                         context['projects'] = Mapproject.objects.filter(title__icontains=title)
                         context['header'] = f"Searching for {title}"
                 else:
                         context["projects"] = Mapproject.objects.all()
                         context["header"] = "All Projects"
                 
                 return context


class ProjectCreate(CreateView):
       model = Mapproject
       fields = ['title','tag','complete','description']
       template_name= "project_create.html"
       success_url = "/project"

class ProjectDetail(DetailView):
       model = Mapproject
       template_name= "project_detail.html"
       context_object_name="project"

       def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
               context = super().get_context_data(**kwargs)
               context['groups']=Group.objects.all()
               mermaid_code = 'graph TD;'
               miniprojects = Miniproject.objects.filter(mapproject=self.object)
               for miniproject in miniprojects:
                       if miniproject.parent:
                               mermaid_code += f"id{miniproject.parent.id}({miniproject.parent.name}) --> id{miniproject.id}({miniproject.name});"
               context['mermaid_code'] = mermaid_code
               return context
               
class ProjectEdit(UpdateView):
        model = Mapproject
        fields = ['title', 'tag','complete','description']
        template_name="project_edit.html"
        
        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['project'] = self.get_object()  # Add this line to include the project object
                return context
        
        def get_success_url(self):
                return reverse('project_detail', kwargs={'pk': self.object.pk})

class ProjectDelete(DeleteView):
        model=Mapproject
        template_name="project_delete.html"
        success_url="/project"

        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['project'] = self.get_object()  # Add this line to include the project object
                return context

class MiniCreate(View):
        def post(self, request, pk):
                name = request.POST.get("name")
                description = request.POST.get("description")
                complete = request.POST.get("complete") == 'True'
                parent_id = request.POST.get("parent")
                mapproject = Mapproject.objects.get(pk=pk)
                parent = Miniproject.objects.get(id=parent_id) if parent_id else None
                Miniproject.objects.create(name=name, description=description, complete=complete, parent=parent, mapproject=mapproject)
                
                mermaid_code = "graph TD;"
                miniprojects = Miniproject.objects.filter(mapproject=mapproject)
                for miniproject in miniprojects:
                        if miniproject.parent:
                                mermaid_code += f"id{miniproject.parent.id}({miniproject.parent.name}) --> id{miniproject.id}({miniproject.name});"

                context = {
                        'mermaid_code': mermaid_code,
                        'project_pk': pk,
                        'project':mapproject,
                }
                return render(request, 'project_detail.html', context)

class MiniDelete(DeleteView):
                model = Miniproject
                template_name = 'mini_delete.html'

                def get_context_data(self, **kwargs):
                        context = super().get_context_data(**kwargs)
                        context['miniproject'] = self.get_object()  # Add this line to include the project object
                        return context
        
                def get_success_url(self):
                         project_pk = self.kwargs['project_pk']
                         return reverse('project_detail', kwargs={'pk': project_pk})


class TaskCreate(View):
        def post(self, request, project_pk, mini_pk):
                description = request.POST.get("description")
                project= Miniproject.objects.get(pk=mini_pk)
                Task.objects.create( description=description,project=project)
                return redirect('project_detail', pk=project_pk)

class GroupProjectAssoc(View):
        def get(self, request, pk, project_pk):
                assoc= request.GET.get("assoc")
                if assoc == "remove":
                        Group.objects.get(pk=pk).projects.remove(project_pk)
                if assoc == "add":
                        Group.objects.get(pk=pk).projects.add(project_pk)
                return redirect('home')
        
class GroupCreate(CreateView):
     model = Group
     fields = ['title']
     template_name = "group_create.html"
     success_url = '/'

class GroupDelete(DeleteView):
        model=Group
        template_name="group_delete.html"
        success_url="/"
        