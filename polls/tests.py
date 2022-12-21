import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        # returns False if the question is in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        # returns True if the question was published within the last day
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_question = Question(pub_date=time)
        self.assertIs(published_question.was_published_recently(), True)


class IndexViewTest(TestCase):
    def test_no_questions(self):
        # If there are no questions, an appropriate message is shown
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question_being_displayed(self):
        past_question = create_question(question_text='my question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [past_question]
                                 )

    def test_future_question_and_past_question(self):
        # If a future question and a past question exists, only a past one is displayed
        future_question = create_question(question_text="my future question", days=20)
        past_question = create_question(question_text="past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_question(self):
        # checks whether both past questions are displayed
        past_question1 = create_question(question_text='question1', days=-30)
        past_question2 = create_question(question_text='question2', days=-90)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question1, past_question2])

class QuestionDetailViewTest(TestCase):
    def test_past_question_detail_view(self):
        past_question = create_question(question_text='text', days=-30)
        url = reverse('polls:details', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:details', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)