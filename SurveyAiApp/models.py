from django.db import models

# Create your models here.

# class SurveyResponse(models.Model):
#     question_number = models.IntegerField()
#     question_type = models.CharField(max_length=20)
#     question = models.CharField(max_length=100)
#     response = models.TextField()

#     def __str__(self):
#         return f"Response to question {self.question_number}"
#     class Meta:
#         app_label = 'SurveyAiApp'

# # class SurveyQuestion(models.Model):
# #     question = models.TextField()
# #     response = models.TextField()
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"Question: {self.question[:50]} - Response: {self.response[:50]}"
# #     class Meta:
# #         app_label = 'SurveyAiApp'

# # class customerSatisfaction(models.Model):
# #     question_number = models.IntegerField()
# #     question_type = models.CharField(max_length=20)
# #     question_text = models.TextField()
# #     options = models.TextField(blank=True, null=True)
# #     answer = models.TextField(null=False)

# #     class Meta:
# #         managed = True  
# #         app_label='SurveyAiApp'

# #     def __str__(self):
# #         return f"Question {self.question_number}: {self.question_text}"
    

# class customerSatisfaction1(models.Model):
#         question_number = models.IntegerField()
#         question_type = models.CharField(max_length=20)
#         question_text = models.TextField()
#         options = models.TextField(blank=True, null=True)
#         answer = models.TextField(null=False)

#         class Meta:
#             managed = True  
#             app_label='SurveyAiApp'

#         def __str__(self):
#             return f"Question {self.question_number}: {self.question_text}"
        


class Question(models.Model):
    question_text = models.CharField(max_length=500, unique=True, null=False)
    is_multi_option = models.BooleanField()
    is_descriptive = models.BooleanField()
    tag = models.CharField(max_length=30, null = True, blank=True)

    def __str__(self):
        s = str(self.question_text) 
        s += "(multi choice)" if self.is_multi_option else "(descriptive)"
        return s

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer =  models.CharField(max_length=100)


class UserSurvey(models.Model):
    user_name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_survey')
    answer =  models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.user_name} :: {self.question} -> {self.answer}'
