from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView, TemplateView, View,\
    UpdateView, DetailView
from .models import Question, Answer
from .utils import QuestionListView, CustomLoginRequiredMixin, \
    UserIsAuthorMixin
from .forms import AskForm, AnswerForm, LoginForm, SignUpForm


class NewQuestionsView(QuestionListView):
    '''Dispays latest question'''
    queryset = Question.objects.new()
    template_name = 'new_questions.html'


class PopularQuestionsView(QuestionListView):
    '''Displays question in order by likes descending'''
    queryset = Question.objects.popular()
    template_name = 'popular_questions.html'


class NoAnswersQuestionsView(QuestionListView):
    '''Displays questions without an answer'''
    queryset = Question.objects.zero_answers()
    template_name = 'empty_questions.html'


class SingleQuestionView(View):
    '''Displays page for a certain question'''
    def setup(self, request, question_id, *args, **kwargs):
        self.question = get_object_or_404(Question, id=question_id)
        super().setup(request, *args, **kwargs)

    def get(self, request, question_id):
        answer_form = AnswerForm(self.question)
        context = {'question': self.question,
                   'answers': self.question.answers.all(),
                   'answer_form': answer_form}
        return render(request, 'single_question.html', context=context)

    def post(self, request, question_id):
        user = request.user
        if not user.is_authenticated:
            return redirect('qa:login_url')
        answer_form = AnswerForm(self.question, request.POST)
        answer_form.instance.author = user
        answer_form.instance.question = self.question
        if answer_form.is_valid():
            answer_form.save()
            question = answer_form.cleaned_data['question']
            question_url = question.get_absolute_url()
            return HttpResponseRedirect(question_url)
        context = {'question': self.question,
                   'answers': self.question.answers.all(),
                   'answer_form': answer_form}
        return render(request, 'single_question.html', context=context)


class SingleAnswerView(DetailView):
    '''Displays page for a certain answer'''

    model = Answer
    context_object_name = 'answer'
    pk_url_kwarg = 'answer_id'
    template_name = 'single_answer.html'


class CreateQuestionView(CustomLoginRequiredMixin, View):
    '''Displays a page for creating new question'''
    def get(self, request):
        question_form = AskForm()
        context = {'question_form': question_form}
        return render(request, 'question_create.html', context=context)

    def post(self, request):
        url = ''
        user = request.user
        if not user.is_authenticated:
            return redirect('qa:login_url')
        question_form = AskForm(request.POST)
        question_form.instance.author = user
        if question_form.is_valid():
            question_created = question_form.save()
            question_url = question_created.get_absolute_url()
            return HttpResponseRedirect(question_url)
        context = {'question_form': question_form, 'question_url': url}
        return render(request, 'question_create.html', context=context)


class QuestionDeleteView(UserIsAuthorMixin,
                         CustomLoginRequiredMixin,
                         DeleteView):
    '''Displays a page for deleting a question'''

    context_object_name = 'question'
    pk_url_kwarg = 'question_id'
    model = Question
    success_url = '/'
    template_name = 'question_delete.html'


class AnswerDeleteView(UserIsAuthorMixin,
                       CustomLoginRequiredMixin,
                       DeleteView):
    '''Displays a page for deleting an question'''

    context_object_name = 'answer'
    pk_url_kwarg = 'answer_id'
    model = Answer
    template_name = 'answer_delete.html'

    def get_success_url(self):
        try:
            self.success_url = self.object.question.get_absolute_url()
        except ObjectDoesNotExist:
            self.success_url = '/'
        return self.success_url


class QuestionUpdateView(UserIsAuthorMixin,
                         CustomLoginRequiredMixin,
                         UpdateView):
    '''Displays a page for editing a question'''

    context_object_name = 'question'
    model = Question
    form_class = AskForm
    pk_url_kwarg = 'question_id'
    template_name = 'question_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = self.get_object().get_absolute_url()
        return self.success_url


class AnswerUpdateView(UserIsAuthorMixin,
                       CustomLoginRequiredMixin,
                       UpdateView):
    '''Displays a page for editing a question'''

    context_object_name = 'answer'
    model = Answer
    form_class = AnswerForm
    pk_url_kwarg = 'answer_id'
    template_name = 'answer_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        question = self.get_object().question
        kwargs['question'] = question
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = self.get_object().question.get_absolute_url()
        return self.success_url


class LoginView(TemplateView):
    '''Displays a login page'''
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_form = LoginForm()
        context['login_form'] = login_form
        return context

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            redirect_url = request.GET.get('next', '/')
            return HttpResponseRedirect(redirect_url)
        context = {'login_form': login_form}
        return super().render_to_response(context)


class SignUpView(TemplateView):
    '''Displays a signup page'''
    template_name = 'signuptemplate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sign_up_form = SignUpForm()
        context['sign_up_form'] = sign_up_form
        return context

    def post(self, request):
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            return LoginView().post(request)
        context = {'sign_up_form': sign_up_form}
        return render(request, 'signuptemplate.html', context=context)


class RedirectLogoutView(CustomLoginRequiredMixin, LogoutView):
    '''Redirects user to the main page after logout'''
    next_page = '/'


class AjaxLikeBtnView(View):
    '''Handles like button logic'''
    def post(self, request, question_id):
        is_authenticated = True
        if not request.user.is_authenticated:
            is_authenticated = False

        question = get_object_or_404(Question, id=question_id)
        try:
            liked = question.likes.get(id=request.user.id)
            question.likes.remove(liked)
            liked_tgl = False
        except User.DoesNotExist:
            question.likes.add(request.user.id)
            liked_tgl = True
        total_rating = question.get_total_rating()
        return JsonResponse({'question_id': question_id,
                             'rating': total_rating,
                             'liked': liked_tgl,
                             'authenticated': is_authenticated})

