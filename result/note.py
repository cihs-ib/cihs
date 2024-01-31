def students(name, Class):
    from result.models import CNAME, STUDENT_INFO
    undone = []
    if name:
        query = STUDENT_INFO.objects.filter(student_name__exact=name, Class__exact=Class)
        if query.count() == 0:
            student_id = name.last_name[0] + name.first_name[0]+'/'+Class[0]+'/'+'2018'[-2:]+'/'+str(name.id)
            qs = STUDENT_INFO(student_name=name, student_id = student_id, birth = '2003-01-28', Class =Class)
            qs.save()
        elif query.filter(student_id__exact=name.last_name[0] + '&ADEBAYO'[0]+'/'+Class[0]+'/'+'2018'[-2:]+'/'+str(name.id)).count() == 0:
            student_id = name.last_name[0] + '&ADEBAYO'[0]+'/'+Class[0]+'/'+'2018'[-2:]+'/'+str(name.id)
            qs = STUDENT_INFO(student_name=name, student_id = student_id, birth = '2003-01-28', Class =Class)
            qs.save()
        else:
            undone.append(name.id)
    return undone
                            