from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
import random





class Profile(models.Model):

    DegreeOfEducation_CHOICES = (
        ("1", "زیردیپلم"),
        ("2", "دیپلم"),
        ("3", "فوق دیپلم"),
        ("4", "لیسانس"),
        ("5", "بالاتر از لیسانس"),
    )

    Post_CHOICES = (
        ("1", "مدیر"),
        ("2", "انبار دار"),
        ("3", "مراجعه کننده"),
        ("4", "راننده"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="نام کاربری")

    picture = models.ImageField(default='default.jpg', upload_to='profile_images',
                                blank=True, verbose_name="عکس"
                                )

    national_code = models.PositiveIntegerField(unique=True, verbose_name="کدملی",
                                                help_text='لطفا کد ملی  را وارد کنید',
                                                error_messages={'unique': u'این کد ملی قبلا ثبت شده است'}
                                                )

    age = models.PositiveIntegerField(verbose_name="سن")

    evidence = models.CharField(max_length=1, choices=DegreeOfEducation_CHOICES, default="4",
                                verbose_name="مدرک تحصیلی"
                                )

    phone = models.PositiveIntegerField(unique=True, verbose_name="شماره تلفن",
                                        help_text='شماره تلفن خود را با 10 رقم وارد کنید. مثل= 9386938466',
                                        error_messages={'unique': u'این شماره تلفن قبلا وارد شده است'}
                                        )

    phone2 = models.PositiveIntegerField(unique=True, null=True, blank=True, verbose_name="شماره تلفن دوم",
                                         help_text='شماره تلفن خود را با 10 رقم وارد کنید. مثل= 9386938466',
                                         error_messages={'unique': u'این شماره تلفن قبلا وارد شده است'}
                                         )

    address = models.TextField(max_length=600, null=True, blank=True, verbose_name="آدرس")
    post = models.CharField(max_length=1, choices=Post_CHOICES, default="4", verbose_name="سمت")



    def __str__(self):
        return "نام کاربری: " + self.user.username + "  ,  " + "سمت: " + self.post +\
               "  ,  " + "شناسه کاربری: " + str(self.id)

    def clean(self):
        to_string_national_code = str(self.national_code)
        if 10 < len(to_string_national_code) or len(to_string_national_code) < 9:
            raise ValidationError({'national_code': _("شماره ملی باید ده رقمی باشد")})

        to_string_phone = str(self.phone)
        if len(to_string_phone) != 10:
            raise ValidationError({'phone': _("شماره تلفن باید ده رقمی باشد")})

        if self.phone2:
            to_string_phone2 = str(self.phone2)
            if len(to_string_phone2) != 10:
                raise ValidationError({'phone2': _("شماره تلفن باید ده رقمی باشد")})

        if self.phone2:
            if self.phone2 == self.phone:
                raise ValidationError(_("هر دو شماره تلفن وارد شده، یکسان است"))

        to_string_age = str(self.age)
        if len(to_string_age) > 2:
            raise ValidationError({'age': _("سن باید حداکثر دو رقمی باشد")})

    class Meta:
        verbose_name = u'پروفایل'
        verbose_name_plural = verbose_name
        ordering = ('post',)


###########################################################################################


class Company(models.Model):
    profile = models.OneToOneField(Profile, null=True, on_delete=models.SET_NULL, verbose_name="مدیر")

    name = models.CharField(max_length=50, verbose_name="نام شرکت")

    phone = models.PositiveIntegerField(unique=True, verbose_name="شماره تلفن",
                                        help_text='شماره تلفن خود را با 10 رقم وارد کنید. مثل= 9386938466',
                                        error_messages={'unique': u'این شماره تلفن قبلا وارد شده است'}
                                        )

    phone2 = models.PositiveIntegerField(unique=True, null=True, blank=True, verbose_name="شماره تلفن دوم",
                                         help_text='شماره تلفن خود را با 10 رقم وارد کنید. مثل= 9386938466',
                                         error_messages={'unique': u'این شماره تلفن قبلا وارد شده است'}
                                         )

    address = models.TextField(max_length=600, verbose_name="ادرس شرکت")

    def __str__(self):
        return "نام شرکت: " + self.name

    def clean(self):
        if self.profile.post != '1':
            raise ValidationError(_("کاربر انتخاب شده مدیر نیست"))

        to_string_phone = str(self.phone)
        if len(to_string_phone) != 10:
            raise ValidationError({'phone': _("شماره تلفن باید ده رقمی باشد")})

        if self.phone2:
            to_string_phone2 = str(self.phone2)
            if len(to_string_phone2) != 10:
                raise ValidationError({'phone2': _("شماره تلفن باید ده رقمی باشد")})

        if self.phone2:
            if self.phone2 == self.phone:
                raise ValidationError(_("هر دو شماره تلفن وارد شده، یکسان است"))

    class Meta:
        verbose_name = u'شرکت'
        verbose_name_plural = verbose_name


###########################################################################################


class Warehouse(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="نام شرکت")

    name = models.CharField(max_length=50, verbose_name="نام انبار", unique=True,
                            error_messages={'unique': u'این نام قبلا وارد شده است'}
                            )
    possibilities = models.TextField(max_length=600, verbose_name="امکانات")

    def __str__(self):
        return "نام انبار: " + self.name + "  ,  " + "نام شرکت: " + self.company.name

    class Meta:
        verbose_name = u'انبار'
        verbose_name_plural = verbose_name
        ordering = ('company__name',)


###########################################################################################


class SelectWarehouse(models.Model):
    name = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="نام انبار")

    def __str__(self):
        return "نام انبار:" + self.name.name + "  ,  " + "نام شرکت: " + self.name.company.name

    class Meta:
        verbose_name = u'انتخاب انبار'
        verbose_name_plural = verbose_name


###########################################################################################


class Location(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="نام انبار")

    name = models.CharField(max_length=50, verbose_name="نام محل استقرار")

    def __str__(self):
        return "نام محل استقرار: " + self.name + "  ,  " + "نام انبار:" + self.warehouse.name

    class Meta:
        verbose_name = u'محل استقرار'
        verbose_name_plural = verbose_name
        ordering = ('warehouse__name',)


###########################################################################################


class Unit(models.Model):
    name = models.CharField(max_length=50, verbose_name="واحد", unique=True,
                            error_messages={'unique': u'این نام قبلا وارد شده است'}
                            )

    def __str__(self):
        return "نام واحد: " + self.name

    class Meta:
        verbose_name = u'واحد'
        verbose_name_plural = verbose_name


###########################################################################################


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="گروه", unique=True,
                            error_messages={'unique': u'این نام قبلا وارد شده است'}
                            )

    number = models.IntegerField(verbose_name="شماره گروه", help_text="شماره گروه سه رقمی را وارد کنید", unique=True,
                                 error_messages={'unique': u'این شماره گروه قبلا وارد شده است'}
                                 )

    def __str__(self):
        return "نام گروه: " + self.name

    def clean(self):
        to_string = str(self.number)
        if len(to_string) != 3:
            raise ValidationError({'number': _("شماره گروه باید سه رقمی باشد")})

    class Meta:
        verbose_name = u'گروه'
        verbose_name_plural = verbose_name


###########################################################################################


class WarehouseHandling(models.Model):

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="انتخاب انبار")
    title = models.CharField(max_length=50, verbose_name="عنوان انبار گردانی")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    finish_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان")
    comment = models.TextField(null=True, blank=True, verbose_name="توضیحات")

    def __str__(self):
        return "نام انبار: " + self.warehouse.name + "  ,  " + "عنوان انبار گردانی: " + self.title

    class Meta:
        verbose_name = u'انبار گردانی'
        verbose_name_plural = verbose_name
        ordering = ('warehouse__name', '-start_date',)

###########################################################################################




class Goods(models.Model):

    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL, verbose_name="انتخاب گروه کالا")

    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL, verbose_name="واحد")

    name = models.CharField(max_length=50, verbose_name="نام کالا", unique=True,
                            error_messages={'unique': u'این نام قبلا وارد شده است'}
                            )

    code = models.CharField(max_length=10, unique=True, verbose_name="کد",
                            help_text="برای تولید خودکار کد کالا، رقم 1 را وارد کنید.",
                            error_messages={'unique': u'این کد قبلا وارد شده است'}
                            )

    def __str__(self):
        return "نام: " + self.name + "  ,  " + "کد: " + str(self.code) + "  ,  " + "واحد:" + self.unit.name\
               + "  ,  " + "گروه:" + self.group.name


    def save(self, *args, **kwargs):
        rand = random.sample(range(0, 9), 4)
        str_rand = ""
        for i in rand:
            str_rand += str(i)

        self.code = str(self.group.number) + str_rand
        super(Goods, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'تعریف اولیه کالا'
        verbose_name_plural = verbose_name
        ordering = ('code',)





#######################################

class RegistrationOfGoods(models.Model):
    goods = models.ForeignKey(Goods, null=True, on_delete=models.SET_NULL, verbose_name="کالا")

    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.SET_NULL, verbose_name="انتخاب انبار")

    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, verbose_name="محل استقرار")


    value = models.IntegerField(blank=True, null=True, verbose_name="مقدار اولیه",
                                validators=[MaxValueValidator(9999999999)]
                                )

    min_value = models.IntegerField(blank=True, null=True, verbose_name="حداقل موجودی",
                                    validators=[MaxValueValidator(9999999999)]
                                    )

    max_value = models.IntegerField(blank=True, null=True, verbose_name="حداکثر موجودی",
                                    validators=[MaxValueValidator(9999999999)]
                                    )

    expiration = models.DateField(blank=True, null=True, verbose_name="تاریخ انقضا")

    value_D = models.IntegerField(blank=True, null=True, verbose_name="مقدار شمارش شده",
                                  validators=[MaxValueValidator(9999999999)]
                                  )
    value_Diff = models.IntegerField(blank=True, null=True, verbose_name="اختلاف مقدار",
                                     validators=[MaxValueValidator(9999999999)]
                                     )

    def __str__(self):
        return "نام: " + self.goods.name + "  ,  " + "کد: " + str(self.goods.code) + "  ,  " + "واحد:" + self.goods.unit.name\
               + "  ,  " + "انبار: " + self.warehouse.name + "  ,  " + "محل استقرار: " + self.location.name



    class Meta:
        verbose_name = u'ثبت کالا'
        verbose_name_plural = verbose_name
        ordering = ('warehouse__name', 'location__name')


###########################################################################################


class EntryGoods(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="شناسه ورود", unique=True,
                             error_messages={'unique': u'این شناسه قبلا وارد شده است'},
                             help_text='این شناسه توسط سرور تولید شده است.')
    registrationOfGoods = models.ForeignKey(RegistrationOfGoods, null=True, on_delete=models.SET_NULL,
                                            verbose_name="نام کالا")

    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.SET_NULL, verbose_name="انبار")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="انبار دار")
    driver_send = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL,
                                    verbose_name="راننده", related_name="driver_send"
                                    )
    SerialForDriver = models.CharField(max_length=10, verbose_name='شماره رسید انبار', blank=True,
                                       help_text='شماره رسید انبار = تاریخ امروز+'
                                                 'شناسه کاربری راننده+شماره ورود راننده'
                                       )


    sender = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL,
                               verbose_name="ارسال کننده", related_name="sender"
                               )


    value = models.IntegerField(verbose_name="مقدار", validators=[MaxValueValidator(9999999999)])
    date = models.DateField(auto_now_add=True, verbose_name="تاریخ ورود")

    def __str__(self):
        return "نام کالا: " + self.registrationOfGoods.goods.name + "  ,  " + "تاریخ ورود: " + str(self.date)\
               + "  ,  " + "نام انبار: " + self.warehouse.name

    def clean(self):
        if self.driver_send.post != '4':
            raise ValidationError(_("کاربر انتخاب شده راننده نیست"))

        if self.sender.post != '3':
            raise ValidationError(_("کاربر انتخاب شده مراجعه کننده نیست"))


    class Meta:
        verbose_name = u'ورود کالا'
        verbose_name_plural = verbose_name
        ordering = ('warehouse__name', '-date',)


##########################################

class SerialGoods_ENG(models.Model):
    entryGoods = models.ForeignKey(EntryGoods, null=True, on_delete=models.SET_NULL, verbose_name="ورود کالا")
    serial = models.CharField(max_length=40, unique=True,  verbose_name="سریال کالا",
                              error_messages={'unique': u'این سریال قبلا وارد شده است'})

    class Meta:
        verbose_name = u'سریال ورود کالا'
        verbose_name_plural = verbose_name
        ordering = ('serial', )


###########################################################################################


class ExitGoods(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="شناسه خروج", unique=True,
                             error_messages={'unique': u'این شناسه قبلا وارد شده است'},
                             help_text='این شناسه توسط سرور تولید شده است.')
    registrationOfGoods = models.ForeignKey(RegistrationOfGoods, null=True, on_delete=models.SET_NULL,
                                            verbose_name="نام کالا")
    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.SET_NULL, verbose_name="انبار")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="انبار دار", blank=True)
    driver_receive = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, verbose_name="راننده",
                                       related_name="driver_receive", blank=True
                                       )

    SerialForDriver = models.CharField(max_length=10, verbose_name='شماره حواله انبار', blank=True,
                                       help_text='شماره حواله انبار = تاریخ امروز+'
                                                 'شناسه کاربری راننده+شماره خروج راننده')

    receiver = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, verbose_name="دریافت کننده",
                                 related_name="receiver"
                                 )


    value = models.IntegerField(verbose_name="مقدار", validators=[MaxValueValidator(9999999999)])


    date = models.DateField(auto_now_add=True, verbose_name="تاریخ خروج")

    address = models.TextField(verbose_name='ادرس', blank=True)

    def __str__(self):
        return "نام کالا: " + self.registrationOfGoods.goods.name + "  ,  " + "تاریخ خروج: " + str(self.date)\
               + "  ,  " + "نام انبار: " + self.warehouse.name

    def clean(self):

        if self.receiver.post != '3':
            raise ValidationError(_("کاربر انتخاب شده مراجعه کننده نیست"))


    class Meta:
        verbose_name = u'خروج کالا'
        verbose_name_plural = verbose_name
        ordering = ('warehouse__name', '-date',)



##########################################

class SerialGoods(models.Model):
    exitGoods = models.ForeignKey(ExitGoods, null=True, on_delete=models.SET_NULL, verbose_name="خروج کالا")
    serial = models.CharField(max_length=40, unique=True,  verbose_name="سریال کالا",
                              error_messages={'unique': u'این سریال قبلا وارد شده است'})

    class Meta:
        verbose_name = u'سریال خروج کالا'
        verbose_name_plural = verbose_name
        ordering = ('serial', )

###########################################################################################


class Requestgoods(models.Model):

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="انبار دار", blank=True)

    req_CHOICES = (
        ("2", "رد"),
        ("1", "قبول"),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="درخواست دهنده")

    goods = models.ForeignKey(Goods, null=True, on_delete=models.SET_NULL, verbose_name="کالا")


    value = models.IntegerField(verbose_name="مقدار", validators=[MaxValueValidator(9999999999)])
    date = models.DateField(auto_now_add=True, verbose_name="تاریخ درخواست")
    result = models.CharField(max_length=1, choices=req_CHOICES, null=True, blank=True, verbose_name="نتیجه درخواست")

    comment = models.TextField(max_length=600, null=True, blank=True, verbose_name='علت رد شدن')
    serial = models.IntegerField(unique=True, error_messages={'unique': u'این شناسه قبلا وارد شده است'},
                                 help_text='این شناسه توسط سرور تولید شده است.',
                                 verbose_name='کد رهگیری(شناسه خروج)',
                                 null=True, blank=True)

    address = models.TextField(verbose_name='ادرس')

    def __str__(self):
        return "نام کالا: " + self.goods.name

    def clean(self):
        if self.profile.post != '3':
            raise ValidationError(_("کاربر انتخاب شده مراجعه کننده نیست"))

    class Meta:
        verbose_name = u'درخواست کالا'
        verbose_name_plural = verbose_name
        ordering = ('profile__user__username', '-date', 'result',)













