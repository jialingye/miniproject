from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('project/', views.ProjectList.as_view(), name="project_list"),
    path('project/create', views.ProjectCreate.as_view(),name="project_create"),
    path('project/<int:pk>/', views.ProjectDetail.as_view(), name="project_detail"),
    path('project/<int:pk>/edit', views.ProjectEdit.as_view(),name="project_edit"),
    path('project/<int:pk>/delete', views.ProjectDelete.as_view(),name="project_delete"),
    path('project/<int:pk>/mini/new', views.MiniCreate.as_view(), name="mini_create"),
    path('project/<int:project_pk>/mini/<int:pk>/delete', views.MiniDelete.as_view(), name="mini_delete"),
    path('project/<int:project_pk>/mini/<int:mini_pk>/new', views.TaskCreate.as_view(), name="task_create"),
    path('group/<int:pk>/project/<int:project_pk>/',views.GroupProjectAssoc.as_view(), name="group_project_assoc"),
    path('group/new/', views.GroupCreate.as_view(), name="group_create"),
    path('group/<int:pk>/delete', views.GroupDelete.as_view(), name="group_delete"),
]