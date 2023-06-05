from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns  # 2,3
from snippets import views

urlpatterns = [
    # path('snippets/', views.snippet_list),    #2
    path('snippets/', views.SnippetList.as_view()),
    # path('snippets/<int:pk>', views.snippet_detail),    #2
    path('snippets/<int:pk>', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
]

# re define urlpatterns agregando a todo el contenido el sufijo de formato
urlpatterns = format_suffix_patterns(urlpatterns)
