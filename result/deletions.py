from .models import QSUBJECT, Post, BTUTOR
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required#, @permission_required
from django.http import JsonResponse

@login_required
def confirm_deleting_a_user(request, pk):
    qry = get_object_or_404(User, pk=pk)
    return render(request, 'result/confirm_delete_a_user.html', {'qry' : qry, 'pk': pk}) 
@login_required
def yes_no(request, pk):#delete single candidate 
    qry = get_object_or_404(User, pk=pk)
    return render(request, 'result/yes_no.html', {'qry' : qry, 'pk': pk})
@login_required  
def delete_user(request, pk):#delete single candidate
    get_object_or_404(User, pk=pk).delete()
    return redirect('all_accounts')

@login_required
def confirm_deletion(request, pk):#sort for a deletion confirmation
    qry = get_object_or_404(QSUBJECT, pk=pk)
    return render(request, 'result/confirm_delete_a_student.html', {'qry' : qry, 'pk': pk})
@login_required
def confirmed_delete(request, pk):#Yes delete
    id = []
    qr = get_object_or_404(QSUBJECT, pk=pk)
    id += [qr.tutor.id]
    qr.delete()
    return redirect('subject_view', pk=id[0], md=1)

@login_required
def warning_delete(request, pk):#Yes deletes
    qry = QSUBJECT.objects.filter(tutor=BTUTOR.objects.get(pk=pk))
    return render(request, 'result/confirm_deleting_a_class_scores.html', {'qry' : qry, 'pk': pk})
@login_required
def delete(request, pk):#Yes deletes
    QSUBJECT.objects.filter(tutor=BTUTOR.objects.get(pk=pk)).delete()
    BTUTOR.objects.get(pk=pk).delete()
    return redirect('home')

@login_required
def deletes(request):#Yes deletes
    QSUBJECT.objects.filter(id__in=[int(request.GET.get('id_'+str(i))) for i in range(int(request.GET.get('end')))]).delete()
    data = {"done":1}
    return JsonResponse(data)
    
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('my_post_list')