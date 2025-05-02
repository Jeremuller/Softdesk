from django.test import TestCase

from django.core.exceptions import ValidationError

from .models import CustomUser

class UserModelTest(TestCase):


     def test_age_validation(self):
         user = CustomUser(username='testuser', age=16, password='password123')
         try:
             user.full_clean()
             user.save()
         except ValidationError:
             self.fail("Userwith valid age raised ValidationError unexpectedly!")

         with self.assertRaises(ValidationError):
             invalid_user = CustomUser(username='testuser_invalid', age=14)
             invalid_user.full_clean()


     def test_default_values(self):
         user = CustomUser(username='testuser', age=16, password='password123')
         user.save()
         self.assertFalse(user.can_data_be_shared)
         self.assertFalse(user.can_be_contacted)


     def test_modify_consents(self):
         user = CustomUser(username='testuser', age=16, password='password123')
         user.save()
         user.can_be_contacted = True
         user.can_data_be_shared = True
         user.save()
         self.assertTrue(user.can_data_be_shared)
         self.assertTrue(user.can_be_contacted)


     def test_username_uniqueness(self):

         user1 = CustomUser(username='uniqueuser', age=16, password='password123')
         user1.save()

         with self.assertRaises(ValidationError):
             user2 = CustomUser(username='uniqueuser', age=16, password='password123')
             user2.full_clean()

     def test_str_method(self):
         user = CustomUser(username='testuser', age=16, password='password123')
         user.save()
         self.assertEqual(str(user), 'testuser')
