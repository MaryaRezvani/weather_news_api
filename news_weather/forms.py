from django import forms
from .regions import regions  # اضافه کردن لیست استان‌ها و شهرها

class CityForm(forms.Form):
    # تعریف STATE_CHOICES به عنوان یک متغیر کلاس
    STATE_CHOICES = [(state, state) for state in regions.keys()]
    
    # انتخاب استان
    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        label="انتخاب استان",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'state-select'})
    )
    
    # انتخاب شهر
    city = forms.ChoiceField(
        choices=[],  # لیست خالی برای شهرها
        label="انتخاب شهر",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # اگر داده‌ای برای استان ارسال شده باشد
        if 'state' in self.data:
            state = self.data['state']
            self.fields['city'].choices = [(city, city) for city in regions.get(state, [])]
        else:
            # اگر داده‌ای برای استان ارسال نشده باشد، لیست شهرها خالی می‌ماند
            self.fields['city'].choices = []
        
        # اگر هیچ انتخابی وجود نداشت، یکی از استان‌ها را به عنوان پیش‌فرض انتخاب کنید
        if not self.data.get('state') and self.STATE_CHOICES:
            default_state = self.STATE_CHOICES[0][0]  # اولین استان را به عنوان پیش‌فرض انتخاب کنید
            self.fields['state'].initial = default_state  # استان پیش‌فرض
            self.fields['city'].choices = [(city, city) for city in regions.get(default_state, [])]  # شهرهای استان پیش‌فرض
            self.fields['city'].initial = self.fields['city'].choices[0][0]  # انتخاب پیش‌فرض شهر از بین شهرهای استان پیش‌فرض
