def paginate(request, objects):
    '''
    Pagination with validation checks
    deprecated
    '''
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(objects, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def new_questions_view(request):
    '''
    View for the question objects listed sorted by addition date desc
    deprecated
    '''
    new_questions = Question.objects.new()
    page = paginate(request, new_questions)
    context = {'questions': new_questions, 'page': page}
    return render(request, 'new_questions.html', context=context)


def popular_questions_view(request):
    '''
    View for the question objects listed sorted by popularity desc
    '''
    popular_questions = Question.objects.popular()
    page = paginate(request, popular_questions)
    context = {'questions': popular_questions, 'page': page}
    return render(request, 'new_questions.html', context=context)

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            request.session.SESSION_COOKIE_NAME = get_random_string(length=32)
            request.session.set_expiry(432000)
            user = login_form.cleaned_data['user']
            request.session['user'] = user.id
            return HttpResponseRedirect('/')
    else:
        login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        user_creation_form = SignUpForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return login_view(request)
    else:
        user_creation_form = SignUpForm()
    context = {'user_creation_form': user_creation_form}
    return render(request, 'signup.html', context)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user_with_the_same_username = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if user_with_the_same_username:
            raise ValidationError('User with the same username already exists.')
        user_with_the_same_email = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if user_with_the_same_email:
            raise ValidationError('User with the same email already exists')
        return self.cleaned_data

    def save(self):
        return User.objects.create_user(**self.cleaned_data)


def single_question_view(request, question_id):
    '''
    View function for single question
    '''
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        user_id = request.session.get('user')
        if not user_id:
            return redirect('qa:login_url')
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.cleaned_data['question'] = question
            user = User.objects.get(id=user_id)
            answer_form.cleaned_data['author'] = user
            answer_form.save()
            url = question.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        answer_form = AnswerForm(initial={'question': question.id})
    context = {'question': question, 'answers': question.answers.all(), 'answer_form': answer_form}
    return render(request, 'single_question.html', context=context)

def create_question_view(request):
    url = ''
    if request.method == 'POST':
        user_id = request.session.get('user')
        if not user_id:
            return redirect('qa:login_url')
        question_form = AskForm(request.POST)
        if question_form.is_valid():
            user = User.objects.get(id=user_id)
            question_form.cleaned_data['author'] = user
            question_created = question_form.save()
            question_url = question_created.get_absolute_url()
            return HttpResponseRedirect(question_url)
    else:
        question_form = AskForm()
    context = {'question_form': question_form, 'question_url': url}
    return render(request, 'question_create.html', context=context)
