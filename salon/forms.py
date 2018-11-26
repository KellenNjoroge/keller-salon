from .models import *
from django import forms


# class NewImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         exclude = ['profile', 'likes', 'imagecomments',]


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = []
        fields = ['profilepic', 'bio','username', 'contact']


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        exclude = []
        fields = ['first_name', 'last_name', 'email']


class NewTown(forms.ModelForm):
    class Meta:
        model = Town
        fields = ['name', 'bio']


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['hood', 'poster']


class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['commentator','comment_post']


# class NewProject(forms.ModelForm):
#     class Meta:
#         model = Project
#         exclude = ['likes', 'profile',]
#
#
# class NewVote(forms.ModelForm):
#     class Meta:
#         model = Vote
#         exclude = ['voter','project']