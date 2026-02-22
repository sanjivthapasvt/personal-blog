#Importing bunch of required things
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

#api view for post get, post, put, delete methods
class PostViewSet(viewsets.ModelViewSet):
    #query set and also order by created at
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    #for searching and ordering
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    #Get permissions if method is get it is allowed to everyone and locked for others
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#views for comments 
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_queryset(self):
        post_slug = self.kwargs.get('post_pk')  # Get the post slug from URL
        return Comment.objects.filter(post__slug=post_slug)
    
    def perform_create(self, serializer):
        post = Post.objects.get(slug=self.kwargs['post_pk'])
        serializer.save(user=self.request.user, post=post)
