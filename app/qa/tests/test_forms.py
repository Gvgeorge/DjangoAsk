from django.test import TestCase
from qa.forms import AskForm, AnswerForm
from qa.models import Question


class TestForms(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            title='test question 1',
            text='Loren ipsum 1',
            rating=14
        )

    def test_ask_form_valid_data(self):
        form = AskForm(data={'title': 'Test title', 'text': 'Test text'})
        self.assertTrue(form.is_valid())

    def test_ask_form_invalid_data(self):
        form = AskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)

    def test_answer_form_valid_data(self):
        form = AnswerForm(self.question, data={'text': 'Test text'})
        self.assertTrue(form.is_valid())

    def test_answer_form_invalid_data(self):
        form = AnswerForm(self.question, data={})
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)




