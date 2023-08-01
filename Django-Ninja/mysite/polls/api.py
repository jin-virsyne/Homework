from ninja import Router
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from typing import List

from .schema import *
from .models import *

router = Router()


@router.get("/", response=List[QuestionOut])
def index(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    qs = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    return render(request, 'polls/index.html', {'latest_question_list': qs})


@router.get("/{question_id}/", response=QuestionOut)
def detail(request, question_id: int):
    """
    Excludes any questions that aren't published yet.
    """
    qs = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=question_id)
    choices = qs.choice_set.all()
    
    question_out = QuestionOut.from_orm(qs)
    question_out.choices = [ChoiceOut.from_orm(choice) for choice in choices]

    return render(request, "polls/detail.html", {"question": question_out})


@router.get("/{question_id}/results/", response=QuestionOut)
def results(request, question_id: int):
    qs = get_object_or_404(Question, pk=question_id)
    choices = qs.choice_set.all()
    
    question_out = QuestionOut.from_orm(qs)
    question_out.choices = [ChoiceOut.from_orm(choice) for choice in choices]

    return render(request, "polls/results.html", {"question": question_out})


@router.post("/{question_id}/vote/")
def vote(request, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        qs = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=question_id)
        choices = qs.choice_set.all()
        
        question_out = QuestionOut.from_orm(qs)
        question_out.choices = [ChoiceOut.from_orm(choice) for choice in choices]
    
        # Redisplay the question voting form
        return render(
            request,
            "polls/detail.html",
            {
                "question": question_out,
                "error_message": "You didn't select a choice."
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        url = f"/polls/{question_id}/results/"
        return HttpResponseRedirect(url)