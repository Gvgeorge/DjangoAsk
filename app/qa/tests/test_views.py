from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from qa.views import CreateQuestionView, NewQuestionsView, PopularQuestionsView, \
    RedirectLogoutView, NoAnswersQuestionsView, SignUpView, LoginView, \
    SingleQuestionView, QuestionDeleteView, AnswerDeleteView, QuestionUpdateView, \
    AnswerUpdateView, SingleAnswerView
from qa.models import Question, Answer, QuestionManager
from urllib.parse import urlencode


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test_user', password='12345')
        self.another_user = User.objects.create(username='another_user', password='12345')
        self.question_1 = Question.objects.create(
            title='test question 1',
            text = 'Loren ipsum 1',
            rating = 14,
            author = self.user
            )
        self.question_2 = Question.objects.create(
            title='test question 2',
            text = 'Loren ipsum 2',
            rating = 20
            )
        self.question_3 = Question.objects.create(
            title='test question 3',
            text = 'Loren ipsum 3',
            rating = 16,
            author=self.user
        )
        self.answer_1 = Answer.objects.create(text='Answer 1',
                                              question=self.question_1,
                                              author=self.user)
        self.answer_2 = Answer.objects.create(text='Answer 2', question=self.question_1)

    def test_new_questions_view(self):
        response = self.client.get(reverse('qa:new_questions_url'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('new_questions.html')
        self.assertTemplateNotUsed('random_template_name_that_doesnt_exist.html')

    def test_popular_questions_view(self):
        response = self.client.get(reverse('qa:popular_questions_url'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('popular_questions.html')
        self.assertTemplateNotUsed('random_template_name_that_doesnt_exist.html')

    def test_empty_questions_view(self):
        response = self.client.get(reverse('qa:empty_questions_url'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('empty_questions.html')
        self.assertTemplateNotUsed('random_template_name_that_doesnt_exist.html')

    def test_single_question_view_get(self):
        response = self.client.get(reverse('qa:single_question_url',
                                           kwargs={'question_id': self.question_1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('single_question.html')
        self.assertTemplateNotUsed('random_template_name_that_doesnt_exist.html')

    def test_single_answer_view_get(self):
        response = self.client.get(reverse('qa:single_answer_url',
                                           kwargs={'answer_id': self.answer_1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('single_answer.html')
        self.assertTemplateNotUsed('random_template_name_that_doesnt_exist.html')

    def test_single_question_view_post(self):
        self.assertEquals(Question.objects.all().count(), 3)
        self.client.force_login(self.user)
        response = self.client.post(reverse('qa:create_question_url'),
                                    {'title': 'Test question 4 title','text': 'test question 4 text'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,reverse('qa:single_question_url',
                                              kwargs={'question_id': Question.objects.new()[0].id}))
        self.assertEquals(Question.objects.all().count(), 4)
        self.assertEquals(Question.objects.new()[0].title, 'Test question 4 title')
        self.assertEquals(Question.objects.new()[0].text, 'test question 4 text')
        self.assertNotEquals(Question.objects.new()[0].title, 'random string')
        self.assertNotEquals(Question.objects.new()[0].text, 'random string')
        self.assertTemplateUsed('single_answer.html')
        self.assertTemplateNotUsed('random_template_name_that_doesnt_exist.html')

    def test_single_answer_post(self):
        self.assertEquals(self.question_1.answers.count(),2)
        question_1_url = self.question_1.get_absolute_url()
        response = self.client.post(question_1_url, {'text': 'Test answer'})
        self.assertRedirects(response, reverse('qa:login_url'))
        self.client.force_login(self.user)
        response = self.client.post(question_1_url, {'text': 'Test answer'})
        self.assertRedirects(response,question_1_url)
        self.assertEquals(self.question_1.answers.count(),3)

    def test_authorization(self):
        response = self.client.post(reverse('qa:create_question_url'),
                                    {'title': 'Test question 4 title','text': 'test question4 text'})
        self.assertEquals(response.status_code, 302)
        qstr = urlencode({'next':'/ask/'})
        self.assertRedirects(response, reverse('qa:login_url') + '?' + qstr)
        self.assertEquals(response.wsgi_request.user.is_authenticated, False)
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEquals(response.wsgi_request.user.is_authenticated, True)
        self.assertEquals(response.wsgi_request.user.username,'test_user')
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/')
        response = self.client.get('/')
        self.assertEquals(response.wsgi_request.user.is_authenticated, False)

    def test_update_question(self):
        response = self.client.post(self.question_1.get_update_url(),
                                    {'title': 'Test question 1 updated',
                                     'text': 'test question 1 updated'})
        self.assertEquals(response.status_code, 302)
        qstr = urlencode({'next': self.question_1.get_update_url()})
        self.assertRedirects(response, reverse('qa:login_url') + '?' + qstr)
        self.client.force_login(self.another_user)
        response = self.client.post(self.question_1.get_update_url(),
                                    {'title': 'Test question 1 updated',
                                     'text': 'test question 1 updated'})
        self.assertEquals(response.status_code, 403)
        self.assertNotEquals(response.status_code, 200)
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.post(self.question_1.get_update_url(),
                                    {'title': 'Title question 1 updated',
                                     'text': 'Text question 1 updated'})
        self.assertEquals(response.wsgi_request.user.is_authenticated, True)
        self.assertEquals(response.wsgi_request.user.username, 'test_user')
        self.assertRedirects(response, self.question_1.get_absolute_url())
        self.question_1.refresh_from_db()
        self.assertEquals(self.question_1.title, 'Title question 1 updated')
        self.assertEquals(self.question_1.text, 'Text question 1 updated')

    def test_delete_question(self):
        self.assertEquals(Question.objects.all().count(), 3)
        question_3_url = self.question_3.get_absolute_url()
        response = self.client.get(self.question_3.get_delete_url())
        self.assertEquals(response.status_code, 302)
        qstr = urlencode({'next': self.question_3.get_delete_url()})
        self.assertRedirects(response, reverse('qa:login_url') + '?' + qstr)
        self.client.force_login(self.another_user)
        response = self.client.get(self.question_3.get_delete_url())
        self.assertEquals(response.status_code, 403)
        self.assertNotEquals(response.status_code, 200)
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.get(self.question_3.get_delete_url())
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.question_3.get_delete_url(), {})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')
        response = self.client.get(question_3_url)
        self.assertEquals(response.status_code, 404)
        self.assertRaises(Question.DoesNotExist, self.question_3.refresh_from_db)
        self.assertEquals(Question.objects.all().count(), 2)

    def test_update_answer(self):
        response = self.client.post(self.answer_1.get_update_url(),
                                    {'text': 'test answer 1 updated'})
        self.assertEquals(response.wsgi_request.user.is_authenticated, False)
        self.assertEquals(response.status_code, 302)
        qstr = urlencode({'next': self.answer_1.get_update_url()})
        self.assertRedirects(response, reverse('qa:login_url') + '?' + qstr)
        self.client.force_login(self.another_user)
        response = self.client.post(self.answer_1.get_update_url(),
                                    {'text': 'test answer 1 updated'})
        self.assertEquals(response.status_code, 403)
        self.assertNotEquals(response.status_code, 200)
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.post(self.answer_1.get_update_url(),
                                    {'text': 'test answer 1 updated'})
        self.assertEquals(response.wsgi_request.user.is_authenticated, True)
        self.assertEquals(response.wsgi_request.user.username, 'test_user')
        self.assertRedirects(response, self.answer_1.question.get_absolute_url())
        self.answer_1.refresh_from_db()
        self.assertEquals(self.answer_1.text, 'test answer 1 updated')

    def test_delete_answer(self):
        self.assertEquals(self.question_1.answers.count(), 2)
        answer_1_url = self.answer_1.get_absolute_url()
        response = self.client.get(self.answer_1.get_delete_url())
        self.assertEquals(response.status_code, 302)
        qstr = urlencode({'next': self.answer_1.get_delete_url()})
        self.assertRedirects(response, reverse('qa:login_url') + '?' + qstr)
        self.client.force_login(self.another_user)
        response = self.client.get(self.answer_1.get_delete_url())
        self.assertEquals(response.status_code, 403)
        self.assertNotEquals(response.status_code, 200)
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.get(self.answer_1.get_delete_url())
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.answer_1.get_delete_url(), {})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.question_1.get_absolute_url())
        response = self.client.get(answer_1_url)
        self.assertEquals(response.status_code, 404)
        self.assertRaises(Answer.DoesNotExist, self.answer_1.refresh_from_db)
        self.assertEquals(self.question_1.answers.count(), 1)

    def test_search_unittest(self):
        qstr = urlencode({'search': '1'})
        response = self.client.get(reverse('qa:new_questions_url') + '?' + qstr)
        self.assertEquals(len(response.context_data['object_list']), 1)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('qa:popular_questions_url') + '?' + qstr)
        self.assertEquals(len(response.context_data['object_list']), 1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context_data['object_list'][0].title, 'test question 1')
        self.assertEquals(response.context_data['object_list'][0].text, 'Loren ipsum 1')


        response = self.client.get(reverse('qa:empty_questions_url') + '?' + qstr)
        self.assertEquals(len(response.context_data['object_list']), 0)
        self.assertEquals(response.status_code, 200)













