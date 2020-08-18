from django.shortcuts import render,redirect
from .models import UserInfo
from django.http import HttpResponseRedirect


# Create your views here.


def login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        try:
            user = UserInfo.objects.get(username=username)
            if user != '':
                if password == user.password:
                    if user.pow == '0':
                        request.session['userid'] = user.username
                        return redirect('/userlist/')
                    if user.pow == '4':
                        request.session['userid'] = user.username
                        return redirect('/matchlist/')
                    else:
                        request.session['userid'] = user.username
                        return redirect('/search/?username='+user.username)
        except Exception as e:
            return render(request, 'login.html', {'error': '账号错误'})
    return render(request, 'login.html')


def logon(request):
    if request.method == 'POST':
        user = request.POST
        username = user['user_username']
        password = user['user_password']
        type = user['user_pow']
        if type == '管理员':
            pow = '4'
        elif type == '普通用户':
            pow = '1'
        elif type == '会员':
            pow = '2'
        elif type == 'VIP会员':
            pow = '3'
        UserInfo.objects.create(username=username,password=password,pow=pow)
        return redirect('/logon/')
    return render(request, 'logon.html')


def logout(request):
    request.session.flush()
    return redirect('/')



