from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_iranian_cellphone_number(value):
    pattern = r"^09\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid Iranian cellphone number.")


# Validator that ensures only A-Z and a-z are allowed
english_validator = RegexValidator(
    regex=r"^[A-Za-z]+$",
    message="Only letters (A-Z) and (a-z) are allowed.",
    code="invalid_english",
)

# Validator that ensures only English and Persian letters are allowed
english_persian_validator = RegexValidator(
    regex=r"^[A-Za-z\u0600-\u06FF]+$",
    message="Only English(A-Z) and Persian(ی-ا) characters are allowed.",
    code="invalid_english_persian",
)

iranian_phone_validator = RegexValidator(
    regex=r"^\+98(9\d{9})$",
    message="Enter a valid Iranian phone number in the format +98912xxxxxxx.",
    code="invalid_iranian_phone",
)


def validate_iranian_national_code(value):
    """
    Validates an Iranian national code (کد ملی).
    """
    if not re.match(r"^\d{10}$", value):
        raise ValidationError("کد ملی باید ۱۰ رقم باشد.")

    # Check for invalid national codes (e.g., all digits the same)
    if value in [
        "0000000000",
        "1111111111",
        "2222222222",
        "3333333333",
        "4444444444",
        "5555555555",
        "6666666666",
        "7777777777",
        "8888888888",
        "9999999999",
    ]:
        raise ValidationError("کد ملی وارد شده معتبر نیست.")

    # Checksum validation
    check = int(value[9])  # آخرین رقم (عدد کنترل)
    s = sum(
        int(value[i]) * (10 - i) for i in range(9)
    )  # مجموع ضرب ارقام در وزن‌های مربوطه
    remainder = s % 11

    if not (
        (remainder < 2 and check == remainder)
        or (remainder >= 2 and check + remainder == 11)
    ):
        raise ValidationError("کد ملی وارد شده معتبر نیست.")
