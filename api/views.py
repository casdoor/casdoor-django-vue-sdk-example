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

import json

from casdoor import CasdoorSDK
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .utils import authz_required


def parse_error(json_string):
    if 'error_description' not in json_string:
        return None, None

    try:
        data = json.loads(json_string)
        error = data.get('error', None)
        error_description = data.get('error_description', None)
        return error, error_description
    except json.JSONDecodeError:
        return "JSONDecodeError", f"the input is not valid JSON:{json_string}"


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class SignIn(View):

    def post(self, request):
        code = request.GET.get('code')
        # state = request.GET.get('state')

        sdk: CasdoorSDK = request.current_app.config.get('CASDOOR_SDK')
        token = sdk.get_oauth_token(code)
        err, error_description = parse_error(str(token))
        if err is not None:
            return JsonResponse({'status': 'error', 'msg': f"{err}: {error_description}"})

        user = sdk.parse_jwt_token(token['access_token'])
        request.session['casdoorUser'] = user

        return JsonResponse({'status': 'ok'})


class SignOut(View):

    @authz_required
    def post(self, request):
        del request.session['casdoorUser']
        return JsonResponse({'status': 'ok'})


class ToLogin(View):

    def get(self, request):
        sdk = request.current_app.config.get('CASDOOR_SDK')
        redirect_url = sdk.get_auth_link(redirect_uri=request.current_app.config.get('REDIRECT_URI'),
                                         state='app-built-in')
        return render(request, 'tologin.html', {'redirect_url': redirect_url})


class Index(View):

    @authz_required
    def get(self, request):
        casdoorUser = request.session.get('casdoorUser')
        context = {
            'title': 'title',
            'username': casdoorUser.get('name')
        }
        return render(request, 'index.html', context)


class Account(View):

    @authz_required
    def get(self, request):
        sdk: CasdoorSDK = request.current_app.config.get('CASDOOR_SDK')
        user = request.session.get('casdoorUser')
        print(user)
        # user_obj = get_object_or_404(user, username=user['name'])
        # data = sdk.get_user(user_obj.username)
        return JsonResponse({'status': 'ok', 'data': sdk.get_user(user['name'])})
