from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone
from .forms import SignUpForm,SignInForm
from django.db import models,connection
from .dbaction import getcustomisedresultbyshiftEmon,getresultbyshiftNrml,getOutsidDefects,defectsalreadydetected,getmostDetectabledefect
from .dbaction import getresult1,getcustomisedresultbyshift,getmostDetectabledefectbyPQG,getTableData,make_user_superuser
from .dbaction import getresult,getresultbyshift,get_pqg_data,userpsswdUpdate,PQGDataUpdate,deletePQG,addPQG
from .models import Dvx,GlobalValue
from datetime import datetime, timedelta
from django.contrib import messages

today_nrml = timezone.now().date()
today = today_nrml.strftime('%d/%m/%Y')
responsabilite_list = get_pqg_data()
yesterday_datetime = today_nrml - timedelta(days=14)
yesterday = yesterday_datetime.strftime("%d/%m/%Y")
print(today,yesterday)



def signIn(request):
    if request.user.is_authenticated:
        return redirect('menu')

    error_message = None

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('menu')
            else:
                error_message = 'Incorrect username or password.'
    else:
        form = SignInForm()

    return render(request, 'signIn.html', {'form': form, 'error_message': error_message})



def indexPage(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu')
    else:
        form = SignUpForm()

    return render(request, 'index.html', {'form': form})

def menuPage(request):
    user = request.user
    fName = user.first_name
    lName = user.last_name
    context={
        'fName': fName,
        'lName': lName,
    }
    return render(request, 'menu.html',context)
    
def get_inside_faults(from_date):
    query = f"""
        SELECT COUNT(*) AS insideFaults
        FROM dvx_v3
        WHERE rsp LIKE 'MON%'
            AND lieu_det LIKE CONCAT('%', responsabilite, '%')
            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return 0
    
def get_cars_number(from_date):
    query = f"""
        SELECT COUNT(*) AS veh
        FROM NEO_EMON
        WHERE dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return 0
    

def mainPage(request):
    responsabilite_list = get_pqg_data()
    checkedCarsNumber = get_cars_number(today)
    if not request.user.is_authenticated:
        return redirect('indexPage')


    
    user = request.user
    fName = user.first_name
    lName = user.last_name
    state=True
    result_list = getresult(today,responsabilite_list)
    if request.method == "GET" and request.GET.get('way') :
        if request.GET.get('way') =="nData":
            responsabilite_list_by_shift=getresultbyshiftNrml(today,result_list)
            state=False
        else :
            responsabilite_list_by_shift=getresultbyshift(today,result_list)        
    else:
        responsabilite_list_by_shift=getresultbyshift(today,result_list)
    outsideFaults=getOutsidDefects(responsabilite_list,today)
    nbrofmissedpqg=defectsalreadydetected(responsabilite_list,today)
    insideFaults=get_inside_faults(today)
    mostDetectabledefect=getmostDetectabledefect(responsabilite_list,today,8)
    context = {
        'state':state,
        'from_date':today,
        'mostDetectabledefect':mostDetectabledefect,
        'nbrofmissedpqg':nbrofmissedpqg,
        'checkedCarsNumbery':checkedCarsNumber,
        'objectif' : get_objectif_value(),
        'insideFaults' : insideFaults,
        'outsideFaults' : outsideFaults,
        'checkedCarsNumber':checkedCarsNumber,
        'result_list': result_list,
        'fName': fName,
        'lName': lName,
        "responsabilite_list_by_shift": responsabilite_list_by_shift,
            }
    return render(request, 'main.html', context)

def statisticPage2(request):
    responsabilite_list = get_pqg_data()

    if not request.user.is_authenticated:
        return redirect('indexPage')
    user = request.user
    fName = user.first_name
    lName = user.last_name
    tableData=getTableData(today,responsabilite_list)
    #tableData2=getTableData(from_date,responsabilite_list)
    mostDetectabledefect=getmostDetectabledefect(responsabilite_list,today,40)
    context = {
        'mostDetectabledefect':mostDetectabledefect,
        'data':tableData,
        'fName': fName,
        'lName': lName,}
    return render(request, 'statistic2.html', context)

def statisticPage(request):
    responsabilite_list = get_pqg_data()
    checkedCarsNumber=get_cars_number(yesterday)
    if not request.user.is_authenticated:
        return redirect('indexPage')
    user = request.user
    fName = user.first_name
    lName = user.last_name
        

    state=True
    result_list = getresult(yesterday,responsabilite_list)
    if request.method == "GET" and request.GET.get('way') :
        if request.GET.get('way') =="nData":
            state=False
            responsabilite_list_by_shift=getresultbyshiftNrml(yesterday,result_list)
        else :
            responsabilite_list_by_shift=getresultbyshift(yesterday,result_list)        
    else:
        responsabilite_list_by_shift=getresultbyshift(yesterday,result_list) 
    outsideFaults=getOutsidDefects(responsabilite_list,yesterday)
    nbrofmissedpqg=defectsalreadydetected(responsabilite_list,yesterday)
    insideFaults=get_inside_faults(yesterday)
    mostDetectabledefect=getmostDetectabledefect(responsabilite_list,yesterday,8)
    context = {
        'state':state,
        'from_date':yesterday,
        'mostDetectabledefect':mostDetectabledefect,
        'nbrofmissedpqg':nbrofmissedpqg,
        'checkedCarsNumbery':checkedCarsNumber,
        'objectif' : get_objectif_value(),
        'insideFaults' : insideFaults,
        'outsideFaults' : outsideFaults,
        'checkedCarsNumber':checkedCarsNumber,
        'result_list': result_list,
        'fName': fName,
        'lName': lName,
        "responsabilite_list_by_shift": responsabilite_list_by_shift,
    }

    return render(request, 'statistic.html', context)

def settingPage(request):
    responsabilite_list = get_pqg_data()

    if not request.user.is_authenticated:
        return redirect('indexPage')

    user = request.user
    fName = user.first_name
    lName = user.last_name
    user_id = user.username
    
    if request.POST.get("id") and request.method == 'POST':
        userpsswdUpdate(request, user_id)
        

    state=False
    if request.user.is_superuser:
        state=True
        if request.POST.get("Static"+responsabilite_list[0][0]) and request.method == 'POST':
            PQGDataUpdate(request, responsabilite_list)
            return redirect('setting')
        elif request.POST.get("pqg") and request.method == 'POST':
            addPQG(request)
            return redirect('setting')
        elif request.POST.get("username") and request.method == 'POST':
            pswd=request.POST.get("pswd")
            if user.check_password(pswd):
                messages.success(request, f"L'Utilisateur {request.POST.get('username')} est maintenant admin.")
                make_user_superuser(request.POST.get("username"))    
            else:
                messages.error(request, "Invalid old password.")
            return redirect('setting')
        elif request.POST.get("obj") and request.method == 'POST':
            new_objectif = request.POST.get("obj")
            pswd = request.POST.get("pswd")

            if user.check_password(pswd):
                try:
                    global_value_instance = GlobalValue.objects.first()
                    global_value_instance.objectif = new_objectif
                    global_value_instance.save()
                    messages.success(request, "L'objectif a été modifié.")
                except GlobalValue.DoesNotExist:
                    messages.error(request, "Global value not found.")
            else:
                messages.error(request, "Invalid old password.")
            return redirect('setting')
    context = {
    'objectif' : get_objectif_value(),
    'fName': fName,
    'lName': lName,
    'id': user_id,
    'items': responsabilite_list, 
    'state':state
    }
    return render(request, 'settingPage.html', context)

def get_objectif_value():
    try:
        global_value_instance = GlobalValue.objects.first()
        return global_value_instance.objectif
    except GlobalValue.DoesNotExist:
        return None


def statisticPage3(request):
    responsabilite_list = get_pqg_data()
    if not request.user.is_authenticated:
        return redirect('indexPage')
    user = request.user
    fName = user.first_name
    lName = user.last_name
    result=[] 
    result1=[]
    pqg=False
    date=False
    dataway=False
    mostDetectabledefect=None
    if request.method == "GET" and request.GET.get('pqg') and request.GET.get('date'):
        date = request.GET.get('date')
        pqg = request.GET.get('pqg')
        for item in responsabilite_list :
            if item[0] == pqg :
                pqgnbr =item[1]+item[2]
        result=getresult1(date,today,pqg)
        if request.GET.get('dataway')=="" or request.GET.get('dataway')=="nData":
            result1=getcustomisedresultbyshift(date,today,pqgnbr,pqg,600)
            dataway="nData"
        elif request.GET.get('dataway')=="Emon":
            dataway="Emon"
            result1=getcustomisedresultbyshiftEmon(date,today,pqgnbr,pqg,600)
        mostDetectabledefect=getmostDetectabledefectbyPQG(date,pqg,today)
            
    context = {
        'mostDetectabledefect':mostDetectabledefect,
        'fName': fName,
        'lName': lName,
        'objectif' : get_objectif_value(),
        'items': responsabilite_list,
        'result' :result,
        'result1' :result1,
        "pqg" :pqg,
        "date":date,
        "dataway":dataway

    }
    return render(request, 'statistic3.html', context)


def logOut(request):
    logout(request)
    return redirect("indexPage")

def pqgSetting(request, pqg):
    deletePQG(request,pqg)
    return redirect('setting')
    