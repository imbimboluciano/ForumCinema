from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy, resolve
from forum.models import *
from .views import signup, login
from .forms import UserCreationForm
from django.contrib.auth import authenticate,  get_user
from django.contrib.auth import views as auth_views
# Create your tests here.    

class BaseTest(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        return super().setUp()
        
        
class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'registrazione.html')
        self.assertEquals(resolve(self.register_url).func,signup)
        
    def test_register(self):
        citazione = Citazione.objects.create(pk = 25,descrizione="djiejdiej")
        avatar = Avatar.objects.create(pk = 1, image="hhdfhedf")
        response = self.client.post(
            self.register_url,{
                'first_name': "I am",
                'last_name': 'Test',
                'username': 'test',
                'email': 'iam.test@test.gov',
                'password1': 'PassTest8',
                'password2': 'PassTest8',
            },format='text/html'
            )
        self.assertEqual(response.status_code,302)
        
        
class LoginTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEquals(resolve(self.login_url).func.view_class,auth_views.LoginView)
    
    def test_login(self):
        citazione = Citazione.objects.create(pk = 25,descrizione="djiejdiej")
        avatar = Avatar.objects.create(pk = 1, image="hhdfhedf")
        user = User.objects.create_user(username='john', password='rambo')
        userprofile = UserProfile.objects.get(user = user)
        userprofile.citazione = citazione
        userprofile.avatar = avatar
        self.assertFalse(get_user(self.client).is_authenticated)
        response = self.client.post(
            self.login_url, {'username': 'john', 'password': 'rambo'}
        )
        self.assertRedirects(response, '/?login=ok')
        self.assertTrue(get_user(self.client).is_authenticated)

class RegistrationFormTest():
    
    def test_registration_form_valid_data(self):
        form = UserCreationForm(data={
            'first_name': 'first_name',
            'last_name': 'last_name',
            'username': 'username',
            'email': 'testemail@gmail.com',
            'password1': 'xokwpsp[q]', 
            'password2': 'xokwpsp[q]',
        })
        self.assertTrue(form.is_valid())
        
        
    def test_registration_form_no_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),6)
    
class LoginFormTest():
    def test_registration_form_valid_data(self):
        form = UserCreationForm(data={
            'username': 'username',
            'password': 'xokwpsp[q]'
        })
        self.assertTrue(form.is_valid())
        
        
    def test_registration_form_no_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),6)