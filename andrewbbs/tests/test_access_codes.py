from django.test import TestCase
from ..models import AccessCode

# Create your tests here.

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

