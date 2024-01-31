from .models import QSUBJECT, Edit_User, BTUTOR, CNAME,  TUTOR_HOME, QUESTION
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.contrib.auth.decorators import login_required
from .updates import average
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg
from django.http import JsonResponse
from django.views.generic import View
import os, csv, json
from django.http import HttpResponse
#from io import BytesIO
import requests
from django.utils import timezone  
module_dir = os.path.dirname(__file__)  # get current directory
#########################################################################################################################
start_time =  time.time()
from random import randrange
from collections import Counter
from .utils import session, Render, Rendered, do_positions, generate_zip, do_grades, cader 
session = session()
 

def offline(request, pk):
    if request.user.is_authenticated:
        if request.user.profile.email_confirmed:
            mains = [BTUTOR.objects.filter(Class__exact=i).order_by('subject') for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
            tutor = None
            if pk != 0:
                tutor = BTUTOR.objects.get(pk=pk)
            return render(request, 'result/desktops.html',{'pk':1, 'names':[i for i in range(100)], 'jss1':mains[0], 'jss2':mains[1], 'jss3':mains[2], 'sss1':mains[3], 'sss2':mains[4], 'sss3':mains[5], 'qry':tutor})
        else:
            return redirect('home')
    else:
        return redirect('subject_view', pk=pk, md=1)

def uniqueness(request, pk): 
    tutor = BTUTOR.objects.get(pk=pk) 
    unique = TUTOR_HOME.objects.filter(first_term__accounts__exact=tutor.accounts, first_term__session__exact = tutor.session)
    return render(request, 'result/page.html', {'tutor':unique.first(), 'page':unique})


def home(request):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every tutor!
    """
    # If a tutor is authenticated then redirect them to the tutor's page
    #[i.save() for i in CNAME.objects.all()]
    if request.user.is_authenticated:#a tutor page 
        page = TUTOR_HOME.objects.filter(tutor=request.user).order_by('created')#, first_term__session__exact=session.profile.session).order_by('id')
        import datetime
        present = datetime.datetime.today()
        past = request.user.last_login
        if not QSUBJECT.objects.all():
           tutors = BTUTOR.objects.all()
           for i in tutors:
                i.second_term = '1st Term' 
                i.third_term = '1st Term'
                i.save()
        if present.year != past.year or present.month != past.month or present.day != past.day:
            login_count = request.user.profile.login_count
            login_count += 1
            user = Edit_User.objects.get(user=request.user)
            user.login_count = login_count
            user.save()
        return render(request, 'result/page.html', {'page':page, 'tutor':page.first()})
    else:#general login page
        return redirect('logins')

def student_exam_page(request, subj_code, pk):
    info = get_object_or_404(CNAME, pk=pk)
    sub_code = ["ACC", "AGR", "ARB", "BIO", "BST", "BUS", "CHE", "CIV", "COM", "CTR", "ECO", "ELE", "ENG", "FUR", "GEO", "GOV", "GRM", "HIS", "ICT", "IRS", "LIT", "MAT", "NAV", "PHY", "PRV", "YOR"]
    if request.GET.get('done', False) != False:
        qr = QSUBJECT.objects.filter(student_name_id__exact=info.id,tutor__subject__exact=sub_code[int(subj_code)], tutor__session__exact=session.profile.session)
        if qr:
          qr.first().exam = int(request.GET.get('scores'))
        else:
          qr = QSUBJECT(student_name=info, exam=int(request.GET.get('scores')), tutor=BTUTOR.objects.filter(Class__exact=info.Class,subject__exact=sub_code[int(subj_code)],session__exact=session.profile.session).first())
        qr.save()
        return JsonResponse({'status':str(qr.created)})

    quetions = QUESTION.objects.filter(subjects__exact=sub_code[int(subj_code)], classes__exact=info.Class, terms__exact=info.term, session__exact= session.profile.session)
    return render(request, 'result/quetions.html', {'quetions':quetions, 'Subject':sub_code[int(subj_code)], 'Class':info.Class, 'Term':info.term})


#@login_required
def student_home_page(request, pk):
    info = get_object_or_404(CNAME, pk=pk)
    if request.GET.get('pk', False) != False:
        qr = QSUBJECT.objects.get(pk=int(request.GET.get('pk', False)))
        return JsonResponse({'status':str(qr.delete())})
    query = QSUBJECT.objects.filter(student_name_id__exact=info.id, tutor__term__exact='1st Term', tutor__session__exact=session.profile.session, tutor__Class__exact=info.Class).order_by('updated')
    return render(request, 'result/student_form.html', {'info':info, 'detail':query})
       
            #
def paginator(request, pages):
    page = request.GET.get('page', 1)
    paginator = Paginator(pages, 30)
    try:
        all_page = paginator.page(page)
    except PageNotAnInteger:
        all_page = paginator.page(1)
    except EmptyPage:
        all_page = paginator.page(paginator.num_pages)
    return all_page


def subject_home(request, pk, cl):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every subject!
    """
    tutor = BTUTOR.objects.get(pk=pk)
    if cl == 1:#class
        detail = 'Results filtered by Class'
        tutor = BTUTOR.objects.filter(Class__exact=tutor.Class).order_by('session')
    elif cl == 2:#term
        detail = 'Results filtered by Term'
        tutor = BTUTOR.objects.filter(term__exact=tutor.term).order_by('session')
    elif cl == 3:#subject
        detail = 'Results filtered by Subject'
        tutor = BTUTOR.objects.filter(subject__exact=tutor.subject).order_by('subject')
    if tutor.count() != 0:    
        return render(request, 'result/tutor_class_filter.html', {'all_page': paginator(request, tutor), 'detail' : detail, 'counts':tutor.count()})
    else:
        return redirect('home') 
def save(mod, posi, pk):
    obj = get_object_or_404(mod, pk=pk)
    obj.posi = posi
    obj.save()

def common(request, pk):
    tutor = get_object_or_404(BTUTOR, pk=pk)
    tutor.save()
    th = [i[0] for i in list(QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id').values_list('posi'))]
    if 'th' in th:
        posi = do_positions([i.avr for i in QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id') if i.avr != None])
        [save(QSUBJECT, posi[i], QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id')[i].id) for i in range(0, len(posi))]
    term = ['-', '1st Term', '2nd Term', '3rd Term'][sorted([int(i) for i in [tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]]])[-1]]
    mains = QSUBJECT.objects.filter(tutor__exact=tutor).order_by('student_name__gender', 'student_name__full_name')#.exclude(fagr__exact=0)
    #for i in CNAME.objects.filter(id__in =[a.student_name_id for a in mains]):
        #i.Class = tutor.Class
       # i.save()
    return [term,  mains, tutor]
def detailView(request, pk, md):##Step 2::  every tutor home detail views all_search_lists
    mains = common(request, pk)
    if mains[1].aggregate(Avg('avr'))['avr__avg'] and md == 1:
        sum_agr = round(mains[1].aggregate(Sum('avr'))['avr__sum'], 1)
        sum_avr = round(mains[1].aggregate(Avg('avr'))['avr__avg'],2)
    else:
        sum_agr = 00
        sum_avr = 00
    if request.user.is_authenticated:#pk to download results pdf
        user = request.user.profile
        user.account_id = mains[2].id
        user.save()
    return render(request, 'result/margged.html',  {'urs':mains[1].count(), 'males' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 2).count(), 'all_page': paginator(request, mains[1]), 'subject_scores':sum_agr, 'subject_pert':sum_avr, 'qry' : mains[2], 'pk': pk, 'term':mains[0], 'classNames':CNAME.objects.filter(Class__exact=mains[2].Class).order_by('gender', 'full_name')})
    
    
def all_View(request, pk, md):##Step 2::  every tutor home detail views all_search_lists 
    mains = common(request, pk)#.order_by('gender')#request.user 
    if mains[1].count() != 0 and int(md) == 2:
        return render(request, 'result/margged.html',  {'males' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 2).count(), 'all_page': mains[1], 'subject_scores':round(mains[1].aggregate(Sum('avr'))['avr__sum'], 1), 'subject_pert':round(mains[1].aggregate(Avg('avr'))['avr__avg'],2),  'term':mains[0], 'qry' : mains[2], 'pk': pk})
    else:
        return redirect('home')
    
#########################################################################################################################


def Student_names_list(request, pk):##Step 2::  every tutor home detail views
    gender = CNAME.objects.all().exclude(gender__exact= pk).order_by('club_two')  
    counted = [gender.filter(Class__exact=i).count() for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/searched_names.html',  {'all_page': paginator(request, gender), 'counts': gender.count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})


##########################PORTAL MANAGEMENT#################################### 
def teacher_accounts(request, md):
    tutors = TUTOR_HOME.objects.all().order_by('first_term__subject')
    if md == 30:
       return render(request, 'result/transfers.html', {'all_page': paginator(request, tutors), 'counts':tutors.count()})
    else:
        return render(request, 'result/transfers.html', {'all_page': tutors, 'counts':tutors.count()})
    


def results_junior_senior(request, pk):
    cls = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']
    tutors = BTUTOR.objects.filter(Class__exact=cls[int(pk)]).exclude(accounts__exact=None).order_by('subject')
    qsubject = [QSUBJECT.objects.filter(tutor__exact=i) for i in  tutors]
    agr = []
    per = []
    for i in qsubject:
        if i.aggregate(Avg('avr'))['avr__avg']:
            agr.append(round(i.aggregate(Sum('avr'))['avr__sum'], 1))
            per.append(round(i.aggregate(Avg('avr'))['avr__avg'],2))
        else:
            agr.append(00)
            per.append(00)
    return render(request, 'result/results_junior_senior.html', {'all_page': zip(tutors, agr, per), 'pk':pk, 'counts':tutors.count(), 'class':cls[int(pk)]})
    

def all_users(request, pk):#show single candidate profile 
    qry = User.objects.all().order_by('username')
    if pk == 0: 
        return render(request, 'result/all_users.html', {'all_page': paginator(request, qry)})
    else:
        return render(request, 'result/all_users.html', {'all_page': qry})

@login_required
def student_info (request, pk):
    if CNAME.objects.get(pk=pk).birth_date:
             birth = "{:%Y-%m-%d}".format(CNAME.objects.get(pk=pk).birth_date)
    else:
          birth = '2011-02-23'
    return render(request, 'result/student_info.html',  {'info':CNAME.objects.get(pk=pk), 'birth_date':birth, 'current':CNAME.objects.filter(Class__exact=CNAME.objects.get(pk=pk).Class), 'pk':pk})    

def student_info_json (request):
        names = ["name", "class", "uid", "term", "opened", "presence", "punctual", "comment", "hbegin", "hend", "wbegin", "wend", "daysAbsent", "purpose", "good", "fair", "poor", "remark", "event", "indoor", "ball", "combat", "track", "jump", "throw", "swim", "lift", "sport_comment", "club_one", "office_one", "contrib_one", "club_two", "office_two", "contrib_two", 'birth', 'title','pname','pocp','contact1','contact2','address']
        listed = [request.GET.get(i) for i in names]
        info = CNAME.objects.get(pk = request.GET.get('pk'))
        info.full_name, info.Class, info.uid, info.term, info.no_open, info.no_present, info.no_absent, info.comment, info.H_begin, info.H_end,info.W_begin, info.W_end, info.no_of_day_abs, info.purpose, info.good, info.fair, info.poor,info.remark, info.event, info.indoor, info.ball, info.combat, info.track, info.jump, info.throw, info.swim, info.lift, info.sport_comment, info.club_one, info.office_one, info.contrib_one, info.club_two, info.office_two, info.contrib_two, info.birth_date, info.title, info.p_name,info.occupation, info.contact1, info.contact2, info.address = listed
        info.save()
        data = {'status': str(info.full_name)}
        return JsonResponse(data)

def card_comment(request):
    obj = get_object_or_404(CNAME, pk=request.GET.get('uid'))
    masters = User.objects.filter(groups__name='Master')
    principals = User.objects.filter(groups__name='Principal')
    if request.user in masters:
        obj.master_comment = request.GET.get('master_comment')
        obj.save()
        data = {'status': "master"}
    elif request.user in principals:
        obj.master_comment = request.GET.get('master_comment')
        obj.principal_comment = request.GET.get('principal_comment')
        obj.save()
        data = {'status': "principal"}
    else:
        data = {'status': "None"}
    return JsonResponse(data)

def searchs(request):
    query = request.GET.get("q")
    reg = CNAME.objects.filter(last_name__icontains = query.upper()).order_by('gender', 'full_name')  
    counted = [CNAME.objects.filter(Class__exact=i).count() for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/searched_names.html',  {'all_page': paginator(request, reg), 'counts': CNAME.objects.all().count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})
      

def search_results(request, pk):
        redir = [x[0] for x in list(QSUBJECT.objects.filter(student_id=CNAME.objects.get(pk=pk).student_id).values_list('id'))]
        return redirect('student_subject_list', pk=redir[0])
        

@login_required 
def editQuest(request, pk):
    if request.GET.get('question', None) != None:
        question = QUESTION.objects.get(pk=int(request.GET.get('pk')))
        question.question=request.GET.get('question')
        question.optionA=request.GET.get('optionA')
        question.optionB=request.GET.get('optionB')
        question.optionC=request.GET.get('optionC')
        question.optionD=request.GET.get('optionD')
        question.answerA=request.GET.get('answerA')
        question.answerB=request.GET.get('answerB')
        question.answerC=request.GET.get('answerC')
        question.answerD=request.GET.get('answerD')
        question.comment=request.GET.get('AnswerComment')
        question.CORRECT=request.GET.get('correctAnswer')
        question.save()
        data = {'status': "Saved!"}
        return JsonResponse(data)
    else:
        quetions = QUESTION.objects.get(pk=pk)
        return render(request, 'result/question_model.html', {'scr':quetions})

def grade_counter(query):
    grade_counts = Counter([i.grade for i in query])
    ordered = grade_counts.most_common()
    return ordered


def accid(request, pk, md):
    user = request.user
    user.profile.account_id = pk
    user.save()
    if md == 0:#import webbrowser
        link = "http://127.0.0.1:8809/result/render/pdf/2/0/"+str(pk)+'/'
    else:#webbrowser.open(link, new=0, autoraise=True)
        link = "http://127.0.0.1:8809/result/render/pdf/1/"+str(pk)+'/0/'
    f = requests.get(link)
    
    #'http://127.0.0.1:8838/result/render/pdf/4/1/'+str(pk)+'/0/'


def auto_pdf_a(request, md):
      if md == 0:
          data = {'done':str(len([accid(request, i.id, md) for i in BTUTOR.objects.filter(id__in=[int(request.GET.get('pk_'+str(a))) for a in range(0, int(request.GET.get('end')))])]))}
      else:
          data = {'ids':[i.id for i in CNAME.objects.filter(Class__exact=request.GET.get('class'))]}
      return JsonResponse(data)

def param_cards(request, this, lists):
    term = sorted([this.first().tutor.first_term[0], this.first().tutor.second_term[0], this.first().tutor.third_term[0]])
    filename = this.first().student_name.last_name+'_'+this.first().student_name.first_name+'_'+str(["", 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(this.first().tutor.Class))+'_'+str(term[-1])
    term = sorted([this.first().tutor.first_term, this.first().tutor.second_term, this.first().tutor.third_term])       
    a,b,c,d,e,f,g,h,i,j = lists
    params = {
            'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i,'j': j, 'this':this.first(), 'today': timezone.now(), 'request': request, 'term':term[-1], 'info':this.first().student_name
            }
    return params, term, filename

def param_marksheets(request, tutor, myHod):
    term = sorted([tutor.first_term, tutor.second_term, tutor.third_term])
    termi = sorted([tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]])
    filepath = 'pdf/marksheets/'+str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(tutor.Class))+'/'+term[-1].split(' ')[0]
    filename = tutor.subject+'_'+str(["", 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(tutor.Class))+'_'+str(termi[-1])
    subjects = QSUBJECT.objects.filter(tutor__exact=tutor).exclude(student_name__gender=0).order_by('student_name__gender', 'student_name__full_name')
    if subjects:
        sumed = round(subjects.aggregate(Sum('avr'))['avr__sum'], 1)
        average = round(subjects.aggregate(Avg('avr'))['avr__avg'], 2)
        params = {
            'subjects' : subjects, 'qry':tutor,'request': request, 'today': timezone.now(), 'sum':sumed, 'avg':average, 'term':term[-1], 'myHod':myHod.filter(profile__department__exact=tutor.accounts.profile.department).first(), 'grade_conuts':grade_counter(subjects)
        }
        return params, filepath, filename
    else:
        return redirect('home')  

    
myHod = User.objects.filter(profile__class_in__exact='HEADS')
def zipped_my_pdfs(request, model, pk):
    clss = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', []]
    if model == 0:
        these = CNAME.objects.filter(session__exact=session.profile.session, Class__exact=clss[int(pk)]).order_by('gender', 'full_name')
        for this in these:
            this = QSUBJECT.objects.filter(student_name_id__exact=this.id, tutor__term__exact='1st Term', tutor__session__exact=session.profile.session, tutor__Class__exact=this.Class).order_by('tutor__subject')
            if this:
                lists = [x for x in this][:10]
                if len(lists) != 10:
                    lists = lists + [None]*(10-len(lists))
                params, term, filename = param_cards(request, this, lists)
                pdf = Render.render('result/card.html', params, 'pdf/cards/'+pk+'/'+term[-1].split(' ')[0]+'/'+str(this.first().student_name.last_name)+'_'+str(this.first().student_name.first_name)+'.pdf', filename)
                clss[-1].append((filename + ".pdf", pdf))
    else:
        tutors = BTUTOR.objects.filter(Class__exact=clss[int(pk)])
        for tutor in tutors:
            params, filepath, filename = param_marksheets(request, tutor, myHod)
            pdf =  Render.render('result/MarkSheetPdf.html', params, filepath+'/'+filename+'.zip', filename)
            clss[-1].append((filename + ".pdf", pdf))
    
    response = HttpResponse(generate_zip(clss[-1]), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(clss[int(pk)]+'.zip')
    return response

def csv_bsh(request, pk):
    clS = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', []][int(pk)]
    col_head_ = ['STUDENT NAME', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 3, 2, 1, 'A', 'Avg', 'posi']
    data = [[[CNAME.objects.get(id=ids).full_name]] + [[a.agr, a.sagr, a.fagr, a.avr] for a in QSUBJECT.objects.filter(student_name__id__exact=ids).order_by('tutor__subject')] for ids in [i.id for i in CNAME.objects.filter(Class__exact=clS)]]
    sets = [x+[[sum([i[-1] for i in x[1:]])/10]] for x in data]
    empty = []
    for i in sets:
        main = i[0]
        for x in i[1:]:
            main.extend(tuple(x))
        empty.append(main)
    posi = do_positions([int(average([i[-1], 0], 't')) for i in empty])
    response = HttpResponse(content_type='application/csv')
    sd = [i+[r] for i, r in zip(empty, posi)]
    sd.insert(0, col_head_)
    writer = csv.writer(response)
    for each in sd:
        writer.writerow(each) 
    response['Content-Disposition'] = "attachment; filename={name}".format(name=clS+'_bsh_.csv')
    return response

def card_summary(this):
    dep = this.filter(tutor__subject__in=['LIT', 'COM', 'PHY']).first()
    eng = QSUBJECT.objects.filter(tutor__Class__exact=dep.tutor.Class, tutor__subject__exact='ENG')
    clls = {'LIT':'Art', 'COM':'Comm', 'PHY':'Sci'} 
    if dep:
        dept = dep.student_name
        dept.dept = clls[dep.tutor.subject]
        dept.no = eng.count()
        dept.total_scores = round(int(this.aggregate(Sum('avr'))['avr__sum'])/len(this), 1)
        dept.grade = do_grades([int(int(round(this.aggregate(Sum('avr'))['avr__sum'], 1))/len(this))], cader(dep.tutor.Class))[0]
        dept.save()
 
def pre(this):
    lists = [x for x in this][:10]
    if len(lists) != 10:
        lists = lists + [None]*(10-len(lists)) 
    return lists   

#QSUBJECT.objects.filter(tutor__exact=tutor).order_by('student_name__gender', 'student_name__full_name')
class Pdf(View):#LoginRequiredMixin, 
    def get(self, request, ty, sx, pk, uk):#CARD
        if ty == 1 or ty == 4:
            this = QSUBJECT.objects.filter(student_name_id__exact=sx, tutor__term__exact='1st Term').order_by('tutor__subject')
            these = [i.id for i in CNAME.objects.filter(Class__exact=this.first().tutor.Class).order_by('id')]
            a,b,c,d,e,f,g,h,i,j = pre(this)
            if uk == 11:
                [card_summary(r) for r in [QSUBJECT.objects.filter(student_name_id__exact=x, tutor__term__exact='1st Term').order_by('tutor__subject') for x in [i.id for i in CNAME.objects.filter(Class__exact=this.first().tutor.Class)]]]
                posi = do_positions([i.total_scores for i in CNAME.objects.filter(Class__exact=this.first().tutor.Class).order_by('id')])
                x = 0
                for i in these:
                    pos = CNAME.objects.get(pk=i)
                    pos.posi = posi[x]
                    pos.save()
                    x += 1
                    this = QSUBJECT.objects.filter(student_name_id__exact=i, tutor__term__exact='1st Term').order_by('tutor__subject')
                    params, term, filename = param_cards(request, this, pre(this))
                    pdf = Render.render('result/card.html', params, 'pdf/cards/'+str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(this.first().tutor.Class))+'/'+term[-1].split(' ')[0]+'/'+str(this.first().student_name.last_name)+'_'+str(this.first().student_name.first_name)+'.pdf', filename)
                return redirect('subject_view', pk=sx, md=1)
            if ty == 4:
                try:
                    term = sorted([this.first().tutor.first_term, this.first().tutor.second_term, this.first().tutor.third_term])
                    return render(request, 'result/three_termx.html',  {'term':term[-1], 'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i,'j': j, 'margged':CNAME.objects.filter(Class__exact=this.first().tutor.Class, session__exact=session.profile.session), 'info':this.first().student_name})
                except:
                       return redirect('student_info', pk=sx)  
            elif this:  
                 params, term, filename = param_cards(request, this, lists)
                 return Render.render('result/card.html', params, 'pdf/cards/'+str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(this.first().tutor.Class))+'/'+term[-1].split(' ')[0]+'/'+str(this.first().student_name.last_name)+'_'+str(this.first().student_name.first_name)+'.pdf', filename)
            else:
                 return redirect('student_info', pk=sx)
        if ty == 2:#SCORE SHEET
            if pk == 0:
                tutor = get_object_or_404(BTUTOR, pk = uk)
            else:
                tutor = get_object_or_404(BTUTOR, pk = int(pk))#
            try:
               params, filepath, filename = param_marksheets(request, tutor, myHod)
               return Render.render('result/MarkSheetPdf.html', params, filepath+'/'+filename+'.pdf', filename)
            except:
                   return redirect('home')
        if ty == 5:
            if request.GET.get('saved'):
                params = {
                'request': request, 'today': timezone.now(), 'a':request.GET.get('subject', None), 
                'b':request.GET.get('topic', None), 'c':request.GET.get('sub_topic', None), 'd':request.GET.get('agenda', None), 'e':request.GET.get('class', None), 'f':request.GET.get('lesson_duration', None), 'g':request.GET.get('curriculum_objective', None), 'h':request.GET.get('lesson_objective', None), 'i':request.GET.get('start', None), 'j':request.GET.get('teacher_resources', None), 'k':request.GET.get('student_resources', None), 'l':request.GET.get('preparation', None), 'm':request.GET.get('board', None), 'n':request.GET.get('assignment', None), 'o':request.GET.get('question3', None), 'p':request.GET.get('question2', None), 'q':request.GET.get('question1', None)
                  }
                return Rendered.render('result/lesson_templatepdf.html', params, 'lesson_templates/'+request.user.username, request.user.username)
            return render(request, 'result/lesson_template.html')#lesson_templates
        if ty == 6:
            if request.GET.get('saved'):
                data = [int(request.GET.get(str(i))) for i in range(int(request.GET.get('size'))) if request.GET.get(str(i)) is not None]
                Class = request.GET.get('Class', None).split(',')
                if len(Class) == 2:
                    for i in CNAME.objects.filter(id__in=data).order_by('gender', 'full_name'):
                        if Class[0] == 'promotions':
                            i.Class = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', 'DON'][int(str(Class[1].split(' ')[-1]))]
                        elif len(Class[1]) == 3:
                            i.club_two = Class[1]
                        else:
                            return redirect('home')
                        i.save()
                params = {
                'request': request, 'today': timezone.now(), 'Class':Class[0], 'students':CNAME.objects.filter(id__in=data).order_by('gender', 'full_name')
                  }
                return Rendered.render('result/shortlisted.html', params, Class[0], Class[0])
            candi = CNAME.objects.all()#filter(club_two__exact='JET')
            #Class = [i[0] for i in list(set(list(candi.values_list('Class'))))]
            param = {"students":candi.count(), "one":candi.filter(Class__exact='JSS 1', gender__exact=1).order_by('gender', 'full_name'), "two":candi.filter(Class__exact='JSS 1', gender__exact=2).order_by('gender', 'full_name'), "three":candi.filter(Class__exact='JSS 2', gender__exact=1).order_by('gender', 'full_name'), "four":candi.filter(Class__exact='JSS 2', gender__exact=2).order_by('gender', 'full_name'), "five":candi.filter(Class__exact='JSS 3', gender__exact=1).order_by('gender', 'full_name'), "six":candi.filter(Class__exact='JSS 3', gender__exact=2).order_by('gender', 'full_name'), "seven":candi.filter(Class__exact='SSS 1', gender__exact=1).order_by('gender', 'full_name'), "eight":candi.filter(Class__exact='SSS 1', gender__exact=2).order_by('gender', 'full_name'), "nine":candi.filter(Class__exact='SSS 2', gender__exact=1).order_by('gender', 'full_name'), "ten":candi.filter(Class__exact='SSS 2', gender__exact=2).order_by('gender', 'full_name'), "eleven":candi.filter(Class__exact='SSS 3', gender__exact=1).order_by('gender', 'full_name'), "tewlve":candi.filter(Class__exact='SSS 3', gender__exact=2).order_by('gender', 'full_name')
            }
            return render(request, 'result/exam_venue.html', param)


def report_card_summary(request):
        cl_ss = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', '']
        if request.POST['Term'] == '3rd Term':
                pmt, nta, rpt = 0, 0, 0
                if request.POST['Class']:
                    scr_bd = ['C', 'A', 'C6', 'C5', 'C4', 'B3', 'B2', 'A1']
                    datum = []
                    for ix in [int(i[-1]) for i in json.loads(request.POST['content'])]:
                        grades = [[], []]#2, 8
                        scr = []
                        for s in QSUBJECT.objects.filter(student_name_id__exact=ix):
                            ix = s.student_name
                            if s.tutor.subject == 'MAT' and s.grade in scr_bd:
                                    grades[0] += [s.grade]
                                    scr += [(s.tutor.subject+' : '+s.grade)]
                            if s.tutor.subject == 'ENG' and s.grade in scr_bd:
                                grades[0] += [s.grade]
                                scr += [(s.tutor.subject+' : '+s.grade)]
                            else:
                                if s.grade in scr_bd:
                                    grades[1] += [s.grade]
                                    scr += [(s.tutor.subject+' : '+s.grade)]
                                else:
                                    scr += [(s.tutor.subject+' : '+s.grade)]
                        eng_mat, other = [len(i) for i in grades]
                        if eng_mat == 2 and other >= 3:
                            new_class, status, remark = cl_ss[cl_ss.index(request.POST['Class'])+1], 'Good result, Promoted to '+cl_ss[cl_ss.index(request.POST['Class'])+1], 'Promoted'
                            pmt += 1
                        elif eng_mat == 1 and other >= 3:
                            new_class, status, remark = cl_ss[cl_ss.index(request.POST['Class'])+1], 'Fear result, Promoted to '+cl_ss[cl_ss.index(request.POST['Class'])+1]+' on trial', 'On Trial'
                            nta += 1
                        else:
                            new_class, status, remark = request.POST['Class'], 'Poor result, you are to repeat '+request.POST['Class'], 'Repeated'
                            rpt += 1
                        scrd = sorted(list(set(scr)))
                        scrd += [None]*10
                        scrd.insert(0, ix.full_name)
                        scrd.insert(11, remark)
                        datum.append(scrd[:12])
                        ix.Class, ix.principal_comment = [new_class, status]
                        ix.save()
                    print(pmt, nta, rpt)
                    sumT = sum([pmt, nta, rpt])
                    pmtt, ntat, rptt = [round(pmt*100/sumT, 2), round(nta*100/sumT, 2), round(rpt*100/sumT, 2)]
                    params = {
                        'request':request, 'today':timezone.now(), 'Class':request.POST['Class'], 'students':datum, 'counts':len(datum), 'pmt':pmt, 'nta':nta, 'rpt':rpt, 'pmtt':pmtt, 'ntat':ntat, 'rptt':rptt
                            }
                    return Rendered.render('result/report_card_summary.html', params, 'pdf/cards/'+str(cl_ss.index(request.POST['Class']))+'/summary', str(cl_ss.index(request.POST['Class'])))
        else:
            data = {'status': str(cl_ss.index(request.POST['Class']))}
        return JsonResponse(data)


file_path = os.path.join(module_dir, 'JSS 2.txt')
def sample_disply(request):
    #os.chdir(file_path)
    empty_list = open(file_path, "r" )
    return HttpResponse(empty_list, content_type='text/plain')

def sample_down(request):
    response = HttpResponse(content_type='text/plain')
    with open(file_path, 'r') as file:
        file_txt = file.read()
        contents = file_txt.split('\n');
        sd = [[x] for x in contents]
    writer = csv.writer(response)
    for each in sd:
        writer.writerow(each) 
    response['Content-Disposition'] ='attachment; filename="samples.txt"'
    return response 

@login_required
def name_down(request, pk, fm,  ps):
    if fm == 2:
       return redirect('pdf', ty=3, sx=0)
    pair_subject =  ["ACC", "AGR", "ARB", "BIO", "BST", "BUS", "CHE", "CIV", "COM", "CTR", "ECO", "ELE", "ENG", "FUR", "GEO", "GOV", "GRM", "HIS", "ICT", "IRS", "LIT", "MAT", "NAV", "PHY", "PRV", "YOR", ' ']
    Class = ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', ''][int(pk)]
    response = HttpResponse(content_type=['', 'application/csv', 'application/pdf', 'text/plain', 'text/plain'][int(fm)])
    contents = CNAME.objects.filter(Class__exact=Class).order_by('gender', 'full_name')
    if fm == 4:
        sd = [[x.id, x.full_name, randrange(11, 20), randrange(8, 10), randrange(8, 10), randrange(21, 60)] for x in contents]
        print(sd)
    elif pk == 6:
        contents = QSUBJECT.objects.filter(tutor__exact=BTUTOR.objects.get(pk=uk)).order_by('student_name__gender', 'student_name__full_name')
        sd = [[x.student_name.full_name, x.test, x.agn, x.atd, x.total, x.exam, x.agr, x.sagr, x.fagr, x.aagr, x.avr, x.grade, x.posi] for x in contents]
        sd = [['Student Name', 'Test', 'Agn', 'Atd', 'Total', 'Exam', '3rd', '2nd', '1st', 'Anuual', 'Avg', 'Grade', 'Posi']]+sd
        tutor = BTUTOR.objects.get(pk=uk)
        term = sorted([tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]])
        Class = tutor.subject+'_'+str(["", 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(tutor.Class))+'_'+str(term[-1])
    elif len(contents) == 0:
        contents = CNAME.objects.filter(Class__exact=Class, session__exact=session.profile.session).order_by('gender', 'full_name')
        sd = [[x.full_name, x.uid, x.birth_date, x.age, x.Class, x.gender, x.term, x.no_open, x.no_present, x.no_absent, x.no_of_day_abs, x.purpose, x.remark, x.W_begin, x.W_end, x.H_begin, x.H_end, x.good,x.fair, x.poor, x.event, x.indoor, x.ball, x.combat, x.track, x.jump, x.throw, x.swim, x.lift, x.sport_comment, x.club_one, x.club_two, x.contrib_one, x.contrib_two, x.master_comment, x.principal_comment, x.resumption, x.id] for x in contents]
    else:
        contents = QSUBJECT.objects.filter(tutor__Class__exact=Class, tutor__subject__exact=pair_subject[int(ps)], tutor__session__exact=session.profile.session).order_by('student_name__gender', 'student_name__full_name')
        sd = [[x.student_name.id, x.student_name.full_name, x.test, x.atd, x.agn, x.exam] for x in contents]
        Class = Class +'_'+pair_subject[int(ps)]
    writer = csv.writer(response)
    for each in sd:
        writer.writerow(each) 
    response['Content-Disposition'] = "attachment; filename={name}".format(name=Class+[' ', '.csv', '.pdf', '.txt', '.txt'][int(fm)])
    return response 


