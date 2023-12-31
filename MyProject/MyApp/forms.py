from django import forms
from . import models
import re





class RegisterAdminForm(forms.Form):
    username = forms.CharField(max_length=20, label="نام کاربری")
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="رمز عبور")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="تکرار رمز عبور")

    def clean(self):
        # data from the form is fetched using super function
        super(RegisterAdminForm, self).clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        flag_username = 0
        while True:
            if (len(username) < 5):
                flag_username = -1
                break
            elif not re.search("[a-z]", username):
                flag_username = -1
                break
            elif not re.search("[A-Z]", username):
                flag_username = -1
                break
            elif not re.search("[_@]", username):
                flag_username = -1
                break
            else:
                flag_username = 0
                break

        if flag_username == -1:
            self._errors['username'] = self.error_class([
                'نام کاربری نامعتبر'
                '(نام کاربری معتبر: حداقل طول5- دارای حروف بزرگ و کوچک انگلیسی- دارای حداقل یک مورد از @  یا _ )'])

        flag = 0
        while True:
            if (len(password) < 8):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@]", password):
                flag = -1
                break
            else:
                flag = 0
                break

        if flag == -1:
            self._errors['password'] = self.error_class([
            'پسورد نامعتبر'
            '(پسورد معتبر: حداقل طول8- دارای حروف بزرگ و کوچک انگلیسی-دارای رقم -'
            'دارای حداقل یک مورد از @  یا _ )'])

        if password != password2:
            self._errors['password2'] = self.error_class([
                'عدم تطابق پسورد'])

        # return any errors if found
        return self.cleaned_data








class change_passwordForm(forms.Form):
    old_password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="رمز عبور قبلی")
    new_password1 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="رمز عبور جدید")
    new_password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="تکرار رمز عبور جدید")

    def clean(self):
        # data from the form is fetched using super function
        super(change_passwordForm, self).clean()

        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        flag = 0
        while True:
            if (len(new_password1) < 8):
                flag = -1
                break
            elif not re.search("[a-z]", new_password1):
                flag = -1
                break
            elif not re.search("[A-Z]", new_password1):
                flag = -1
                break
            elif not re.search("[0-9]", new_password1):
                flag = -1
                break
            elif not re.search("[_@]", new_password1):
                flag = -1
                break
            else:
                flag = 0
                break

        if flag == -1:
            self._errors['new_password1'] = self.error_class([
            'پسورد نامعتبر'
            '(پسورد معتبر: حداقل طول8- دارای حروف بزرگ و کوچک انگلیسی-دارای رقم -'
            'دارای حداقل یک مورد از @  یا _ )'])

        if new_password1 != new_password2:
            self._errors['new_password2'] = self.error_class([
                'عدم تطابق پسورد'])

        # return any errors if found
        return self.cleaned_data








class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="نام کاربری")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="رمز عبور")








################################Driver##############################################

class ExitGoods_view_ByFilter_SerialForDriver_DRIVER(forms.Form):

    SerialForDriver = forms.CharField(label='شماره حواله انبار',
                                      widget=forms.TextInput(attrs={'placeholder': 'شماره حواله انبار = تاریخ امروز '
                                                                                   '+ شناسه کاربری راننده + '
                                                                                   'شماره خروج راننده'}))



class EntryGoods_view_ByFilter_SerialForDriver_DRIVER(forms.Form):

    SerialForDriver = forms.CharField(label='شماره رسید انبار',
                                      widget=forms.TextInput(attrs={'placeholder': 'شماره رسید انبار = تاریخ امروز '
                                                                                   '+ شناسه کاربری راننده + '
                                                                                   'شماره ورود راننده'}))





################################Refferd##############################################




class RequestgoodsForm(forms.ModelForm):

    class Meta:
        model = models.Requestgoods
        fields = '__all__'







class Requestgoods_All_ByFilter_Date_Refferd_FORM(forms.Form):
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')








#####################################Warehouse###################################################



class Select_WarehouseForm(forms.ModelForm):

    class Meta:
        model = models.SelectWarehouse
        fields = '__all__'





class GoodsCreateForm(forms.ModelForm):

    expiration = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                 required=False, label='تاریخ انقضاء')

    class Meta:
        model = models.RegistrationOfGoods
        fields = '__all__'










class alarm_expirationForm(forms.Form):

    CHOICES = [('1', 'انبار جاری'),
               ('2', 'تمام انبارهای شرکت')]
    select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="")





class alarm_min_valueForm(forms.Form):

    CHOICES = [('1', 'انبار جاری'),
               ('2', 'تمام انبارهای شرکت')]
    select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="")






class alarm_max_valueForm(forms.Form):

    CHOICES = [('1', 'انبار جاری'),
               ('2', 'تمام انبارهای شرکت')]
    select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="")





class Goods_viewByCode_FORM(forms.Form):

    code = forms.CharField(max_length=18, label='کد کالا')


class Goods_viewByName_FORM(forms.Form):

    name = forms.CharField(max_length=30, label='نام کالا')

















class DefineGoods_Create_FORM(forms.ModelForm):

    unit = forms.ModelChoiceField(queryset=models.Unit.objects.all(), label='واحد')

    class Meta:
        model = models.Goods
        fields = '__all__'








class DefineGoods_viewByCode_FORM(forms.Form):

    code = forms.CharField(max_length=18, label='کد کالا')







class DefineGoods_viewByName_FORM(forms.Form):

    name = forms.CharField(max_length=30, label='نام کالا')





############################@@@@@@@@@@@@@@@@@@@########################

















class UnitForm(forms.ModelForm):

    class Meta:
        model = models.Unit
        fields = '__all__'







class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = '__all__'







class EntryGoodsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(EntryGoodsForm, self).__init__(*args, **kwargs)



    class Meta:
        model = models.EntryGoods
        fields = '__all__'



    def clean(self):
        # data from the form is fetched using super function
        super(EntryGoodsForm, self).clean()

        user = self.cleaned_data.get('user')
        u = self.request.user
        if user != u:
            self._errors['user'] = self.error_class([
                ' کاربر انتخاب شده اشتباه است! لطفا نام کاربری خودتان را انتخاب کنید'])

        return self.cleaned_data







class EntryGoods_view_ByFilter_WarehouseName_Form(forms.Form):

    WarehouseName = forms.ModelChoiceField(queryset=models.Warehouse.objects.all(), label='نام انبار')






class EntryGoods_view_ByFilter_DriverName_Form(forms.Form):
    DriverName = forms.ModelChoiceField(queryset=models.Profile.objects.filter(post='4'), label='نام راننده')






class EntryGoods_view_ByFilter_ReferredName_Form(forms.Form):
    ReferredName = forms.ModelChoiceField(queryset=models.Profile.objects.filter(post='3'), label='نام مراجعه کننده')






class EntryGoods_view_ByFilter_WarehouseName_Date_Form(forms.Form):
    WarehouseName = forms.ModelChoiceField(queryset=models.Warehouse.objects.all(), label='نام انبار')
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')






class EntryGoods_view_ByFilter_WarehouseName_Date_DriverName_Form(forms.Form):
    WarehouseName = forms.ModelChoiceField(queryset=models.Warehouse.objects.all(), label='نام انبار')
    DriverName = forms.ModelChoiceField(queryset=models.Profile.objects.filter(post='4'), label='نام راننده')
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')






class SearchSerial_ENG_FORM(forms.Form):

    serial = forms.CharField(max_length=40, label='سریال کالا وارد شده')






class EntryGoods_view_ByFilter_SerialForDriver(forms.Form):

    SerialForDriver = forms.CharField(label='سریال ورود راننده',
                                      widget=forms.TextInput(attrs={'placeholder': 'سریال ورود راننده = تاریخ امروز '
                                                                                   '+ شناسه کاربری راننده + '
                                                                                   'شماره ورود راننده'}))


















class ExitGoodsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ExitGoodsForm, self).__init__(*args, **kwargs)


    class Meta:
        model = models.ExitGoods
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
        }


    def clean(self):
        # data from the form is fetched using super function
        super(ExitGoodsForm, self).clean()

        user = self.cleaned_data.get('user')
        u = self.request.user
        if user != u:
            self._errors['user'] = self.error_class([
                ' کاربر انتخاب شده اشتباه است! لطفا نام کاربری خودتان را انتخاب کنید'])

        return self.cleaned_data





class ExitGoods_view_ByFilter_SerialForDriver(forms.Form):

    SerialForDriver = forms.CharField(label='سریال خروج راننده',
                                      widget=forms.TextInput(attrs={'placeholder': 'سریال خروج راننده = تاریخ امروز '
                                                                                   '+ شناسه کاربری راننده + '
                                                                                   'شماره خروج راننده '
                                                                    }))







class ExitGoods_view_ByFilter_WarehouseName_Form(forms.Form):

    WarehouseName = forms.ModelChoiceField(queryset=models.Warehouse.objects.all(), label='نام انبار')






class ExitGoods_view_ByFilter_DriverName_Form(forms.Form):
    DriverName = forms.ModelChoiceField(queryset=models.Profile.objects.filter(post='4'), label='نام راننده')






class ExitGoods_view_ByFilter_ReferredName_Form(forms.Form):
    ReferredName = forms.ModelChoiceField(queryset=models.Profile.objects.filter(post='3'), label='نام مراجعه کننده')






class ExitGoods_view_ByFilter_WarehouseName_Date_Form(forms.Form):
    WarehouseName = forms.ModelChoiceField(queryset=models.Warehouse.objects.all(), label='نام انبار')
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')





class ExitGoods_view_ByFilter_WarehouseName_Date_DriverName_Form(forms.Form):
    WarehouseName = forms.ModelChoiceField(queryset=models.Warehouse.objects.all(), label='نام انبار')
    DriverName = forms.ModelChoiceField(queryset=models.Profile.objects.filter(post='4'), label='نام راننده')
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')



class SearchSerial_FORM(forms.Form):

    serial = forms.CharField(max_length=40, label='سریال کالا خارج شده')

























class Requestgoods_All_ByFilter_Date_FORM(forms.Form):
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')






class Requestgoods_respondForm(forms.ModelForm):

    class Meta:
        model = models.Requestgoods
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 15}),
        }




###################################################################################################




















class WarehouseHandling_Form(forms.ModelForm):

    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label=' تاریخ شروع')
    finish_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label=' تاریخ پایان', required=False)
    class Meta:
        model = models.WarehouseHandling
        fields = '__all__'






class WarehouseHandling_FilterByDate_Form(forms.Form):
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='از تاریخ ')
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='تا تاریخ ')



class WarehouseHandling_GoodsValue(forms.Form):
    GoodsValue = forms.IntegerField(label='موجودی انبار')







class Requestgoods_all_items_SearchByCode_FORM(forms.Form):
    serial = forms.IntegerField(label='کد رهگیری(شناسه خروج)')


