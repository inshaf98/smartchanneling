from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
import datetime
from django.db.models import Q
import requests
from django.http import JsonResponse

from django.db.models import Case, When, F

#loading trained_model
import joblib as jb
model = jb.load('trained_mnb.joblib')

def Home(request):
    covData = True
    result = None
    slSummary = None
    while (covData):
        try:
            result = requests.get('https://www.hpb.health.gov.lk/api/get-current-statistical')
            slSummary = result.json()['data']
            covData=False
        except:
            covData = False


    # Sending Request & getting JSON file
    url = 'https://newsapi.org/v2/top-headlines?category=health&language=en&sortBy=publishedAt&apiKey=d8a8c1dd1c1e4a36a67302e05c9361b2'
    response = requests.get(url)
    data = response.json()
    new = data['articles']
    request.session['passnews'] = new

    # Seperate Each news
    title = []
    desc = []
    img = []
    dat = []
    ur = []

    for i in range(6):
        mynews = new[i]
        title.append(mynews['title'])
        desc.append(mynews['description'])
        img.append(mynews['urlToImage'])
        dat.append(mynews['publishedAt'])
        ur.append(mynews['url'])

        mylist = zip(title, desc, img, dat,ur)

    # Getting News Articles From Database
    fit = News_Article.objects.filter(category="Fitness").order_by("-date")[:1]
    travel = News_Article.objects.filter(category="Travel").order_by("-date")[:2]
    heat = News_Article.objects.filter(Q(category='Healthy Eating')|Q(category='Wellness')).order_by("-date")

    # Passing Data to HTML Templates as Dictionary
    d = {'fit': fit, 'travel': travel, 'heat':heat, 'mylist':mylist, 'slSummary':slSummary}
    return render(request,'home.html', d)

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""

        # Checking login details
        if user:
            try:
                sign = UserProfile.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error ="pass1"
            else:
                login(request, user)
                error="pass2"
        else:
            error = "incorrect"

    d = {'error': error}
    return render(request, 'login.html', d)




def Logout(request):
    logout(request)
    return redirect('home')

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        nic = request.POST['nic']
        add = request.POST['add']
        im = request.FILES['image']
        dat = datetime.date.today()

    # Check if Username and email exists
        if User.objects.filter(username=u).exists():
            error="already"

        elif User.objects.filter(email=e).exists():
            error = "ealready"

        elif UserProfile.objects.filter(nic=nic).exists():
            error = "nic_exist"

        else:
            # Create User
            user = User.objects.create_user(email=e, username=u, password=p, first_name=f, last_name=l)
            UserProfile.objects.create(user=user, contact=con, address=add, nic=nic, image=im, dob=d)
            error = "create"

    d = {'error': error}
    return render(request, 'register.html',d)

def Admin_Home(request):

    # Getting Count of all objects and Pass to template file
    use = 0
    doc = 0
    nws = 0
    feed = 0
    req = 0
    payment = 0
    for i in UserProfile.objects.all():
        use += 1
    for i in Doctor.objects.all():
        doc += 1
    for i in News_Article.objects.all():
        nws += 1
    for i in Feedback.objects.all():
        feed += 1
    for i in Payment.objects.all():
        payment += 1
    for i in Consult.objects.filter(advice__isnull=True):
        req += 1
    d = {'use': use, 'doc': doc, 'nws' : nws, 'feed': feed, 'payment':payment, 'req':req}
    return render(request, 'admin_home.html',d)



def predict(request):

    symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
                    'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm',
                    'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
                    'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid',
                    'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness',
                    'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
                    'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history',
                    'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption',
                    'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples',
                    'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                    'red_sore_around_nose', 'yellow_crust_ooze']


    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':
        return render(request, 'predict.html', {"list2": alphabaticsymptomslist})

    elif request.method == 'POST':

        inputno = int(request.POST["noofsym"])
        print(inputno)

    if (inputno == 0):
        return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

    else:

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")

        print(psymptoms)

        testingsymptoms = []
        # putting zero in all coloumn fields
        for x in range(0, len(symptomslist)):
            testingsymptoms.append(0)

        # update 1 where symptoms gets matched...(if any selected symptoms matches the column then update it with 1)
        for k in range(0, len(symptomslist)):

            for z in psymptoms:
                if (z == symptomslist[k]):
                    testingsymptoms[k] = 1

        # finally the input test will be a 132 long binary value ex: 0,0,1,0,0,0,1
        inputtest = [testingsymptoms]

        print(inputtest)

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore = y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        userr = User.objects.get(id=request.user.id)
        sign = UserProfile.objects.get(user=userr)
        ag = sign.dob

        us = str(sign)

        from datetime import date
        today = date.today()
        age = today.year - ag.year - ((today.month, today.day) < (ag.month, ag.day))



    return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , 'us':us, 'age':age })





def View_My_Detail(request):

    # Getting user profile Details
    user = User.objects.get(id=request.user.id)
    sign = UserProfile.objects.get(user=user)

    if sign.prime_subscription == None:
        prime_status = 'no_plan'

    elif datetime.date.today() >= sign.prime_subscription:
        prime_status = 'expired'

    else:
        prime_status = 'active'

    print(prime_status)

    d ={'pro':sign, 'ps':prime_status}
    return render(request, 'profile.html',d)

def Add_Doctor(request):
    error = ""
    type = Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        cat = request.POST['type']
        add = request.POST['add']
        slmc_reg = request.POST['slmc']
        im = request.FILES['image']
        dat = datetime.date.today()


        # Check if doctor already exist with same username
        if User.objects.filter(username=u, is_staff=True).exists():
            error = "already"
        else:
            user = User.objects.create_user(email=e, username=u, password=p, first_name=f, last_name=l)
            Doctor.objects.create(category=cat, image=im, user=user, contact=con, address=add, slmc=slmc_reg)
            error = "create"

            sf = User.objects.get(username=u, is_staff=False)
            sf.is_staff = True
            sf.save()
    d = {'error': error, 'type': type}
    return render(request, 'add_doctor.html',d)


def Manage_doctor(request):

        # Query for filter active doctor
        users = User.objects.filter(is_active=True, is_staff=True, is_superuser=False)
        dp = Doctor.objects.filter(user__in=users)
        d = {'dp': dp}
        return render(request, 'manage_doctor.html', d)

def Update_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    type = Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['type']
        try:
            im = request.FILES['image']
            doc.image = im
            doc.save()
        except:
            pass
        dat = datetime.date.today()
        doc.user.first_name = f
        doc.user.last_name = l
        doc.user.email = e
        doc.contact = con
        doc.category = cat
        doc.address = add
        doc.user.save()
        doc.save()
        error = "success"
    d = {'error': error, 'doc': doc, 'type': type}
    return render(request, 'update_doctor.html',d)

def Delete_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    use = doc.user
    dc = User.objects.filter(is_staff=True, username=use, is_superuser=False)
    dcs = dc[0]
    dcs.is_active = False
    dcs.save()
    return redirect('manage_doctor')

def Update_profile(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    sign = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        try:
            im = request.FILES['image']
            sign.image = im
            sign.save()
        except:
            pass
        to1 = datetime.date.today()
        to1 = datetime.date.today()
        sign.user.first_name = f
        sign.user.last_name = l
        sign.user.email = e
        sign.contact = con
        sign.address = add
        sign.user.save()
        sign.save()
        terror = "create"
    d = {'terror': terror, 'doc': sign}
    return render(request, 'update_profile.html',d)


def Add_article(request):

    cat = ArticleCategory.objects.all()
    error = ""
    if request.method == 'POST':
        t = request.POST['Title']
        c = request.POST['content']
        img = request.FILES['image']
        ct = request.POST['cts']
        dat = datetime.date.today()
        News_Article.objects.create(title=t, content=c, category=ct, date=dat, image=img)
        error = "addnews"
    d = {'error': error, 'cat':cat}
    return render(request, 'add_article.html',d)

def Manage_article(request):
    news = News_Article.objects.all()
    d = {'news': news}
    return render(request, 'manage_article.html',d)

def Update_article(request,pid):
    nw = News_Article.objects.get(id=pid)
    cat = ArticleCategory.objects.all()
    error = ""
    if request.method == 'POST':
        t = request.POST['title']
        c = request.POST['content']
        catg = request.POST['cts']

        try:
            img = request.FILES['image']
            nw.image=img
            nw.save()
        except:
            pass
        dat = datetime.date.today()
        nw.title = t
        nw.content = c
        nw.date = dat
        nw.category = catg
        nw.save()
        error = "update"
    d = {'error':error,'nw':nw, 'cat':cat}
    return render(request,'update_article.html',d)


def delete_news(request,pid):
    nw = News_Article.objects.get(id=pid)
    nw.delete()
    return redirect('manage_news')


def Manage_user(request):
    users = User.objects.filter(is_active=True, is_staff=False)
    up = UserProfile.objects.filter(user__in=users)
    d = {'up':up}
    return render(request, 'manage_user.html',d)

def delete_user(request,pid):
    doc = UserProfile.objects.get(id=pid)
    use=doc.user
    dc = User.objects.filter(is_staff=False, username=use)
    dcs = dc[0]
    # Disable the user without actually deleting
    dcs.is_active=False
    dcs.save()
    return redirect('manage_user')

def View_feedback(request):
    fb = Feedback.objects.all()
    d = {'fb': fb}
    return render(request, 'view_feedback.html',d)

def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

def Send_feedback(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    sign = UserProfile.objects.get(user=user)
    to1 = datetime.date.today()
    if request.method == "POST":
        t = request.POST['uname']
        te = request.POST['msg']
        Feedback.objects.create(user=sign,messages=te,date=to1)
        terror = "create"
    d = {'user': sign, 'terror': terror}
    return render(request, 'send_feedback.html',d)

def Change_password(request):
    error = ""

    if request.method=="POST":
        current = request.POST['cpwd']
        nw1 = request.POST['pwd1']
        nw2 = request.POST['pwd2']

        user = User.objects.get(id=request.user.id)
        check = user.check_password(current)
        if check == True:
            if nw1 == nw2:
                user.set_password(nw1)
                user.save()
                error = "yes"
            else:
                error = "not"

        else:
            error="cperror"

    d = {'error':error}
    return render(request, 'change_password.html',d)

def Consultation(request):
    uer = ""
    prime_status=""
    error = ""
    symlist=""
    sign=""
    age=""
    docc=""
    if request.user.is_superuser or request.user.is_staff:
        uer = "admin"
    else:
        user_id = User.objects.get(id=request.user.id)
        uname = UserProfile.objects.get(user=user_id)
        if uname.prime_subscription == None or datetime.date.today() >= uname.prime_subscription:
            prime_status = "false"
            print('No Subscription')
        else: prime_status = "True"

        error=""
        docc = Doctor.objects.all()

        symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
                        'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
                        'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
                        'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
                        'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
                        'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
                        'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm',
                        'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                        'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
                        'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid',
                        'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                        'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness',
                        'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
                        'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                        'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                        'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history',
                        'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                        'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption',
                        'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples',
                        'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                        'red_sore_around_nose', 'yellow_crust_ooze']

        symlist = sorted(symptomslist)

        userr = User.objects.get(id=request.user.id)
        sign = UserProfile.objects.get(user=userr)
        bday = sign.dob
        from datetime import date
        today = date.today()
        age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))



        if request.method == "POST":
            feet = request.POST['feet']
            inch = request.POST['inch']

            ht = feet + "  " + inch
            ftt = feet.split(' Feet')[0]
            inchh = inch.split(' Inch')[0]

            # Convert the feet to inches and then calculate height in Meters
            fttFloat = float(ftt)
            inchhFloat = float(inchh)
            height = ((fttFloat * 12) + inchhFloat) * 0.0254

            cs = Consult()
            cs.user = userr
            cs.fname = request.POST['fname']
            cs.age = request.POST['age']
            weight = request.POST['weight']
            cs.height = ht
            cs.weight = weight

            # BMI Calculation
            bmii = float(weight)/(height*2)
            bmi = round(bmii, 1)
            if bmi < 18.0:
                cs.bmi = str(bmi) + " - " + "Under Weight"
                cs.save()
            elif 24.9 > bmi > 18.0:
                cs.bmi = str(bmi) + " - " + "Normal Weight"
                cs.save()

            elif 29.9 > bmi > 25.0:
                cs.bmi = str(bmi) + " - " + "Over Weight"
                cs.save()
            else:
                cs.bmi = str(bmi) + " - " + "Obese"
                cs.save()


            sym = request.POST.getlist("symptoms")
            cs.symptoms = ', '.join(sym)
            cs.allergiesEms = request.POST.get('amc','')
            dcc = request.POST['doc']
            dcs = dcc.split(' -')[0]
            cs.doc = dcs
            # cs.doc = request.POST['doc']
            cs.date = datetime.date.today()

            if 'img1' in request.FILES:
                cs.img1 = request.FILES['img1']
                cs.save()

            if 'img2' in request.FILES:
                cs.img2 = request.FILES['img2']
                cs.save()

            if 'img3' in request.FILES:
                cs.img3 = request.FILES['img3']
                cs.save()
            cs.save()
            error = "sent"
            # Passing values feet ranging from 3 to 9 with 1 step and inches from 0 to 13


    d = {'uer':uer,'prime':prime_status, 'error':error, 'symlist':symlist, 'user':sign, 'age':age, 'docc':docc, 'ft': range(3,9,1), 'in': range(13)}
    return render(request, 'consult.html', d)


def View_requests(request):
    error=""
    doc = request.user.username
    pro = Consult.objects.filter(doc=doc, advice__isnull=True).order_by('-date')

    d={'error':error, 'pro':pro, 'all':all}
    return render(request, 'view_requests.html', d)

def Diagnosis(request,pid):
    error = ""
    pr = Consult.objects.get(id=pid)
    ph = Consult.objects.filter(user=pr.user, fname=pr.fname, advice__isnull=False)

    if request.method == "POST":
        pr.advice = request.POST.get('advice', '')

        if 'pre_img' in request.FILES:
            pr.prescribe_img = request.FILES['pre_img']
            pr.save()

        pr.save()
        error = "send"

    d={'error': error, 'pr': pr, 'ph': ph}
    return render(request, 'diagnose.html', d)

def Past_report(request,pid):
    error = ""
    pr = Consult.objects.get(id=pid)
    docc = pr.doc
    doc = User.objects.get(username=docc)


    d={'error': error, 'pr': pr, 'doc':doc}
    return render(request, 'past_report.html', d)

def Report(request):
    error=""
    user = User.objects.get(id=request.user.id)
    pro = Consult.objects.filter(user=user).order_by('-advice')


    d={'error':error, 'pro':pro}
    return render(request, 'report.html', d)

def Read_Article(request,pid):
    error=""
    con = News_Article.objects.get(id=pid)
    recent = News_Article.objects.all().order_by('-date')[:3]
    related = News_Article.objects.filter(Q(category=con.category) & ~Q(id=pid))
    d = {'error': error, 'con':con, 'recent':recent, 'related':related}
    return render(request, 'read_article.html', d)

def Manage_requests(request):
    pro = Consult.objects.filter(advice__isnull=True).order_by('-date')
    d={'pro':pro}
    return render(request, 'manage_requests.html', d)

def delete_request(request,pid):
    dr = Consult.objects.get(id=pid)
    dr.delete()
    return redirect('manage_requests')

def See_all(request,cid):
    error = ""
    pid = str(cid)
    if pid == "news":
        error = "news"
    elif pid == "fitness":
        error = "fitness"
    elif pid == "travel":
        error = "travel"
    elif pid == "heat":
        error="HEWT"

    new = request.session['passnews']
    # Seperate Each news
    title = []
    desc = []
    img = []
    dat = []
    ur = []

    for i in range(len(new)):
        mynews = new[i]
        title.append(mynews['title'])
        desc.append(mynews['description'])
        img.append(mynews['urlToImage'])
        dat.append(mynews['publishedAt'])
        ur.append(mynews['url'])

        mylist = zip(title, desc, img, dat, ur)

    # Getting News Articles From Database
    fit = News_Article.objects.filter(category="Fitness").order_by("date")
    travel = News_Article.objects.filter(category="Travel").order_by("date")
    heat = News_Article.objects.filter(Q(category='Healthy Eating') | Q(category='Wellness'))

    # Passing Data to HTML Templates as Dictionary
    d = {'error': error, 'fit': fit, 'travel': travel, 'heat': heat, 'mylist': mylist}

    return render(request, 'see_all.html', d)

def Checkout(request):

    return render(request, 'checkout.html')

def Payments(request):
    from django.http import HttpResponse
    from dateutil.relativedelta import relativedelta

    user_id = User.objects.get(id=request.user.id)

    today = datetime.date.today()
    user = UserProfile.objects.get(user=user_id)
    prime_sub = user.prime_subscription


    if request.method == "POST":
            if 'tr_id' in request.POST:
                amount = request.POST['amount']
                email = request.POST['email']
                tr_id = request.POST['tr_id']

                if amount == '4.00': pkg = 1
                elif amount == '15.00': pkg = 6
                else: pkg = 12

                if prime_sub == None or today >= prime_sub:
                    prime_exp_date = today + relativedelta(months = pkg)


                elif prime_sub > today:
                        remaining_days = prime_sub - today
                        prime_pkg = today + relativedelta(months = pkg)
                        prime_exp_date = prime_pkg + datetime.timedelta(days = remaining_days.days)

                else:
                    print('Payment Error')

                Payment.objects.create(user=user, payment_date=today, email=email, amount=amount, tr_id=tr_id)
                user.prime_subscription = prime_exp_date
                user.save()
                print('Payment Success')

                return HttpResponse('success')
            else:
                return HttpResponse('Transaction Fail')
    else:
        print('No Requests')

    return redirect('checkout')

def Payment_history(request):
    pays = Payment.objects.all()
    uname = ""
    error = ""

    if request.user.is_authenticated:
        if request.user.is_staff and request.user.is_superuser == False:
            error = 'staff'

        elif request.user.is_superuser:
            print('Superuser')
        else:
            userr = User.objects.get(id=request.user.id)
            sign = UserProfile.objects.get(user=userr)
            print(sign)
            uname = Payment.objects.filter(user=sign)

    else:
        error = 'login'
    d = {'payment': pays, 'uname': uname, 'error': error}
    return render(request, 'payment_history.html',d)
