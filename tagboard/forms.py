from django import forms
import sqlite3
class PartTagForm(forms.Form):
    tagname = forms.CharField(max_length=50, required=True)
    def validate(self):
        if(self.is_valid()):
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            data = self.cleaned_data['tagname']
            cur.execute('select * from tagboard_parttags where tagname = ?;',(data,))
            rows = cur.fetchone()
            if(rows is None):
                return(True)
            else:
                return(False)
class LocTagForm(forms.Form):
    tagname = forms.CharField(max_length=50, required=True)
    def validate(self):
        if(self.is_valid()):
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            data = self.cleaned_data['tagname']
            cur.execute('select * from tagboard_loctags where tagname = ?;',(data,))
            rows = cur.fetchone()
            if(rows is None):
                return(True)
            else:
                return(False)
    
class EditUserTagForm(forms.Form):
    uid = forms.CharField(max_length=50, required=True)
    def retrieveTag(self):
        if(self.is_valid()):
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            data = self.cleaned_data['uid']
            cur.execute('select tags from tagboard_users where uid = ?;',(data,))
            row = cur.fetchone()
            return(row)


class DeleteTagForm(forms.Form):
    uid = forms.CharField(max_length=50)
    tag = forms.CharField()

class AddTagForm(forms.Form):
    uid = forms.CharField(max_length=50)
    tag = forms.CharField()

    def retrieveTags(self):
        if(self.is_valid()):
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cd = self.cleaned_data
            uid = cd['uid']
            tag = cd['tag']
            cur.execute('select tags from tagboard_users where uid = ?;',(uid,))
            res = cur.fetchone()
            s = ''.join(res,)
            return(s)