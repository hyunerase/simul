from django.shortcuts import render
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.

def kakao_login(request):
    # 카카오 로그인 URL로 리디렉션
    return redirect(settings.KAKAO_LOGIN_URI)

def kakao_callback(request):
    # 1. 인가 코드 받아오기
    code = request.GET.get("code")
    if not code:
        return redirect("login")  # 로그인 실패 시 로그인 페이지로 리디렉션

    # 2. 인가 코드를 사용해 액세스 토큰 요청
    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_REST_API_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
        },
    )
    token_json = token_request.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return redirect("login")  # 액세스 토큰 요청 실패 시 로그인 페이지로 리디렉션

    # 3. 액세스 토큰으로 사용자 정보 요청
    user_info_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_info = user_info_request.json()

    kakao_account = user_info.get("kakao_account")
    email = kakao_account.get("email")

    # 4. 사용자 정보를 통해 로그인 또는 회원가입 처리
    user, created = User.objects.get_or_create(username=email)
    if created:
        user.set_unusable_password()  # 소셜 로그인 사용자는 비밀번호 설정 불가

    login(request, user)

    return redirect("home")  # 로그인 후 홈 페이지로 리디렉션

