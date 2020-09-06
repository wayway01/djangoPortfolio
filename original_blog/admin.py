from django.contrib import admin
from .models import Post, Comment, Reply, Tag

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5

class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]

class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text')
    list_display = ['title', 'is_public', 'date_updated', 'date_created', 'title_len']
    list_filter = ['is_public', 'tag']
    ordering = ('-date_updated')

    def title_len(self, obj):
        return len(obj.title)

    title_len.short_description = 'タイトル文字数'


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tag)
