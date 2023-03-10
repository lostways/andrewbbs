from django.test import TestCase
from ..models import Member
from ..models import AccessCode

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