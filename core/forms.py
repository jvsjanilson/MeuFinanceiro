from django import forms


class TextInputBootstrap(forms.TextInput):
    def __init__(self, attrs=None, render_value=False):
        old_attrs = attrs
        if attrs is None:
            attrs = {}
            attrs['class'] = 'form-control form-control-sm'
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] = old_attrs['class'] + ' form-control form-control-sm'
            except KeyError:
                attrs['class'] = 'form-control form-control-sm'
        super().__init__(attrs)



class SelectBootstrap(forms.Select):
    def __init__(self, attrs=None, render_value=False):
        old_attrs = attrs
        if attrs is None:
            attrs = {}
            attrs['class'] = 'form-select form-select-sm'
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] = old_attrs['class'] + ' form-select form-select-sm'
            except KeyError:
                attrs['class'] = 'form-select form-select-sm'
        super().__init__(attrs)



class NumberInputBootstap(forms.NumberInput):
    def __init__(self, attrs=None, render_value=False):
        old_attrs = attrs
        if attrs is None:
            attrs = {}
            attrs['class'] = 'form-control form-control-sm'
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] = old_attrs['class'] + ' form-control form-control-sm'
            except KeyError:
                attrs['class'] = 'form-control form-control-sm'
        super().__init__(attrs)


class CheckboxInputBootstrap(forms.CheckboxInput):
    def __init__(self, attrs=None, render_value=False):
        old_attrs = attrs
        if attrs is None:
            attrs = {}
            attrs['class'] = 'form-check-input'
        else:
            try:
                if attrs['class'] != "":
                    attrs['class'] = old_attrs['class'] + ' form-check-input'
            except KeyError:
                attrs['class'] = 'form-check-input'
        super().__init__(attrs)    
