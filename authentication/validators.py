from django.core.exceptions import ValidationError

def validate_age(age):
    if age < 15:
        raise ValidationError(
            f"{age} is not an acceptable age to sign in. Users must be at least 15 years old."
        )
