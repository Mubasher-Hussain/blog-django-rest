import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from blogs.models import Blogs, Comment
from blogs.permissions import IsAuthorOrReadOnly
from blogs.serializers import BlogsSerializer, CommentSerializer


class BlogsList(generics.ListCreateAPIView):
    """List all blogs, or create a new blog"""
    queryset = Blogs.objects.all().order_by('-updated_at')
    serializer_class = BlogsSerializer
    
    def get_queryset(self):
        """For displaying author specific posts if author is specified in url"""
        return_query = None
        if self.kwargs:
            try:
                author = User.objects.get(username=self.kwargs['author'])
                return_query = Blogs.objects.filter(author=author).order_by('-updated_at')
            except:
                print('Author not found')
        else:
            return_query = Blogs.objects.all().order_by('-updated_at')
        return return_query
            
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




class BlogsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific Blog"""
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Blogs.objects.all().order_by('-updated_at')
    serializer_class = BlogsSerializer

    def retrieve(self, request, pk):
        """For adding isAuthor field to return data for edit/delete options"""
        data = {}
        blogObj = self.get_object()
        blogSerialized = self.serializer_class(blogObj)
        data['post'] = blogSerialized.data
        if request.user.is_authenticated:
            data['isAuth'] = 'yes' if blogObj in request.user.blogs_set.all() else ''
        return Response(data)


class CommentsDetail(generics.ListCreateAPIView):
    """Create or display comments"""
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def get_queryset(self):
        """To list only Blog specific comments"""
        return_query = Comment.objects.filter(source_post_id=self.kwargs['pk']).order_by('-created_at')
        return return_query

    def perform_create(self, serializer):
        serializer.save(commentator=self.request.user, source_post=Blogs.objects.get(id=self.kwargs['pk']))
    

        
def register_request(request):
    """For registering of users"""
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            user = User.objects.create_user(body['username'], body['email'], body['password'])
            return JsonResponse({'success': "Registered."})
        except:
            return JsonResponse({'error': "Error"})
    

@ensure_csrf_cookie
def login_request(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = authenticate(username=body['username'], password=body['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'Success': 'Logged In'})
        else:
            return JsonResponse({'error': "Invalid username or password."})       


def logout_request(request):
    logout(request)
    return JsonResponse({'Success': 'Logged Out'})