# #coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
import requests,json
from django.shortcuts import redirect  #重新定向模块
#from django.conf import setting


def index(request):
    context = {}
    if not (request.session.has_key('username') and request.session['username'] != ''):
        return redirect('login.html')
    context['username'] = request.session['username']
    return render(request, 'index.html',context)

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.POST['username'] == '':
            return HttpResponse('用户名为空请重新输入')
        if request.POST['password'] == '':
            return HttpResponse('密码为空请重新输入')

        data = json.dumps({
            "auth":{
                "identity":{
                    "methods":[
                        "password"
                    ],
                    "password":{
                        "user":{
                            "name":username,
                            "domain":{
                                "name":"Default"
                            },
                            "password": password
                        }
                    }
                },
            }
        })

        info = requests.post('http://192.168.119.128:5000/v3/auth/tokens', data)
        head = info.headers
        x = requests.structures.CaseInsensitiveDict(head)
        js = dict(x)
        info = info.json()
        if info.has_key('token'):
            request.session['tokenid'] = js['X-Subject-Token']
            request.session['token'] = info
            request.session['userid'] = info['token']['user']['id']
            request.session['username'] = info['token']['user']['name']
        
           
            return redirect('index.html')
            return HttpResponse("登陆成功")
        else:
            return HttpResponse("用户名密码错误")
        
    return render(request,'login.html')

def image(request):
    context = {}
    if not (request.session.has_key('username') and request.session['username'] != ''):
        return redirect('login.html')
    headers={'X-Auth-Token':request.session['tokenid']}
    images = requests.get('http://192.168.119.128:9292/v2/images',headers=headers)
    if images.status_code == 200:
        projects = requests.get('http://192.168.119.128:5000/v3/auth/projects', headers=headers)
        if projects.status_code == 200:
            projectslist=projects.json()
            projectslist=projectslist['projects']
            plist={}
            for one in  projectslist:
                plist[one['id']] = one['name']
            
            context['plist']=plist
        imageslist = images.json()
        if not imageslist.has_key('images'):
            return HttpResponse("系统错误，青稍后再试")
        context['list'] = imageslist['images']
        
    else:
        return HttpResponse("系统错误，请稍后再试")
    return render(request,'image.html',context)



def network(request):
    context = {}
    if not (request.session.has_key('username') and request.session['username'] != ''):
        return redirect('login.html')
    headers={'X-Auth-Token':request.session['tokenid']}
    networks = requests.get('http://192.168.119.128:9696/v2.0/networks',headers=headers)
    if networks.status_code == 200:
        projects = requests.get('http://192.168.119.128:5000/v3/auth/projects', headers=headers)
        if projects.status_code == 200:
            projectslist=projects.json()
            projectslist=projectslist['projects']
            plist={}
            for one in  projectslist:
                plist[one['id']] = one['name']
            context['plist']=plist
            networkslist = networks.json()
            context['list'] = networkslist['networks']
            
    else: 
        return HttpResponse("系统错误")
    return render(request,'network.html',context)



