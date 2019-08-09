from django.shortcuts import render
from django.template import RequestContext
from .models import LocTags,PartTags,Users
from . import forms
import sqlite3, string
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@csrf_protect
def LocTagPage(request):
    query_request = LocTags.objects.all()
    return(render(request,'loctagboard.html',{'obj': query_request}))


def PartTagPage(request):
    query_set = PartTags.objects.all()
    return(render(request,'parttagboard.html',{'object': query_set}))

def HomePage(request):
    return(render(request,'taghome.html'))

def addLocTag(request):
    form = forms.LocTagForm()
    return(render(request,"addlt.html",{"form":form}))

def addPartTag(request):
    form = forms.PartTagForm()
    return(render(request,"addpt.html",{"form":form}))

def NewLocTag(request):
    if(request.method == "POST"):
        f = forms.LocTagForm(request.POST)
        if(f.validate()):
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Insert into tagboard_loctags values(?);',(f.cleaned_data['tagname'],))
            conn.commit()
            conn.close()
        else:
            f = forms.LocTagForm()
            return(render(request,"addlt.html",{"form":f,"ErrorMessage":"already existing tag"}))
    else:
        f = forms.LocTagForm()
        return(render(request,'addlt.html',{"form":f}))
    return(LocTagPage(request))

def NewPartTag(request):
    if(request.method == "POST"):
        f = forms.PartTagForm(request.POST)
        if(f.validate()):
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Insert into tagboard_parttags values(?);',(f.cleaned_data['tagname'],))
            conn.commit()
            conn.close()
        else:
            f = forms.PartTagForm()
            return(render(request,"addpt.html",{"form":f,"ErrorMessage":"already existing tag"}))
    else:
        f = forms.PartTagForm()
        return(render(request,'addpt.html',{"form":f}))
    return(PartTagPage(request))


def EditUserTags(request,error=''):
    all_users = Users.objects.all()
    return(render(request,'showusers.html',{'users':all_users,'error':error}))
    
def ModifyUser(request):
   if(request.method=="POST"):
        f = forms.EditUserTagForm(request.POST)
        tags = ''.join(f.retrieveTag())
        if(tags is None):
            error = "No such user exists"
            return(EditUserTags(request,error))
        else:
            taglist = tags.split(',')
            return(render(request,'modut.html',{'tags':taglist,"uid":request.POST.get('uid')}))


def DeleteTag(request):
    if(request.method=="POST"):
        f = forms.DeleteTagForm(request.POST)
        if(f.is_valid()):
            d = f.cleaned_data
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('select tags from tagboard_users where uid = ?;',(d['uid'],))
            row = cur.fetchone()
            s = ''.join(row)
            l = s.split(',')
            s = ''
            for entry in l:
                if(entry != d['tag']):
                    s += entry+','
            s = s[:len(s)-1:1]
            cur.execute('update tagboard_users set tags = ? where uid = ?;',(s,d['uid'])) 
            conn.commit()
            conn.close()
            return(ModifyUser(request))


def AddUserTag(request,error=''):
    if(request.method=="POST"):
        return(render(request,'addut.html',{'uid':request.POST.get('uid'),'ErrorMessage':error}))
            

def AddUTag(request):
    if(request.method=='POST'):
        f = forms.AddTagForm(request.POST)
        s = f.retrieveTags()
        if(s is not None):
            l = s.split(',')      
            t = request.POST.get('tag')
            u = request.POST.get('uid')
            if(t in l):
                return(AddUserTag(request,'The tag already exists'))
            else:
                s += ','+t 
                conn = sqlite3.connect('db.sqlite3')
                cur = conn.cursor()
                cur.execute('update tagboard_users set tags = ? where uid = ?;',(s,u,))  
                conn.commit()
                conn.close()
                return(AddUserTag(request,'Tag Successfully Added'))

def DelLocTag(request):
    if(request.method=="POST"):
        delTag = request.POST.get('tagname')
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute('delete from tagboard_loctags where tagname=?;',(delTag,))
        conn.commit()
        conn.close()
        return(LocTagPage(request))
    
def DelPartTag(request):
    if(request.method=="POST"):
        delTag = request.POST.get('tagname')
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute('delete from tagboard_parttags where tagname=?;',(delTag,))
        conn.commit()
        conn.close()
        return(PartTagPage(request))
