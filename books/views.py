# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import request
from books.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.template import RequestContext
import time
cursor = connection.cursor()
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
def register(request):
    username_error = False
    if request.method == 'POST':
        if len(User.objects.filter(username = request.POST['username']))>0:
            username_error = True
        else:
            u = User.objects.create_user(request.POST['username'], request.POST['pre_email']+'@'+request.POST['post_email'], request.POST['password'])
            
            u.save()
            return HttpResponseRedirect('/')
    return render_to_response('register.html' ,{'username_error': username_error}, context_instance = RequestContext(request))
@login_required
def search_result(request):
    token = ""
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
        elif request.POST.has_key('book_search'):
            token = 'book'
            cursor.execute("select * from search_author_book where author_name like %s or book_name like %s", ['%'+request.POST['book']+'%', '%'+request.POST['book']+'%'])
            result = dictfetchall(cursor)
        elif request.POST.has_key('group_search'):
            token = 'group'
            cursor.execute("select * from group_builder where group_name like %s", ['%'+request.POST['group']+'%'])
            result = dictfetchall(cursor)    
        elif request.POST.has_key('user_search'):
            token = 'profile'
            result = User.objects.filter(username= request.POST['user'])
              
    return render_to_response("search_result.html",{'token':token, 'result':result, }, context_instance = RequestContext(request))         
@login_required
def tag(request,tag_id):
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    if tag_id == 'hot':
        cursor.execute("select count(*) as counts, BID_id as book_id, BTitle as book_name from add_book join book on BID_id = BISBN group by BID_id order by counts desc;")
        book = dictfetchall(cursor)
    else:
        cursor.execute("select * from tag_search where tag_id = %s", [int(tag_id)])
        book = dictfetchall(cursor)
    return render_to_response("tag.html", {'book': book}, context_instance = RequestContext(request))
@login_required
def book(request, book_id):
    have_favorite = False
    if request.method == 'POST':
        if request.POST.has_key('quit_favorite'):
            cursor.execute('delete from add_book where FID_id = (select FID from favorite where UID_id = %s) and BID_id = %s', [request.user.id, book_id])
            transaction.commit()
        elif request.POST.has_key('favorite'): 
            n = AddBook(FID = Favorite.objects.get(UID = request.user), BID = Book.objects.get(BISBN = book_id))
            n.save()
        elif request.POST.has_key('submit'):

            r = Remark(RTitle = request.POST["title"], RContent = request.POST["content"], RDate = time.strftime('%Y-%m-%d',time.localtime(time.time())), UID = request.user, BID = Book.objects.get(BISBN = book_id) )
            r.save()
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    cursor.execute('select * from favorite_book where owner_name = %s and book_id = %s', [request.user.username, book_id])
    if len(dictfetchall(cursor))>0:
        have_favorite = True
    book = Book.objects.get(BISBN = book_id)
    cursor.execute('select * from tag_search where book_id=%s', [book_id])
    tag = dictfetchall(cursor)
    cursor.execute("select * from book_author where book_id = %s", [book_id])
    author = dictfetchall(cursor)[0]
    cursor.execute("select * from remark_book_author where book_id = %s", [book_id])
    remark_list = dictfetchall(cursor)
    return render_to_response("book_detail.html",{'have_favorite':have_favorite, 'book':book, 'tag':tag, 'author':author, 'remark_list':remark_list,}, context_instance = RequestContext(request))         
@login_required 
def remark(request, remark_id):
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    cursor.execute("select * from remark_book_author where remark_id = %s", [int(remark_id)])
    remark = dictfetchall(cursor)[0]
    return render_to_response("remark.html", {'remark': remark}, context_instance = RequestContext(request))
@login_required
def article(request, article_id):
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    cursor.execute("select * from article_author_group where article_id = %s", [int(article_id)])
    article = dictfetchall(cursor)[0]
    return render_to_response("article.html", {'article': article}, context_instance = RequestContext(request))
@login_required
def group(request, group_id):
    have_joined = False
    if request.method == 'POST':
        if request.POST.has_key("article"):
            a = Article(ATTitle = request.POST["title"], ATContent = request.POST["content"], ATDate = time.strftime('%Y-%m-%d',time.localtime(time.time())), UID = request.user, GID =Group.objects.get(GID =  int(group_id)))
            a.save()
        elif request.POST.has_key("join"):
            j = Join(GID =Group.objects.get(GID =  int(group_id)), UID = request.user)
            j.save()
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    if len(Join.objects.filter(UID = request.user, GID =Group.objects.get(GID = int(group_id)) ))>0 or Group.objects.get(GID = int(group_id)).GBuilder==request.user:
        have_joined = True
    
    cursor.execute("select * from article_author_group where group_id = %s", [int(group_id)])
    article_list = dictfetchall(cursor)
    cursor.execute("select * from group_builder where group_id = %s", [int(group_id)])
    manager = dictfetchall(cursor)[0]
    cursor.execute("select * from join_group where group_id = %s", [int(group_id)])
    member = dictfetchall(cursor)
    return render_to_response("group_detail.html", {'article_list': article_list, 'manager': manager, 'member': member, 'have_joined':have_joined, }, context_instance = RequestContext(request))
@login_required
def homepage(request):
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
    tag = Tag.objects.all()
    cursor.execute("select * from search_author_book")
    book = dictfetchall(cursor)[-5:]
    cursor.execute("select * from group_builder")
    group = dictfetchall(cursor)[-5:]
    cursor.execute("select * from remark_author")
    remark = dictfetchall(cursor)[-5:]
    cursor.execute("select * from article_author")
    article = dictfetchall(cursor)[-5:]
    return render_to_response("homepage.html", {'tag':tag, 'book':book, 'group':group, 'remark':remark, 'article':article}, context_instance = RequestContext(request))
    
@login_required
def profile(request, username):  
    user = User.objects.get(username = username)
    cursor.execute("select remark_id, remark_name from remark_author where author_name = %s", [username])
    remark_list = dictfetchall(cursor)
    cursor.execute("select book_id, book_name from favorite_book where owner_name = %s", [username])
    favorite_list = dictfetchall(cursor)
    cursor.execute("select article_name, article_id from article_author where author_name = %s", [username])
    article_list = dictfetchall(cursor)
    cursor.execute("select group_name, group_id from join_group where member_name = %s", [username])
    group_list = dictfetchall(cursor)
    cursor.execute("select group_id, group_name from group_builder where builder_name = %s", [username])
    manager_list = dictfetchall(cursor)
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
        elif request.POST.has_key('change_password'):
            request.user.set_password(request.POST['password'])
            request.user.save()
        elif request.POST.has_key('create_group'):
            g = Group(GBuilder = request.user, GName = request.POST["group"], GBuildDate =  time.strftime('%Y-%m-%d',time.localtime(time.time())))
            g.save()
            cursor.execute("select group_id, group_name from group_builder where builder_name = %s", [username])
            manager_list = dictfetchall(cursor)
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/accounts/login/')
        else:
            for i in remark_list:
                if request.POST.has_key(i['remark_name']):
                    Remark.objects.filter(RID = i['remark_id']).delete()
                    cursor.execute("select remark_id, remark_name from remark_author where author_name = %s", [username])
                    remark_list = dictfetchall(cursor)
                    break
            for i in article_list:
                if request.POST.has_key(i['article_name']):
                    Article.objects.filter(ATID = i['article_id']).delete()
                    cursor.execute("select article_name, article_id from article_author where author_name = %s", [username])
                    article_list = dictfetchall(cursor)
                    break
            for i in favorite_list:
                if request.POST.has_key(i['book_id']):
                    cursor.execute("delete from add_book where FID_id = (select FID from favorite where UID_id = %s) and BID_id = BID", [request.user.id])
                    transaction.commit()
                    cursor.execute("select book_id, book_name from favorite_book where owner_name = %s", [username])
                    favorite_list = dictfetchall(cursor)
                    break                
            for i in group_list:
                if request.POST.has_key('group'+str(i['group_id'])):
                    Join.objects.filter(UID = request.user, GID =Group.objects.get(GID =int(i['group_id']) ) ).delete()
                    Article.objects.filter(UID = request.user, GID = Group.objects.get(GID =int(i['group_id']) )).delete()
                    cursor.execute("select group_name, group_id from join_group where member_name = %s", [username])
                    group_list = dictfetchall(cursor)     
                    cursor.execute("select article_name, article_id from article_author where author_name = %s", [username])
                    article_list = dictfetchall(cursor)      
                    break
            for i in manager_list:
                if request.POST.has_key('manager'+str(i['group_id'])):
                    Article.objects.filter(GID = Group.objects.get(GID =int(i['group_id']) )).delete()
                    Join.objects.filter(GID =Group.objects.get(GID =int(i['group_id']) )).delete()
                    Group.objects.filter(GID = int(i['group_id'])).delete()
                    cursor.execute("select group_id, group_name from group_builder where builder_name = %s", [username])
                    manager_list = dictfetchall(cursor)
                    cursor.execute("select article_name article_id from article_author where author_name = %s", [username])
                    article_list = dictfetchall(cursor)
                    break

    return render_to_response('profile.html', {'user':user,'remark_list':remark_list, 'article_list':article_list, 'favorite_list':favorite_list, 'group_list':group_list, 'manager_list':manager_list}, context_instance = RequestContext(request)) 

    
    
            

            
                
            
            
                    
