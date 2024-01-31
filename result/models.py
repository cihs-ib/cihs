from django.db import models
from django.urls import reverse 
from datetime import date
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
################################################################################################'18/19'
        
class BTUTOR(models.Model):#
    accounts = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, help_text='loggon-account:move account here', related_name='btutor')
    teacher_name = models.CharField(max_length=50, blank=True, null=True, help_text='Subject Teacher')###
    codex = tuple([('----', 'None'), ('ACC', 'Account'), ('AGR', 'Agric. Sc.'), ('ARB', 'Arabic'), ('BST', 'Basic Science and Technology'), ('BIO', 'Biology'), ('BUS', 'Business Studies'), ('CTR', 'Catering'), ('CHE', 'Chemistry'), ('CIV', 'Civic Education'), ('COM', 'Commerce'), ('ECO', 'Economics'), ('ELE', 'Electrical'), ('ENG', 'English'), ('FUR', 'Furthe Mathematics'), ('GRM', 'Garment Making'), ('GEO', 'Geography'), ('GOV', 'Government'), ('HIS', 'History'), ('ICT', 'Information Technology'), ('IRS', 'Islamic Studies'), ('LIT', 'Litrature'), ('MAT', 'Mathematics'), ('MKT', 'Marketing'), ('NAV', 'National Value'), ('PHY', 'Physics'), ('PRV', 'Pre-Vocation'), ('YOR', 'Yoruba')])
    subject = models.CharField(max_length=30, choices= codex, blank=True, null=True, default='ENG', help_text='select subject NAME',)
    class_status = (('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SSS 1', 'sss_one'), ('SSS 2', 'sss_two'), ('SSS 3', 'sss_three'))
    Class = models.CharField(max_length=30, choices=class_status, null=True, default='JSS 1', help_text='select subject CLASS')
    term_status = (('1st Term', 'first term'), ('2nd Term', 'second term'), ('3rd Term', 'third term'))
    term = models.CharField(max_length=30, choices=term_status, blank=True, default='1st Term', null=True, help_text='select subject TERM')
    first_term = models.CharField(max_length=30, blank=True, default='1st Term', null=True)
    second_term = models.CharField(max_length=30, blank=True, default='1st Term', null=True)
    third_term = models.CharField(max_length=30, blank=True, default='1st Term', null=True)
    model_summary = models.CharField(max_length=1000, default='tutor', blank=True, null=True)
    model_in = models.CharField(max_length=8, default='qsubject', blank=True, null=True)
    males = models.IntegerField(null=True, blank=True, default='0', help_text='Enter number of male in class')
    females = models.IntegerField(null=True, blank=True, default='0', help_text='Enter number of female in class')
    cader = models.CharField(max_length=1, blank=True, null=True, help_text='Senior/Junior')
    account_status = (('active', 'Active'), ('delete', 'Delete'))
    status = models.CharField(max_length=8, choices=account_status, blank=True, default='active', null=True, help_text='Account Status')
    session = models.CharField(max_length=8, blank=True, null=True)###
    teacher_in = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_account', help_text= 'Class Teachers')
    subject_teacher_id = models.CharField(max_length=200, blank=True, null=True, help_text='Class teacher id')
    created = models.DateTimeField(max_length=200, default=str(datetime.date.today()))
    updated = models.DateTimeField(editable=False, blank=True, null=True,)
    pdf = models.FileField(upload_to='static/result/pdf/', null=True, default='default.pdf')
    class Meta:
          ordering = ('teacher_name',) # helps in alphabetical listing. Sould be a tuple
    def __str__(self):
        """String for representing the Model object."""#marksheets/2/3rd/BUS_18_0.pdf
        #termi = sorted([self.first_term[0], self.second_term[0], self.third_term[0]])
        cdo = str(["", 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(self.Class))+'_-_'+self.session[-2:]
        return f'{self.subject}_{cdo}_0.pdf:{self.accounts.username}:/{self.id}/{self.updated.day}/{self.updated.month}/{self.updated.year}_{self.updated.hour}:{self.updated.minute}:{self.updated.second}'
    
    def save(self):
        from .utils import session
        #self.updated = datetime.datetime.today()
        if not self.id:
            self.created = datetime.date.today()
            self.session = session().profile.session
        if self.accounts is not None:
            self.teacher_name = f'{self.accounts.profile.title} {self.accounts.profile.last_name} : {self.accounts.profile.first_name}'
            subj = ['----', 'ACC', 'AGR', 'ARB', 'BST', 'BIO', 'BUS', 'CTR', 'CHE', 'CIV', 'COM', 'ECO', 'ELE', 'ENG', 'FUR', 'GRM', 'GEO', 'GOV', 'HIS', 'ICT', 'IRS', 'LIT', 'MAT', 'NAV', 'PHY', 'PRV', 'YOR', 'BST1',  'BST2']
            #self.subject_teacher_id = str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(self.Class))+"-"+str(subj.index(self.subject))+"-"+str(self.accounts.id)
        self.model_summary = self.accounts.profile.last_name[0]+self.accounts.profile.first_name[0]
        if BTUTOR.objects.filter(accounts__exact = self.accounts, Class__exact = self.Class, term__exact=self.term, subject__exact=self.subject, session__exact=self.session).count() is not 0:
            males = QSUBJECT.objects.filter(tutor__exact=BTUTOR.objects.filter(accounts = self.accounts, Class = self.Class, term=self.term, subject=self.subject, session=self.session).first(), student_name__gender__exact = 1).count()
            females = QSUBJECT.objects.filter(tutor__exact=BTUTOR.objects.filter(accounts = self.accounts, Class = self.Class, term=self.term, subject=self.subject, session=self.session).first(), student_name__gender__exact = 2).count()
            if males is not 0:
                self.males = males
                self.females = females
        super(BTUTOR, self).save()
        
    def get_absolute_url(self):
        """Returns the url to access a result_grade updates."""
        return reverse('subject_view', args=[str(self.id), 1])
   
class TUTOR_HOME(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, help_text='loggon-account:move account here', related_name='home_tutor')
    teacher_name = models.CharField(max_length=50, blank=True, null=True, help_text='Subject Teacher')###
    first_term = models.ForeignKey(BTUTOR, on_delete=models.CASCADE, null=True, blank=True, help_text='Not editable', related_name='first')
    second_term = models.ForeignKey(BTUTOR, on_delete=models.SET_NULL, null=True, blank=True, help_text='Not editable', related_name='second')
    third_term = models.ForeignKey(BTUTOR, on_delete=models.SET_NULL, null=True, blank=True, help_text='Not editable', related_name='third')
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(editable=False, blank=True, null=True,)
    class Meta:
          ordering = ('teacher_name',) # helps in alphabetical listing. Sould be a tuple
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.teacher_name}'
    
    def save(self):
        if not self.id:
            self.created = datetime.date.today()
        self.teacher_name = f'{self.tutor.profile.title}{self.tutor.profile.last_name} : {self.tutor.profile.first_name}'
        self.updated = datetime.datetime.today()
        super(TUTOR_HOME, self).save()
        
    def get_absolute_url(self):
        """Returns the url to access a result_grade updates."""
        return reverse('uniqueness', args=[str(self.first_term_id)])
    
   
class CNAME(models.Model):
    last_name = models.CharField(max_length=30, default='Surname', blank=True, null=True)
    middle_name = models.CharField(max_length=30, default='Middle nmae', blank=True, null=True)
    first_name = models.CharField(max_length=30, default='First name', blank=True, null=True)
    full_name = models.CharField(max_length=200, default='Surname', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, default='2000-10-01', help_text='Date format: MM/DD/YYYY')
    age = models.CharField(max_length=30, default='14', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(editable=False, blank=True, null=True,)
    gender = models.IntegerField(blank=True, null=True, default= 1, validators=[MaxValueValidator(2), MinValueValidator(1)])
    uid = models.CharField(max_length=200, default='2019/JS_1/10', null=True)
    session = models.CharField(max_length=80, blank=True, null=True)###
    Class = models.CharField(max_length=30, null=True, default='JSS 1', help_text='select subject CLASS')
    term_status = (('1st Term', 'first term'), ('2nd Term', 'second term'), ('3rd Term', 'third term'))
    term = models.CharField(max_length=30, blank=True, default='1st Term', null=True)
    no_open = models.IntegerField(blank=True, null=True, default= 122,)
    no_present = models.IntegerField(blank=True, null=True, default= 122,)
    no_absent = models.IntegerField(blank=True, null=True, default= 0,)
    contact = models.IntegerField(blank=True, null=True, default= 0,)
    address = models.CharField(max_length=200, default='23, Akogun Street Olunloyo, Ibadan, Oyo State.', null=True, blank=True)
    comment = models.CharField(max_length=200, default='Satisfactory', null=True, blank=True)
    H_begin = models.FloatField(max_length=40, blank=True, null=True, default= 1.76,)
    H_end = models.FloatField(max_length=40, blank=True, null=True, default= 1.78,)
    W_begin = models.FloatField(max_length=40, blank=True, null=True, default= 60.76,)
    W_end = models.FloatField(max_length=40, blank=True, null=True, default= 60.78,)
    no_of_day_abs = models.IntegerField(blank=True, null=True, default= 0,)
    purpose = models.CharField(max_length=200, default='Not Specified', null=True)
    good = models.CharField(max_length=100, default='None', null=True, blank=True)
    fair = models.CharField(max_length=100, default='None', null=True, blank=True)
    poor = models.CharField(max_length=100, default='None', null=True, blank=True)
    remark = models.CharField(max_length=100, default='Good keep it up', null=True, blank=True)
    event = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    indoor = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    ball = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    combat = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    track = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    jump = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    throw = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    swim = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    lift = models.CharField(max_length=100,  default='_____', null=True, blank=True)
    sport_comment = models.CharField(max_length=200, default='Satisfactory', null=True, blank=True)
    club_one = models.CharField(max_length=200, default='MSSN', null=True, blank=True)
    club_two = models.CharField(max_length=200, default='JET', null=True, blank=True)
    office_one = models.CharField(max_length=200, default='Member', null=True, blank=True)
    office_two = models.CharField(max_length=200, default='Member', null=True, blank=True)
    contrib_one = models.CharField(max_length=200, default='Active member', null=True, blank=True)
    contrib_two = models.CharField(max_length=200, default='Active member', null=True, blank=True)
    sex = models.CharField(max_length=100, blank=True, null=True, default= "Male")
 
    #Parent Info
    title = models.CharField(max_length=200, default='Mr/Mrs', null=True, blank=True)
    p_name = models.CharField(max_length=200, default='OLAGUNJU MUSLIM', null=True, blank=True)
    occupation = models.CharField(max_length=200, default='Trading', null=True, blank=True)
    contact1 = models.CharField(max_length=13, default='2348068302532', null=True, blank=True)
    contact2 = models.CharField(max_length=13, default='2348078302538', null=True, blank=True)
    address = models.CharField(max_length=200, default='23, Akogun Street Olunloyo, Ibadan, Oyo State.', null=True, blank=True)

    master_comment = models.CharField(max_length=115, blank=True, null=True, default= 'He is a responsible and reliable student.')
    principal_comment = models.CharField(max_length=115, blank=True, null=True, default= 'Fairly good performance, you can do better.')
    resumption = models.DateTimeField(editable=False, blank=True, null=True,)

    total_scores = models.IntegerField(blank=True, null=True, default=0)
    grade = models.CharField(max_length=115, blank=True, null=True, default="null")
    posi = models.CharField(max_length=5, blank=True, null=True, default="th")
    no = models.IntegerField(blank=True, null=True, default=0)
    dept = models.CharField(max_length=5, blank=True, null=True, default="nill")

    serial_no = models.IntegerField(blank=True, null=True, default=0)
    
    class Meta:
          ordering = ('gender', 'Class', 'full_name') # helps in alphabetical listing. Sould be a tuple
    #https://dhnygxib7cbg0.cloudfront.net/static/result/css/result.css
    def save(self):
        from .utils import session
        from .models import QSUBJECT 
        today = datetime.date.today()
        if self.birth_date:
            self.age = str(int((today - date(int(str(self.birth_date).split('-')[0]), int(str(self.birth_date).split('-')[1]), int(str(self.birth_date).split('-')[2]))).days/365))
        if not self.id:
            self.created = today
            self.session = session().profile.session
        print('cname_model')
        bsheet = QSUBJECT.objects.filter(student_id__exact=self.id, tutor__Class__exact=self.Class, tutor__session__exact=session().profile.session)
        if bsheet.count() >= 9:
            all_avg = [i.avr for i in bsheet if i.avr is not None]
            self.annual_scores = round(sum(all_avg), 2)
            self.annual_avr = round((sum(all_avg)/sum(x > 0 for x in all_avg)), 2)
        self.resumption = session().profile.resumption
        self.updated = today
        self.last_name = self.full_name.split(' ')[0]
        self.first_name = self.full_name.split(' ')[1]
        if self.uid:# == "2019/JS_1/10" and self.id:
              self.uid = "CIHS/"+str(int(self.session[2:]) - 1)+"/"+str(self.id)
              print(self.uid)
        self.sex = ['', 'Male', 'Female'][int(self.gender)]
        super(CNAME, self).save()
        
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name} {self.first_name}'
        
    def get_absolute_url(self):
        """Returns the url to access a detail record for this student."""
        return reverse('student_names', args=[str(self.id)])
       
class QSUBJECT(models.Model):#step5-subject 
     student_name = models.ForeignKey(CNAME, on_delete=models.CASCADE, null=True)#
     student_id = models.CharField(max_length=115, blank=True, null=True)
     test = models.IntegerField(blank=True, null=True, default=0)
     agn = models.IntegerField(blank=True, null=True, default=0)
     atd = models.IntegerField(blank=True, null=True, default=0)
     total = models.IntegerField(blank=True, null=True, default=0)
     exam = models.IntegerField(blank=True, null=True, default=0)
     agr = models.IntegerField(blank=True, null=True, default=0)
     gender = models.IntegerField(blank=True, null=True, default= 1, validators=[MaxValueValidator(2), MinValueValidator(1)])#
     created = models.DateTimeField(auto_now_add=True) 
     updated = models.DateTimeField(editable=False, blank=True, null=True,)
     tutor = models.ForeignKey(BTUTOR, on_delete=models.CASCADE, blank=True, null=True)
     cader_options = (('s', 'Senior'), ('j', 'Junior'))
     cader = models.CharField(max_length=1, choices=cader_options, blank=True, null=True)
     model_in = models.CharField(max_length=8, default='qsubject', blank=True, null=True)
     annual_scores = models.IntegerField(blank=True, null=True, default=0)
     annual_avr = models.FloatField(max_length=4, blank=True, null=True, default=0)
     fagr = models.IntegerField(blank=True, null=True, default=0)
     sagr = models.IntegerField(blank=True, null=True, default=0)
     aagr = models.IntegerField(blank=True, null=True, default=0)
     avr = models.FloatField(max_length=4, blank=True, null=True)
     grade = models.CharField(max_length=5, blank=True, null=True)
     posi = models.CharField(max_length=5, blank=True, null=True)


     ###Just for searching
     logged_in = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, help_text='subject_teacher', related_name='logins')
     term = models.CharField(max_length=30, blank=True, null=True)
     qteacher = models.CharField(max_length=100, blank=True, null=True)
     
     class Meta:
          ordering = ('student_name__gender', 'student_name__full_name') # helps in alphabetical listing. Sould be a tuple
    
     def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}:{self.student_name}:{str(self.tutor.subject)[:3]}:{self.tutor.Class}:{self.tutor.term}'
     
     def save(self):
        from .utils import do_grades, cader
        from .updates import average, get_serial_no
        if self.tutor is not None:
            if self.tutor.first_term == '1st Term' and self.tutor.second_term == '1st Term':
                self.avr = self.fagr = self.agr 
            if self.tutor.first_term == '1st Term' and self.tutor.second_term == '2nd Term' and self.tutor.third_term == '1st Term':
                self.avr = self.sagr = self.agr
            self.aagr = sum([int(i) for i in [self.fagr, self.sagr] if i is not None])
            if self.tutor.third_term == '3rd Term':
                dim = [int(i) for i in [self.agr, self.fagr, self.sagr] if i is not None]
                self.aagr = sum(dim)
                self.avr = average(dim, 't')
                self.grade = do_grades([int(self.avr)], cader(self.tutor.Class))[0]
            self.qteacher = self.tutor.teacher_name
        if self.student_name.full_name:
            slp = self.student_name.full_name.split(' ')+['OTHER']
            self.student_id = get_serial_no(self.student_name)
            self.gender = self.student_name.gender
        if self.grade == 'null':
            self.grade = do_grades([int(self.agr)], cader(self.tutor.Class))[0]
        cname = CNAME.objects.get(pk=self.student_name.id)
        if self.student_name.uid == None:
            cname.uid = self.student_id
        cname.term = self.tutor.term
        tutor = self.tutor
        if self.student_name.Class == self.tutor.Class:
            tutor.updated = datetime.datetime.today()
            tutor.save()  
            cname.save()
            super(QSUBJECT, self).save()
            
     def get_absolute_url(self):
        """Returns the url to access a detail record for this student."""
        return reverse('subject_view', args=[str(self.id), 1])
    
################################################################################################         

class Edit_User(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE,  blank=True, null=True, related_name='profile')
   status = (('Mr.', 'Mr'), ('Mrs.', 'Mrs'),('Miss.', 'Miss'), ('Sir.', 'Senior officer'), ('Ma.', 'Madam'), ('Mall.', 'Mallam'), ('Ust.', 'Ustadh'), ('Alh.', 'Alhaj'), ('Dr.', 'Doctor'), ('Engr.', 'Engineer'))
   title = models.CharField(max_length=15, choices=status, null=True, help_text='Select title to address you.', default= 'Mr.')
   last_name = models.CharField(max_length=20, null=True, help_text='(Surname)-Required')
   first_name = models.CharField(max_length=20, null=True, help_text='(Other names)-Required')
   photo = models.ImageField(upload_to='static/result/images/', null=True, default='default.jpg')
   image = models.CharField(max_length=30, null=True, blank=True,)
   bio = models.TextField(blank=True, help_text='Your summarised biography',  default= 'I am a professional science teacher, currently working with the aboved named School. If you plan on changing the font face and its color only once on a web page, you need to change its attributes in the element tag. Using the style attribute, you may specify the font face and color with font-family, color, and the font size with font-size, as shown in the example below.')
   phone = models.CharField(max_length=20, blank=True, help_text='Hotline')
   city = models.CharField(max_length=15, blank=True, help_text='Your town in the state of origin', default= 'Ibadan')
   country = models.CharField(max_length=10, blank=True, default= 'Nigeria', help_text='Nationality')
   organization = models.CharField(max_length=10, blank=True, help_text='Oganization affliated with', default= 'IIRO')
   location = models.CharField(max_length=30, blank=True, help_text='Current location')
   birth_date = models.DateField(null=True, blank=True, help_text='Date format: MM/DD/YYYY')
   section_status = (('Sc', 'Sciences'), ('SSc', 'Social Sciences'), ('Art', 'Arts and Humanities'))
   department = models.CharField(max_length=30, choices=section_status, blank=True, null=True)
   account_id = models.CharField(max_length=1130, default = 0, blank=True, null=True)
   email_confirmed = models.BooleanField(default=False, help_text='True/False')
   class_status = (('JSS 1', 'ONE'), ('JSS 2', 'TWO'), ('JSS 3', 'THREE'), ('SSS 1', 'FOUR'), ('SSS 2', 'FIVE'), ('SSS 3', 'SIX'), ('HEADS', 'HOD'))
   class_in = models.CharField(max_length=15, choices=class_status, blank=True, null=True, help_text='Select class in charge', default= None)
   login_count = models.IntegerField(blank=True, null=True, default= 0,)
   code = tuple([('2018', '2017/2018'), ('2019', '2018/2019'), ('2020', '2019/2020'), ('2021', '2020/2021'), ('2022', '2021/2022'), ('2023', '2022/2023'), ('2024', '2023/2024'), ('2025', '2024/2025'), ('2026', '2025/2026'), ('2027', '2026/2027'), ('2028', '2027/2028'), ('2029', '2028/2029'), ('2030', '2029/2030'), ('2031', '2030/2031'), ('2032', '2031/2032'), ('2033', '2032/2033'), ('2034', '2033/2034'), ('2035', '2034/2035'), ('2036', '2035/2036'), ('2037', '2036/2037'), ('2038', '2037/2038'), ('2039', '2038/2039'), ('2040', '2039/2040'), ('2041', '2040/2041'), ('2042', '2041/2042'), ('2043', '2042/2043'), ('2044', '2043/2044'), ('2045', '2044/2045'), ('2046', '2045/2046'), ('2047', '2046/2047'), ('2048', '2047/2048')])
   session = models.CharField(max_length=30, choices= code, null=True, default='2018',help_text='select academic SESSION',)
   resumption = models.DateField(null=True, blank=True, help_text='Date format: MM/DD/YYYY', default=str(datetime.date.today()))
   def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}:{self.user.username}'
   class Meta:
          ordering = ('account_id',)
   
   def save(self, *args, **kwargs):
        self.image = 'result/images/default.jpg'
        if self.photo.name is not 'default.jpg':
            self.image = 'result/images/default.jpg'#'result/images/'+str(self.user.username)+'.jpg'
        if self.user.email is not None and self.last_name is not None or self.first_name is not None:
            self.email_confirmed = True
        super(Edit_User, self).save(*args, **kwargs)

   def get_absolute_url(self):
        return reverse('pro_detail', args=[str(self.user.id)])
    
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Edit_User.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Edit_User.objects.create(user=instance)
    instance.profile.save()

class Post(models.Model):
    Account_Username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(max_length=1000)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
 
    def __str__(self):
        return self.subject

   
class QUESTION(models.Model):
    subjects = models.CharField(max_length=200, default='Undefined', null=True)#su
    classes = models.CharField(max_length=200, default='Undefined', null=True)#cl
    terms = models.CharField(max_length=200, default='Undefined', null=True)#tm
    question = models.CharField(max_length=1000, default='What is the missing question here?', null=True)
    section_status = (('correct', 'Answer'), ('wrong', 'Wrong'))
    optionA = models.CharField(max_length=200, default='Undefined', null=True)
    answerA = models.CharField(max_length=200, choices=section_status, default='wrong', null=True)
    optionB = models.CharField(max_length=200, default='Undefined', null=True)
    answerB = models.CharField(max_length=200, choices=section_status, default='wrong', null=True)
    optionC = models.CharField(max_length=200, default='Undefined', null=True)
    answerC = models.CharField(max_length=200, choices=section_status, default='wrong', null=True)
    optionD = models.CharField(max_length=200, default='Undefined', null=True)
    answerD = models.CharField(max_length=200, choices=section_status, default='wrong', null=True)
    CORRECT = models.CharField(max_length=200, default='Undefined', null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(editable=False, blank=True, null=True,)
    questNum = models.CharField(max_length=200, default='Undefined', null=True)
    serial_no = models.IntegerField(blank=True, null=True, default= 0,)
    photo = models.ImageField(upload_to='static/result/question_image/', null=True, default='Undefined')
    image_link = models.CharField(max_length=200, default='default.jpg', null=True)
    image = models.BooleanField(default=False, help_text='True/False')
    session = models.CharField(max_length=8, blank=True, null=True)###sx
    class Meta:
          ordering = ('id',) # helps in alphabetical listing. Sould be a tuple
    
    def save(self):
        if self.CORRECT == self.optionA :
            self.answerA = 'correct'
        elif self.CORRECT == self.optionB :
            self.answerB = 'correct'
        elif self.CORRECT == self.optionC :
            self.answerC = 'correct'
        else:
            self.answerD = 'correct'
        if not self.id:
            from .utils import session
            self.session = session().profile.session
            self.created = datetime.date.today()
        self.updated = datetime.datetime.today()
        self.published_date = timezone.now()
        self.questNum = str('Question'+str(self.serial_no))
        self.image_link = '/static/result/question_image/'+'image_'+self.subjects+'_'+str(['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', 'None'].index(self.classes))+'_'+str(['1st Term', '2nd Term', '3rd Term', 'None'].index(self.terms))+'_'+str(self.session)+'_'+str(self.serial_no)+'.jpg'
        super(QUESTION, self).save()
    def __str__(self):
        return self.subjects 
