from django.contrib import admin
from ...Quiz.models.QuizModel import QuizCategory, QuizQuestion, QuotesForBio, FamousQuotes, DailyFunFact
from unfold.admin import ModelAdmin


@admin.register(QuizCategory)
class QuizCategoryAdmin(ModelAdmin):
    list_display = ('name', 'created_at')  # Jadval ustunlari
    search_fields = ('name',)  # Qidiruv uchun ustunlar


@admin.register(QuizQuestion)
class QuizQuestionAdmin(ModelAdmin):
    list_display = ('question', 'category', 'difficulty_level', 'created_at')  # Jadval ustunlari
    search_fields = ('question', 'category__name', 'difficulty_level')  # Qidiruv uchun ustunlar
    list_filter = ('category__name', 'difficulty_level')  # Filtrlash uchun ustunlar
    list_per_page = 10  # Sahifa ba'zi ustunlarini ko'rsatish




@admin.register(QuotesForBio)
class QuotesForBioAdmin(ModelAdmin):
    list_display = ('author', 'quote', 'created_at')  # Jadval ustunlari
    search_fields = ('author', 'quote')  # Qidiruv uchun ustunlar
    list_per_page = 20  # Sahifa ba'zi ustunlarini ko'rsatish

@admin.register(DailyFunFact)
class DailyFunFactAdmin(ModelAdmin):
    list_display = ('text', 'created_at')  # Jadval ustunlari
    search_fields = ('text',)  # Qidiruv uchun ustunlar
    list_per_page = 20  # Sahifa ba'zi ustunlarini ko'rsatish
    
@admin.register(FamousQuotes)
class FamousQuotesAdmin(ModelAdmin):
    list_display = ('quote', 'author', 'created_at')  # Jadval ustunlari
    search_fields = ('quote', 'author')  # Qidiruv uchun ustunlar
    list_per_page = 20  # Sahifa ba'zi ustunlarini ko'rsatish


