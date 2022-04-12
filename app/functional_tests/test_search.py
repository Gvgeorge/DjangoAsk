from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse
from urllib.parse import urlparse, urlunparse
import time
from qa.models import Question, Answer
from selenium.webdriver import FirefoxOptions

# opts = FirefoxOptions()
# opts.add_argument("--headless")
# browser = webdriver.Firefox(firefox_options=opts)


class TestSearchForm(StaticLiveServerTestCase):
    def setUp(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")

        self.browser = webdriver.Firefox('functional_tests/', options=opts)
        self.user = User.objects.create(username='test_user', password='12345')
        self.another_user = User.objects.create(
            username='another_user', password='12345')
        self.question_1 = Question.objects.create(
            title='test question 1',
            text='Loren ipsum 1',
            rating=14,
            author=self.user
            )
        self.question_2 = Question.objects.create(
            title='test question 2',
            text='Loren ipsum 2',
            rating=20
            )
        self.question_3 = Question.objects.create(
            title='test question 3',
            text='Loren ipsum 3',
            rating=16,
            author=self.user
        )
        self.answer_1 = Answer.objects.create(text='Answer 1',
                                              question=self.question_1,
                                              author=self.user)
        self.answer_2 = Answer.objects.create(
            text='Answer 2', question=self.question_1)

    def tearDown(self):
        self.browser.close()

    def test_search_front_page(self):
        search_string = 'ipsum 1'
        qstr = urlencode({'search': search_string})
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element_by_name('search').send_keys(search_string)
        time.sleep(2)
        self.browser.find_element_by_class_name('btn-outline-success').click()
        time.sleep(2)
        url = urlparse(self.browser.current_url)
        unparsed_url = urlunparse(('', '', url.path, '', url.query, ''))
        self.assertEquals(unparsed_url, '/?' + qstr)
        question_list = self.browser.find_elements_by_class_name(
            'question_container')
        self.assertEquals(len(question_list), 1)

    def test_search_new(self):
        search_string = 'ipsum 1'
        qstr = urlencode({'search': search_string})
        self.browser.get(self.live_server_url +
                         reverse('qa:new_questions_url'))
        time.sleep(2)
        self.browser.find_element_by_name('search').send_keys(search_string)
        time.sleep(2)
        self.browser.find_element_by_class_name('btn-outline-success').click()
        time.sleep(2)
        url = urlparse(self.browser.current_url)
        unparsed_url = urlunparse(('', '', url.path, '', url.query, ''))
        self.assertEquals(
            unparsed_url, reverse('qa:new_questions_url') + '?' + qstr)
        question_list = self.browser.find_elements_by_class_name(
            'question_container')
        self.assertEquals(len(question_list), 1)

    def test_search_popular(self):
        search_string = 'ipsum 1'
        qstr = urlencode({'search': search_string})
        self.browser.get(
            self.live_server_url + reverse('qa:popular_questions_url'))
        time.sleep(2)
        self.browser.find_element_by_name('search').send_keys(search_string)
        time.sleep(2)
        self.browser.find_element_by_class_name('btn-outline-success').click()
        time.sleep(2)
        url = urlparse(self.browser.current_url)
        unparsed_url = urlunparse(('', '', url.path, '', url.query, ''))
        self.assertEquals(unparsed_url,
                          reverse('qa:popular_questions_url') + '?' + qstr)
        question_list = self.browser.find_elements_by_class_name(
            'question_container')
        self.assertEquals(len(question_list), 1)

    def test_search_empty(self):
        search_string = 'ipsum 3'
        qstr = urlencode({'search': search_string})
        self.browser.get(self.live_server_url + reverse(
            'qa:empty_questions_url'))
        time.sleep(2)
        self.browser.find_element_by_name('search').send_keys(search_string)
        time.sleep(2)
        self.browser.find_element_by_class_name('btn-outline-success').click()
        time.sleep(2)
        url = urlparse(self.browser.current_url)
        unparsed_url = urlunparse(('', '', url.path, '', url.query, ''))
        self.assertEquals(unparsed_url,
                          reverse('qa:empty_questions_url') + '?' + qstr)
        question_list = self.browser.find_elements_by_class_name(
            'question_container')
        self.assertEquals(len(question_list), 1)

    def test_search_from_another_page(self):
        search_string = 'ipsum 1'
        qstr = urlencode({'search': search_string})
        self.browser.get(self.live_server_url +
                         self.question_2.get_absolute_url())
        time.sleep(2)
        self.browser.find_element_by_name('search').send_keys(search_string)
        time.sleep(2)
        self.browser.find_element_by_class_name('btn-outline-success').click()
        time.sleep(2)
        url = urlparse(self.browser.current_url)
        unparsed_url = urlunparse(('', '', url.path, '', url.query, ''))
        self.assertEquals(unparsed_url, '/?' + qstr)
        question_list = self.browser.find_elements_by_class_name(
            'question_container')
        self.assertEquals(len(question_list), 1)
