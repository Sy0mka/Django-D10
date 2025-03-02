from django.core.exceptions import ValidationError
from django.utils import timezone
from timezone_field import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

    def clean(self):
        user = self.instance.author.user
        today_posts = Post.objects.filter(
            author__user=user,
            created_at__date=timezone.now().date()
        ).count()
        if today_posts >= 3:
            raise ValidationError('Нельзя публиковать более 3 новостей в сутки!')
        return super().clean()