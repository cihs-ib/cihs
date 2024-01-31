# in any app that you want celery tasks, make a tasks.py and the celery app will autodiscover that file and those tasks.
from __future__ import absolute_import
from celery import shared_task
from .utils import session, Render, generate_zip 
from .views import zipped_my_pdfs 
from django.http import HttpResponse

@shared_task#@task(name="generate cards/marksheet")
def zipped_my_pdfs_(request, model, pk):
    clss = zipped_my_pdfs(request, model, pk)
    response = HttpResponse(generate_zip(clss[-1]), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(clss[int(pk)]+'.zip')
    return response
    
    

def delayed_task(request, model, pk):
    clss = zipped_my_pdfs_.delay(request, model, pk)