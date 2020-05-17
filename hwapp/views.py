import time

import pymssql
from django.contrib.auth import authenticate
from django.contrib.auth.views import logout
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

# Create your views here.
def index1(request):
    #return HttpResponse("Hello Django World!")
    return render_to_response('index.html')


def Goods(request):
    conn = pymssql.connect(server='localhost', user='sa', password='', database='my_db')
    cursor = conn.cursor(as_dict=True)
    cursor.execute("""select * from 商品""")
    row = cursor.fetchall()
    return render(request,'IO.html',{'Goods':row})

def AdminG(request):
    conn = pymssql.connect(server='localhost', user='sa', password='', database='my_db')
    cursor = conn.cursor(as_dict=True)
    cursor.execute("""select * from 商品""")
    row = cursor.fetchall()
    return render(request,'admin_func.html',{'Goods':row})

def CGoods(request):
    ID = ""
    NAME = ""
    OUTPUT = ""
    INPUT = ""
    MET = ""
    if request.method == 'POST':
        ID=request.POST.get('ID')
        NAME=request.POST.get('NAME')
        OUTPUT=request.POST.get("OUTPUT")
        INPUT=request.POST.get('INPUT')
        MET=request.POST.get('MET')
    print(ID,NAME,OUTPUT,INPUT,MET)
    conn = pymssql.connect(server='localhost', user='sa', password='', database='my_db')
    cursor = conn.cursor(as_dict=True)
    if MET == 'MOD':
        cursor.execute('''UPDATE 商品
        SET 商品名=%s,售价=%s,进价=%s
        WHERE 商品ID=%s;
        ''',(NAME,OUTPUT,INPUT,ID))
        cursor.execute("commit")
        print('修改')
    if MET == 'ADD':
        cursor.execute('''INSERT INTO 商品
        VALUES (%s,%s,%s,%s);
        ''',(ID,NAME,OUTPUT,INPUT))
        cursor.execute("commit")
        print('添加')
    if MET == 'SUB':
        cursor.execute('''DELETE FROM 商品
        WHERE 商品ID=%s;
        ''',(ID))
        cursor.execute("commit")
        print('删除')
    cursor.execute("""select * from 商品""")
    row = cursor.fetchall()
    return render(request,'Look.html',{'Goods':row})

def Look(request):
    return render(request,'Look.html')

def BUY(request):

    conn = pymssql.connect(server='localhost', user='sa', password='', database='my_db')
    cursor = conn.cursor()
    cursor.execute("""select 商品ID from 商品""")
    row = cursor.fetchall()
    NUMS = {}
    MET = ''
    if request.method == 'POST':
        for i in row:
            for j in i:
                NUMS[j]=request.POST.get(j,'None')
        MET=request.POST.get('MET','None')
    print(NUMS)
    times =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(times)
    cursor.execute('''INSERT INTO 订单(下单日期,支付方式)
    VALUES (%s,%s);
    ''', (times,MET))
    cursor.execute("commit")
    cursor.close()
    conn = pymssql.connect(server='localhost', user='sa', password='', database='my_db')
    cursor = conn.cursor()
    cursor.execute("""select * from 商品""")
    row = cursor.fetchall()
    return render(request, 'LookBuy.html')


def test(request):
    return render(request,'test.html')

def login(request):
    return render(request,'login.html')

def admin_login(request):
    return render(request,'admin_login.html')

def do_login(request):
    Username=""
    Password=""
    check_box = ""
    if request.method == 'POST':
        Username=request.POST.get('Username',None)
        Password=request.POST.get('Password',None)
        check_box=request.POST.get("check_box_list",None)
    print(Username,Password,check_box)
    conn = pymssql.connect(server='localhost', user='sa', password='', database='my_db')
    cursor = conn.cursor(as_dict=True)
    if check_box == None:
        cursor.execute('select * from 用户 where 用户名=%s AND  密码=%s ',(Username,Password))
        row=cursor.fetchone()
        if row:
            return render(request,'success.html',{'Username':Username})
        else:
            return render(request,'failurs.html',{'Username':Username})
    else:
        cursor.execute('select * from 管理员 where 管理员ID=%s AND  密码=%s ', (Username, Password))
        row = cursor.fetchone()
        if row:
            return render(request, 'admin_login.html', {'Username': Username})
        else:
            return render(request, 'failurs.html', {'Username': Username})


