from django import forms
from django.contrib import admin
from .models import Game, Post, UserProfile, Genre


class GameAdmin(admin.ModelAdmin):
    list_display = ("is_home", "title",)
    list_display_links = ("title",)
    list_editable = ("is_home",)
    search_fields = ("title", "is_home",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['genres'].required = False
        return form

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['description'].required = False


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Game, GameAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)
admin.site.register(Genre)
