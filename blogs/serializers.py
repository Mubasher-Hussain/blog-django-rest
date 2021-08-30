from rest_framework import serializers
from .models import Blogs, Comment


class BlogsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Blogs 
        fields = ('id', 'title', 'content', 'author', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    commentator = serializers.ReadOnlyField(source='commentator.username')
    source_post = serializers.ReadOnlyField(source='source_post.id')
    class Meta:
        model = Comment 
        fields = ('id', 'content', 'commentator', 'source_post', 'created_at' )
