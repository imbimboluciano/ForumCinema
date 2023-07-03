from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import *
from .views import ReviewListView


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.home_url = reverse('home')
        self.login_url = reverse('login')
        self.access = [reverse('forum:discover'), reverse('forum:groupspage'), reverse('forum:pubblicareview')]
        citazione = Citazione.objects.create(pk = 25,descrizione="djiejdiej")
        avatar = Avatar.objects.create(pk = 1, image="hhdfhedf")
        self.user = User.objects.create_user(username='john', password='rambo')
        userprofile = UserProfile.objects.get(user = self.user)
        userprofile.citazione = citazione
        userprofile.avatar = avatar
        return super().setUp()

# Create your tests here.
class HomeTestView(BaseTest):
    
    def test_can_view_page_correctly(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(resolve(self.home_url).func.view_class,ReviewListView)
        
    def test_home_with_anonymous_user(self):
        movie = Movie.objects.create(titolo= "dheduehud")
        review = Review.objects.create(movie=movie, user = self.user, date_published= timezone.now())
        
        response = self.client.get(self.home_url)
        self.assertQuerysetEqual(response.context["object_list"],Review.objects.all())
        
    def test_home_with_registered_user(self):
        movie = Movie.objects.create(titolo= "dheduehud")
        review = Review.objects.create(movie=movie, user = self.user, date_published= timezone.now())
        response = self.client.post(
            self.login_url, {'username': 'john', 'password': 'rambo'}
        )
        
        response = self.client.get(self.home_url)
        self.assertQuerysetEqual(response.context["object_list"],[])
        
        
class AccessToOtherPage(BaseTest):
    
    def test_access_anonymous_user(self):        
        for access in self.access:
            response = self.client.get(access)
            self.assertEqual(response.status_code,302)
            
        
    def test_access_registered_user(self):
        
        response = self.client.post(
            self.login_url, {'username': 'john', 'password': 'rambo'}
        )
        
        for access in self.access:
            response = self.client.get(access)
            self.assertEqual(response.status_code,200)