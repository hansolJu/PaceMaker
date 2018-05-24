from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserBackend(object):
    def authenticate(self, hukbun=None):
        try:  # 유저가 있는 경우
            user = UserModel.objects.get(hukbun=hukbun)
        except UserModel.DoesNotExist:#info에 유저가 없는경우
            user = None #???
        return user
    def get_user(self, hukbun):
        try:
            return UserModel.objects.get(pk=hukbun)
        except:
            return None