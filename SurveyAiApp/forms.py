from django import forms

# Define a Django form for paragraph-based questions
class ParagraphQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your response here...'}))

# Define a Django form for multiple-choice questions
class MultipleChoiceQuestionForm(forms.Form):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for index, option in enumerate(options):
            self.fields[f'response_{index+1}'] = forms.BooleanField(label=option, required=False)

# Define a Django form for dropdown questions
class DropdownQuestionForm(forms.Form):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response'] = forms.ChoiceField(choices=[(option, option) for option in options])

# Combine all question forms into one master form
class SurveyForm(forms.Form):
    def __init__(self, questions_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question_data in questions_data:
            question_type = question_data.get('question_type')
            question_text = question_data.get('question_text')
            if question_type == 'paragraph':
                self.fields[f'question_{question_data["question_number"]}'] = forms.CharField(
                    label=question_text,
                    widget=forms.Textarea(attrs={'placeholder': 'Enter your response here...'})
                )
            elif question_type == 'multiple_choice':
                options = question_data.get('options', [])
                self.fields[f'question_{question_data["question_number"]}'] = forms.ChoiceField(
                    label=question_text,
                    choices=[(option, option) for option in options],
                    widget=forms.CheckboxSelectMultiple
                )
            elif question_type == 'dropdown':
                options = question_data.get('options', [])
                self.fields[f'question_{question_data["question_number"]}'] = forms.ChoiceField(
                    label=question_text,
                    choices=[(option, option) for option in options],
                    widget=forms.Select
                )
