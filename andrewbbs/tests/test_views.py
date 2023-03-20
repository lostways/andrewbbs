# Tests for the views in the andrewbbs app
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from ..models import AccessCode
from ..models import Screen
from ..models import Member

User = get_user_model()

class ScreenTestCase(TestCase):
      
    def setUp(self):
      self.access_code_123 = AccessCode.objects.create(code="testCaseCode123")
      self.access_code_345 = AccessCode.objects.create(code="testCaseCode345")
      self.access_code_679 = AccessCode.objects.create(code="testCaseCode678")
  
      test_user = User.objects.create_user(
          handle="testuser",
          phone="+1234567890",
          password="testpassword"
      )
  
      self.screen_1 = Screen.objects.create(
          title="Test1",
          body="Test One Body",
          slug="test-1",
          published=True,
          author = test_user
      )
  
      self.screen_2 = Screen.objects.create(
          title="Test2",
          body="Test Two Body",
          slug="test-2",
          published=True,
          author = test_user
      )
  
      self.screen_3 = Screen.objects.create(
          title="Test3",
          body="Test Three Body",
          slug="test-3",
          published=True,
          author = test_user
      )
  
      self.screen_1.codes.add(self.access_code_123)
      self.screen_1.codes.add(self.access_code_345)
      self.screen_2.codes.add(self.access_code_345)
      self.screen_2.codes.add(self.access_code_679)
      self.screen_3.codes.add(self.access_code_123)
      self.screen_3.codes.add(self.access_code_679)
  
    def test_screen_list_no_codes(self):
      """Test that screen list view returns access code view if no codes are unlocked"""
      response = self.client.get(reverse('screen-list'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'access.html')
    
    def test_screen_list_unlocked_session(self):
      """Test that screen list view returns screen list if codes in session"""
      session = self.client.session
      session['codes'] = ["testCaseCode123"]
      session.save()

      screens = Screen.objects.filter(
          codes__code__in=["testCaseCode123"],
        ).distinct().order_by("-updated_at")

      response = self.client.get(reverse('screen-list'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'screens/screen_list.html')
      self.assertQuerysetEqual(response.context['screen_list'], screens)

    def test_screen_list_unlocked_user(self):
      """Test that screen list view returns screen list if codes in user"""
      
      test_user = User.objects.create_user(
        handle="testuser2",
        phone="+1234567892",
        password="testpassword",
        unlocked_codes=["testCaseCode123"]
      )

      screens = Screen.objects.filter(
          codes__code__in=["testCaseCode123"],
        ).distinct().order_by("-updated_at")

      self.client.force_login(test_user)

      response = self.client.get(reverse('screen-list'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'screens/screen_list.html')
      self.assertQuerysetEqual(response.context['screen_list'], screens)
  
    def test_screen_detail_locked(self):
      response = self.client.get(reverse('screen-detail', kwargs={'slug': self.screen_1.slug}))
      self.assertEqual(response.status_code, 404)
    
    def test_screen_detail_unlocked_session(self):
      session = self.client.session
      session['codes'] = ["testCaseCode123"]
      session.save()
      response = self.client.get(reverse('screen-detail', kwargs={'slug': self.screen_1.slug}))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'screens/screen_detail.html')
      self.assertEqual(response.context['screen'], self.screen_1)
      
    def test_screen_detail_unlocked_user(self):
      test_user = User.objects.create_user(
        handle="testuser2",
        phone="+1234567892",
        password="testpassword",
        unlocked_codes=["testCaseCode123"]
      )
      self.client.force_login(test_user)
      response = self.client.get(reverse('screen-detail', kwargs={'slug': self.screen_1.slug}))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'screens/screen_detail.html')
      self.assertEqual(response.context['screen'], self.screen_1)

class AccessTestCase(TestCase):  
  
  def setUp(self):
    self.access_code_123 = AccessCode.objects.create(code="testCaseCode123")

    test_user = User.objects.create_user(
        handle="testuser",
        phone="+1234567890",
        password="testpassword"
    )

    self.screen_1 = Screen.objects.create(
        title="Test1",
        body="Test One Body",
        slug="test-1",
        published=True,
        author = test_user
    )

    self.screen_2 = Screen.objects.create(
        title="Test2",
        body="Test Two Body",
        slug="test-2",
        published=True,
        author = test_user
    )

    self.screen_1.codes.add(self.access_code_123)
    self.screen_2.codes.add(self.access_code_123)

  def test_access_code_view(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'access.html')
    self.assertContains(response, 'Enter Access Code')
    self.assertContains(response, 'Submit')

  def test_access_code_valid(self):
    response = self.client.post(reverse('access'), data={'code': 'testCaseCode123'})
    
    # Assert that the user is redirected to the screen list
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('screen-list'))

    # Assert that the code is in the session now
    self.assertEqual(self.client.session['codes'], ['testCaseCode123'])
  
  def test_access_code_valid_logged_in(self):
    test_user = User.objects.create_user(
      handle="testuser2",
      phone="+1234567892",
      password="testpassword"
    )
    self.client.force_login(test_user)
    response = self.client.post(reverse('access'), data={'code': 'testCaseCode123'})
    
    # Assert that the user is redirected to the screen list
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('screen-list'))

    # Assert that the code is in the user's unlocked codes
    test_user = User.objects.get(handle="testuser2")
    self.assertEqual(test_user.unlocked_codes, ['testCaseCode123'])

  def test_access_code_invalid(self):
    response = self.client.post('/', data={'code': 'invalidCode'})
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'access.html')
  
  def test_access_code_already_unlocked(self):
    session = self.client.session
    session['codes'] = ["testCaseCode123", "testCaseCode345"]
    session.save()
    response = self.client.post(reverse('access'), data={'code': 'testCaseCode123'})

    # Assert that the user is redirected to the screen list
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('screen-list'))

    # Assert that the codes in the session are still the same
    self.assertEqual(self.client.session['codes'], ['testCaseCode123', 'testCaseCode345'])

class MemberTestCase(TestCase):  
  
  def setUp(self):
    self.member_1 = Member.objects.create(
      handle="testuser",
      phone="+12345678901",
      password="testpassword"
    )
  
  def test_member_register_view(self):
    response = self.client.get(reverse('member-register'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'members/register.html')
    self.assertContains(response, 'New Member')
    self.assertContains(response, 'Register')
  
  def test_member_register_valid(self):
    data = {
      'handle': 'testuser2',
      'phone_0': 'US', # Phone number field is split into two fields
      'phone_1': '2345678920',
      'first_name': 'Test',
      'last_name': 'User',
      'zip': '12345',
    }

    response = self.client.post(reverse('member-register'), data)
    #print(response.content)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('member-login'))
    self.assertEqual(Member.objects.count(), 2)

    new_member = Member.objects.get(handle='testuser2')

    self.assertEqual(new_member.phone.as_e164, '+12345678920')
    self.assertEqual(new_member.first_name, 'Test')
    self.assertEqual(new_member.last_name, 'User')
    self.assertEqual(new_member.zip, '12345')
    self.assertEqual(new_member.is_staff, False)
    self.assertEqual(new_member.unlocked_codes, [])
  
  def test_member_register_valid_with_codes(self):
    data = {
      'handle': 'testuser2',
      'phone_0': 'US', # Phone number field is split into two fields
      'phone_1': '2345678920',
      'first_name': 'Test',
      'last_name': 'User',
      'zip': '12345',
    }

    # Put codes in the session
    session = self.client.session
    session['codes'] = ["testCaseCode123", "testCaseCode345"]
    session.save()

    response = self.client.post(reverse('member-register'), data)
    #print(response.content)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('member-login'))
    self.assertEqual(Member.objects.count(), 2)

    new_member = Member.objects.get(handle='testuser2')

    self.assertEqual(new_member.unlocked_codes, ['testCaseCode123', 'testCaseCode345'])
  
