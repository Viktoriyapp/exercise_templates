from collections.abc import Callable
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def range_validator(value: Decimal):
    if not 0 <= value <= 1000: # hardcoded values here is not good
        raise ValidationError("The value must be in the range 0-1000") # message hardcoded as well not good
    # because we want to reuse it

#Better option
def range_validator2(min_value: int, max_value: int) -> Callable:# also we can add a custom message
    def validator(value) -> None:
        if not min_value <= value <= max_value:
            raise ValidationError(f"The value must be in the range {min_value} - {max_value}")

    return validator # like using a decorator

#Even better
@deconstructible
class RangeValidator:
    def __init__(self, min_value: int, max_value: int, message: str='') -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    @property
    def min_value(self):
        return self.__min_value

    @min_value.setter
    def min_value(self, value):
        if value < 0:
            raise ValueError('Min value cannot be null')
            # ValueError bcs this is not a validation that happens during runtime with user

        self.__min_value = value

    def __call__(self, value:Decimal) -> None: # we overwrite it so that it can be called after making an instance
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

