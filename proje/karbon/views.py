from django.shortcuts import render,redirect #HTML sayfası döndürür,yönlendirme yapar.
from . forms import CreateUserForm,LoginForm #kayıt formu oluşturmak için                    
from django.contrib.auth.models import auth #kullanıcı işlemleri için
from django.contrib.auth import authenticate,login,logout #kullanıcıyı doğrulayıp giriş-çıkış yapar.
from django.contrib.auth.decorators import login_required #kullanıcının giriş yapmadan sayfaya girmesini engeller.
from django.contrib import messages #kullanıcıya mesaj göstermek için.
from .models import EmissionRecord
from django.contrib.auth import update_session_auth_hash
from .forms import PasswordChangingForm

#Sadece sayfayı gösterir.
def homepage(request):
    return render(request,'karbon/index.html')

#Kayıt işlemi için
def register(request):
    #Form oluşturma işlemi
    form = CreateUserForm(request.POST)
    #Formu kontrol eder
    if form.is_valid():
        form.save() #veri tabanına kullanıcıyı ekler
        messages.success(request,"Kullanıcı oluşturuldu!")
        return redirect('login') #login sayfasına yönlendirir
    context = {'RegistrationForm':form} #template'e form gönderiyoruz.
    return render(request,'karbon/register.html',context)

#Giriş işlemi için
def my_login(request):
    form = LoginForm()
    if request.method == 'POST': #Kullanıcı butona bastı mı kontrolü
        form = LoginForm(request,data=request.POST) #bastıysa formu doldur.
        if form.is_valid(): #bilgileri doğrulamak için
           #Kullanıcı bilgilerini alma.
           username = request.POST.get('username') 
           password = request.POST.get('password')

           user = authenticate(request,username = username,password = password) #doğruysa user döner yanlışsa none.

           if user is not None: #none değilse
               auth.login(request,user) #sisteme giriş yap.
               return redirect('hesaplama') #hesaplama sayfasına yönlendir.
           
          
    context = {'LoginForm':form}
    return render(request,'karbon/login.html',context) #sayfayı gösterme

#Hesaplama işlemi çin
@login_required(login_url='login')
def hesaplama(request):

    from .forms import EmissionForm
    from .models import EmissionRecord

    form = EmissionForm(request.POST or None) #form oluştur, veri varsa doldur yoksa boş.
    #başlangıç değerleri boş
    scope1 = None
    scope2 = None
    total = None
    #yüzdelik kısım
    scope1_percent = 0
    scope2_percent = 0

    if request.method == "POST" and form.is_valid(): #butona basılınca form doğruysa
        #verileri al
        electricity = form.cleaned_data['electricity']
        natural_gas = form.cleaned_data['natural_gas']
        fuel_type = form.cleaned_data['fuel_type']
        fuel_amount = form.cleaned_data['fuel_amount']
       
       # Emisyon faktörleri
        ELECTRICITY_FACTOR = 0.442
        NATURAL_GAS_FACTOR = 2.06672
        FUEL_FACTORS = {
        'benzin': 2.06916,
        'dizel': 2.57082,
        'lpg': 1.55713,
        }
        
        fuel_factor = FUEL_FACTORS[fuel_type]
        scope1 = ( natural_gas * NATURAL_GAS_FACTOR) + (fuel_amount * fuel_factor)
        scope2 = electricity * ELECTRICITY_FACTOR
        total = scope1 + scope2

        
        if total > 0: #sıfıra bölmeyi engellemek için
            #grafik için
            scope1_percent = (scope1 / total) * 100
            scope2_percent = (scope2 / total) * 100

        #Yeni kayıt oluştur
        EmissionRecord.objects.create(
            user=request.user, #giriş yapan kullanıcıya bağla
            electricity=electricity,
            natural_gas=natural_gas,
            fuel_type=fuel_type,
            fuel_amount=fuel_amount,
            scope1=scope1,
            scope2=scope2,
            total_emission=total
        )

    records = EmissionRecord.objects.filter(user=request.user).order_by('-created_at') #tüm kayıtları al

    #Kayıtları template'e gönder.
    context = {
        'form': form,
        'scope1': scope1,
        'scope2': scope2,
        'total': total,
        'scope1_percent': scope1_percent,   
        'scope2_percent': scope2_percent,
        'records': records,   
    }

    return render(request,'karbon/hesaplama.html',context) #HTML'e gönder.

#Kullanıcının çıkış işlemi
def user_logout(request):
    auth.logout(request)
    return redirect("") #anasayfaya dönüş için             

def bilgilerim(request):
    user = request.user

    # Kullanıcının kayıtlarını al
    records = EmissionRecord.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'records': records
    }

    return render(request, 'karbon/bilgilerim.html', context)        

#Kullanıcı şifre değiştirme işlemi için
def sifre_degistir(request):

    if request.method == 'POST':

        form = PasswordChangingForm(user=request.user, data=request.POST)

        if form.is_valid():

            user = form.save()

            # Kullanıcıyı sistemden atmaz
            update_session_auth_hash(request, user)

            messages.success(request, "Şifren başarıyla güncellendi!")

            return redirect('bilgilerim')

    else:

        form = PasswordChangingForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'karbon/sifre_degistir.html', context)               