import operator
import time

from django.shortcuts import render,redirect
from .models import MatchInfo,AthleteInfo
from django.db.models import Q, F
from user.models import UserInfo
from urllib.parse import quote
import urllib.request
import string
import requests
from collections import Counter
import json
import datetime
# Create your views here.


def search(request):
    # if request.method == 'GET':
    #     mlist = []
    #     name = "马来西亚"
    #     url = 'https://creator.zoho.com.cn/api/json/badminton/view/view_ShiPin?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_ShiPinMingCheng.Contains("' + name + '"))'
    #     # url = 'https://creator.zoho.com.cn/api/json/badminton/view/view_SaiShi?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi'
    #     # print(url)
    #     data = requests.get(url).text
    #     data = data.replace(' ','').split('0=')[1][:-1]
    #     data = json.loads(data)
    #     # print(data)
    #     content = data['form_ShiPin']
    #     for i in content:
    #         print(i)
    #     #     img_url = i['Image_LOGO'].split('"')
    #     #     if len(img_url) > 1:
    #     #         img1 = img_url[1]
    #     #         # print(img1)
    #     #         img2 = img1.split('download/')
    #     #         # print(img2)
    #     #         img = 'https://creator.zoho.com.cn/file' + img2[0] + 'download?filepath=/' + img2[1]
    #     #         # print(img)
    #     #         name = i['Single_Line_SaiShiZhongWenMing'].split('-')[0]
    #     #         year = i['Single_Line_SaiShiZhongWenMing'].split('-')[1]
    #     #         print(name,year)
    #     #         # data = {
    #     #         #     'name': i['Single_Line_SaiShiZhongWenMing'].split('-')[0],
    #     #         #     'year': i['Single_Line_SaiShiZhongWenMing'].split('-')[0],
    #     #         #     'img': img,
    #     #         #     'start_time': i['Date_field_KaiShiRiQi'],
    #     #         #     'end_time': i['Date_field_JieShuRiQi']
    #     #         # }
    #     #         # mlist.append(data)
    #     # # print(mlist)
    if request.method == 'POST':
        listcon = []
        list1 = []
        list2 = []
        ln = []
        data = request.POST
        content = data['content'].split(" ")
        if content[0] == '':
            return redirect('/')
        else:
            for i in content:
                # print(i)
                if i.encode('UTF-8').isalpha() == True:
                    ln.append(i)
                else:
                    listcon.append(i)
            a = ' '.join(ln)
            # print(a)
            if len(a) != 0:
                name_url = 'https://creator.zoho.com.cn/api/json/badminton/view/view_YunDongYuan?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_YingWenMing==("' + a + '"))'
                data = requests.get(name_url).text
                # print(data)
                data = data.replace(' ', '').split('0=')[1][:-1]
                data = json.loads(data)
            # print(data)
            # user = AthleteInfo.objects.filter(english_name=a)
                for i in data['form_YunDongYuan']:
                    listcon.append(i['Single_Line_ZhongWenMing'])
            for i in listcon:
                # print(i)
                # match = MatchInfo.objects.filter(Q(match_name__icontains=i) | Q(player_a__icontains=i)
                #                                  | Q(player_b__icontains=i) | Q(match_round=i))
                url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_ShiPin_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_ShiPinMingCheng.Contains("' + i + '"))'
                data = requests.get(url).text
                data = data.replace(' ', '').split('0=')[1][:-1]
                data = json.loads(data)
                for j in data['form_ShiPin']:
                    # print(type(str(j)))
                    list1.append(str(j))
            # l1 = dict(Counter(list1))
            # list2 = [key for key, value in l1.items() if value > 1]
            # print(list1)
            if len(listcon) == 1:
                for i in list1:
                    # print(i)
                    # print(json.loads(i))
                    if i not in list2:
                        list2.append(i)
            if len(listcon) == 2:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 3 > value > 1]
            if len(listcon) == 3:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 4 > value > 2]
            if len(listcon) == 4:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 5 > value > 3]
            if len(listcon) == 5:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 6 > value > 4]
            data = {}
            listb = []
            # print(list2)
            for i in list2:
                # print(i,type(i))
                i = eval(i)
                # name_a1 = i['Query_YunDongYuan_A1']
                # name_a2 = i['Query_YunDongYuan_A2']
                # name_b1 = i['Query_YunDongYuan_B1']
                # name_b2 = i['Query_YunDongYuan_B2']
                result = i['Dropdown_BiSaiJieGuo']
                score = i['Single_Line_BiFen']
                match_date = i['Date_field_BiSaiRiQi']
                n = i['Single_Line_ShiPinMingCheng'].split('-')
                # print(n,len(n))
                if int(n[5]) != 9:
                    icon = 'https://s3.cn-northwest-1.amazonaws.com.cn/video.hbang.com.cn/' + n[0] + '/' + n[1] + '-' + \
                           n[2] + '-' + n[3] + '/' + n[4] + '/' + i['Single_Line_ShiPinMingCheng'] + '.mp4'
                    # print(icon)
                    html = requests.head(icon)
                    re = html.status_code
                    if len(n) == 9:
                        name_a1 = n[6]
                        name_a2 = ''
                        name_b1 = n[8]
                        name_b2 = ''
                    if len(n) == 11:
                        name_a1 = n[6]
                        name_a2 = '~' + n[7]
                        name_b1 = n[9]
                        name_b2 = '~' + n[10]
                    data = {
                        'icon': icon,
                        'name_a1': name_a1,
                        'name_a2': name_a2,
                        'name_b1': name_b1,
                        'name_b2': name_b2,
                        'result': result,
                        'score': score,
                        'date': match_date
                    }
                    # print(data)
                    if re == 200:
                        listb.append(data)
            sorted(listb, key=lambda keys: data['date'])
            listb.reverse()
            return render(request, 'list.html', {'listb': listb})

    return render(request, 'search.html')


def project(request):
    if request.method == 'GET':
        pname = request.GET.get('name')
        year = request.GET.get('year')
    if request.method == 'POST':
        listcon = []
        list1 = []
        list2 = []
        ln = []
        data = request.POST
        content = data['content'].split(" ")
        if content[0] == '':
            return redirect('/')
        else:
            for i in content:
                # print(i)
                if i.encode('UTF-8').isalpha() == True:
                    ln.append(i)
                else:
                    listcon.append(i)
            a = ' '.join(ln)
            if len(a) != 0:
                name_url = 'https://creator.zoho.com.cn/api/json/badminton/view/view_YunDongYuan?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_YingWenMing==("' + a + '"))'
                data = requests.get(name_url).text
                # print(data)
                data = data.replace(' ', '').split('0=')[1][:-1]
                data = json.loads(data)
                # print(data)
                # user = AthleteInfo.objects.filter(english_name=a)
                for i in data['form_YunDongYuan']:
                    listcon.append(i['Single_Line_ZhongWenMing'])
            for i in listcon:
                # print(i)
                # match = MatchInfo.objects.filter(Q(match_name__icontains=i) | Q(player_a__icontains=i)
                #                                  | Q(player_b__icontains=i) | Q(match_round=i))
                url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_ShiPin_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_ShiPinMingCheng.Contains("' + i + '"))'
                data = requests.get(url).text
                data = data.replace(' ', '').split('0=')[1][:-1]
                data = json.loads(data)
                for j in data['form_ShiPin']:
                    # print(type(str(j)))
                    list1.append(str(j))
            # l1 = dict(Counter(list1))
            # list2 = [key for key, value in l1.items() if value > 1]
            # print(list1)
            if len(listcon) == 1:
                for i in list1:
                    # print(i)
                    # print(json.loads(i))
                    if i not in list2:
                        list2.append(i)
            if len(listcon) == 2:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 3 > value > 1]
            if len(listcon) == 3:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 4 > value > 2]
            if len(listcon) == 4:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 5 > value > 3]
            if len(listcon) == 5:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 6 > value > 4]
            data = {}
            listb = []
            # print(list2)
            for i in list2:
                # print(i,type(i))
                i = eval(i)
                # name_a1 = i['Query_YunDongYuan_A1']
                # name_a2 = i['Query_YunDongYuan_A2']
                # name_b1 = i['Query_YunDongYuan_B1']
                # name_b2 = i['Query_YunDongYuan_B2']
                result = i['Dropdown_BiSaiJieGuo']
                score = i['Single_Line_BiFen']
                match_date = i['Date_field_BiSaiRiQi']
                n = i['Single_Line_ShiPinMingCheng'].split('-')
                # print(n,len(n))
                if int(n[5]) != 9:
                    icon = 'https://s3.cn-northwest-1.amazonaws.com.cn/video.hbang.com.cn/' + n[0] + '/' + n[1] + '-' + \
                           n[2] + '-' + n[3] + '/' + n[4] + '/' + i['Single_Line_ShiPinMingCheng'] + '.mp4'
                    # print(icon)
                    html = requests.head(icon)
                    re = html.status_code
                    if len(n) == 9:
                        name_a1 = n[6]
                        name_a2 = ''
                        name_b1 = n[8]
                        name_b2 = ''
                    if len(n) == 11:
                        name_a1 = n[6]
                        name_a2 = '~' + n[7]
                        name_b1 = n[9]
                        name_b2 = '~' + n[10]
                    data = {
                        'icon': icon,
                        'name_a1': name_a1,
                        'name_a2': name_a2,
                        'name_b1': name_b1,
                        'name_b2': name_b2,
                        'result': result,
                        'score': score,
                        'date': match_date
                    }
                    # print(data)
                    if re == 200:
                        listb.append(data)
            sorted(listb, key=lambda keys: data['date'])
            listb.reverse()
            return render(request, 'list.html', {'listb': listb})

    return render(request, 'project.html', {'name':pname, 'year':year})


def list(request):
    if request.method == 'GET':
        list1 = []
        mlist = []
        name = request.GET.get('name')
        year = request.GET.get('year')
        pproject = request.GET.get('project')
        # name = "马来西亚"
        # pproject = '男单'
        url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_ShiPin_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_ShiPinMingCheng.Contains("' + name + '"))'
        # url = 'https://creator.zoho.com.cn/api/json/badminton/view/view_ShiPin?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_ShiPinMingCheng.Contains("马来西亚"))'

        print(url)
        data = requests.get(url).text
        # print(data)
        data = data.replace(' ', '').split('0=')[1][:-1]
        data = json.loads(data)
        # print(data)
        content = data['form_ShiPin']
        for i in content:
            list1.append(i)
        list2 = list1
        data = {}
        listb = []
        for i in list2:
            # print(i,type(i))
            i = eval(str(i))
            # name_a1 = i['Query_YunDongYuan_A1']
            # name_a2 = i['Query_YunDongYuan_A2']
            # name_b1 = i['Query_YunDongYuan_B1']
            # name_b2 = i['Query_YunDongYuan_B2']
            result = i['Dropdown_BiSaiJieGuo']
            score = i['Single_Line_BiFen']
            match_date = i['Date_field_BiSaiRiQi']
            n = i['Single_Line_ShiPinMingCheng'].split('-')
            # print(n)
            if int(n[5]) != 9 and n[4] == pproject:
                icon = 'https://s3.cn-northwest-1.amazonaws.com.cn/video.hbang.com.cn/' + n[0] + '/' + n[1] + '-' + \
                       n[2] + '-' + n[3] + '/' + n[4] + '/' + i['Single_Line_ShiPinMingCheng'] + '.mp4'
                # print(icon)
                html = requests.head(icon)
                re = html.status_code
                if len(n) == 9:
                    name_a1 = n[6]
                    name_a2 = ''
                    name_b1 = n[8]
                    name_b2 = ''
                if len(n) == 11:
                    name_a1 = n[6]
                    name_a2 = '~' + n[7]
                    name_b1 = n[9]
                    name_b2 = '~' + n[10]
                data = {
                    'icon': icon,
                    'name_a1': name_a1,
                    'name_a2': name_a2,
                    'name_b1': name_b1,
                    'name_b2': name_b2,
                    'result': result,
                    'score': score,
                    'date': match_date
                }
                if re == 200:
                    listb.append(data)
        # sorted(listb, key=lambda keys: data['date'])
        listb.reverse()
        # print(listb)
        return render(request, 'list.html', {'listb': listb})
    if request.method == 'POST':
        listcon = []
        list1 = []
        list2 = []
        ln = []
        data = request.POST
        content = data['content'].split(" ")
        if content[0] == '':
            return redirect('/')
        else:
            for i in content:
                # print(i)
                if i.encode('UTF-8').isalpha() == True:
                    ln.append(i)
                else:
                    listcon.append(i)
            a = ' '.join(ln)
            if len(a) != 0:
                name_url = 'https://creator.zoho.com.cn/api/json/badminton/view/view_YunDongYuan?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_YingWenMing==("' + a + '"))'
                data = requests.get(name_url).text
                # print(data)
                data = data.replace(' ', '').split('0=')[1][:-1]
                data = json.loads(data)
                # print(data)
                # user = AthleteInfo.objects.filter(english_name=a)
                for i in data['form_YunDongYuan']:
                    listcon.append(i['Single_Line_ZhongWenMing'])
            for i in listcon:
                # print(i)
                # match = MatchInfo.objects.filter(Q(match_name__icontains=i) | Q(player_a__icontains=i)
                #                                  | Q(player_b__icontains=i) | Q(match_round=i))
                url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_ShiPin_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Single_Line_ShiPinMingCheng.Contains("' + i + '"))'
                data = requests.get(url).text
                data = data.replace(' ', '').split('0=')[1][:-1]
                data = json.loads(data)
                for j in data['form_ShiPin']:
                    # print(type(str(j)))
                    list1.append(str(j))
            # l1 = dict(Counter(list1))
            # list2 = [key for key, value in l1.items() if value > 1]
            # print(list1)
            if len(listcon) == 1:
                for i in list1:
                    # print(i)
                    # print(json.loads(i))
                    if i not in list2:
                        list2.append(i)
            if len(listcon) == 2:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 3 > value > 1]
            if len(listcon) == 3:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 4 > value > 2]
            if len(listcon) == 4:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 5 > value > 3]
            if len(listcon) == 5:
                l1 = dict(Counter(list1))
                list2 = [key for key, value in l1.items() if 6 > value > 4]
            data = {}
            listb = []
            # print(list2)
            for i in list2:
                # print(i,type(i))
                i = eval(i)
                # name_a1 = i['Query_YunDongYuan_A1']
                # name_a2 = i['Query_YunDongYuan_A2']
                # name_b1 = i['Query_YunDongYuan_B1']
                # name_b2 = i['Query_YunDongYuan_B2']
                result = i['Dropdown_BiSaiJieGuo']
                score = i['Single_Line_BiFen']
                match_date = i['Date_field_BiSaiRiQi']
                n = i['Single_Line_ShiPinMingCheng'].split('-')
                # print(n,len(n))
                if int(n[5]) != 9:
                    icon = 'https://s3.cn-northwest-1.amazonaws.com.cn/video.hbang.com.cn/' + n[0] + '/' + n[1] + '-' + \
                           n[2] + '-' + n[3] + '/' + n[4] + '/' + i['Single_Line_ShiPinMingCheng'] + '.mp4'
                    # print(icon)
                    html = requests.head(icon)
                    re = html.status_code
                    if len(n) == 9:
                        name_a1 = n[6]
                        name_a2 = ''
                        name_b1 = n[8]
                        name_b2 = ''
                    if len(n) == 11:
                        name_a1 = n[6]
                        name_a2 = '~' + n[7]
                        name_b1 = n[9]
                        name_b2 = '~' + n[10]
                    data = {
                        'icon': icon,
                        'name_a1': name_a1,
                        'name_a2': name_a2,
                        'name_b1': name_b1,
                        'name_b2': name_b2,
                        'result': result,
                        'score': score,
                        'date': match_date
                    }
                    # print(data)
                    if re == 200:
                        listb.append(data)
            sorted(listb, key=lambda keys: data['date'])
            listb.reverse()
            return render(request, 'list.html', {'listb': listb})
    return render(request,'list.html')
#
#
# def search(request):
#     if request.method == 'GET':
#         list1 = []
#         try:
#             username = request.session['userid']
#         except Exception as e:
#             username = '1'
#         user = UserInfo.objects.get(username=username)
#         list2 = Match.objects.all()
#         data = {}
#         mli = []
#         if user.pow == '1':
#             for i in list2:
#                 now = datetime.date.today() - datetime.timedelta(days=1)
#                 old = datetime.datetime.strptime(i.start_time, '%Y-%m-%d').date()
#                 if old < now:
#                     data = {
#                         'name': i.name,
#                         'img': i.img,
#                         'start_time': i.start_time,
#                         'end_time': i.end_time,
#                     }
#                     mli.append(data)
#         else:
#             for i in list2:
#                 data = {
#                     'name': i.name,
#                     'img': i.img,
#                     'start_time': i.start_time,
#                     'end_time': i.end_time,
#                 }
#                 mli.append(data)
#         ll = []
#         n = len(mli)
#         for i in range(n):
#             for j in range(n-i-1):
#                 if datetime.datetime.strptime(mli[j]['start_time'], '%Y-%m-%d').date() < datetime.datetime.strptime(mli[j+1]['start_time'], '%Y-%m-%d').date():
#                     mli[j], mli[j+1] = mli[j+1], mli[j]
#
#     if request.method == 'POST':
#         listcon = []
#         list1 = []
#         list2 = []
#         data = request.POST
#         username = data['username']
#         if username == '':
#             username = '1'
#         user = UserInfo.objects.get(username=username)
#         content = data['content'].split(" ")
#
#         if content[0] == '':
#             return redirect('/')
#         else:
#             for i in content:
#                 listcon.append(i)
#             for i in listcon:
#                 match = MatchInfo.objects.filter(Q(rotation=i) | Q(name_a__icontains=i) | Q(name_b__icontains=i)
#                                                  | Q(match__icontains=i) | Q(project__icontains=i))
#                 for j in match:
#                     list1.append(j)
#             # l1 = dict(Counter(list1))
#             # list2 = [key for key, value in l1.items() if value > 1]
#             for i in list1:
#                 if i not in list2:
#                     list2.append(i)
#             if len(listcon) > 1:
#                 l1 = dict(Counter(list1))
#                 list2 = [key for key, value in l1.items() if value > 1]
#             data = {}
#             listb = []
#             if user.pow == '1':
#                 for i in list2:
#                     now = datetime.date.today() - datetime.timedelta(days=1)
#                     old = i.date
#                     if old < now:
#                         data ={
#                             'icon' : i.icon,
#                             'name1' : i.name_a,
#                             'name2' : i.name_b,
#                             'rotation' : i.rotation,
#                             'score1' : i.score1,
#                             'score2' : i.score2,
#                             'game_score' : i.game_score,
#                             'match' : i.match,
#                             'date' : i.date,
#                         }
#                         listb.append(data)
#             else:
#                 for i in list2:
#                     data = {
#                         'icon': i.icon,
#                         'name1': i.name_a,
#                         'name2': i.name_b,
#                         'rotation': i.rotation,
#                         'score1': i.score1,
#                         'score2': i.score2,
#                         'game_score': i.game_score,
#                         'match': i.match,
#                         'date': i.date,
#                     }
#                     listb.append(data)
#             sorted(listb, key=lambda keys:data['date'])
#             listb.reverse()
#             return render(request, 'list.html', {'listb':listb})
#
#     return render(request, 'search.html', {'mlist': mli})
#
#
# def input(request):
#     if request.method == 'POST':
#         data = request.POST
#         MatchInfo.objects.create(
#             name_a=data['name_a'],
#             name_b=data['name_b'],
#             project=data['project'],
#             icon=data['icon'],
#             content_a=data['content_a'],
#             content_b=data['content_b'],
#             score1=data['score1'],
#             score2=data['score2'],
#             game_score=data['game_score'],
#             rotation=data['rotation'],
#             match=data['match'],
#             date=data['date'],
#             pow=data['match_pow']
#         )
#         return redirect('/input/')
#     return render(request, 'input.html')
#
#
# def inputmatch(request):
#     if request.method == 'POST':
#         data = request.POST
#         Match.objects.create(
#             name=data['name'],
#             img = data['img'],
#             start_time = data['start_time'],
#             end_time = data['end_time']
#         )
#         return redirect('/matchlist')
#     return render(request, 'inputmatch.html')
#
#
# def userlist(request):
#     list = []
#     user = UserInfo.objects.all()
#     for i in user:
#         if i.pow == '0':
#             data = {'username':i.username,'pow':'超级管理员'}
#         if i.pow == '1':
#             data = {'username':i.username,'pow':'普通用户'}
#         if i.pow == '2':
#             data = {'username':i.username,'pow':'会员'}
#         if i.pow == '3':
#             data = {'username':i.username,'pow':'VIP会员'}
#         if i.pow == '4':
#             data = {'username':i.username,'pow':'管理员'}
#         list.append(data)
#     return render(request, 'userlist.html', {'userlist':list})
#
#
# def matchlist(request):
#     mlist = []
#     matchlist = []
#     matchinfo = MatchInfo.objects.all()
#     if request.method == 'GET':
#         for i in matchinfo:
#             if i.match not in mlist:
#                 mlist.append(i.match)
#
#     if request.method == 'POST':
#         for x in matchinfo:
#             if x.match not in mlist:
#                 mlist.append(x.match)
#         match = request.POST.get('match')
#         project = request.POST.get('project')
#         for j in matchinfo:
#             if j.match == match and j.project == project:
#                 matchlist.append(j)
#         matchlist.reverse()
#         return render(request, 'matchlist.html',{'matchlist':matchlist,'mlist':mlist, 'match':match, 'project':project})
#     return render(request, 'matchlist.html', {'mlist':mlist})
#
#
# def update(request):
#     url = request.path_info
#     mid = url.split('=')[1]
#     if request.method == 'GET':
#         data = MatchInfo.objects.filter(id=mid)
#     if request.method == 'POST':
#         data = request.POST
#         MatchInfo.objects.filter(id=mid).update(
#             name_a=data['name_a'],
#             name_b=data['name_b'],
#             project=data['project'],
#             icon=data['icon'],
#             content_a=data['content_a'],
#             content_b=data['content_b'],
#             score1=data['score1'],
#             score2=data['score2'],
#             game_score=data['game_score'],
#             rotation=data['rotation'],
#             match=data['match'],
#             pow=data['match_pow']
#         )
#         return redirect('/matchlist/')
#     return render(request, 'update.html', {'data': data})
#
#
#
#
#
