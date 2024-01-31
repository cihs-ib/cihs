from collections import Counter
from .models import QSUBJECT, CNAME, BTUTOR, QUESTION
from django.shortcuts import render, redirect, get_object_or_404
from .utils import do_grades, do_positions, cader, round_half_up, session
from django.contrib.auth.decorators import login_required
import time
import datetime
from datetime import timedelta
from django.contrib import messages
from statistics import mean

session = session()

def check(inp, ):
    try:
        inp = inp.replace(',', '.')
        num_float = float(inp)
        num_int = int(num_float)
        return num_int == num_float
    except ValueError:
        return False
    
def sort_key(dim):#sort with first elements of the list
    return dim[0]

def check_repeated_names(valid_input):
    word_counts = Counter([r[0] for r in valid_input])
    repeated_name = word_counts.most_common()
    ideces = [list(x) for x in repeated_name if x[1] != 1]
    for i in range(0, len(ideces)):
        repeated_names = [valid_input[valid_input.index(x)][0] + str(valid_input.index(x)) for x in valid_input if x[0] == ideces[i][0]]
        each = [valid_input.index(x) for x in valid_input if x[0] == ideces[i][0]]
        for r in range(0, len(repeated_names)):
            valid_input[each[r]][0] = str(repeated_names[r])
    return valid_input


@login_required
def upload_new_subject_scores(request, pk):
    start_time = time.time()
    tutor = get_object_or_404(BTUTOR, pk=pk)
    term = sorted([tutor.first_term, tutor.second_term, tutor.third_term])[-1] 
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            return render(request, 'result/file_extension_not_txt.html')
        file_txt = my_file.read().decode("ISO-8859-1")
        contents = file_txt.split('\n');
        named_scores = [[], [], []]#[compltet_data_for_each_student, scores, name_only]
        for line in contents:
            each_student = [new.strip() for new in line.split(',')]
            named_scores[0] += [each_student]
        valid_input = [n[:] for n in named_scores[0] if len(n) > 2]
                #####################REPEATED NAMES######################################
        valid_input = check_repeated_names(valid_input)
        ##########################ERROR CHECK##########
        for i in range(0, len(valid_input)):
            output = [check(s) for s in valid_input[i][1:]]
            if len(output) == 9:
                if output != [False, True, True, True, True, True, True, True, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':tutor.subject})
            elif len(output) == 5:
                if output != [False, True, True, True, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':tutor.subject})
            else:
                return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':tutor.subject})
        if QSUBJECT.objects.filter(tutor__subject__exact='BST', tutor__Class__exact=tutor.Class, tutor__first_term__exact='1st Term', tutor__session__exact=tutor.session): 
            if len(valid_input[0][1:]) == 9:#BST ONLY: Reduced 8 to 4 columns by averaging.
                valid_input = [[x[0].split('¿')[-1], x[1], round_half_up(mean([int(i) for i in x[2:4]])), round_half_up(mean([int(i) for i in x[4:6]])), round_half_up(mean([int(i) for i in x[6:8]])), round_half_up(mean([int(i) for i in x[8:10]]))] for x in valid_input]
        x = cader(tutor.Class)
        try:
           raw_scores = [[x[0].split('¿')[-1],  x[1], int(x[2]), int(x[3]), int(x[4]), sum([int(i) for i in x[2:5]]), int(x[5]), sum([sum([int(i) for i in x[2:5]]), int(x[5])])] for x in valid_input]       
           posi = do_positions([int(i[-1]) for i in raw_scores][:])
           grade = do_grades([int(i[-1]) for i in raw_scores][:], x)
           final = [x+[y]+[z] for x,y,z in zip(raw_scores, grade, posi)]
           from .updates import get_or_create
           [get_or_create(tutor, i[0], i) for i in final if CNAME.objects.filter(id__exact=i[0]).exists() and i[5] != 0]
           if tutor.subject == 'BST1' or tutor.subject == 'BST2':
                tutor.subject = 'BST'
           tutor.save()
        except:
            print('error!')
            return redirect('home')
        elapsed_time_secs = time.time() - start_time
        msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
        messages.success(request, msg)
        print(msg)
    else:
        return render(request, 'result/loader.html', {'pk':pk, 'qry':tutor, 'term':term})
    ######################STAGE 2 ::: UPLOAD SCORES##################ENDS
    return redirect('offline', pk=pk)

###############################################################################
###
def setup_questions(request): 
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            return render(request, 'result/file_extension_not_txt.html')
        file_txt = my_file.read().decode("ISO-8859-1")
        text = file_txt.split('_')
        crop = [i.split('\t') for i in text]
        valid = [i for i in crop if len(i) == 2]
        if len(valid) % 6 == 0:
            filterd = [[i[1] for i in valid if len(i) == 2][i*6:(i+1)*6] for i in range((len([i[1] for i in valid if len(i) == 2])+6-1)//6)]
            serial_no = [i+1 for i in range(len(filterd))]
            [QUESTION(subjects=request.POST.get('Subject', False),classes=request.POST.get('Class', False),terms=request.POST.get('Term', False),question=i[0],optionA=i[1],optionB=i[2],optionC=i[3],optionD=i[4],CORRECT=i[5], comment=i[5], serial_no=r, session=session).save() for i,r in zip(filterd,serial_no) if len(i) == 6]
        else:
            from django.http import HttpResponse
            return HttpResponse([valid], content_type='text/plain')#
    else:#
        return render(request, 'result/question_loader.html')
    return redirect('home') 

def regMe(dim):
    #global reged
    #if len(dim) == 5:#FAGBENRO WARIS, 2011-03-16, 1
         reged = CNAME(full_name = dim[0].upper() +' '+ dim[1].upper(), last_name = dim[0].upper(), middle_name = dim[0].upper(), first_name = dim[1].upper(), gender = int(dim[3]), birth_date = dim[2], Class = dim[4])
         reged.save()
         return reged.id
def massRegistration(request):
    start_time = time.time()
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            return render(request, 'result/file_extension_not_txt.html', {'input':'not .txt'})
        file_txt = my_file.read().decode("utf-8")
        contents = file_txt.split('\n');
        names = []
        for line in contents:
            each_student = [new.strip() for new in line.split(',')]
            names += [each_student]
        valid_names = [n[:] for n in names if len(n) is not 1]
        for i in range(0, len(valid_names)):
            output = [check(s) for s in valid_names[i]]
            if len(output) == 4:
                if output != [False, False, False, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_names[i]})
            else:
                return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_names[i]})
        if request.POST.get('Class'):
                    valid_names = [i + [request.POST.get('Class')] for i in valid_names]
                    regeds = [regMe(i) for i in valid_names]
                    cname = CNAME.objects.filter(id__in= regeds)
                    student_id = [i.last_name[0]+i.first_name[0]+'/'+i.Class[0]+'/'+i.session[-2:]+'/'+str(i.id) for i in cname]
        else:
               return render(request, 'result/names_loader.html')
        elapsed_time_secs = time.time() - start_time
        msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
        messages.success(request, msg)
        print(msg)
    else:
        return render(request, 'result/names_loader.html')
    ######################STAGE 2 ::: UPLOAD SCORES##################ENDS
    return render(request, 'result/regSuccessful.html', {'reged':zip(cname, student_id)})


