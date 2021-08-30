from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.

from utils.jwt_auth import create_token, parse_payload


class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "august" and password == "123456":
            # 创建token
            payload = {
                'username': username,
                'password': password
            }
            token = create_token(payload)
            return JsonResponse({'status': True, 'token': token})
        else:
            return HttpResponse("登录失败")


class OrderView(View):
    def get(self, request, *args, **kwargs):
        '''
        以查询字符串的方式传递token
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        token = request.GET.get('token')
        result = parse_payload(token)
        if result['status']:
            return JsonResponse({'status': True, 'data': '有权限查看'})
        return JsonResponse({'status': False, 'data': '无权限查看'})


class CenterView(View):
    def get(self, request, *args, **kwargs):
        '''
        以请求头的方式传递token
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        # header key必须增加前缀HTTP，同时大写;header key中带有中横线，那么自动会被转成下划线
        authorization = request.META.get('HTTP_AUTHORIZATION')
        if authorization:
            header, token = authorization.split(' ')
            result = parse_payload(token)
            print(header, token)
            if header.lower() == 'jwt' and result['status']:
                return JsonResponse({'status': True, 'data': '有权限查看'})
        return JsonResponse({'status': False, 'data': '无权限查看'})
