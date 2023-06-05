from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # 1
from django.http import Http404  # 3
from django.views.decorators.csrf import csrf_exempt  # 1
from rest_framework.parsers import JSONParser  # 1
from rest_framework.decorators import api_view  # 2
from rest_framework.response import Response  # 2,3
from rest_framework.views import APIView  # 3
from rest_framework import status  # 2,3
from rest_framework import mixins, generics  # 3
from snippets.models import Snippet  # 1,2,3
from snippets.serializers import SnippetSerializer  # 1,2,3
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions

# Create your views here.

"""
# codigo del tutorial Nro. 2
# vista basada en funciones,
# implementada con decorador @api_view()
# @csrf_exempt   #1
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    '''
    List all code snippets, or create a new snippet.
    Enumere todos los fragmentos de código o cree uno nuevo.
    '''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)    #1
        # serializer = SnippetSerializer(data=data)     #1
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)  #1
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors, status=400)    #1
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
# codigo del tutorial Nro. 3
# vista basada en clases,
# implementada con herencia rest_framework APIView
"""
class SnippetList(APIView):
    '''
    List all code snippets, or create a new snippet.
    Enumere todos los fragmentos de código o cree uno nuevo.
    '''
    def get(self, request, format= None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def post(self, request, format= None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
# codigo del tutorial Nro. 3
# vista basada en clases,
# implementada con herencia rest_framework mixins y generics
"""
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    '''
    List all code snippets, or create a new snippet.
    Enumere todos los fragmentos de código o cree uno nuevo.
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""

# codigo del tutorial Nro. 3
# vista basada en clases,
# implementada con herencia rest_framework generics


class SnippetList(generics.ListCreateAPIView):
    '''
    List all code snippets, or create a new snippet.
    Enumere todos los fragmentos de código o cree uno nuevo.
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


"""
# codigo del tutorial Nro. 2
# vista basada en funciones,
# implementada con decorador @api_view()
# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # return HttpResponse(status=404)    #1
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        # return JsonResponse(serializer.data)    #1
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)    #1
        # serializer = SnippetSerializer(snippet, data=data)    #1
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)    #1
            return Response(serializer.data)
        # return JsonResponse(serializer.errors, status=400)    #1
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        # return HttpResponse(status=204)    #1
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# codigo del tutorial Nro. 3
# vista basada en clases,
# implementada con herencia rest_framework APIView
"""
class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
# codigo del tutorial Nro. 3
# vista basada en clases,
# implementada con herencia rest_framework mixins y generics
"""
class SnippetDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    '''
    Obtiene, actualiza o destruye un fragmentos de código.
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

# codigo del tutorial Nro. 3
# vista basada en clases,
# implementada con herencia rest_framework  generics


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Obtiene, actualiza o destruye un fragmentos de código.
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
