from typing import List
from .models import *
from ninja import ModelSchema

class ChoiceIn(ModelSchema):
    class Config:
        model = Choice
        model_fields = ["choice_text", "votes"]

class ChoiceOut(ModelSchema):
    class Config:
        model = Choice
        model_fields = ["id", "choice_text", "votes"]
        
class QuestionIn(ModelSchema):
    choices: List[ChoiceIn] = []
    
    class Config:
        model = Question
        model_fields = ["question_text", "pub_date"]

class QuestionOut(ModelSchema):
    choices: List[ChoiceOut] = []
    
    class Config:
        model = Question
        model_fields = ["id", "question_text", "pub_date"]
    