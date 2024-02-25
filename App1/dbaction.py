from .models import dvx_v3,PQGSettings
from django.db.models import Case, Count, IntegerField, Value, When,F, Q
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from collections import Counter
from django.db.models.functions import ExtractDay, Cast,Concat
from django.db import models
from django.db import connection
from datetime import datetime, timedelta



#to make the app more flexible i use this function to get pqg data from data base exemple of the return ('HC1',number of static verification,number of static verification) 
def get_pqg_data():
    data = []

    pqg_settings = PQGSettings.objects.all()
    for setting in pqg_settings:
        data.append((setting.PQG, setting.Static, setting.Dynamic))

    return data

# this function returns the number of dvx_v3 defects detected 
def getdvx_v3countAction(responsabilite,from_date):
        sql = f"""  
     SELECT COUNT(*)
FROM dvx_v3
WHERE dvx_v3.rsp = "%{responsabilite}%"
AND dvx_v3.lieu_det NOT LIKE "%{responsabilite}%"
AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
AND CONCAT(vis, " ", dvx_v3.lieu_det, " ", dvx_v3.nature_det) NOT IN (
    SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
    FROM dvx_v3
    WHERE dvx_v3.rsp = "%{responsabilite}%"
        AND dvx_v3.lieu_det = "%{responsabilite}%"
        AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
); """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        nombreDefautsOutside = int(result[0])
        return nombreDefautsOutside

def getinsidedef(responsabilite,from_date):
    sql = f"""  
SELECT COUNT(*)
FROM dvx_v3
WHERE dvx_v3.rsp = "%{responsabilite}%"
AND dvx_v3.lieu_det NOT LIKE "%{responsabilite}%"
AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d')
AND CONCAT(vis, " ", dvx_v3.lieu_det, " ", dvx_v3.nature_det) NOT IN (
    SELECT CONCAT(vis, " ", dvx_v3.lieu_det, " ", dvx_v3.nature_det) AS defaut
    FROM dvx_v3
    WHERE dvx_v3.rsp like "%{responsabilite}%"
    AND dvx_v3.lieu_det like "%{responsabilite}%"
    AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d')
);
"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
    nombreDefautsOutside = int(result[0])
    return nombreDefautsOutside
#THIS FUNCTION RETURNS THE PERCENTAGE OF PQG EFFICIENCY ('HC1',00%)
def getresult(from_date,responsabilite_list):
    result_list = []
    for responsabilite in responsabilite_list:
        nombreDefautsOutside=getdvx_v3countAction(responsabilite[0],from_date)
        nombreDefautsInside = getinsidedef(responsabilite,from_date)
        total = 100 * nombreDefautsInside/(nombreDefautsOutside+nombreDefautsInside)
        result_list.append((responsabilite[0], total))
    return result_list
#THIS FUNCTION RETURN THE NUMBER OF DEFECTS DETECTED IN PQG AND dvx_v3



def defectsalreadydetected(liste, from_date):
    sum=0
    for item in liste :
        sql = f""" 
        SELECT COUNT(*)
        FROM dvx_v3
        WHERE dvx_v3.rsp = "%{item[0]}%"
        AND dvx_v3.lieu_det NOT LIKE "%{item[0]}%"
        AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
        AND CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) IN (
            SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
            FROM dvx_v3
            WHERE dvx_v3.resp = "%{item[0]}%"
                AND dvx_v3.lieu_det = "%{item[0]}%"
                AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
        )
        ;"""

        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        sum+=int(result[0])
    return sum
#THIS FUNCTION RETURN THE TABLE OF THE MOST DETECTABLE DEFETCS 
#NBR VARIABLE SINIFIE THE NUMBER OF THE LINES THAT THE QUERY WILL RETURNS
def getmostDetectabledefect(responsabilite_list,from_date,nbr):
    sql = f""" 
        SELECT count(dvx_v3.Vis) as count,
        concat(dvx_v3.loc_def,"/",dvx_v3.nature_det) AS defauts
        ,rsp
        from dvx_v3
        WHERE ("""
    for item in responsabilite_list:
        sql+=f" dvx_v3.rsp='{item[0]}' OR"
    if sql.endswith("OR"):
        sql = sql[:-3]

    sql+=f""" ) AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
        GROUP BY rsp,defauts
        ORDER BY COUNT DESC 
        LIMIT {nbr};"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return (result)
#THIS FUNCTION RETURN THE TOTAL NUMBER OF THE dvx_v3 IN ALL PQGS
def getOutsidDefects(liste,from_date) :
    sum=0
    for item in liste:
        nombreDefautsOutside=getdvx_v3countAction(item[0],from_date)
        sum += nombreDefautsOutside
    return sum
#function to make user super utilisateur by his id 
def make_user_superuser(username):
    try:
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.save()
        return True, f"User {username} is now a superuser."
    except User.DoesNotExist:
        return False, f"User {username} does not exist."

#A SUPP
def get_shift_counts(date, r):
    results_array = []

    main_query_sql = f"""
        SELECT tournee_de_detection, COUNT(vis) AS count_vis
        FROM dvx_v3
        WHERE vis IN (SELECT vis
        FROM dvx_v3
        WHERE dvx_v3.dateheure = STR_TO_DATE("{date}", '%Y-%m-%d ')
            AND rsp LIKE '%{r}%'
            AND  lieu_det NOT LIKE '%{r}%')
            AND lieu_det LIKE '%{r}%'
        GROUP BY tournee_de_detection
    """

    # Execute the queries using your database connection
    with connection.cursor() as cursor:
        cursor.execute(main_query_sql)
        results_queryset = cursor.fetchall()

    for item in results_queryset:
        results_array.append((item[1], item[0]))

    return results_array

#A modifier !!!!!!!
def getresultbyshift(from_date,result_list):
    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    responsabilite_list_by_shift=[]
    for r in result_list :
        nombreDefautsOutside=getdvx_v3countAction(r[0],from_date)
        sql=f"""
        SELECT COUNT(*) AS nombreDefautsInside
        FROM dvx_v3
        WHERE dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND rsp LIKE '%{r[0]}%'
            AND lieu_det LIKE '%{r[0]}%'
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        nombreDefautsInside=float(result[0])
        total=nombreDefautsInside+nombreDefautsOutside
        responsabilite = []  
        date = [("14:00", "22:00"), ("6:00", "14:00")]
        for count, h in enumerate(date):
            sql = f"""  
            SELECT COUNT(*) AS nombres
            FROM dvx_v3 
            JOIN NEO_EMON ON dvx_v3.Vis = NEO_EMON.VIS 
            WHERE 
            rsp LIKE "{r[0]}" AND
            dvx_v3.lieu_det not LIKE "{r[0]}"
            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND CONCAT(dvx_v3.vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) NOT IN (
                SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
                FROM dvx_v3
                WHERE dvx_v3.rsp = "{r[0]}"
                    AND dvx_v3.lieu_det = "{r[0]}"
                    AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
                )
            AND STR_TO_DATE(vis.EMON, '%m/%d/%Y %H:%i:%s') BETWEEN '{formatted_start_date} {h[0]}' AND '{formatted_start_date} {h[1]}';
            """
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
            sql = f"""  
            SELECT COUNT(*) AS nombres
            FROM dvx_v3 
            JOIN vis ON dvx_v3.Vis = vis.VIS 
            WHERE 
            responsabilite LIKE "{r[0]}" 
            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND dvx_v3.Lieu_de_detection  LIKE "{r[0]}"
            AND STR_TO_DATE(vis.EMON, '%m/%d/%Y %H:%i:%s') BETWEEN '{formatted_start_date} {h[0]}' AND '{formatted_start_date} {h[1]}';
            """
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result1 = cursor.fetchone()
            res=float(result1[0])+float(result[0])
            i = ""
            date=start_date.strftime('%m/%d')
            current_shift = get_shift_for_week(date)        
            if count == 0:
                i = current_shift[1]
            elif count == 1:
                i = current_shift[0]
            if total != 0 and i:
                t = (int(res) * float(r[1])) / total
                responsabilite.append((i, t))
            else:
                responsabilite.append((i, 0))
        
        sql = f"""  
            SELECT COUNT(*) AS nombres
            FROM dvx_v3 
            JOIN NEO_EMON ON dvx_v3.vis = NEO_EMON.VIS 
            WHERE 
            resp LIKE "{r[0]}" AND
            dvx_v3.lieu_det not LIKE "{r[0]}"
            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND CONCAT(dvx_v3.vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) NOT IN (
                SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
                FROM dvx_v3
                WHERE dvx_v3.resp = "{r[0]}"
                    AND dvx_v3.lieu_det = "{r[0]}"
                    AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
                )
            AND (STR_TO_DATE(vis.EMON, '%m/%d/%Y %H:%i:%s') BETWEEN '{formatted_start_date} 22:00' AND '{formatted_start_date} 23:59'
        OR STR_TO_DATE(vis.EMON, '%m/%d/%Y %H:%i:%s') BETWEEN '{formatted_start_date} 00:00' AND '{formatted_start_date} 06:00')
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            dvx_v3 = cursor.fetchone()
        sql = f"""  
        SELECT COUNT(*) AS nombres
            FROM dvx_v3 
            JOIN vis ON dvx_v3.Vis = vis.VIS 
            WHERE 
            rsp LIKE "{r[0]}" 
            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND dvx_v3.lieu_det  LIKE "{r[0]}"
            AND (STR_TO_DATE(vis.EMON, '%m/%d/%Y %H:%i:%s') BETWEEN '{formatted_start_date} 22:00' AND '{formatted_start_date} 23:59'
        OR STR_TO_DATE(vis.EMON, '%m/%d/%Y %H:%i:%s') BETWEEN '{formatted_start_date} 00:00' AND '{formatted_start_date} 06:00');
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            PQG = cursor.fetchone()
        res=float(PQG[0])+float(dvx_v3[0])
        i = "N"
        t=0
        if res != 0:
                t = (int(res) * float(r[1])) / total
        responsabilite.append((i, t))      
        responsabilite_list_by_shift.extend(responsabilite)
    return responsabilite_list_by_shift


def getdvx_v3countActionByShift(responsabilite,from_date,shift):
        sql = f"""  
        SELECT count(*)
        FROM dvx_v3
        WHERE dvx_v3.rsp = "{responsabilite}"
        AND equipe_resp like "{shift}"
        AND dvx_v3.lieu_det NOT LIKE "{responsabilite}"
        AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
        AND CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) NOT IN (
            SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
            FROM dvx_v3
            WHERE dvx_v3.rsp = "{responsabilite}"
                AND dvx_v3.lieu_det = "{responsabilite}"
                AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
        ) """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        nombreDefautsOutside = int(result[0])
        return nombreDefautsOutside
def get_PQG_by_shift(from_date, r, shift):
    query = f"""
        SELECT COUNT(*) AS PQGbyShift
        FROM dvx_v3
        WHERE dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND rsp LIKE '%{r[0]}%'
            AND lieu_det LIKE '%{r[0]}%'
            AND equipe_resp LIKE '%{shift}%'
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return 0
def get_nombre_defauts_inside(from_date, r):
    query = f"""
        SELECT COUNT(*) AS nombreDefautsInside
        FROM dvx_v3
        WHERE dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND rsp LIKE '%{r[0]}%'
            AND lieu_det LIKE '%{r[0]}%'
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return 0
def getresultbyshiftNrml(from_date,result_list):
    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    responsabilite_list_by_shift=[]
    for r in result_list :
        nombreDefautsOutside=getdvx_v3countAction(r[0],from_date)
        nombreDefautsInside =get_nombre_defauts_inside(from_date, r)
        total=nombreDefautsInside+nombreDefautsOutside
        responsabilite = []  
        for shift in "A","B","N":
            dvx_v3byShift=getdvx_v3countActionByShift(r[0],from_date,shift)
            PQGbyShift = get_PQG_by_shift(from_date, r, shift)
            res=float(PQGbyShift)+float(dvx_v3byShift)     
            if total != 0 :
                t = (float(res) * float(r[1])) / total
                responsabilite.append((shift, t))
            else:
                responsabilite.append((shift, 0))
        responsabilite_list_by_shift.extend(responsabilite)
    return responsabilite_list_by_shift

def userpsswdUpdate(request, user_id):
    old_password = request.POST.get('oldpswd')
    new_password = request.POST.get('newpswd')
    confirm_password = request.POST.get('conpswd')

    user = User.objects.get(username=user_id)

    if new_password != confirm_password:
        messages.error(request, "New password and confirm password do not match.")
    elif user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password updated successfully.")
    else:
        messages.error(request, "Invalid old password.")

    return redirect('setting')
def PQGDataUpdate(request,responsabilite_list):
    for i in responsabilite_list :
        try:
            if( int(i[1]) != int(request.GET.get(f"Static{i[0]}")) or int(i[2])!= int(request.GET.get(f"Dynamic{i[0]}"))) :
                PQGSettings.objects.filter(PQG=i[0]).update(Static=request.GET.get(f"Static{i[0]}"), Dynamic=request.GET.get(f"Dynamic{i[0]}"))
                messages.success(request, "PQG DATA updated successfully.")
                return redirect('setting')
        except:
            messages.error(request, "INVALIDE DATA TYPE")
            return redirect('setting')
        
def addPQG(request):
    newPQG=PQGSettings(PQG=request.GET.get("pqg").upper(),Static=request.GET.get("static"),Dynamic=request.GET.get("dynamic"))
    newPQG.save()
    messages.success(request, "PQG has been ADDED successfully.")
    return redirect('setting')
def deletePQG(request ,pqg):
    PQGSettings.objects.filter(PQG=pqg).delete()
    messages.success(request, "PQG has been DELETED successfully.")
    return redirect('setting')

#result of both inside and outside u can use the commented function to make the main charts take the data with the normal way
def get_inside_faults(from_date, r):
    query = f"""
        SELECT COUNT(*) AS insideFaults
        FROM dvx_v3
        WHERE rsp LIKE 'MON%'
            AND lieu_det LIKE '%{r[0]}%'
            AND rsp LIKE '%{r[0]}%'
            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return 0
def get_count_for_tournee(from_date, r, i):
    query = f"""
        SELECT COUNT(*) AS count_for_tournee
        FROM dvx_v3
        WHERE dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
            AND rsp LIKE '%{r[0]}%'
            AND equipe_det = {i}
            AND lieu_det LIKE '%{r[0]}%'
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return 0
def getTableData(from_date,responsabilite_list):
    tableData=[]
    for r in responsabilite_list:
        table=[]
        outsideFaults=getdvx_v3countAction(r[0],from_date)
        insideFaults=get_inside_faults(from_date, r)
        for i in "A","B","N","##":
            sql=f"""
                    SELECT COUNT(*) FROM dvx_v3 
                    WHERE dvx_v3.rsp = "{r[0]}"
                    AND dvx_v3.lieu_det not LIKE "{r[0]}"
                    AND equipe_resp like "{i}"
                    AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d ')
                    AND CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) not IN (
                        SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
                        FROM dvx_v3
                        WHERE dvx_v3.rsp = "{r[0]}"
                            AND dvx_v3.lieu_det = "{r[0]}"
                            AND dvx_v3.dateheure = STR_TO_DATE("{from_date}", '%Y-%m-%d '))
            """
            with connection.cursor() as cursor:
                cursor.execute(sql)
                x = cursor.fetchone()
            y =get_count_for_tournee(from_date, r, i)
            table.append((i,y,x))
        tableData.append((r[0],outsideFaults,insideFaults,table))
    return tableData

#

def process_date_string(date_str, date_format="%d/%m/%Y"):
    date_object = datetime.strptime(date_str, date_format)
    result_date = date_object - timedelta(days=14)
    return result_date.strftime('%Y-%m-%d'), date_object.strftime('%Y-%m-%d')



def getresult1(date,from_date,responsabilite_list):
    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    if date=="week":
        end_date = start_date - timedelta(days=7)
    if date=="twoWeek":
        end_date = start_date - timedelta(days=14)
    if date=="month":
     end_date = start_date - timedelta(days=30)
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    formatted_end_date = end_date.strftime('%Y-%m-%d')
    sql = f"""
    SELECT CONCAT(Month(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s')),"/",Day(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s'))) AS DAY,
    COUNT(*)  AS COUNT
    FROM dvx_v3 
    WHERE STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
    AND rsp LIKE '{responsabilite_list}%'
    AND lieu_det  like '{responsabilite_list}%'
    GROUP BY DAY
    ORDER BY DAY
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    sql = f"""
    SELECT CONCAT(Month(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s')),"/",Day(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s'))) AS DAY,
    COUNT(*)  AS COUNT
    FROM dvx_v3 
    WHERE STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
    AND rsp LIKE '{responsabilite_list}%'
    AND lieu_det  not like '{responsabilite_list}%'
    AND CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) not IN (
        SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
        FROM dvx_v3
        WHERE dvx_v3.rsp = "{responsabilite_list}"
            AND dvx_v3.lieu_det like "{responsabilite_list}"
            AND STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
    )
    GROUP BY DAY
    ORDER BY DAY
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result1 = cursor.fetchall()
    t3=[]
    for t1_entry, t2_entry in zip(result1, result):
        t1_date, t1_value = t1_entry
        t2_date, t2_value = t2_entry
        
        if t1_date == t2_date:
            t1_value = int(t1_value)
            t2_value = int(t2_value)
            
            if t2_value + t1_value != 0:
                percentage = (t2_value * 100) / (t2_value + t1_value)
                t3_entry = ( t1_date, percentage)
                t3.append(t3_entry)
            else:
                percentage = 100
                t3_entry = ( t1_date, percentage)
                t3.append(t3_entry)

    data_array=[]
    for row in t3 :
        data_array.append((row[0],row[1]))
    return data_array





def getcustomisedresultbyshift(date,from_date,pqgnbr,responsabilite_list,vehNbr):
    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    if date=="week":
        end_date = start_date - timedelta(days=7)
    if date=="twoWeek":
        end_date = start_date - timedelta(days=14)
    if date=="month":
     end_date = start_date - timedelta(days=30)
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    formatted_end_date = end_date.strftime('%Y-%m-%d')


    sql = f"""
    SELECT
        equipe_resp,
        CONCAT(Month(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s')),"/",Day(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s'))) AS DAY,
        COUNT(*)  AS COUNT
    FROM
        dvx_v3
    WHERE
        STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
        AND rsp LIKE '{responsabilite_list}%'
        AND dvx_v3.lieu_det NOT LIKE "{responsabilite_list}"
        AND CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) not IN (
        SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
        FROM dvx_v3
        WHERE dvx_v3.rsp = "{responsabilite_list}"
            AND dvx_v3.lieu_det like "{responsabilite_list}"
            AND STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
    )
    and equipe_resp <> "##"

    GROUP BY
        equipe_resp, DAY
    ORDER BY DAY;
    ;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    sql=f"""
        SELECT
            equipre_resp,
            CONCAT(Month(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s')),"/",Day(STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s'))) AS DAY,
            COUNT(*)  AS COUNT
        FROM
            dvx_v3
        WHERE
            STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
            and equipre_resp <> "##"
            AND rsp LIKE '{responsabilite_list}'
            AND dvx_v3.lieu_det LIKE "{responsabilite_list}"
        GROUP BY
            equipre_resp, DAY
        ORDER BY
            DAY;
        ;"""
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result1 = cursor.fetchall()

    t3=[]
    for t1_entry, t2_entry in zip(result1, result):
        t1_flag, t1_date, t1_value = t1_entry
        t2_flag, t2_date, t2_value = t2_entry
        
        if t1_flag == t2_flag and t1_date == t2_date:
            t1_value = int(t1_value)
            t2_value = int(t2_value)
            
            if t2_value + t1_value != 0:
                percentage = (t1_value * 100) / (t2_value + t1_value)
                t3_entry = (t1_flag, t1_date, percentage)
                t3.append(t3_entry)


    data_array=[]
    for i in "A","B","N","##":
        for row in t3 :
            if row[0]==i:
                data_array.append((row[0],(row[1],row[2])))

    return data_array

def getpersentageperdayandshift(pqgnbr,vehNbr,formatted_end_date,formatted_start_date,responsabilite_list,startH,endingH):
    sql = f"""
    SELECT  CONCAT(Month(STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s')),"/",DAY(STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s'))) AS DAY,
    COUNT(*)AS Count
    FROM dvx_v3
    JOIN vis ON dvx_v3.Vis = vis.VIS
    WHERE STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s')
    BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
    AND HOUR(STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s'))
    BETWEEN {startH} AND {endingH}
    AND rsp LIKE '{responsabilite_list}%'
    AND lieu_det LIKE "{responsabilite_list}"
    GROUP BY DAY
    ORDER BY DAY;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    sql = f"""
    SELECT  CONCAT(Month(STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s')),"/",DAY(STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s'))) AS DAY,
    COUNT(*)AS Count
    FROM dvx_v3
    JOIN vis ON dvx_v3.Vis = vis.VIS
    WHERE STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s')
    BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
    AND HOUR(STR_TO_DATE(Emon, '%m/%d/%Y %H:%i:%s'))
    BETWEEN {startH} AND {endingH}
    AND rsp LIKE '{responsabilite_list}%'
    AND lieu_det Not LIKE "{responsabilite_list}"
    AND CONCAT(dvx_v3.vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) not IN (
    SELECT CONCAT(vis, " ", dvx_v3.loc_def, " ", dvx_v3.nature_det) AS defaut
    FROM dvx_v3
    WHERE dvx_v3.rsp = "{responsabilite_list}"
        AND dvx_v3.lieu_det like "{responsabilite_list}"
        AND STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{formatted_end_date}' AND '{formatted_start_date}'
)
    GROUP BY DAY
    ORDER BY DAY;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result2 = cursor.fetchall()
    t3=[]


    for t1_entry, t2_entry in zip(result2, result):
        t1_date, t1_value = t1_entry
        t2_date, t2_value = t2_entry
        
        if t1_date == t2_date:
            t1_value = int(t1_value)
            t2_value = int(t2_value)
            
            if t2_value + t1_value != 0:
                percentage = (t2_value * 100) / (t2_value + t1_value)
                t3_entry = ( t1_date, percentage)
                t3.append(t3_entry)
    return t3

def getcustomisedresultbyshiftEmon(date, from_date, pqgnbr, responsabilite_list, vehNbr):
    try :
        start_date = datetime.strptime(from_date, '%d/%m/%Y')
        if date == "week":
            end_date = start_date - timedelta(days=7)
        elif date == "twoWeek":
            end_date = start_date - timedelta(days=14)
        elif date == "month":
            end_date = start_date - timedelta(days=30)
        else:
            raise ValueError("Invalid 'date' parameter. It should be 'week', 'twoWeek', or 'month'.")

        formatted_start_date = start_date.strftime('%Y-%m-%d')
        formatted_end_date = end_date.strftime('%Y-%m-%d')
        time_intervals = [("14", "21"), ("6", "13")]
        data_array = []

        for count, h in enumerate(time_intervals):
            result=getpersentageperdayandshift(pqgnbr,vehNbr,formatted_end_date,formatted_start_date,responsabilite_list,h[0],h[1])
            for row in result:
                i = ""
                current_shift = get_shift_for_week(row[0])               
                if count == 0:
                    i = current_shift[1]
                elif count == 1:
                    i = current_shift[0]
                data_array.append((i, (row[0], row[1])))


        result=getpersentageperdayandshift(pqgnbr,vehNbr,formatted_end_date,formatted_start_date,responsabilite_list,00,5)
        result2=getpersentageperdayandshift(pqgnbr,vehNbr,formatted_end_date,formatted_start_date,responsabilite_list,22,23)
        i = "N"
        for row in result:
            for row2 in result2:
                if row[0]==row2[0]:
                    #row[1]=float(row2[1])+float(row[1])
                    percentage=(float(row2[1])+float(row[1]))/2
            data_array.append((i, (row[0], percentage)))
    except Exception as e:
        data_array=[]
    return data_array

def getmostDetectabledefectbyPQG(date,pqg,today):
    start_date = datetime.strptime(today, '%d/%m/%Y')
    if date == "week":
        end_date = start_date - timedelta(days=7)
    elif date == "twoWeek":
        end_date = start_date - timedelta(days=14)
    elif date == "month":
        end_date = start_date - timedelta(days=30)
    else:
        raise ValueError("Invalid 'date' parameter. It should be 'week', 'twoWeek', or 'month'.")
    sql = f""" 
        SELECT count(dvx_v3.Vis) as count,
        concat(dvx_v3.loc_def,"/",dvx_v3.nature_det) AS defauts
        ,rsp
        from dvx_v3
        WHERE dvx_v3.rsp='{pqg}'  
        AND STR_TO_DATE(dateheure, '%d/%m/%Y %H:%i:%s') BETWEEN '{end_date}' AND '{start_date}'
        GROUP BY rsp,defauts
        HAVING count > 9
        ORDER BY COUNT DESC ;
"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return (result)
    
    
def get_shift_for_week(target_date):
    import datetime
    current_year=datetime.datetime.now().year
    new_target_date = f"{target_date}/{current_year}"
    target_date = datetime.datetime.strptime(new_target_date, "%m/%d/%Y")
    start_date = datetime.datetime.strptime("07/24/2023", "%m/%d/%Y")
    shifts = ["B", "A"]
    weeks_diff = (target_date - start_date).days // 7
    shift_index = weeks_diff % len(shifts)
    current_shift=[]
    current_shift.append(shifts[shift_index])
    if current_shift[0] =="A":
        current_shift.append("B")
    else:
        current_shift.append("A")

**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
****************************************************************************************************************************************************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
****************************************************************************************************************************************************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
****************************************************************************************************************************************************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
***************************************************************************************************************************************
*************************************************************************************************************************************
**************************************************************************************************************************************
**************************************************************************************************************************************
    return current_shift
    """
