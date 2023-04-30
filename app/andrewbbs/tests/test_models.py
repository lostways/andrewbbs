from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import AccessCode
from ..models import Screen
from ..models import Member
from ..models import Message

User = get_user_model()

class MessageTestCase(TestCase):
  def setUp(self):
    self.test_sender = User.objects.create_user(
      handle="testsender",
      phone="+1234567890",
      password="testpassword"
    )

    self.test_recipient = User.objects.create_user(
      handle="testrecipient",
      phone="+1234567891",
      password="testpassword"
    )
  
  def test_message_send(self):
    test_message = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body",
      subject="Test Message Subject"
    )

    self.assertEqual(test_message.sender, self.test_sender)
    self.assertEqual(test_message.recipient, self.test_recipient)
    self.assertEqual(test_message.body, "Test Message Body")
    self.assertEqual(test_message.subject, "Test Message Subject")

  def test_messages_get(self):
    test_message_1 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 1",
      subject="Test Message Subject 1"
    )

    test_message_2 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 2",
      subject="Test Message Subject 2"
    )

    test_message_3 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 3",
      subject="Test Message Subject 3"
    )

    # Get all messages sent to test_recipient
    recipeient_messages = Message.objects.received_messages(self.test_recipient)

    # Check that the messages are in the correct order
    self.assertEqual(len(recipeient_messages), 3)
    self.assertEqual(recipeient_messages[0].body, "Test Message Body 3") 
    self.assertEqual(recipeient_messages[1].body, "Test Message Body 2")
    self.assertEqual(recipeient_messages[2].body, "Test Message Body 1")

    # Get all messages sent by test_sender
    sender_messages = Message.objects.sent_messages(self.test_sender)

    # Check that the messages are in the correct order
    self.assertEqual(len(sender_messages), 3)
    self.assertEqual(sender_messages[0].body, "Test Message Body 3")
    self.assertEqual(sender_messages[1].body, "Test Message Body 2")
    self.assertEqual(sender_messages[2].body, "Test Message Body 1")

  def test_messages_unread(self):
    test_message_1 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 1",
      subject="Test Message Subject 1"
    )

    test_message_2 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 2",
      subject="Test Message Subject 2"
    )

    test_message_3 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 3",
      subject="Test Message Subject 3"
    )

    test_message_4 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 4",
      subject="Test Message Subject 4",
      read=True
    )

    test_message_5 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 5",
      subject="Test Message Subject 4",
      read=True
    )

    # Get all messages sent to test_recipient
    unread_messages = Message.objects.unread_messages(self.test_recipient)

    # Check that the messages are in the correct order
    self.assertEqual(len(unread_messages), 3)
    self.assertEqual(unread_messages[0].body, "Test Message Body 3") 
    self.assertEqual(unread_messages[1].body, "Test Message Body 2")
    self.assertEqual(unread_messages[2].body, "Test Message Body 1")

  def test_messages_read(self):
    test_message_1 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 1",
      subject="Test Message Subject 1"
    )

    test_message_2 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 2",
      subject="Test Message Subject 2"
    )

    test_message_3 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 3",
      subject="Test Message Subject 3"
    )

    test_message_4 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 4",
      subject="Test Message Subject 4",
      read=True
    )

    test_message_5 = Message.objects.create(
      sender=self.test_sender,
      recipient=self.test_recipient,
      body="Test Message Body 5",
      subject="Test Message Subject 4",
      read=True
    )

    # Get all messages sent to test_recipient
    read_messages = Message.objects.read_messages(self.test_recipient)

    # Check that the messages are in the correct order
    self.assertEqual(len(read_messages), 2)
    self.assertEqual(read_messages[0].body, "Test Message Body 5") 
    self.assertEqual(read_messages[1].body, "Test Message Body 4")
  
def test_message_mark_read(self):
  test_message_1 = Message.objects.create(
    sender=self.test_sender,
    recipient=self.test_recipient,
    body="Test Message Body 1",
    subject="Test Message Subject 1"
  )

  message = Message.objects.get(id=test_message_1.id)
  self.assertEqual(message.read, False)

  message.mark_read()
  message = Message.objects.get(id=test_message_1.id)
  self.assertEqual(message.read, True)



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