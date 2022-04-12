from django.urls import path
from .views import LoginView, PopularQuestionsView, QuestionDeleteView, \
    RedirectLogoutView, SignUpView, CreateQuestionView, NewQuestionsView, \
    NoAnswersQuestionsView, SingleQuestionView, QuestionUpdateView, \
    AnswerUpdateView, AjaxLikeBtnView, AnswerDeleteView, SingleAnswerView


app_name = 'qa'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('signup/', SignUpView.as_view(), name='signup_url'),
    path('ask/', CreateQuestionView.as_view(), name='create_question_url'),
    path('popular/', PopularQuestionsView.as_view(),
         name='popular_questions_url'),
    path('new/', NewQuestionsView.as_view(),
         name='new_questions_url'),
    path('empty/', NoAnswersQuestionsView.as_view(),
         name='empty_questions_url'),
    path('logout/', RedirectLogoutView.as_view(), name='logout_url'),
    path('question/<int:question_id>/', SingleQuestionView.as_view(),
         name='single_question_url'),
    path('question/<int:question_id>/delete/', QuestionDeleteView.as_view(),
         name='question_delete_url'),
    path('question/<int:question_id>/update/', QuestionUpdateView.as_view(),
         name='question_update_url'),
    path('answer/<int:answer_id>/update/', AnswerUpdateView.as_view(),
         name='answer_update_url'),
    path('answer/<int:answer_id>/delete/', AnswerDeleteView.as_view(),
         name='answer_delete_url'),
    path('answer/<int:answer_id>/', SingleAnswerView.as_view(),
         name='single_answer_url'),
    path('question/<int:question_id>/like', AjaxLikeBtnView.as_view(),
         name='question_like_url'),
    path('', NewQuestionsView.as_view())
]
