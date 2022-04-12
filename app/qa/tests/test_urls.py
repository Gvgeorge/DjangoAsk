from django.test import SimpleTestCase
from django.urls import resolve, reverse
from qa.views import CreateQuestionView, NewQuestionsView, \
    PopularQuestionsView, RedirectLogoutView, NoAnswersQuestionsView, \
    SignUpView, LoginView, SingleQuestionView, QuestionDeleteView, \
    AnswerDeleteView, QuestionUpdateView, AnswerUpdateView, SingleAnswerView


class TestUrls(SimpleTestCase):

    def test_login(self):
        url = reverse('qa:login_url')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_signup(self):
        url = reverse('qa:signup_url')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_create_question(self):
        url = reverse('qa:create_question_url')
        self.assertEquals(resolve(url).func.view_class, CreateQuestionView)

    def test_popular_questions(self):
        url = reverse('qa:popular_questions_url')
        self.assertEquals(resolve(url).func.view_class, PopularQuestionsView)

    def test_new_questions(self):
        url = reverse('qa:new_questions_url')
        self.assertEquals(resolve(url).func.view_class, NewQuestionsView)

    def test_empty(self):
        url = reverse('qa:empty_questions_url')
        self.assertEquals(resolve(url).func.view_class, NoAnswersQuestionsView)

    def test_logout(self):
        url = reverse('qa:logout_url')
        self.assertEquals(resolve(url).func.view_class, RedirectLogoutView)

    def test_single_question(self):
        url = reverse('qa:single_question_url', kwargs={'question_id': 1})
        self.assertEquals(resolve(url).func.view_class, SingleQuestionView)

    def test_question_delete(self):
        url = reverse('qa:question_delete_url', kwargs={'question_id': 1})
        self.assertEquals(resolve(url).func.view_class, QuestionDeleteView)

    def test_question_update(self):
        url = reverse('qa:question_update_url', kwargs={'question_id': 1})
        self.assertEquals(resolve(url).func.view_class, QuestionUpdateView)

    def test_single_answer(self):
        url = reverse('qa:single_answer_url', kwargs={'answer_id': 1})
        self.assertEquals(resolve(url).func.view_class, SingleAnswerView)

    def test_answer_update(self):
        url = reverse('qa:answer_update_url', kwargs={'answer_id': 1})
        self.assertEquals(resolve(url).func.view_class, AnswerUpdateView)

    def test_answer_delete(self):
        url = reverse('qa:answer_delete_url', kwargs={'answer_id': 1})
        self.assertEquals(resolve(url).func.view_class, AnswerDeleteView)

