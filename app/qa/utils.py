from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


class QuestionListView(ListView):
    context_object_name = 'questions'
    paginate_orphans = 3

    def setup(self, request, *args, **kwargs):
        '''parent class for all questionlist views'''
        try:
            page_size = int(request.GET.get('limit', 15))
        except ValueError:
            page_size = 15
        if page_size > 100:
            page_size = 15
        self.paginate_by = page_size
        self.search_string = request.GET.get('search')
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disable_search_redirect'] = True
        return context

    def get_queryset(self):
        if not self.search_string:
            return super().get_queryset()
        queryset = self.queryset.filter(
            Q(title__icontains=self.search_string) |
            Q(text__icontains=self.search_string))
        return queryset


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
    permission_denied_message = 'Please log in'
    raise_exception = False


class UserIsAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_permission_denied_message(self):
        return f'You have to be the author of the \
            {self.model.__name__.lower()} to edit or delete it'
