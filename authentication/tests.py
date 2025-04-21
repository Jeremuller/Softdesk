from django.test import TestCase

from django.core.exceptions import ValidationError

from .models import CustomUser

class UserModelTest(TestCase):

     def user_age_validation_test(self):
         user = CustomUser(username='testuser', age=16)
         try:
             user.full_clean()
             user.save()
         except ValidationError:
             self.fail("Userwith valid age raised ValidationError unexpectedly!")

         with self.assertRaises(ValidationError):
             invalid_user = CustomUser(username='testuser_invalid', age=14)
             invalid_user.full_clean()
