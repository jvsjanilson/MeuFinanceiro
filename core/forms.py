from django import forms


class TextInputBootstrap(forms.TextInput):
    def __init__(self, attrs=None, render_value=False):
        attrs = {'class': 'form-control'}
        super().__init__(attrs)


class SelectBootstrap(forms.Select):
    def __init__(self, attrs=None, render_value=False):
        attrs = {'class': 'form-select'}
        super().__init__(attrs)


class NumberInputBootstap(forms.NumberInput):
    def __init__(self, attrs=None, render_value=False):
        attrs = {'class': 'form-control'}
        super().__init__(attrs)


class CheckboxInputBootstrap(forms.CheckboxInput):
    def __init__(self, attrs=None, render_value=False):
        attrs = {'class': 'form-check-input'}
        super().__init__(attrs)