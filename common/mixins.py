from typing import Any


class DisableFormFieldsMixin:
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].disabled = True