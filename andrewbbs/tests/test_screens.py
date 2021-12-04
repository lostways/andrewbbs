from django.test import TestCase
from ..models import Screen
from ..models import AccessCode
from ..models import User

# Create your tests here.

class ScreenTestCase(TestCase):
    
    def setUp(self):
        self.access_code_123 = AccessCode.objects.create(code="testCaseCode123")
        self.access_code_345 = AccessCode.objects.create(code="testCaseCode345")
        self.access_code_679 = AccessCode.objects.create(code="testCaseCode678")

        test_user = User.objects.create(username="screentest", password="screentest")

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

