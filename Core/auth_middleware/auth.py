from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        try: 
          user = UserModel.objects.get(Q(username__iexact=kwargs.get('username')) | Q(email__iexact=kwargs.get('username')))
        except UserModel.DoesNotExist:
          UserModel().set_password(kwargs.get('password'))
        except UserModel.MultipleObjectsReturned:
          return UserModel.objects.filter(email=kwargs.get('username')).order_by('id').first()
        else:
          if user.check_password(kwargs.get('password')) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None