from datetime import date 
from django.test import TestCase
from mentor.questionaire.tests import UserLogin, AdminLogin
from mentor.counter.models import Counter 
from django.core.urlresolvers import reverse

class GotoViewTest(TestCase):
    def test_url_empty(self):
        url = ''
        response = self.client.get('/goto/' + url)

        # It should return an 404 page
        self.assertEqual(response.status_code, 404)

    def test_url_not_emtry(self):
        url = 'http://google.com'
        response = self.client.get('/goto/' + url)

        # Make sure that a counter is saved
        savedUrls = Counter.objects.filter(url=url)
        self.assertEqual(len(savedUrls), 1)

        # And it is redirected to url
        self.assertRedirects(response, url)

class CSVReportView(AdminLogin):
    def test_get(self):
        response = self.client.get(reverse('counter-reporting'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            'start_date' : date.today(),
            'end_date' : date.today(),
        }

        counter = Counter(url="http://google.com")
        counter.save()

        response = self.client.post(reverse('counter-reporting'), data)

        # Test if a csv response is generated
        self.assertEqual(response['Content-Type'], 'text/csv')

class ListReportView(AdminLogin):
    def test_get(self):
        response = self.client.get(reverse('counter-list'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            'start_date' : date.today(),
            'end_date' : date.today(),
        }

        response = self.client.post(reverse('counter-list'), data)
        self.assertEqual(response.status_code, 200)

        counter = Counter(url="http://google.com")
        counter.save()
        self.assertEqual(len(Counter.objects.all()),1)
        response = self.client.post(reverse('counter-list'), data)

        self.assertEqual(response.context['has_counters'], 1)

