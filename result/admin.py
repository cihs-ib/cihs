from django.contrib import admin
from .models import BTUTOR, CNAME, QSUBJECT, Edit_User, QUESTION, TUTOR_HOME
admin.site.register(TUTOR_HOME)#
#admin.register(TUTOR_HOME)
########################################################
# Define the admin class
class subject_main(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'tutor',  'updated', 'fagr', 'sagr', 'sagr', 'avr')
    fields = [('student_name', 'gender', 'cader', 'student_id'), ('test', 'agn', 'atd', 'total', 'exam', 'agr', 'fagr', 'sagr', 'aagr', 'avr'), ('grade', 'posi'),'tutor']#, 'subject']

@admin.register(BTUTOR)
class model_teacher(admin.ModelAdmin):
    list_display = ('accounts', 'teacher_name', 'subject', 'Class', 'subject_teacher_id', 'session', 'males',  'females')
    fields = [('model_in','accounts', 'teacher_name'), ('subject', 'Class', 'first_term', 'second_term', 'third_term', 'males',  'females'), ('term', 'session')]

@admin.register(CNAME)
class model_names(admin.ModelAdmin):
    list_display = ('uid', 'Class','full_name', 'updated', 'session', 'age', 'total_scores', 'grade', 'posi', 'no', 'dept')
    fields = [('uid', 'last_name', 'first_name', 'full_name', 'Class'), ('gender', 'birth_date'), ('no_open', 'no_present', 'no_absent', 'comment'), ('H_begin', 'H_end', 'W_begin', 'W_end', 'no_of_day_abs', 'purpose'), ('good', 'fair', 'poor', 'remark'), ('event', 'indoor', 'ball', 'combat', 'track', 'jump', 'throw', 'swim', 'lift', 'sport_comment'), ('club_one', 'club_two', 'office_one', 'office_two', 'contrib_one', 'contrib_two')]

@admin.register(Edit_User)
class model_profile(admin.ModelAdmin):
    list_display = ('title', 'user','department')
    fields = [('title', 'user', 'account_id', 'class_in'), ('photo', 'image'), 'bio', ('phone', 'city', 'country', 'organization', 'location', 'birth_date', 'department'), 'email_confirmed', ('session', 'resumption')]

@admin.register(QUESTION)
class model_QUESTION(admin.ModelAdmin):
    list_display = ('id','subjects', 'classes', 'terms', 'questNum', 'updated')
    fields = [('subjects', 'classes', 'terms', 'questNum', 'CORRECT'), ('question', 'photo', 'image'), ('optionA', 'optionB', 'optionC', 'optionD'), ('answerA', 'answerB', 'answerC', 'answerD'), 'comment']

admin.site.register(QSUBJECT, subject_main)#second_term
# Register your models here.
