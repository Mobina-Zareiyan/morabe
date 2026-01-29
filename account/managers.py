# Django Built-in Modules
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _



# -----------------------------
#         UserManager
# -----------------------------
class UserManager(BaseUserManager):

    def create_user(self, mobile_number, password= None, **extra_fields):

        required_fields = ['first_name', 'last_name', 'date_birth', 'national_code',]

        for field in required_fields:
            if field not in extra_fields:
                raise ValueError(f'کاربر باید {field} داشته باشد.')

        user = self.model(
            mobile_number=mobile_number,
            **extra_fields
        )


        user.set_password(password)
        # برا چند پایگاه داده
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_authenticate', True)


        required_fields = ['first_name', 'last_name',
                           'date_birth', 'national_code']

        for field in required_fields:
            if field not in extra_fields:
                raise ValueError(f'Superuser must have {field}')

        return self.create_user(mobile_number, password, **extra_fields)
