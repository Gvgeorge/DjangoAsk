from django.test import TestCase
from qa.models import Question, Answer


class TestModels(TestCase):
    def setUp(self):
        self.question_1 = Question.objects.create(
            title='test question 1',
            text='Loren ipsum 1',
            rating=14
            )
        self.question_2 = Question.objects.create(
            title='test question 2',
            text='Loren ipsum 2',
            rating=20
            )
        self.question_3 = Question.objects.create(
            title='test question 3',
            text='Loren ipsum 3',
            rating=16
            )
        self.answer_1 = Answer.objects.create(
            text='Answer 1', question=self.question_1)
        self.answer_2 = Answer.objects.create(
            text='Answer 2', question=self.question_1)

    def test_number_of_answers_per_question(self):
        self.assertEquals(self.question_1.answers.count(), 2)
        self.assertEquals(self.question_2.answers.count(), 0)
        self.assertNotEquals(self.question_3.answers.count, 8)

    def test_question_manager_questions_with_no_answers(self):
        self.assertIn(self.question_2, Question.objects.zero_answers())
        self.assertIn(self.question_3, Question.objects.zero_answers())
        self.assertNotIn(self.question_1, Question.objects.zero_answers())

    def test_question_manager_new_questions(self):
        self.assertEquals(Question.objects.new()[0], self.question_3)
        self.assertEquals(Question.objects.new()[1], self.question_2)
        self.assertEquals(Question.objects.new()[2], self.question_1)
        self.assertNotEquals(Question.objects.new()[1], self.question_3)

    def test_question_manager_popular_questions(self):
        self.assertEquals(Question.objects.popular()[0], self.question_2)
        self.assertEquals(Question.objects.popular()[1], self.question_3)
        self.assertEquals(Question.objects.popular()[2], self.question_1)
        self.assertNotEquals(Question.objects.popular()[1], self.question_2)

    def test_question_update_url(self):
        self.assertEquals(self.question_1.get_update_url(),
                          f'/question/{self.question_1.id}/update/')

    def test_question_delete_url(self):
        self.assertEquals(self.question_1.get_delete_url(),
                          f'/question/{self.question_1.id}/delete/')

    def test_answer_get_url(self):
        self.assertEquals(self.answer_1.get_absolute_url(),
                          f'/answer/{self.answer_1.id}/')

    def test_answer_update_url(self):
        self.assertEquals(self.answer_1.get_update_url(),
                          f'/answer/{self.answer_1.id}/update/')

    def test_answer_delete_url(self):
        self.assertEquals(self.answer_1.get_delete_url(),
                          f'/answer/{self.answer_1.id}/delete/')
