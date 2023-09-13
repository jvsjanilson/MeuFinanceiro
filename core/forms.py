from django import forms


class TextInputBootstrap(forms.TextInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'form-control form-control-sm'}
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] += ' form-control form-control-sm'
            except KeyError:
                attrs['class'] = 'form-control form-control-sm'
        super().__init__(attrs)


class TextareaInputBootstrap(forms.Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'form-control form-control-sm'}
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] += ' form-control form-control-sm'
            except KeyError:
                attrs['class'] = 'form-control form-control-sm'
        super().__init__(attrs)


class SelectBootstrap(forms.Select):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'form-select form-select-sm'}
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] += ' form-select form-select-sm'
            except KeyError:
                attrs['class'] = 'form-select form-select-sm'
        super().__init__(attrs)


class NumberInputBootstap(forms.NumberInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'form-control form-control-sm'}
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] += ' form-control form-control-sm'
            except KeyError:
                attrs['class'] = 'form-control form-control-sm'
        super().__init__(attrs)


class CheckboxInputBootstrap(forms.CheckboxInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'form-check-input'}
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] += ' form-check-input'
            except KeyError:
                attrs['class'] = 'form-check-input'
        super().__init__(attrs)    


class DateInputBootstrap(forms.DateInput):

    def __init__(self, attrs=None, format=None):
        self.format = format or None
        if attrs is None:
            attrs = {'class': 'form-control form-control-sm', 'type': 'date'}
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] += ' form-control form-control-sm'
                if attrs['type'] != "":
                    attrs['type'] = 'date'
            except KeyError:
                attrs['class'] = 'form-control form-control-sm'
                attrs['type'] = 'date'
        super().__init__(attrs, format)
