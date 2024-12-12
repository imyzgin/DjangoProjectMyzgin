from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Publisher)

#@admin.register(Quiz)
#class QuizAdmin(admin.ModelAdmin):
#    pass

# Register your models here.
