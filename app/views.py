from django.shortcuts import render
from django.shortcuts import render, redirect
from firebase_admin import auth, firestore
from django.views import View
from app.__firebase__ import db
from django.http import JsonResponse
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import random, json
import midtransclient
from datetime import date
from django.contrib.auth import logout, login, authenticate
# Create your views here.
from django.contrib import messages

class ViewHomePage(View):
    template = 'pages/home.html'
    def get(self, request):
        ref = db.collection('Carousel').order_by(u'position')
        data = ref.stream()
        carousels = []
        for item in data :
            dict_ = item.to_dict()
            dict_['id']=item.id
            carousels.append(dict_)
        ref_profil = db.collection('Profil')
        data_profil = ref_profil.stream()
        profil = []
        for item_profil in data_profil:
            dict_ =item_profil.to_dict()
            profil.append(dict_)
        ref_misi = db.collection('Missions').where('type','==','i')
        data_misi = ref_misi.stream()
        misi = []
        for item_misi in data_misi:
            dict_= item_misi.to_dict()
            dict_['id'] = item_misi.id
            info = (item_misi.to_dict()['detail'][:80] + '..') if len(item_misi.to_dict()['detail']) > 75 else item_misi.to_dict()['detail']
            dict_['subtitle'] = info
            don_ = []
            ref_donation = db.collection('s-transactions').where('mis_id','==',item_misi.id)
            data_donation = ref_donation.stream()
            for i_donation in data_donation:
                try :
                    don_.append(float(i_donation.to_dict()['gross_amount']))
                except :
                    don_.append(0)
            total = sum(don_)
            dict_['col'] = total
            dict_['persen']= round((total/float(item_misi.to_dict()['target'])*100),4)
            dict_['target']=  "{:,.2f}".format(float(item_misi.to_dict()['target']))
            dict_['collected'] = "{:,.2f}".format(float(total))
            misi.append(dict_)
        try:
            list_random = random.choice(misi)
        except : 
            list_random= None
        return render(request, self.template,{'carousel':carousels, 'profil':profil,
                                               'misi_penting':list_random,
                                               'title':'Home',
                                               'misi':misi})      

class ViewAbout(View):
    template = 'pages/about.html'
    def get(self, request):
        ref_profil = db.collection('Profil')
        data_profil = ref_profil.stream()
        profil = []
        for item_profil in data_profil:
            dict_ =item_profil.to_dict()
            profil.append(dict_)
        return render(request, self.template,{'title':'About','profil':profil})

class ViewTeam(View):
    template = 'pages/team.html'
    def get(self, request):
        data = db.collection('Team').order_by(
    'pos', direction=firestore.Query.ASCENDING).stream()
        list_ = []
        for item in data:
            dict_ = item.to_dict()
            dict_['id'] = item.id
            list_.append(dict_)
        return render(request,self.template,{'title':'Team','data':list_})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

class ViewRegister(View):
    template='pages/register.html'
    def get(self, request):
        return render(request, self.template,{'title':'Register'})

class ViewMisi(View):
    template = 'pages/misi.html'
    def get(self, request):
        ref_misi = db.collection('Missions')
        data_misi = ref_misi.stream()
        misi = []
        for item_misi in data_misi:
            dict_= item_misi.to_dict()
            dict_['id'] = item_misi.id
            info = (item_misi.to_dict()['detail'][:80] + '..') if len(item_misi.to_dict()['detail']) > 75 else item_misi.to_dict()['detail']
            dict_['subtitle'] = info
            don_ = []
            ref_donation = db.collection('s-transactions').where('mis_id','==',item_misi.id)
            data_donation = ref_donation.stream()
            for i_donation in data_donation:
                try :
                    don_.append(float(i_donation.to_dict()['gross_amount']))
                except :
                    don_.append(0)
            total = sum(don_)
            dict_['col'] = total
            dict_['persen']= round((total/float(item_misi.to_dict()['target'])*100),4)
            dict_['target']=  "{:,.2f}".format(float(item_misi.to_dict()['target']))
            dict_['collected'] = "{:,.2f}".format(float(total))
            misi.append(dict_)
        return render(request, self.template,{'title':'Misi', 'misi':misi})      

class DetailMisi(View):
    template = 'pages/detail.html'
    def get(self, request, mis_id):
        ref_misi = db.collection('Missions').document(mis_id)
        data_misi = ref_misi.get()
        misi = []
        
        dict_= data_misi.to_dict()
        dict_['id'] = data_misi.id
        don_ = []
        ref_donation = db.collection('s-transactions').where('mis_id','==',data_misi.id)
        data_donation = ref_donation.stream()
        for i_donation in data_donation:
                try :
                    don_.append(float(i_donation.to_dict()['gross_amount']))
                except :
                    don_.append(0)
        total = sum(don_)
        dict_['col'] = total
        dict_['persen']= round((total/float(data_misi.to_dict()['target'])*100),4)
        dict_['target']=  "{:,.2f}".format(float(data_misi.to_dict()['target']))
        dict_['collected'] = "{:,.2f}".format(float(total))
        misi.append(dict_)
        return render(request, self.template,{'title': 'Detail', 'detail':misi,'id':data_misi.id})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

class ViewNews(View):
    template = 'pages/news.html'
    def get(self, request):
        ref_article = db.collection('Article-Web')
        data_article = ref_article.stream()
        l_article = []
        for article in data_article:
            dict_ = article.to_dict()
            dict_['id']= article.id
            info = (article.to_dict()['detail'][:80] + '..') if len(article.to_dict()['detail']) > 75 else article.to_dict()['detail']
            dict_['subtitle'] = info
            l_article.append(dict_)
        return render(request, self.template,{'title':'News', 'article':l_article})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

class DetailNews(View):
    template = 'pages/newsdetail.html'
    def get(self, request, news_id):
        ref_new = db.collection('Article-Web').document(news_id)
        data_new = ref_new.get()
        return  render(request, self.template,{'title':'Detail', 'detail':data_new.to_dict()})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
class ViewProposal(View):
    template = 'pages/proposal.html'
    def get(self, request):
        return render(request, self.template,{'title':'Proposal'})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

class ViewLogin(View):
    template= 'pages/login.html'
    def get(self, request):
        return render (request, self.template,{'title':'Login'})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

class PostLogin(View):
    def post(self, request):
        status = ''
        uid= request.POST['uid']
        data_user = db.collection('User').document(uid).get().to_dict()
        full_name = data_user['full_name']
        email = data_user['email']
        phone = data_user['phone']
        try:
            User.objects.get(username=uid)
        except :
            print('register')
            user = User.objects.create_user(uid, email=email, password=uid+phone, first_name=full_name, last_name=phone)
            user.save()
        user = authenticate(username=uid, password=uid+phone)
        if user is not None:
            login(request, user)
            status = 'OK'
        return HttpResponse(status)

class PostRegister(View):
    template='pages/register.html'
    def post(self, request):
        status = ''
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pwd1']
        try:
            user = auth.create_user(
            email=email,
            email_verified=False,
            # phone_number=phone,
            password=password,
            display_name=full_name,
            # photo_url='http://www.example.com/12345678/photo.png',
            disabled=False)
            print('Sucessfully created new user: {0}'.format(user.uid))
            db.collection('User').document(user.uid).set({'uid':user.uid,
                                                          'full_name':full_name,
                                                          'email':email,'phone':phone})
            messages.success(request, 'Registrasi Berhasil')
        except :
            messages.error(request,'Email telah terdaftar')
        return render(request, self.template,{'title':'Register'})
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class ViewSuccess(View):
    template = 'pages/success.html'
    def get(self, request):
        return render(request, self.template)

class PostProposal(View):
    template = 'pages/proposal.html'
    def post(self, request):
        uid = request.POST['uid']
        full_name = request.POST['full_name']
        city = request.POST['city']
        email = request.POST['email']
        phone = request.POST['phone']
        photo =  request.POST['u_photo']
        card = request.POST['u_card']
        proposal = request.POST['u_proposal']
        today = date.today()
        d4 = today.strftime("%Y-%m-%d")
        data = {
            'uid':uid,
            'name':full_name,
            'address':city,
            'email':email,
            'phone':phone,
            'id_card':card,
            'photo':photo,
            'proposal':proposal,
            'date':d4
        }
        try:
            db.collection('Proposal').document().set(data)
            messages.success(request, 'Proposal telah berhasil diajukan')
        except :
            messages.error(request,'Terjadi masalah di server mohon hubingi admin')
        return render(request, self.template,{'title':'Proposal'})

class HandlePayment(View):
    def post(self, request):
        snap = midtransclient.Snap(
        is_production=True,
        server_key='Mid-server-QeAV3hB7JRhAaU4GOTY_nxCN',
        client_key='Mid-client-WrMb-HVBxMZrefnq')
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        transaction = snap.create_transaction(body)
        return JsonResponse(transaction, safe=False)

class HandleRecord(View):
    def post(self, request):
        don_id = request.POST['don_id']
        amount = request.POST['amount']
        today = date.today()
        d4 = today.strftime("%Y-%m-%d")
        don_name = request.POST['don_name']
        mis_id = request.POST['mis_id']
        mis_name = request.POST['mis_name']
        data = {
            'don_id' : don_id,
            'amount' : float(amount),
            'don_name' : don_name,
            'date' : d4,
            'mis_id' : mis_id,
            'mis_name' : mis_name
        }
        print(data)
        db.collection('Donations').document().set(data)
        return HttpResponse('OK')