# Copyright 2022 The Casdoor Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from config import Config

from .utils import authz_required


class SignIn(View):
    def post(self, request):
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'status': 'error', 'msg': 'the code parameter is missing'})

        sdk = Config.CASDOOR_SDK
        token = sdk.get_oauth_token(code)
        if 'error' in token:
            return JsonResponse({'status': 'error', 'msg': f"{token['error']}: {token.get('error_description', '')}"})

        user = sdk.parse_jwt_token(token['access_token'])
        request.session['casdoorUser'] = user

        return JsonResponse({'status': 'ok'})


class SignOut(View):
    def post(self, request):
        request.session.pop('casdoorUser', None)
        return JsonResponse({'status': 'ok'})


class ToLogin(View):
    def get(self, request):
        redirect_url = Config.CASDOOR_SDK.get_auth_link(redirect_uri=Config.REDIRECT_URI)
        return render(request, 'tologin.html', {'redirect_url': redirect_url})


class Account(View):
    @authz_required
    def get(self, request):
        return JsonResponse({'status': 'ok', 'data': request.session.get('casdoorUser')})
