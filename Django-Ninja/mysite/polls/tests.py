import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice

# Create your tests here.
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_question_w_choice(question_text, days = 0):
    """
    Create a question with the given `question_text` and create choices
    to pair with the question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    Choice.objects.create(question=question, choice_text="choice1")
    Choice.objects.create(question=question, choice_text="choice2")
    return question


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get("/polls/")
        assert response.status_code == 200
        assert "No polls are available." in response.content.decode()
        assert "latest_question_list" in response.context
        assert len(response.context["latest_question_list"]) == 0
        
    
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get("/polls/")
        assert list(response.context["latest_question_list"]) == [question]
        
        
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get("/polls/")
        assert "No polls are available." in response.content.decode()
        assert "latest_question_list" in response.context
        assert len(response.context["latest_question_list"]) == 0
        
        
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get("/polls/")
        assert list(response.context["latest_question_list"]) == [question]
        
    
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get("/polls/")
        assert set(response.context["latest_question_list"]) == {question2, question1}


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = f"/polls/{future_question.id}/"
        response = self.client.get(url)
        assert response.status_code == 404
        
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text and the choice's text.
        """
        past_question = create_question_w_choice(question_text="Past Question.", days=-5)
        url = f"/polls/{past_question.id}/"
        response = self.client.get(url)
        assert past_question.question_text in response.content.decode()
        assert "choice2" in response.content.decode()
        
    
    def test_vote_submission_success(self):
        """
        A success vote submission will redirect user to Results page,
        and shows increment value in the votes
        """
        question = create_question_w_choice(question_text="Question.")
        choices = question.choice_set.all()
        form_data = { "choice": choices[0].id }
        
        response = self.client.post(f"/polls/{question.id}/vote/", data=form_data)
        assert response.status_code == 302
        url = f"/polls/{question.id}/results/"
        assert response.url == url
        
        response = self.client.get(url)
        assert f"{choices[0].choice_text} -- 1" in response.content.decode()
        assert f"{choices[1].choice_text} -- 0" in response.content.decode()
        
        
    def test_vote_submission_failed(self):
        """
        A failed vote submission will return user to Detail page
        with an error message
        """
        question = create_question_w_choice(question_text="Question.")
        form_data = {}
        
        response = self.client.post(f"/polls/{question.id}/vote/", data=form_data)
        assert "You didn't select a choice." in response.context["error_message"]


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        assert future_question.was_published_recently() == False


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        assert old_question.was_published_recently() == False
   
        
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        assert recent_question.was_published_recently() == True