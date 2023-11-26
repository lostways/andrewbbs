# Tests for the views in the andrewbbs app
from unittest import mock
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from ..models import AccessCode
from ..models import Screen
from ..models import Member
from ..models import Message


User = get_user_model()


class MessageTestCase(TestCase):
    def setUp(self):
        self.test_sender = User.objects.create_user(
            handle="testsender", phone="+1234567890", password="testpassword"
        )

        self.test_recipient = User.objects.create_user(
            handle="testrecipient", phone="+1234567891", password="testpassword"
        )

    def test_send_message_view_unauthenticated(self):
        response = self.client.get(reverse("member-message-send"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, f"{settings.LOGIN_URL}?next={reverse('member-message-send')}"
        )

    def test_send_message_view_get(self):
        self.client.force_login(self.test_sender)
        response = self.client.get(reverse("member-message-send"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/messages/message_send.html")

    def test_send_message_view_post(self):
        self.client.force_login(self.test_sender)

        # Test with twilio provider
        settings.SMS_PROVIDER = "local"

        with mock.patch("andrewbbs.SMS.local.SMS.send_sms") as mock_send_sms:
            mock_send_sms.return_value = True
            response = self.client.post(
                reverse("member-message-send"),
                {
                    "recipient": self.test_recipient.handle,
                    "subject": "Test Message Subject",
                    "body": "Test Message Body",
                },
            )
            mock_send_sms.assert_called_once_with(
                self.test_recipient.phone.as_e164,
                f"Andrew BBS: New msg from {self.test_sender.handle}!",
            )

            # print(response.content)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("member-message-sent"))

            self.assertEqual(Message.objects.count(), 1)
            self.assertEqual(Message.objects.first().sender, self.test_sender)
            self.assertEqual(Message.objects.first().recipient, self.test_recipient)
            self.assertEqual(Message.objects.first().subject, "Test Message Subject")
            self.assertEqual(Message.objects.first().body, "Test Message Body")

    def test_send_message_view_invalid_recipient(self):
        self.client.force_login(self.test_sender)

        response = self.client.post(
            reverse("member-message-send"),
            {
                "recipient": "invalidrecipient",
                "subject": "Test Message Subject",
                "body": "Test Message Body",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/messages/message_send.html")
        self.assertEqual(
            response.context["form"].errors["recipient"][0], "Handle not found"
        )
        self.assertEqual(Message.objects.count(), 0)

    def test_message_inbox_view_unauthenticated(self):
        response = self.client.get(reverse("member-message-inbox"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, f"{settings.LOGIN_URL}?next={reverse('member-message-inbox')}"
        )

    def test_message_inbox_view_get(self):
        self.client.force_login(self.test_recipient)

        # Create 3 unread messages, 2 of which are sent to the test recipient
        # and 1 of which is sent by the test recipient

        message_1 = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject 1",
            body="Test Message Body 1",
        )

        message_2 = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject 2",
            body="Test Message Body 2",
        )

        message_3 = Message.objects.create(
            sender=self.test_recipient,
            recipient=self.test_sender,
            subject="Test Message Subject 3",
            body="Test Message Body 3",
        )

        # Create 2 read messages, both of which are sent to the test recipient
        message_4 = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject 4",
            body="Test Message Body 4",
            read=True,
        )

        message_5 = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject 5",
            body="Test Message Body 5",
            read=True,
        )

        response = self.client.get(reverse("member-message-inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/messages/message_inbox.html")

        self.assertEqual(response.context["unread_messages"].count(), 2)
        self.assertEqual(response.context["unread_messages"][0], message_2)
        self.assertEqual(response.context["unread_messages"][1], message_1)

        self.assertEqual(response.context["read_messages"].count(), 2)
        self.assertEqual(response.context["read_messages"][0], message_5)
        self.assertEqual(response.context["read_messages"][1], message_4)

        self.assertContains(response, message_1.subject)
        self.assertContains(response, message_2.subject)
        self.assertContains(response, message_4.subject)
        self.assertContains(response, message_5.subject)

        self.assertNotContains(response, message_3.subject)

        self.assertEqual(response.context["page_title"], "Inbox")

    def test_message_sent_view_unauthenticated(self):
        response = self.client.get(reverse("member-message-sent"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, f"{settings.LOGIN_URL}?next={reverse('member-message-sent')}"
        )

    def test_message_sent_view_get(self):
        self.client.force_login(self.test_sender)

        # Create 3 messages, 2 of which are sent by the test sender
        # and 1 of which is sent to the test sender

        message_1 = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject 1",
            body="Test Message Body 1",
        )

        message_2 = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject 2",
            body="Test Message Body 2",
        )

        message_3 = Message.objects.create(
            sender=self.test_recipient,
            recipient=self.test_sender,
            subject="Test Message Subject 3",
            body="Test Message Body 3",
        )

        response = self.client.get(reverse("member-message-sent"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/messages/message_sent.html")
        self.assertEqual(response.context["messages"].count(), 2)
        self.assertEqual(response.context["messages"][0], message_2)
        self.assertEqual(response.context["messages"][1], message_1)

        # print(response.content)
        self.assertContains(response, "Test Message Subject 1")
        self.assertContains(response, "Test Message Subject 2")
        self.assertNotContains(response, "Test Message Subject 3")
        self.assertEqual(response.context["page_title"], "Sent Messages")

    def test_message_detail_view_unauthenticated(self):
        message = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject",
            body="Test Message Body",
        )

        response = self.client.get(
            reverse("member-message-detail", kwargs={"uuid": message.uuid})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{settings.LOGIN_URL}?next={reverse('member-message-detail', kwargs={'uuid': message.uuid})}",
        )

    def test_message_detail_view_get_sender(self):
        self.client.force_login(self.test_sender)

        message = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject",
            body="Test Message Body",
        )

        response = self.client.get(
            reverse("member-message-detail", kwargs={"uuid": message.uuid})
        )

        # message should not be marked as read
        message = Message.objects.get(pk=message.pk)
        self.assertFalse(message.read)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/messages/message_detail.html")
        self.assertEqual(response.context["message"], message)

    def test_message_detail_view_get_recipeint(self):
        self.client.force_login(self.test_recipient)

        message = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject",
            body="Test Message Body",
        )

        response = self.client.get(
            reverse("member-message-detail", kwargs={"uuid": message.uuid})
        )

        # message should be marked as read
        message = Message.objects.get(pk=message.pk)
        self.assertTrue(message.read)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/messages/message_detail.html")
        self.assertEqual(response.context["message"], message)

    def test_message_detail_view_not_authorised(self):
        new_user = User.objects.create_user(
            handle="newuser", phone="+1234567894", password="newpassword"
        )

        self.client.force_login(new_user)

        message = Message.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            subject="Test Message Subject",
            body="Test Message Body",
        )

        response = self.client.get(
            reverse("member-message-detail", kwargs={"uuid": message.uuid})
        )
        self.assertEqual(response.status_code, 404)


class ScreenTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            handle="testuser", phone="+1234567890", password="testpassword"
        )

        self.access_code_123 = AccessCode.objects.create(
            code="testCaseCode123",author=test_user
        )
        self.access_code_345 = AccessCode.objects.create(
            code="testCaseCode345", author=test_user
        )
        self.access_code_679 = AccessCode.objects.create(
            code="testCaseCode678", author=test_user
        )

        self.screen_1 = Screen.objects.create(
            title="Test1",
            body="Test One Body",
            slug="test-1",
            published=True,
            author=test_user,
        )

        self.screen_2 = Screen.objects.create(
            title="Test2",
            body="Test Two Body",
            slug="test-2",
            published=True,
            author=test_user,
        )

        self.screen_3 = Screen.objects.create(
            title="Test3",
            body="Test Three Body",
            slug="test-3",
            published=True,
            author=test_user,
        )

        self.screen_1.codes.add(self.access_code_123)
        self.screen_1.codes.add(self.access_code_345)
        self.screen_2.codes.add(self.access_code_345)
        self.screen_2.codes.add(self.access_code_679)
        self.screen_3.codes.add(self.access_code_123)
        self.screen_3.codes.add(self.access_code_679)

    def test_screen_list_no_codes(self):
        """Test that screen list view returns access code view if no codes are unlocked"""
        response = self.client.get(reverse("screen-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access.html")

    def test_screen_list_unlocked_session(self):
        """Test that screen list view returns screen list if codes in session"""
        session = self.client.session
        session["codes"] = ["testCaseCode123"]
        session.save()

        screens = (
            Screen.objects.filter(
                codes__code__in=["testCaseCode123"],
            )
            .distinct()
            .order_by("-updated_at")
        )

        response = self.client.get(reverse("screen-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_list.html")
        self.assertQuerysetEqual(response.context["screen_list"], screens)

    def test_screen_list_unlocked_user(self):
        """Test that screen list view returns screen list if codes in user"""

        test_user = User.objects.create_user(
            handle="testuser2",
            phone="+1234567892",
            password="testpassword",
            unlocked_codes=["testCaseCode123"],
        )

        screens = (
            Screen.objects.filter(
                codes__code__in=["testCaseCode123"],
            )
            .distinct()
            .order_by("-updated_at")
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse("screen-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_list.html")
        self.assertQuerysetEqual(response.context["screen_list"], screens)

    def test_screen_detail_locked(self):
        response = self.client.get(
            reverse("screen-detail", kwargs={"slug": self.screen_1.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_screen_detail_unlocked_session(self):
        session = self.client.session
        session["codes"] = ["testCaseCode123"]
        session.save()
        response = self.client.get(
            reverse("screen-detail", kwargs={"slug": self.screen_1.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_detail.html")
        self.assertEqual(response.context["screen"], self.screen_1)

    def test_screen_detail_unlocked_user(self):
        test_user = User.objects.create_user(
            handle="testuser2",
            phone="+1234567892",
            password="testpassword",
            unlocked_codes=["testCaseCode123"],
        )
        self.client.force_login(test_user)
        response = self.client.get(
            reverse("screen-detail", kwargs={"slug": self.screen_1.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_detail.html")
        self.assertEqual(response.context["screen"], self.screen_1)


class AccessTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            handle="testuser", phone="+1234567890", password="testpassword"
        )

        self.access_code_123 = AccessCode.objects.create(
            code="testCaseCode123", author=test_user
        )

        self.screen_1 = Screen.objects.create(
            title="Test1",
            body="Test One Body",
            slug="test-1",
            published=True,
            author=test_user,
        )

        self.screen_2 = Screen.objects.create(
            title="Test2",
            body="Test Two Body",
            slug="test-2",
            published=True,
            author=test_user,
        )

        self.screen_1.codes.add(self.access_code_123)
        self.screen_2.codes.add(self.access_code_123)

    def test_access_code_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access.html")
        self.assertContains(response, "Enter Access Code")
        self.assertContains(response, "Submit")

    def test_access_code_valid(self):
        response = self.client.post(reverse("access"), data={"code": "testCaseCode123"})

        # Assert that the user is redirected to the screen list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("screen-list"))

        # Assert that the code is in the session now
        self.assertEqual(self.client.session["codes"], ["testCaseCode123"])

    def test_access_code_valid_logged_in(self):
        test_user = User.objects.create_user(
            handle="testuser2", phone="+1234567892", password="testpassword"
        )
        self.client.force_login(test_user)
        response = self.client.post(reverse("access"), data={"code": "testCaseCode123"})

        # Assert that the user is redirected to the screen list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("screen-list"))

        # Assert that the code is in the user's unlocked codes
        test_user = User.objects.get(handle="testuser2")
        self.assertEqual(test_user.unlocked_codes, ["testCaseCode123"])

    def test_access_code_invalid(self):
        response = self.client.post("/", data={"code": "invalidCode"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access.html")

    def test_access_code_already_unlocked(self):
        session = self.client.session
        session["codes"] = ["testCaseCode123", "testCaseCode345"]
        session.save()
        response = self.client.post(reverse("access"), data={"code": "testCaseCode123"})

        # Assert that the user is redirected to the screen list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("screen-list"))

        # Assert that the codes in the session are still the same
        self.assertEqual(
            self.client.session["codes"], ["testCaseCode123", "testCaseCode345"]
        )


class MemberTestCase(TestCase):
    def setUp(self):
        self.member_1 = Member.objects.create(
            handle="testuser", phone="+12345678901", password="testpassword"
        )

    def test_member_register_view_no_codes(self):
        response = self.client.get(reverse("member-register"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("screen-list"))

    def test_member_register_view_unlocked_codes(self):
        session = self.client.session
        session["codes"] = ["testCaseCode123"]
        session.save()

        response = self.client.get(reverse("member-register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/register.html")
        self.assertContains(response, "New Member")
        self.assertContains(response, "Register")

    def test_member_register_valid(self):
        data = {
            "handle": "testuser2",
            "phone_0": "US",  # Phone number field is split into two fields
            "phone_1": "2345678920",
            "first_name": "Test",
            "last_name": "User",
            "zip": "12345",
        }

        # Put codes in the session
        session = self.client.session
        session["codes"] = ["testCaseCode123", "testCaseCode345"]
        session.save()

        response = self.client.post(reverse("member-register"), data)
        # print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("member-login"))
        self.assertEqual(Member.objects.count(), 2)

        new_member = Member.objects.get(handle="testuser2")

        self.assertEqual(new_member.phone.as_e164, "+12345678920")
        self.assertEqual(new_member.first_name, "Test")
        self.assertEqual(new_member.last_name, "User")
        self.assertEqual(new_member.zip, "12345")
        self.assertEqual(new_member.is_staff, False)
        self.assertEqual(
            new_member.unlocked_codes, ["testCaseCode123", "testCaseCode345"]
        )

    def test_member_register_valid_with_codes(self):
        data = {
            "handle": "testuser2",
            "phone_0": "US",  # Phone number field is split into two fields
            "phone_1": "2345678920",
            "first_name": "Test",
            "last_name": "User",
            "zip": "12345",
        }

        # Put codes in the session
        session = self.client.session
        session["codes"] = ["testCaseCode123", "testCaseCode345"]
        session.save()

        response = self.client.post(reverse("member-register"), data)
        # print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("member-login"))
        self.assertEqual(Member.objects.count(), 2)

        new_member = Member.objects.get(handle="testuser2")
        self.assertEqual(
            new_member.unlocked_codes, ["testCaseCode123", "testCaseCode345"]
        )

    def test_member_register_invalid(self):
        data = {
            "handle": "testuser",
            "phone_0": "US",  # Phone number field is split into two fields
            "phone_1": "2345678920",
            "first_name": "Test",
            "last_name": "User",
            "zip": "12345",
        }

        session = self.client.session
        session["codes"] = ["testCaseCode123", "testCaseCode345"]
        session.save()

        response = self.client.post(reverse("member-register"), data)
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/register.html")
        self.assertEqual(Member.objects.count(), 1)
        self.assertContains(response, "Member with this Handle already exists.")

    def test_member_login_view(self):
        response = self.client.get(reverse("member-login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/login.html")
        self.assertContains(response, "Login")

    def test_member_login_valid(self):
        data = {
            "handle": "testuser",
        }

        testuser_id = self.member_1.id

        # Test with twilio provider
        settings.SMS_PROVIDER = "local"

        # Mock the send_code method on the twilio provider
        with mock.patch("andrewbbs.SMS.local.SMS.otp_send_code") as mock_send_code:
            mock_send_code.return_value = True
            response = self.client.post(reverse("member-login"), data)
            mock_send_code.assert_called_once_with("+12345678901")
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(
                response, reverse("member-login-verify", kwargs={"pk": testuser_id})
            )

    def test_member_login_verify_view(self):
        testuser_id = self.member_1.id

        response = self.client.get(
            reverse("member-login-verify", kwargs={"pk": testuser_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/verify.html")
        self.assertContains(response, "Auth Code")
        self.assertNotContains(response, "Invalid Code")

    def test_member_login_verify_valid(self):
        data = {
            "code": "123456",
        }

        testuser_phone = self.member_1.phone.as_e164
        testuser_id = self.member_1.id

        # Test with twilio provider
        settings.SMS_PROVIDER = "local"

        with mock.patch("andrewbbs.SMS.local.SMS.otp_verify_code") as mock_verify_code:
            mock_verify_code.return_value = "approved"
            response = self.client.post(
                reverse("member-login-verify", kwargs={"pk": testuser_id}), data
            )
            mock_verify_code.assert_called_once_with(testuser_phone, "123456")
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("screen-list"))

    def test_member_login_verify_invalid(self):
        data = {
            "code": "123456",
        }

        testuser_phone = self.member_1.phone.as_e164
        testuser_id = self.member_1.id

        # Test with twilio provider
        settings.SMS_PROVIDER = "local"

        with mock.patch("andrewbbs.SMS.local.SMS.otp_verify_code") as mock_verify_code:
            mock_verify_code.return_value = False
            response = self.client.post(
                reverse("member-login-verify", kwargs={"pk": testuser_id}), data
            )
            mock_verify_code.assert_called_once_with(testuser_phone, "123456")
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "members/verify.html")
            self.assertContains(response, "Invalid code")

class AccessCodeEditTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            handle="testuser", phone="+1234567890", password="testpassword"
        )

        self.other_user = User.objects.create_user(
            handle="otheruser", phone="+1234567891", password="testpassword"
        )

        self.access_code_123 = AccessCode.objects.create(
            code="testCaseCode123", author=self.test_user
        )
        self.access_code_345 = AccessCode.objects.create(
            code="testCaseCode345", author=self.test_user
        )
        self.access_code_678 = AccessCode.objects.create(
            code="testCaseCode678", author=self.test_user
        )
        
        # code that is not created by the test user
        self.access_code_679 = AccessCode.objects.create(
            code="testCaseCode679", author=self.other_user
        )

        self.screen_1 = Screen.objects.create(
            title="Test1",
            body="Test One Body",
            slug="test-1",
            published=True,
            author=self.test_user,
        )

        self.screen_2 = Screen.objects.create(
            title="Test2",
            body="Test Two Body",
            slug="test-2",
            published=True,
            author=self.test_user,
        )

        self.screen_3 = Screen.objects.create(
            title="Test3",
            body="Test Three Body",
            slug="test-3",
            published=True,
            author=self.test_user,
        )

        self.screen_1.codes.add(self.access_code_123)
        self.screen_1.codes.add(self.access_code_345)
        self.screen_2.codes.add(self.access_code_345)
        self.screen_2.codes.add(self.access_code_678)
        self.screen_3.codes.add(self.access_code_123)
        self.screen_3.codes.add(self.access_code_678)

    def test_access_code_list_view(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("access-code-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access_codes/access_code_list.html")
        self.assertEqual(response.context["access_codes"].count(), 3)
        self.assertEqual(response.context["access_codes"][0], self.access_code_123)
        self.assertEqual(response.context["access_codes"][1], self.access_code_345)
        self.assertEqual(response.context["access_codes"][2], self.access_code_678)

    def test_access_code_list_view_unauthenticated(self):
        response = self.client.get(reverse("access-code-list"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{settings.LOGIN_URL}?next={reverse('access-code-list')}",
        )

    def test_access_code_detail_view(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("access-code-detail", kwargs={"pk": self.access_code_123.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access_codes/access_code_detail.html")
        self.assertEqual(response.context["form"].instance, self.access_code_123)

    def test_access_code_detail_view_unauthorised(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("access-code-detail", kwargs={"pk": self.access_code_679.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_access_code_detail_view_unauthenticated(self):
        response = self.client.get(
            reverse("access-code-detail", kwargs={"pk": self.access_code_123.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{settings.LOGIN_URL}?next={reverse('access-code-detail', kwargs={'pk': self.access_code_123.pk})}",
        )

    def test_access_code_create_view(self):
        create_test_user = User.objects.create_user(
            handle="createtestuser", phone="+1234567810", password="testpassword"
        )

        self.client.force_login(create_test_user)
        response = self.client.get(reverse("access-code-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access_codes/access_code_detail.html")
        self.assertEqual(response.context["form"].instance.enabled, True)

        # Test creating new code
        response = self.client.post(
            reverse("access-code-create"), data={"code": "newCode", "enabled": True}
        )
        
        users_codes = AccessCode.objects.get_by_user(create_test_user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("access-code-list"))
        self.assertEqual(users_codes.count(), 1)
        self.assertEqual(users_codes.last().code, "newCode")
        self.assertEqual(users_codes.last().author, create_test_user)


    def test_access_code_create_view_unauthenticated(self):
        response = self.client.get(reverse("access-code-create"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{settings.LOGIN_URL}?next={reverse('access-code-create')}",
        )

class ScreenEditTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            handle="testuser", phone="+1234567890", password="testpassword"
        )

        self.other_user = User.objects.create_user(
            handle="otheruser", phone="+1234567891", password="testpassword"
        )

        self.access_code_123 = AccessCode.objects.create(
            code="testCaseCode123", author=self.test_user
        )
        self.access_code_345 = AccessCode.objects.create(
            code="testCaseCode345", author=self.test_user
        )
        self.access_code_678 = AccessCode.objects.create(
            code="testCaseCode678", author=self.test_user
        )
        
        # code that is not created by the test user
        self.access_code_679 = AccessCode.objects.create(
            code="testCaseCode679", author=self.other_user
        )

        self.screen_1 = Screen.objects.create(
            title="Test1",
            body="Test One Body",
            slug="test-1",
            published=True,
            author=self.test_user,
        )

        self.screen_2 = Screen.objects.create(
            title="Test2",
            body="Test Two Body",
            slug="test-2",
            published=True,
            author=self.test_user,
        )

        self.screen_3 = Screen.objects.create(
            title="Test3",
            body="Test Three Body",
            slug="test-3",
            published=True,
            author=self.test_user,
        )

        self.screen_4 = Screen.objects.create(
            title="Test4",
            body="Test Four Body",
            slug="test-4",
            published=True,
            author=self.other_user,
        )

        self.screen_1.codes.add(self.access_code_123)
        self.screen_1.codes.add(self.access_code_345)
        self.screen_2.codes.add(self.access_code_345)
        self.screen_2.codes.add(self.access_code_678)
        self.screen_3.codes.add(self.access_code_123)
        self.screen_3.codes.add(self.access_code_678)

    def test_screen_create_list_view(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("screen-edit-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_edit_list.html")
        self.assertEqual(response.context["screen_list"].count(), 3)
        self.assertEqual(response.context["screen_list"][0], self.screen_3)
        self.assertEqual(response.context["screen_list"][1], self.screen_2)
        self.assertEqual(response.context["screen_list"][2], self.screen_1)

    def test_screen_create_list_view_unauthenticated(self):
        response = self.client.get(reverse("screen-edit-list"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{settings.LOGIN_URL}?next={reverse('screen-edit-list')}",
        )
    
    def test_screen_create_detail_view(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("screen-edit-detail", kwargs={"pk": self.screen_1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_edit_detail.html")
        self.assertEqual(response.context["form"].instance, self.screen_1)

    def test_screen_create_detail_view_unauthorised(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("screen-edit-detail", kwargs={"pk": self.screen_4.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_screen_create_detail_view_unauthenticated(self):
        response = self.client.get(
            reverse("screen-edit-detail", kwargs={"pk": self.screen_1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{settings.LOGIN_URL}?next={reverse('screen-edit-detail', kwargs={'pk': self.screen_1.pk})}",
        )
        
    def test_screen_edit_detail_save_view(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse("screen-edit-detail", kwargs={"pk": self.screen_1.pk}),
            data={"title": "Test1",
                  "slug": "test-1",
                  "body": "Test One Body Change", 
                  "codes": [self.access_code_123.pk,self.access_code_345.pk],
                  "published": True},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("screen-edit-list"))
        self.assertEqual(Screen.objects.count(), 4)
        self.assertEqual(Screen.objects.last().title, "Test1")
        self.assertEqual(Screen.objects.last().body, "Test One Body Change")
        self.assertEqual(Screen.objects.last().codes.count(), 2)
        self.assertEqual(Screen.objects.last().codes.first(), self.access_code_123)
        self.assertEqual(Screen.objects.last().codes.last(), self.access_code_345)
        self.assertEqual(Screen.objects.last().published, True)
        self.assertEqual(Screen.objects.last().author, self.test_user)

    def test_screen_edit_detail_save_view_code_unauthorised(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse("screen-edit-detail", kwargs={"pk": self.screen_1.pk}),
            data={"title": "Test1",
                  "slug": "test-1",
                  "body": "Test One Body Change", 
                  "codes": [self.access_code_123.pk,self.access_code_679.pk],
                  "published": True},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_edit_detail.html")
        self.assertContains(response, "Invalid access code")

    def test_screen_create_view(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("screen-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "screens/screen_edit_detail.html")
        self.assertEqual(response.context["form"].instance.published, False)

        # Test creating new screen
        response = self.client.post(
            reverse("screen-create"), data={"title": "Test Five",
                  "body": "Test Five Body", 
                  "codes": [self.access_code_123.pk,self.access_code_345.pk],
                  "published": True}
        )
        
        users_screens = Screen.objects.get_by_user(self.test_user)
        new_screen = users_screens.filter(title="Test Five").first()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("screen-edit-list"))
        self.assertEqual(users_screens.count(), 4)
        self.assertEqual(new_screen.title, "Test Five")
        self.assertEqual(new_screen.body, "Test Five Body")
        self.assertEqual(new_screen.slug, "test-five")
        self.assertEqual(new_screen.codes.count(), 2)
        self.assertEqual(new_screen.codes.first(), self.access_code_123)
        self.assertEqual(new_screen.codes.last(), self.access_code_345)
        self.assertEqual(new_screen.published, True)
        self.assertEqual(new_screen.author, self.test_user)















