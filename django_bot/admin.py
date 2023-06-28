from django.contrib import admin

from django_bot.models import QuestionKeyword, Keyword, Question, AllowedLinks


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword')


class QuestionKeywordAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'keyword_text')

    def question_text(self, obj):
        return obj.question.__str__()

    def keyword_text(self, obj):
        return obj.keyword.__str__()


class AllowedLinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'link')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(QuestionKeyword, QuestionKeywordAdmin)
admin.site.register(AllowedLinks, AllowedLinksAdmin)
