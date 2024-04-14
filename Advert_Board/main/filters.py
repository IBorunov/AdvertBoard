from django_filters import ModelChoiceFilter, FilterSet

from .models import Response, Post


class ResponseFilter(FilterSet):
    post = ModelChoiceFilter(
        queryset=Response.objects.all(),
        lookup_expr='exact',
        label='Объявление',
        empty_label='Все объявления',
        field_name='post_id'
    )

    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])

