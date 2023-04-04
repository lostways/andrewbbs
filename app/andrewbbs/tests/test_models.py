from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import AccessCode
from ..models import Screen
from ..models import Member

User = get_user_model()

class MemberTestCase(TestCase):
  
  def test_add_member(self):
    test_member = Member.objects.create(
      handle="testMember",
      phone="1234567890",
      first_name="Test",
      last_name="Member",
      zip="12345",
      unlocked_codes=["testCode", "testCode2"]
    )

    self.assertEqual(test_member.handle, "testMember")
    self.assertEqual(test_member.phone, "1234567890")
    self.assertEqual(test_member.first_name, "Test")
    self.assertEqual(test_member.last_name, "Member")
    self.assertEqual(test_member.zip, "12345")
    self.assertEqual(test_member.unlocked_codes, ["testCode", "testCode2"])

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

    self.valid_codes_array = [
        "testCaseCode345",
        "testCaseCode678",
        "testCaseCode123",
        "notACode"
    ]

  def test_get_access_code(self):
    self.screen_2.codes.set([self.access_code_123,self.access_code_345])
    self.screen_3.codes.set([self.access_code_345])

    unlocked_screens = Screen.objects.filter(
        codes__code__in=self.valid_codes_array
    ).distinct()
    
    self.assertEqual(unlocked_screens.count(), 2)

class AccessCodeTestCase(TestCase):
    
  def setUp(self):
    AccessCode.objects.create(code="testCaseCode123")
    AccessCode.objects.create(code="testCaseCode345")
    AccessCode.objects.create(code="testCaseCode678")

    self.valid_code = "testCaseCode345"
    self.invalid_code = "notACode"
    self.valid_codes_array = [
        "testCaseCode345",
        "testCaseCode678",
        "testCaseCode123",
        "notACode"
    ]
    self.invalid_codes_array = [
        "notACode",
        "notACode2",
        "notACode3",
    ]

  def test_get_access_code(self):
    code_valid = AccessCode.objects.get(code=self.valid_code)
    self.assertEqual(code_valid.code, self.valid_code)

    with self.assertRaises(AccessCode.DoesNotExist):
      AccessCode.objects.get(code=self.invalid_code)

  def test_get_access_codes(self):
    codes_valid = AccessCode.objects.filter(code__in=self.valid_codes_array)
    codes_invalid = AccessCode.objects.filter(code__in=self.invalid_codes_array)

    self.assertEqual(codes_valid.count(), 3)
    self.assertEqual(codes_invalid.count(), 0)

  def test_disable_code(self):
    AccessCode.objects.create(code="testCaseCode000", enabled=False)
    codes_array = self.valid_codes_array
    codes_array.append("testCaseCode000")

    codes_valid = AccessCode.objects.filter(code__in=codes_array,
                                            enabled=True)

    self.assertEqual(codes_valid.count(), 3)