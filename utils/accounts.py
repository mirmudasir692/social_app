from rest_framework_simplejwt.tokens import RefreshToken

from dotenv import load_dotenv
import os
import requests

import logging
load_dotenv()


class AccountsServicesClass:
    @classmethod
    def verify_mobile_number(self, phone=None):
        try:
            if phone is not None:
                api_key = os.getenv("VERIFY_MOBILE_API_KEY")
                response = requests.get(
                    f"https://phonevalidation.abstractapi.com/v1/?api_key={api_key}&phone={phone}")
                response.raise_for_status()
                data = response.json()
                return data.get("valid") == True
        except requests.RequestException as e:
            logging.error(f"Error verifying mobile number: {e}")
            return False

    @classmethod
    def verify_email(cls, email=None):
        try:
            if email is not None:
                api_key = os.getenv("VERIFY_MOBILE_API_KEY")
                response = requests.get(
                    f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}")
                print(response.status_code)
                if response.status_code == 200:
                    return True
                else:
                    return False
        except requests.RequestException as e:
            logging.error(f"Error verifying email: {e}")
            return


class GenerateTokens:
    @staticmethod
    def default_profile_pic():
        return "media/user placeholder/avatar-1577909_1280.png"

    @classmethod
    def get_tokens(cls, user):
        refresh_token = RefreshToken.for_user(user)
        data = {
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
            "user_id": str(user.id),
            "is_authenticated": True,
            "profile_pic": user.profile_pic.url if user.profile_pic else "/media/user placeholder/avatar-1577909_1280.png",
            "username": user.username
        }
        return data
