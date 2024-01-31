from django.urls import path as url
#from django.conf.urls import patterns, include, url
from.import views, imports, posts, sign_up_or_log_in, creates, deletions, updates#, tasks
urlpatterns = [
            #####EXPORTS #######IMPORTS#####  path('<int:pk>/', views.detail, name='detail'),
            url('home/', views.home, name='home'),
            url('offline/<int:pk>/', views.offline, name='offline'),
            url('massRegistration/', imports.massRegistration, name='massRegistration'),
            url('samples_down/', views.sample_down, name='samples_down'),
            url('name_down/<int:pk>/<int:fm>/<int:ps>/', views.name_down, name='name_down'),
            url('samples_disp/', views.sample_disply, name='samples_disp'),
            url('upload_txt/<int:pk>/', imports.upload_new_subject_scores, name='upload_txt'),
            url('setup_questions/', imports.setup_questions, name='setup_questions'),            
            url('user_qury/', sign_up_or_log_in.user_qury, name='user_qury'),
         			 #####VIEWS##### responsive_updates 
            url('all_users/<int:pk>/', views.all_users, name='all_users'),           
            #url('delayed_task/<int:model>/<int:pk>/', tasks.delayed_task, name='delayed_task'),#
            url('zip_pdf/<int:model>/<int:pk>/', views.zipped_my_pdfs, name='zip_pdf'),#file, clasS, term
            url('searchs', views.searchs, name='searchs'),
            url('card_comments', views.card_comment, name='card_comments'),
            url('student_info/<int:pk>/', views.student_info, name='student_info'),
            url('student_info_json/', views.student_info_json, name='student_info_json'),
            url('student_exam_page/<int:subj_code>/<int:pk>/', views.student_exam_page, name='student_exam_page'),
            url('accid/<int:pk>/<int:md>/', views.accid, name='accid'),
            url('csv_bsh/<int:pk>/', views.csv_bsh, name='csv_bsh'),
            url('subject_home/<int:pk>/<int:cl>/', views.subject_home, name='subject_home'),
            url('render/pdf/<int:ty>/<int:sx>/<int:pk>/<int:uk>/', views.Pdf.as_view(), name='pdf'),
            url('uniqueness/<int:pk>/', views.uniqueness, name='uniqueness'),
            url('student_home_page/<int:pk>/', views.student_home_page, name='student_home_page'), 
            url('<int:pk>/<int:md>/', views.detailView, name='subject_view'),###################### 
            url('_all/<int:pk>/<int:md>/', views.all_View, name='subject_view_all'),#################### student_subject_list zipped_my_pdfs
            url('report_card_summary/', views.report_card_summary, name='report_card_summary'),
            url('student_names/<int:pk>/', views.Student_names_list, name='student_names'),
            #results_junior_senior#annual_sheet
            url('subject/transfers/<int:md>/', views.teacher_accounts, name='transfers'),
            url('auto_pdf_a/transfers/<int:md>/', views.auto_pdf_a, name='auto_pdf_a'),
            url('editQuest/<int:pk>/', views.editQuest, name='editQuest'),
            url('results_junior_senior/<int:pk>/', views.results_junior_senior, name='results_junior_senior'),
            url('search_results/<int:pk>/', views.search_results, name='search_results'),
            			 #####CREATES##### ques_subject_updates  
            
            
            url('create_new_teacher/', creates.create_new_subject_teacher, name='teacher_create'),
            url('logins/', sign_up_or_log_in.loggin, name='logins'),
            url('log_out/', sign_up_or_log_in.logout, name='log_out'),
            url('admin_page/', sign_up_or_log_in.admin_page, name='admin_page'),
            url('passwords/<int:pk>/', sign_up_or_log_in.password1, name='passwords'),
            url('password/', sign_up_or_log_in.password2, name='password'),
            url('InputTypeError/', sign_up_or_log_in.InputTypeError, name='InputTypeError'),
            url('all_accounts/', sign_up_or_log_in.all_users, name='all_accounts'),
              #####POSTS%###### search_tutors
            url('my_post/post_list', posts.my_post, name='my_post_list'),
            url('post/post_list', posts.post_list, name='post_list'),
            url('post/<int:pk>/', posts.post_detail, name='post_detail'),
            url('post/new/', posts.post_new, name='post_new'),
            url('post_edit/<int:pk>/', posts.post_edit.as_view(), name='post_edit'),
            url('drafts/', posts.post_draft_list, name='post_draft_list'),#post approvals student_in_none new_student_name
            
            url('posts_publishing/<int:pk>/publish/', posts.posts_publishing, name='posts_publishing'),
              ####DELETE%######  auto_pdf_a
            url('delete_warning/deletions/<int:pk>/', deletions.confirm_deletion, name='delete_warning'),
            url('delete_a_student/deletions/<int:pk>/', deletions.confirmed_delete, name='delete'),
            url('deletions/', deletions.deletes, name='deletes'),
            url('yes_no/deletions/<int:pk>/', deletions.yes_no, name='yes_no'),
            url('warning_delete/deletions/<int:pk>/', deletions.warning_delete, name='warning_delete'),
            url('deletes/deletions/<int:pk>/', deletions.delete, name='confirmed'), 
            url('confirm_deleting_a_user/ deletions/<int:pk>/', deletions.confirm_deleting_a_user, name='confirm_deleting_a_user'),
            url('deletes/deletions/<int:pk>/', deletions.delete, name='confirmed'),
            url('delete_a_user/deletions/<int:pk>/', deletions.delete_user, name='delete_a_user'),
            url('post_remove/ deletions/<int:pk>/', deletions.delete_post, name='post_remove'),
            			 #####UPDATES%###### 
            url('edit_accounts/updates/<int:pk>/', updates.Users_update.as_view(), name='edit_accounts'),
            url('create_local_accounts/updates/<int:x>/', updates.create_local_accounts, name='create_local_accounts'),
            url('tutor/updates/<int:pk>/', updates.Teacher_model_view, name='tutor_update'),
            url('responsive_updates/<int:pk>/<int:uk>/', updates.responsive_updates, name='responsive_updates'),
            #
            url('need_tutor', updates.need_tutor, name='need_tutor'),
            url('question_image/<int:pk>/', updates.question_image, name='question_image'),
            
            url('synchronizing/<int:last>/<int:subject>/<int:Class>/', updates.synch, name='synch'),
            url('pro_detail/updates/<int:pk>/', updates.profiles, name='pro_detail'),####
            url('user/updates/<int:pk>/', updates.ProfileUpdate.as_view(), name='user_update'),#####
            url('upload_photo/updates/<int:pk>/', updates.profile_picture, name='upload_photo'),#####
            url('Cname_edit/updates/<int:pk>/', updates.Cname_edit.as_view(), name='Cname_edit'),####
            
               
            url('', sign_up_or_log_in.flexbox, name='flexing'),
                    
				]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
