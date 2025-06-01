from django.db import models


class QuizCategory(models.Model):
    name = models.CharField(max_length=255)
    api_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('multiple', 'Multiple Choice'),
        ('boolean', 'True/False'),
    ]
    
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, verbose_name="Quiz Category")
    difficulty_level = models.CharField(max_length=10, default='easy', choices=DIFFICULTY_CHOICES, verbose_name="Difficulty Level")
    question = models.TextField(verbose_name="Question")
    type = models.CharField(
        max_length=10, 
        choices=QUESTION_TYPE_CHOICES,
        default='multiple', 
        verbose_name="Question Type"
    )
    incorrect_answers = models.JSONField(
        verbose_name="Incorrect Answers",
        help_text="Multiple choice uchun variantlar ro'yxati, boolean uchun bo'sh massiv"
    )
    correct_answer = models.CharField(
        max_length=255, 
        verbose_name="Correct Answer",
        help_text="Multiple choice uchun to'g'ri javob, boolean uchun 'True' yoki 'False'"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.type == 'boolean':
            if self.correct_answer not in ['True', 'False']:
                raise ValidationError("Boolean savol uchun correct_answer 'True' yoki 'False' bo'lishi kerak")
            if self.incorrect_answers != []:
                raise ValidationError("Boolean savol uchun incorrect_answers bo'sh massiv bo'lishi kerak")
        
        if self.type == 'multiple' and not self.incorrect_answers:
            raise ValidationError("Multiple choice savol uchun incorrect_answers to'ldirilishi shart")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.question[:20]}"



class QuotesForBio(models.Model):
    author = models.CharField(max_length=255, verbose_name="Quotes author")
    quote = models.TextField(verbose_name="Quote text")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.author} - {self.quote[:30]}"

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"


class DailyFunFact(models.Model):
    text = models.TextField(verbose_name="Fun fact text")
    options = models.JSONField(verbose_name="Fun fact options")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.text[:30]}"

class FamousQuotes(models.Model):
    quote = models.TextField(verbose_name="Famous quote text")
    author = models.CharField(max_length=255, verbose_name="Famous quote author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.quote[:30]} - {self.author}"
