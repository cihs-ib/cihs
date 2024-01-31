from .models import TUTOR_HOME
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.contrib.auth.models import User
from django.conf import settings
import zipfile
#mport os#, boto3, requests

def session():
    return User.objects.filter(is_superuser__exact=True).first()

def cader(qry):
    clas = [['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'], ['', 'jss_one', 'jss_two', 'jss_three', 'sss_one', 'sss_two', 'sss_three']]
    x = clas[0].index(qry)
    if x <= 3:
        cader = 'j'
    else:
        cader = 's'
    return cader

def listofgrades(cader):#marks in ranges with 5 as class intervals
    e = [26, 31, 's', 'j']
    ds = [[], [], []]
    for i in range(100, 0, -1):#marks 100%
        ds[0].append(i)
    ds[1].append(0)
    for i in range(e[e.index(cader)-2], 100, 5):#12 classes of scores with 75 & 70 as (A1, A) and 39 as F
        ds[1].append(i)
    for i in range(0, len(ds[1])):
        if i <= 11:
          ds[2].append(ds[0][ds[1][i]:ds[1][i+1]])
    return ds[2]

def do_grades(scores, cader):#list
    grd = [[], [], ['A1', 'B2', 'B3', 'C4', 'C5', 'C6', 'D7', 'E8', 'F9', 'F9', 'F9', 'F9'], ['A', 'C', 'C', 'C', 'C', 'P', 'P', 'F', 'F', 'F', 'F', 'F'], [0, 1, 's', 'j']]
    dr = listofgrades(cader)#[0, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96] for junior and [0, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96] for sinior
    done = False;
    while not done:
        s = len(scores)
        if s >= 1:
            for r in range(0, len(dr)):
                if set_limit(scores[0], 39, 99) in dr[r]:
                    grd[1].append(grd[grd[4].index(cader)][r])
            del(scores[0])
        elif s == 0:
            done = True
    return grd[1]

def sort_pos(testlist):
    global mark_orde
    testlist = sorted(testlist, key=None, reverse=True)
    mark_orde = testlist
    sae = []
    seo = []
    for i in range(0, len(testlist)):
        se = []
        for position, item in enumerate(testlist):
            if item == testlist[i]:
                se.append(position+1)
        seo.append(se)
    for i in range(0, len(seo)):
        sae.append(seo[i][0])
    return sae
def generate_positions(length):
    posi = []
    for i in range(1, length+1):
        if i > 3 and i < 21:
            posi += [str(i)+'th']
        else:
            inx = str(i)[-1]
            if inx == '1':#21
                posi += [str(i)+'st']
            elif inx == '2':#22
                posi += [str(i)+'nd']
            elif inx == '3':#23
                posi += [str(i)+'rd']
            else:
                posi += [str(i)+'th']
    return posi      
def pos_t(w):
    gov = ['1st']+ generate_positions(200) 
    dss = []
    for i in range(0, len(w)):
        dss.append(gov[w[i]])
    return dss

def marg_marks_positions(testlist, first_last_th, mark_orde):
    marks = []
    position = []
    marg_list = [marks, position]
    dlist = testlist[:]
    print('element in the lists:')
    print('Marks:', testlist[0], 'Ordered_marks:', mark_orde[0], 'Position:', first_last_th[0])
    done = False;
    while not done:
        n = len(dlist)
        if n >= 1:
            get = dlist[0]
            if get in mark_orde:
                H = mark_orde.index(get)
                position.append(first_last_th[H])
                marks.append(get)
                del(dlist[0])
        elif n == 0:
            done = True
    return marg_list
def do_positions(df):
    testlist = df#mark_list(df)
    w = sort_pos(testlist)
    first_last_th = pos_t(w)
    responses = marg_marks_positions(testlist, first_last_th, mark_orde)
    return responses[1]

import math
def round_half_up(n, decimals=0):
    multiplier = 10**decimals
    return math.floor(n*multiplier + 0.5)/multiplier

def set_limit(x, Min, Max):
    if x < Min:
        x = Min
    elif x > Max: 
        x = Max
    else:
        x = x
    return x

def may_not(r, dg):
   if len([i for i in dg if i[-1] == r]) != 0:
       return [dg.index([i for i in dg if i[-1] == r][x])+1 for x in range(len([i for i in dg if i[-1] == r]))]
   else:
       return [0]

def s3_session():
    aws_session = boto3.Session('AKIAZXDZRFQVP24YW7UU', '32hOmVzUovuSW89PjoSYS2WNBm3IE/JKyosYehQh')# boto3.Session(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    return aws_session
    
def upload_to_s3(content, path):
    aws_session = s3_session()
    s3 = aws_session.resource('s3')
    s3.Bucket('uqhs').put_object(Key=path, Body=content)
    
def listpdf():
    basepath = settings.MEDIA_ROOT + '/pdf'
    for entry in os.listdir(basepath):#cards, marksheete|/pdf
        for cls in os.listdir(os.path.join(basepath, entry)):#class|/pdf/cards
            for term in os.listdir(os.path.join(basepath, entry+'/'+cls)):
                for doc in os.listdir(os.path.join(basepath, entry+'/'+cls+'/'+term)):
                    os.chdir(os.path.join(basepath, entry+'/'+cls+'/'+term))
                    with open(doc, 'rb') as file:
                        if len(file.name.split('_')) == 2:
                            file_name = file.name.split('.')[0]+'_'+term[0]+'.pdf'
                        else:
                            file_name = 'broadsheets/'+cls+'/'+term+'/'+file.name
                        file_name = 'broadsheets/'+cls+'/'+term+'/'+file.name    
                        upload_to_s3(file, file_name)
class Render:
    @staticmethod
    def render(path: str, params: dict, filepath, filename):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type = "application/pdf")
            response['Content-Disposition'] = "attachment; filename={name}.pdf".format(name=filename)
            print(filepath)
            result = open('C:/Users/USER/AppData/Local/Programs/Python/cihs/citadel/result/static/result/'+filepath, 'wb')
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            result.close()
            try:
                upload_to_s3(response.content, filepath.split('.')[0]+'.pdf')
            except:
                print('No connection')
            if filepath.split('.')[-1] == 'zip':#updated
                return response.getvalue()#updated
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)

def generate_zip(files):
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.writestr(file[0], file[1])
    return mem_zip.getvalue()



class Rendered:
    @staticmethod
    def render(path: str, params: dict, filepath, filename):
        template = get_template(path)
        html = template.render(params)
        path = os.path.join(settings.MEDIA_ROOT, filepath)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type = "application/pdf")
            response['Content-Disposition'] = "attachment; filename={name}.pdf".format(name='summary')
            result = open('C:/Users/USER/AppData/Local/Programs/Python/cihs/citadel/result/static/result/pdf/shortlistedVenues/'+filename+'.pdf', 'wb')
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            result.close()
            print('saved to offline!')
        data = {'status': filename}
        return JsonResponse(data)
