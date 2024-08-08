from rest_framework import serializers
from blog.models import BlogModel

class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogModel
        excludes = ["created_at", "updated_at"]
        fields = [
                'user',
                'title',
                'blog_text',
                'main_img', 'uid']