from django.shortcuts import render
from . import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import *
from django.contrib.auth.models import Group
from datetime import date
from django.db.models import Q     #for filter by or
from django.db.models import F     #for filter by two field
import random





def index(request):
    return render(request, 'index.html', {})



def about(request):
    return render(request, 'about.html', {})






def RegisterAdmin(request):
    form = forms.RegisterAdminForm()
    message = ''
    admin_count = models.Profile.objects.filter(post='1').count()
    if admin_count == 0:
        if request.method == 'POST':
            form = forms.RegisterAdminForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email='',
                    password=form.cleaned_data['password'],
                    first_name='',
                    last_name='',
                )
                if user is not None:
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    message ='ثبت نام با موفعقیت انجام شد.'
                else:
                    message = 'ثبت نام ناموفق'

        return render(
            request, 'RegisterAdmin.html', context={'form': form, 'message': message})

    else:
        return render(
            request, 'RegisterAdmin.html', context={'form': '', 'message': ''})




def admin(request):
    pass




def logout_user(request):
    logout(request)
    return redirect('/')



def login_page(request):
    logout(request)
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)

                p = models.Profile.objects.get(user=user)
                if p.post == '2':
                    return redirect('/warehousekeeper/')
                elif p.post == '3':
                    return redirect('/referred/')
                elif p.post == '4':
                    return HttpResponseRedirect('/driver/')
                else:
                    message = 'کاربر وارد شده، وجود ندارد'
            else:
                message = 'ورود ناموفق'
    return render(
        request, 'login.html', context={'form': form, 'message': message})







@login_required(login_url='/login/')
def change_password(request):
    form = forms.change_passwordForm()
    message = ''
    if request.method == 'POST':
        form = forms.change_passwordForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.user.username,
                password=form.cleaned_data['old_password'],
            )
            if user is not None:
                new_password = form.cleaned_data['new_password1']
                username = request.user.username
                u = User.objects.get(username__exact=username)
                u.set_password(new_password)
                u.save()
                message = 'رمز عبور با موفعقیت تقییر کرد'

            else:
                message = 'لطفا رمز قبلی خود را به درستی وارد کنید'
    return render(
        request, 'change-password.html', context={'form': form, 'message': message})








@login_required(login_url='/login/')
def viewprofile(request):
    context = {}
    u = request.user
    u_post = models.Profile.objects.get(user=u)
    context["user"] = models.User.objects.get(username=u.username)
    context["profile"] = models.Profile.objects.get(user=u)

    if u_post.post == "2":
        return render(request, "ViewProfile_Warehousekeeper.html", context)
    elif u_post.post == "3":
        return render(request, "ViewProfile_Referred.html", context)
    else:
        return render(request, "ViewProfile_Driver.html", context)








##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
################################################################################################

@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def warehousekeeper(request):
    context = {}

    count = models.SelectWarehouse.objects.all().count()
    if count == 0:
        w = models.Warehouse.objects.all()[0]
        sw = models.SelectWarehouse.objects.create(name=w)
        sw.save()

    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    context["SelectWarehouse_Name"] = models.Warehouse.objects.filter(id=sw_id)
    return render(request, 'WarehouseKeeper_Profile.html', context)





@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def selectwarehouse(request):
    context = {}
    message = ''

    obj = models.SelectWarehouse.objects.all()[0]

    form = forms.Select_WarehouseForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        message = 'انبار با موفعقیت انتخاب شد'

    context["form"] = form
    context["message"] = message
    return render(request, "Select_Warehouse.html", context)






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def GoodsCreate(request):
    context = {}
    message = ''

    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)
    form = forms.GoodsCreateForm(request.POST or None, initial={'warehouse':w,})
    form.fields["location"].queryset = models.Location.objects.filter(warehouse=w)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=w.id)

    if form.is_valid():
        l = form.cleaned_data['location']
        g = form.cleaned_data['goods']
        check = models.RegistrationOfGoods.objects.filter(warehouse=w).filter(location=l) \
            .filter(goods=g).count()
        if check == 0:
            message = ' کالا با موفعقیت ثبت شد'
            form.save()
        else:
            message = ' کالا وارد شده برای محل استقرار انتخاب شده، قبلا ثبت شده است.'

    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GoodsCreate.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsview(request):
    context = {}
    message = ''
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name
    context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse=sw_id)
    count = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).count()
    if count == 0:
        message = "کالایی در این انبار وجود ندارد"
    context["message"] = message
    context["alarm"] = ""
    context["filterdate"] = ""

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GoodsView.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsview_NAME(request):
    context = {}
    message = ''
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name
    context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).order_by('goods__name')
    count = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).count()
    if count == 0:
        message = "کالایی در این انبار وجود ندارد"
    context["message"] = message
    context["alarm"] = ""
    context["filterdate"] = ""

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GoodsView.html", context)






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsview_MaxValue(request):
    context = {}
    message = ''
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name
    context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).order_by('-value')
    count = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).count()
    if count == 0:
        message = "کالایی در این انبار وجود ندارد"
    context["message"] = message
    context["alarm"] = ""
    context["filterdate"] = ""

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GoodsView.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsview_MinValue(request):
    context = {}
    message = ''
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name
    context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).order_by('value')
    count = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).count()
    if count == 0:
        message = "کالایی در این انبار وجود ندارد"
    context["message"] = message
    context["alarm"] = ""
    context["filterdate"] = ""

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GoodsView.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsview_CODE(request):
    context = {}
    message = ''
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name
    context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).order_by('goods__code')
    count = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).count()
    if count == 0:
        message = "کالایی در این انبار وجود ندارد"
    context["message"] = message
    context["alarm"] = ""
    context["filterdate"] = ""

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GoodsView.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsdelete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.RegistrationOfGoods, id=id)

    if request.method == "POST":
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'

        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Goodsdelete.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goodsupdate(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.RegistrationOfGoods, id=id)
    obj_warehouse = obj.warehouse
    obj_location = obj.location
    obj_goods = obj.goods


    form = forms.GoodsCreateForm(request.POST or None, instance=obj)

    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)
    form.fields["location"].queryset = models.Location.objects.filter(warehouse=w)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=w.id)

    if form.is_valid():
        w_form = form.cleaned_data['warehouse']
        l = form.cleaned_data['location']
        g = form.cleaned_data['goods']
        check = models.RegistrationOfGoods.objects.filter(warehouse=w).filter(location=l) \
            .filter(goods=g).count()

        if w_form == obj_warehouse and l == obj_location and g == obj_goods:
            form.save()
            message = 'با موفعقیت ویرایش شد'
        elif check == 0:
            form.save()
            message = 'با موفعقیت ویرایش شد'
        else:
            message = ' کالا وارد شده برای محل استقرار انتخاب شده، قبلا ثبت شده است.'

        context['update'] = 'Yes'

    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Goodsupdate.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def alarm_expiration(request):
    context = {}
    message = ''
    form = forms.alarm_expirationForm(request.POST or None)

    if form.is_valid():
        select = form.cleaned_data['select']

        if select == '1':
            sw = models.SelectWarehouse.objects.all()[0]
            sw_id = sw.name
            today = date.today()

            context["dataset"] = models.RegistrationOfGoods.objects\
                .filter(warehouse=sw_id)\
                .filter(Q(expiration__year=today.year, expiration__month=today.month) |
                        Q(expiration__year=today.year, expiration__month__lte=today.month))

            count = models.RegistrationOfGoods.objects\
                .filter(warehouse=sw_id)\
                .filter(Q(expiration__year=today.year, expiration__month=today.month)
                        | Q(expiration__year=today.year, expiration__month__lte=today.month)).count()

            if count == 0:
                message = "کالایی که تاریخ انقضاء آن نزدیک باشد، وجود ندارد"

        if select == '2':
            today = date.today()

            context["dataset"] = models.RegistrationOfGoods.objects\
                .filter(Q(expiration__year=today.year, expiration__month=today.month)
                        | Q(expiration__year=today.year, expiration__month__lte=today.month))

            count = models.RegistrationOfGoods.objects\
                .filter(Q(expiration__year=today.year, expiration__month=today.month)
                        | Q(expiration__year=today.year, expiration__month__lte=today.month)).count()

            if count == 0:
                message = "کالایی که تاریخ انقضاء آن نزدیک باشد، وجود ندارد"

        context["message"] = message
        context["alarm"] = " کالاهای موجود در انبار که تاریخ انقضاء آنها گذشته یا تاریخ انقضاء آنها نزدیک است"
        return render(request, "GoodsView.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "alarm_expiration.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def alarm_min_value(request):
    context = {}
    message = ''
    form = forms.alarm_min_valueForm(request.POST or None)

    if form.is_valid():
        select = form.cleaned_data['select']

        if select == '1':
            sw = models.SelectWarehouse.objects.all()[0]
            sw_id = sw.name
            context["dataset"] = models.RegistrationOfGoods.objects \
                .filter(warehouse=sw_id) \
                .filter(value__lte=F('min_value'))

            count = models.RegistrationOfGoods.objects \
                .filter(warehouse=sw_id) \
                .filter(value__lte=F('min_value')).count()

            if count == 0:
                message = "کالایی که موجودی آن به حداقل رسیده باشد، وجود ندارد"


        if select == '2':
            context["dataset"] = models.RegistrationOfGoods.objects.filter(value__lte=F('min_value'))
            count = models.RegistrationOfGoods.objects.filter(value__lte=F('min_value')).count()

            if count == 0:
                message = "کالایی که موجودی آن به حداقل رسیده باشد، وجود ندارد"


        context["message"] = message
        context["alarm"] = "نمایش کالاهایی که موجودی آنها به حداقل رسیده است"
        return render(request, "GoodsView.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "alarm_min_value.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def alarm_max_value(request):
    context = {}
    message = ''
    form = forms.alarm_max_valueForm(request.POST or None)

    if form.is_valid():
        select = form.cleaned_data['select']

        if select == '1':
            sw = models.SelectWarehouse.objects.all()[0]
            sw_id = sw.name
            context["dataset"] = models.RegistrationOfGoods.objects \
                .filter(warehouse=sw_id) \
                .filter(value__gte=F('max_value'))

            count = models.RegistrationOfGoods.objects \
                .filter(warehouse=sw_id) \
                .filter(value__gte=F('max_value')).count()

            if count == 0:
                message = "کالایی که موجودی آن به حداکثر رسیده باشد، وجود ندارد"


        if select == '2':
            context["dataset"] = models.RegistrationOfGoods.objects.filter(value__gte=F('max_value'))
            count = models.RegistrationOfGoods.objects.filter(value__gte=F('max_value')).count()

            if count == 0:
                message = "کالایی که موجودی آن به حداکثر رسیده باشد، وجود ندارد"


        context["message"] = message
        context["alarm"] = "نمایش کالاهایی که موجودی آنها به حداکثر رسیده است"
        return render(request, "GoodsView.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "alarm_max_value.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goods_viewByCode(request):
    context = {}
    message = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    form = forms.Goods_viewByCode_FORM(request.POST or None)

    if form.is_valid():
        c = form.cleaned_data['code']
        context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
            .filter(goods__code=c)
        count = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
            .filter(goods__code=c).count()
        if count == 0:
            message = "کالایی با این کد وجود ندارد"

        context["message"] = message
        context["alarm"] = ''
        return render(request, "GoodsView.html", context)

    context["form"] = form


    return render(request, "Goods_viewByCode.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goods_viewByName(request):
    context = {}
    message = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    form = forms.Goods_viewByName_FORM(request.POST or None)

    if form.is_valid():
        n = form.cleaned_data['name']
        context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
            .filter(goods__name__contains=n)
        count = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
            .filter(goods__name__contains=n).count()
        if count == 0:
            message = "کالایی با این نام وجود ندارد"

        context["message"] = message
        context["alarm"] = ''
        return render(request, "GoodsView.html", context)

    context["form"] = form

    return render(request, "Goods_viewByName.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Goods_viewByName_AllWarehouse(request):
    context = {}
    message = ''
    form = forms.Goods_viewByName_FORM(request.POST or None)

    if form.is_valid():
        n = form.cleaned_data['name']
        context["dataset"] = models.RegistrationOfGoods.objects.filter(goods__name__contains=n)
        count = models.RegistrationOfGoods.objects.filter(goods__name__contains=n).count()
        if count == 0:
            message = "کالایی با این نام وجود ندارد"

        context["message"] = message
        context["alarm"] = 'نمایش کالا در تمام انبار'
        return render(request, "GoodsView.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Goods_viewByName.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def DefineGoods_Create(request):
    context = {}
    message = ''

    form = forms.DefineGoods_Create_FORM(request.POST or None)
    if form.is_valid():
        message = ' کالا با موفعقیت ثبت شد'
        form.save()
    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "DefineGoods_Create.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def DefineGoods_view(request):
    context = {}
    message = ''
    context["dataset"] = models.Goods.objects.all()
    count = models.Goods.objects.all().count()
    if count == 0:
        message = "کالایی تعریف نشده است"
    context["message"] = message


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "DefineGoods_view.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def DefineGoods_delete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.Goods, id=id)

    if request.method == "POST":
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'

        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "DefineGoods_delete.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def DefineGoods_update(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.Goods, id=id)

    form = forms.DefineGoods_Create_FORM(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        message = 'با موفعقیت ویرایش شد'
        context['update'] = 'Yes'

    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "DefineGoods_update.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def DefineGoods_viewByCode(request):
    context = {}
    message = ''
    form = forms.DefineGoods_viewByCode_FORM(request.POST or None)

    if form.is_valid():
        c = form.cleaned_data['code']
        context["dataset"] = models.Goods.objects.filter(code=c)
        count = models.Goods.objects.filter(code=c).count()
        if count == 0:
            message = "کالایی با این کد وجود ندارد"


        context["message"] = message
        return render(request, "DefineGoods_view.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "DefineGoods_viewByCode.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def DefineGoods_viewByName(request):
    context = {}
    message = ''
    form = forms.DefineGoods_viewByName_FORM(request.POST or None)

    if form.is_valid():
        n = form.cleaned_data['name']
        context["dataset"] = models.Goods.objects.filter(name__contains=n)
        count = models.Goods.objects.filter(name__contains=n).count()
        if count == 0:
            message = "کالایی با این نام وجود ندارد"


        context["message"] = message
        return render(request, "DefineGoods_view.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "DefineGoods_viewByName.html", context)
















@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def UnitCreate(request):
    context = {}
    message = ''

    form = forms.UnitForm(request.POST or None)
    if form.is_valid():
        message = 'واحد با موفعقیت ثبت شد'
        form.save()

    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "UnitCreate.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Unitview(request):
    context = {}
    message = ''

    context["dataset"] = models.Unit.objects.all()
    if context["dataset"] == "":
        message = "شما هیچ واحدی ثبت نکردید"
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Unitview.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Unitdelete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.Unit, id=id)

    if request.method == "POST":
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'

        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Unitdelete.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Unitupdate(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.Unit, id=id)

    form = forms.UnitForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        message = 'با موفعقیت ویرایش شد'
        context['update'] = 'Yes'

    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Unit_update.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def GroupCreate(request):
    context = {}
    message = ''

    form = forms.GroupForm(request.POST or None)
    if form.is_valid():
        message = 'گروه با موفعقیت ثبت شد'
        form.save()

    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "GroupCreate.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Groupview(request):
    context = {}
    message = ''

    context["dataset"] = models.Group.objects.all()
    if context["dataset"] == "":
        message = "شما هیچ گروهی ثبت نکردید"
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Groupview.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Groupdelete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.Group, id=id)

    if request.method == "POST":
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'

        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Groupdelete.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Groupupdate(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.Group, id=id)

    form = forms.GroupForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        message = 'با موفعقیت ویرایش شد'
        context['update'] = 'Yes'

    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Groupupdate.html", context)













@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_Create(request):
    context = {}
    message = ''

    u = models.User.objects.get(username=request.user.username)
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)



    rand = random.sample(range(1, 11), 10)
    strings = [str(integer) for integer in rand]
    a_string = "".join(strings)
    an_integer = int(a_string)




    form = forms.EntryGoodsForm(request.POST or None, request=request, initial={'user':u, 'warehouse':w,
                                                                                 'id':an_integer,})
    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["driver_send"].queryset = models.Profile.objects.filter(post='4')
    form.fields["sender"].queryset = models.Profile.objects.filter(post='3')
    form.fields["registrationOfGoods"].queryset = models.RegistrationOfGoods.objects.filter(warehouse=w)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=sw_id)


    if form.is_valid():
        #######################

        #######################
        value = form.cleaned_data['value']
        Goods = form.cleaned_data['registrationOfGoods']
        GoodsId = Goods.id
        g = get_object_or_404(models.RegistrationOfGoods, id=GoodsId)
        g.value = g.value + value
        g.save()
        message = 'ورود کالا با موفعقیت ثبت شد'
        form.save()
        ############################
        EG_ID = form.cleaned_data['id']
        EG = get_object_or_404(models.EntryGoods, id=EG_ID)
        for v in range(value):
            rand = random.sample(range(0, 99), 15)
            str_rand = ""
            for i in rand:
                str_rand += str(i)

            s = models.SerialGoods_ENG.objects.create(entryGoods=EG, serial=str_rand)
            s.save()




    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_Create_W.html", context)

















@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id)
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_ByFilter_Filter_DateAsc(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id).order_by('date')
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_ByFilter_Filter_MaxValue(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id).order_by('-value')
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_ByFilter_Filter_MinValue(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id).order_by('value')
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_ByFilter_Filter_Location(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id).order_by('warehouse')
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_ByFilter_Filter_Driver(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id).order_by('driver_send__user')
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_ByFilter_Filter_Sender(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.EntryGoods.objects.filter(warehouse=w_id).order_by('sender__user')
    count = models.EntryGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "ورود کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_W.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_delete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.EntryGoods, id=id)
    value = obj.value
    Goods = obj.registrationOfGoods.id
    if request.method == "POST":
        g = get_object_or_404(models.RegistrationOfGoods, id=Goods)
        g.value = g.value - value
        g.save()
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'
        models.SerialGoods_ENG.objects.filter(entryGoods=obj).delete()


        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_delete_W.html", context)






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_update(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.EntryGoods, id=id)
    value_sub = obj.value
    Goods_sub = obj.registrationOfGoods.id
    g_old = get_object_or_404(models.RegistrationOfGoods, id=Goods_sub)



    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)
    form = forms.EntryGoodsForm(request.POST or None, instance=obj, request=request)
    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["driver_send"].queryset = models.Profile.objects.filter(post='4')
    form.fields["sender"].queryset = models.Profile.objects.filter(post='3')
    form.fields["registrationOfGoods"].queryset = models.RegistrationOfGoods.objects.filter(warehouse=w)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=sw_id)



    if form.is_valid():

        g_old.value = g_old.value - value_sub
        g_old.save()
        value_add = form.cleaned_data['value']
        Goods_add = form.cleaned_data['registrationOfGoods']
        Goods_add_id = Goods_add.id
        g_new = get_object_or_404(models.RegistrationOfGoods, id=Goods_add_id)
        g_new.value = g_new.value + value_add
        g_new.save()
        message = 'ورود کالا با موفعقیت ویرایش شد'
        form.save()
        context['update'] = 'Yes'
        ############################
        models.SerialGoods_ENG.objects.filter(entryGoods=obj).delete()
        ############################
        EG_ID = form.cleaned_data['id']
        EG = get_object_or_404(models.EntryGoods, id=EG_ID)
        for v in range(value_add):
            rand = random.sample(range(0, 99), 15)
            str_rand = ""
            for i in rand:
                str_rand += str(i)

            s = models.SerialGoods_ENG.objects.create(entryGoods=EG, serial=str_rand)
            s.save()



    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_update_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_SerialForDriver(request):
    context = {}
    message = ''
    form = forms.EntryGoods_view_ByFilter_SerialForDriver(request.POST or None)

    if form.is_valid():

        SerialForDriver_Create = form.cleaned_data['SerialForDriver']
        #######################
        context['dataset'] = models.EntryGoods.objects.filter(SerialForDriver=SerialForDriver_Create)
        count = models.EntryGoods.objects.filter(SerialForDriver=SerialForDriver_Create).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'

        context["SerialForDriver_Create"] = SerialForDriver_Create
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_SerialForDriver.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_serial(request, serial):
    context = {}
    message = ''

    SerialForDriver_Create = serial

    context['dataset'] = models.EntryGoods.objects.filter(SerialForDriver=SerialForDriver_Create)
    count = models.EntryGoods.objects.filter(SerialForDriver=SerialForDriver_Create).count()
    if count == 0:
        context["message"] = 'موردی یافت نشد'

    context["SerialForDriver_Create"] = SerialForDriver_Create
    return render(request, "EntryGoods_view_W.html", context)















@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter(request):
    context = {}
    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_WarehouseName(request):
    context = {}
    message = ''
    form = forms.EntryGoods_view_ByFilter_WarehouseName_Form(request.POST or None)

    if form.is_valid():
        WarehouseName = form.cleaned_data['WarehouseName']
        context['dataset'] = models.EntryGoods.objects.filter(warehouse=WarehouseName)
        count = models.EntryGoods.objects.filter(warehouse=WarehouseName).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_FORM_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_DriverName(request):
    context = {}
    message = ''
    form = forms.EntryGoods_view_ByFilter_DriverName_Form(request.POST or None)

    if form.is_valid():
        DriverName = form.cleaned_data['DriverName']
        context['dataset'] = models.EntryGoods.objects.filter(driver_send=DriverName)
        count = models.EntryGoods.objects.filter(driver_send=DriverName).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_FORM_W.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_ReferredName(request):
    context = {}
    message = ''
    form = forms.EntryGoods_view_ByFilter_ReferredName_Form(request.POST or None)

    if form.is_valid():
        ReferredName = form.cleaned_data['ReferredName']
        context['dataset'] = models.EntryGoods.objects.filter(sender=ReferredName)
        count = models.EntryGoods.objects.filter(sender=ReferredName).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_FORM_W.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_WarehouseName_Date(request):
    context = {}
    message = ''
    form = forms.EntryGoods_view_ByFilter_WarehouseName_Date_Form(request.POST or None)

    if form.is_valid():
        WarehouseName = form.cleaned_data['WarehouseName']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.EntryGoods.objects.filter(warehouse=WarehouseName)\
            .filter(date__range=[from_date, to_date])

        count = models.EntryGoods.objects.filter(warehouse=WarehouseName)\
            .filter(date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_FORM_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_WarehouseName_Date_DriverName(request):
    context = {}
    message = ''
    form = forms.EntryGoods_view_ByFilter_WarehouseName_Date_DriverName_Form(request.POST or None)

    if form.is_valid():
        WarehouseName = form.cleaned_data['WarehouseName']
        DriverName = form.cleaned_data['DriverName']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.EntryGoods.objects.filter(warehouse=WarehouseName) \
            .filter(driver_send=DriverName).filter(date__range=[from_date, to_date])

        count = models.EntryGoods.objects.filter(warehouse=WarehouseName) \
            .filter(driver_send=DriverName).filter(date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "EntryGoods_view_ByFilter_FORM_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def EntryGoods_Serials(request, id):
    context = {}
    message = ''

    obj = get_object_or_404(models.EntryGoods, id=id)
    context["dataset"] = models.SerialGoods_ENG.objects.filter(entryGoods=obj)
    count = models.SerialGoods_ENG.objects.filter(entryGoods=obj).count()
    if count == 0:
        message = "سریالی برای این ورود کالا یافت نشد"
    context["message"] = message


    return render(request, "EntryGoods_Serials.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def SearchSerial_ENG(request):
    context = {}
    message = ''
    form = forms.SearchSerial_ENG_FORM(request.POST or None)

    if form.is_valid():
        s = form.cleaned_data['serial']
        try:
            SerialGoods = models.SerialGoods_ENG.objects.get(serial=s)
            SerialGoods_id = SerialGoods.entryGoods.id
            context["dataset"] = models.EntryGoods.objects.filter(id=SerialGoods_id)
        except:
            message = "کالایی با این سریال وارد نشده است"

        context["message"] = message
        return render(request, "EntryGoods_view_W.html", context)

    context["form"] = form

    return render(request, "SearchSerial_ENG.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_Create(request):
    context = {}
    message = ''

    u = models.User.objects.get(username=request.user.username)
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)


    rand = random.sample(range(1, 11), 10)
    strings = [str(integer) for integer in rand]
    a_string = "".join(strings)
    an_integer = int(a_string)


    form = forms.ExitGoodsForm(request.POST or None, request=request, initial={'user':u, 'warehouse':w,
                                                                               'id':an_integer,})
    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["driver_receive"].queryset = models.Profile.objects.filter(post='4')
    form.fields["receiver"].queryset = models.Profile.objects.filter(post='3')
    form.fields["registrationOfGoods"].queryset = models.RegistrationOfGoods.objects.filter(warehouse=w)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=sw_id)


    if form.is_valid():


        value = form.cleaned_data['value']
        Goods = form.cleaned_data['registrationOfGoods']
        GoodsId = Goods.id
        g = get_object_or_404(models.RegistrationOfGoods, id=GoodsId)
        g.value = g.value - value

        if g.value < 0:
            message = 'موجودی کالا موردنظر کافی نیست.'
        else:
            g.save()
            message = 'خروج کالا با موفعقیت ثبت شد'
            form.save()
    ############################
            EG_ID = form.cleaned_data['id']
            EG = get_object_or_404(models.ExitGoods, id=EG_ID)
            for v in range(value):
                rand = random.sample(range(0, 99), 15)
                str_rand = ""
                for i in rand:
                    str_rand += str(i)

                s = models.SerialGoods.objects.create(exitGoods=EG, serial=str_rand)
                s.save()



    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_Create_W.html", context)














@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_Create_For_Referred(request):
    context = {}
    message = ''

    u = models.User.objects.get(username=request.user.username)
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)


    ############################################

    goods_id = request.session.get('goods_id')
    value_session = request.session.get('value_session')
    profilre_id = request.session.get('profilre_id')
    address_session = request.session.get('address_session')
    serial_session = request.session.get('serial_session')



    receiver_initial = models.Profile.objects.get(id=profilre_id)


    form = forms.ExitGoodsForm(request.POST or None, request=request, initial={'user': u,
                                                                               'warehouse': w,
                                                                               'receiver': receiver_initial,
                                                                               })

    form.fields["id"].initial = serial_session
    form.fields["address"].initial = address_session
    form.fields["value"].initial = value_session
    form.fields["registrationOfGoods"].queryset = models.RegistrationOfGoods.objects.filter(goods__id=goods_id)\
        .filter(warehouse=w)
    form.fields["receiver"].queryset = models.Profile.objects.filter(id=profilre_id)

    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["driver_receive"].queryset = models.Profile.objects.filter(post='4')
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=sw_id)
    ############################################

    if form.is_valid():
        #######################

        #######################

        value = form.cleaned_data['value']
        Goods = form.cleaned_data['registrationOfGoods']
        GoodsId = Goods.id
        g = get_object_or_404(models.RegistrationOfGoods, id=GoodsId)
        g.value = g.value - value

        if g.value < 0:
            message = 'موجودی کالا موردنظر کافی نیست.'
        else:
            g.save()
            message = 'خروج کالا با موفعقیت ثبت شد'
            form.save()
    ############################
            EG_ID = form.cleaned_data['id']
            EG = get_object_or_404(models.ExitGoods, id=EG_ID)
            for v in range(value):
                rand = random.sample(range(0, 99), 15)
                str_rand = ""
                for i in rand:
                    str_rand += str(i)

                s = models.SerialGoods.objects.create(exitGoods=EG, serial=str_rand)
                s.save()



    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_Create_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_Create_For_Referred_id(request, id):
    context = {}
    message = ''

    u = models.User.objects.get(username=request.user.username)
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)


    ############################################

    RequestGoods = models.Requestgoods.objects.get(id=id)
    goods_id = RequestGoods.goods.id
    value_session = RequestGoods.value
    profilre_id = RequestGoods.profile.id
    address_session = RequestGoods.address
    serial_session = RequestGoods.serial



    receiver_initial = models.Profile.objects.get(id=profilre_id)


    form = forms.ExitGoodsForm(request.POST or None, request=request, initial={'user': u,
                                                                               'warehouse': w,
                                                                               'receiver': receiver_initial,
                                                                               })

    form.fields["id"].initial = serial_session
    form.fields["address"].initial = address_session
    form.fields["value"].initial = value_session
    form.fields["registrationOfGoods"].queryset = models.RegistrationOfGoods.objects.filter(goods__id=goods_id)\
        .filter(warehouse=w)
    form.fields["receiver"].queryset = models.Profile.objects.filter(id=profilre_id)

    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["driver_receive"].queryset = models.Profile.objects.filter(post='4')
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=sw_id)
    ############################################

    if form.is_valid():
        #######################

        #######################

        value = form.cleaned_data['value']
        Goods = form.cleaned_data['registrationOfGoods']
        GoodsId = Goods.id
        g = get_object_or_404(models.RegistrationOfGoods, id=GoodsId)
        g.value = g.value - value

        if g.value < 0:
            message = 'موجودی کالا موردنظر کافی نیست.'
        else:
            g.save()
            message = 'خروج کالا با موفعقیت ثبت شد'
            form.save()
    ############################
            EG_ID = form.cleaned_data['id']
            EG = get_object_or_404(models.ExitGoods, id=EG_ID)
            for v in range(value):
                rand = random.sample(range(0, 99), 15)
                str_rand = ""
                for i in rand:
                    str_rand += str(i)

                s = models.SerialGoods.objects.create(exitGoods=EG, serial=str_rand)
                s.save()



    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_Create_W.html", context)














@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id)
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_ByFilter_Filter_DateAsc(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id).order_by('date')
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_ByFilter_Filter_MaxValue(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id).order_by('-value')
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_ByFilter_Filter_MinValue(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id).order_by('value')
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_ByFilter_Filter_Location(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id).order_by('warehouse')
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_ByFilter_Filter_Driver(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id).order_by('driver_receive__user')
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_ByFilter_Filter_Sender(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name
    context["dataset"] = models.ExitGoods.objects.filter(warehouse=w_id).order_by('receiver__user')
    count = models.ExitGoods.objects.filter(warehouse=w_id).count()
    if count == 0:
        message = "خروج کالا برای این انبار ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_delete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.ExitGoods, id=id)
    value = obj.value
    Goods = obj.registrationOfGoods.id
    if request.method == "POST":
        g = get_object_or_404(models.RegistrationOfGoods, id=Goods)
        g.value = g.value + value
        g.save()
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'
        ############################
        models.SerialGoods.objects.filter(exitGoods=obj).delete()


        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_delete_W.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_update(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.ExitGoods, id=id)
    value_sub = obj.value
    Goods_sub = obj.registrationOfGoods.id
    g_old = get_object_or_404(models.RegistrationOfGoods, id=Goods_sub)

    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name.id
    w = models.Warehouse.objects.get(id=sw_id)
    form = forms.ExitGoodsForm(request.POST or None, instance=obj, request=request)
    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["driver_receive"].queryset = models.Profile.objects.filter(post='4')
    form.fields["receiver"].queryset = models.Profile.objects.filter(post='3')
    form.fields["registrationOfGoods"].queryset = models.RegistrationOfGoods.objects.filter(warehouse=w)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=sw_id)


    if form.is_valid():

        g_old.value = g_old.value + value_sub
        g_old.save()
        value_add = form.cleaned_data['value']
        Goods_add = form.cleaned_data['registrationOfGoods']
        Goods_add_id = Goods_add.id
        g_new = get_object_or_404(models.RegistrationOfGoods, id=Goods_add_id)
        g_new.value = g_new.value - value_add

        if g_new.value < 0:
            g_old.value = g_old.value - value_sub
            g_old.save()
            message = 'موجودی کالا موردنظر کافی نیست.'

        else:
            g_new.save()
            message = 'خروج کالا با موفعقیت ویرایش شد'
            form.save()
            context['update'] = 'Yes'
            ############################
            models.SerialGoods.objects.filter(exitGoods=obj).delete()
            ############################
            EG_ID = form.cleaned_data['id']
            EG = get_object_or_404(models.ExitGoods, id=EG_ID)
            for v in range(value_add):
                rand = random.sample(range(0, 99), 15)
                str_rand = ""
                for i in rand:
                    str_rand += str(i)

                s = models.SerialGoods.objects.create(exitGoods=EG, serial=str_rand)
                s.save()




    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_update_W.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_SerialForDriver(request):
    context = {}
    message = ''
    form = forms.ExitGoods_view_ByFilter_SerialForDriver(request.POST or None)

    if form.is_valid():
        #######################

        SerialForDriver = form.cleaned_data['SerialForDriver']

        #######################
        context['dataset'] = models.ExitGoods.objects.filter(SerialForDriver=SerialForDriver)
        count = models.ExitGoods.objects.filter(SerialForDriver=SerialForDriver).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'

        context["SerialForDriver_Create"] = SerialForDriver
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGOOds_view_ByFilter_SerialForDriver.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_SerialForDriver_Serial(request, serial):
    context = {}
    message = ''

    SerialForDriver = serial
    context['dataset'] = models.ExitGoods.objects.filter(SerialForDriver=SerialForDriver)
    count = models.ExitGoods.objects.filter(SerialForDriver=SerialForDriver).count()
    if count == 0:
        context["message"] = 'موردی یافت نشد'

    context["SerialForDriver_Create"] = SerialForDriver
    return render(request, "ExitGoods_view_W.html", context)

















@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter(request):
    context = {}
    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)


    return render(request, "ExitGoods_view_ByFilter_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_WarehouseName(request):
    context = {}
    message = ''
    form = forms.ExitGoods_view_ByFilter_WarehouseName_Form(request.POST or None)

    if form.is_valid():
        WarehouseName = form.cleaned_data['WarehouseName']
        context['dataset'] = models.ExitGoods.objects.filter(warehouse=WarehouseName)
        count = models.ExitGoods.objects.filter(warehouse=WarehouseName).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_ByFilter_FORM_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_DriverName(request):
    context = {}
    message = ''
    form = forms.ExitGoods_view_ByFilter_DriverName_Form(request.POST or None)

    if form.is_valid():
        DriverName = form.cleaned_data['DriverName']
        context['dataset'] = models.ExitGoods.objects.filter(driver_receive=DriverName)
        count = models.ExitGoods.objects.filter(driver_receive=DriverName).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_ByFilter_FORM_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_ReferredName(request):
    context = {}
    message = ''
    form = forms.ExitGoods_view_ByFilter_ReferredName_Form(request.POST or None)

    if form.is_valid():
        ReferredName = form.cleaned_data['ReferredName']
        context['dataset'] = models.ExitGoods.objects.filter(receiver=ReferredName)
        count = models.ExitGoods.objects.filter(receiver=ReferredName).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_ByFilter_FORM_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_WarehouseName_Date(request):
    context = {}
    message = ''
    form = forms.ExitGoods_view_ByFilter_WarehouseName_Date_Form(request.POST or None)

    if form.is_valid():
        WarehouseName = form.cleaned_data['WarehouseName']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.ExitGoods.objects.filter(warehouse=WarehouseName)\
            .filter(date__range=[from_date, to_date])

        count = models.ExitGoods.objects.filter(warehouse=WarehouseName)\
            .filter(date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_ByFilter_FORM_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_WarehouseName_Date_DriverName(request):
    context = {}
    message = ''
    form = forms.ExitGoods_view_ByFilter_WarehouseName_Date_DriverName_Form(request.POST or None)

    if form.is_valid():
        WarehouseName = form.cleaned_data['WarehouseName']
        DriverName = form.cleaned_data['DriverName']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.ExitGoods.objects.filter(warehouse=WarehouseName) \
            .filter(driver_receive=DriverName).filter(date__range=[from_date, to_date])

        count = models.ExitGoods.objects.filter(warehouse=WarehouseName) \
            .filter(driver_receive=DriverName).filter(date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_ByFilter_FORM_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ExitGoods_Serials(request, id):
    context = {}
    message = ''

    obj = get_object_or_404(models.ExitGoods, id=id)
    context["dataset"] = models.SerialGoods.objects.filter(exitGoods=obj)
    count = models.SerialGoods.objects.filter(exitGoods=obj).count()
    if count == 0:
        message = "سریالی برای این خروج کالا یافت نشد"
    context["message"] = message


    return render(request, "ExitGoods_Serials.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def SearchSerial(request):
    context = {}
    message = ''
    form = forms.SearchSerial_FORM(request.POST or None)

    if form.is_valid():
        s = form.cleaned_data['serial']
        try:
            SerialGoods = models.SerialGoods.objects.get(serial=s)
            SerialGoods_id = SerialGoods.exitGoods.id
            context["dataset"] = models.ExitGoods.objects.filter(id=SerialGoods_id)
        except:
            message = "کالایی با این سریال خارج نشده است"

        context["message"] = message
        return render(request, "ExitGoods_view_W.html", context)

    context["form"] = form

    return render(request, "SearchSerial.html", context)













@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_unanswered(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None)
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''


    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_DateAsc(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None).order_by('date')
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_MaxValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None).order_by('-value')
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_MinValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None).order_by('value')
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_GoodsName(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None).order_by('goods__name')
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_Warehousekeeper(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None).order_by('user__username')
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_Applicant(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result=None).order_by('profile__user__username')
    count = models.Requestgoods.objects.filter(result=None).count()
    if count == 0:
        message = "درخواست بی پاسخ وجود ندارد"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_unanswered_W.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted_ByFilter_Filter_DateAsc(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1').order_by('date')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted_ByFilter_Filter_MaxValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1').order_by('-value')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted_ByFilter_Filter_MinValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1').order_by('value')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted_ByFilter_Filter_GoodsName(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1').order_by('goods__name')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted_ByFilter_Filter_Warehousekeeper(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1').order_by('user__username')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_accepted_ByFilter_Filter_Applicant(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='1').order_by('profile__user__username')
    count = models.Requestgoods.objects.filter(result='1').count()
    if count == 0:
        message = "درخواست قبول شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '1'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected_ByFilter_Filter_DateAsc(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2').order_by('date')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected_ByFilter_Filter_MaxValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2').order_by('-value')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected_ByFilter_Filter_MinValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2').order_by('value')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected_ByFilter_Filter_GoodsName(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2').order_by('goods__name')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected_ByFilter_Filter_Warehousekeeper(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2').order_by('user__username')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_rejected_ByFilter_Filter_Applicant(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.filter(result='2').order_by('profile__user__username')
    count = models.Requestgoods.objects.filter(result='2').count()
    if count == 0:
        message = "درخواست رد شده وجود ندارد"
    context["message"] = message
    context["filterdate"] = '2'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all(request):
    context = {}
    message = ''
    form = forms.Requestgoods_All_ByFilter_Date_FORM(request.POST or None)

    if form.is_valid():
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.Requestgoods.objects.filter(date__range=[from_date, to_date])

        count = models.Requestgoods.objects.filter(date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Requestgoods_All_ByFilter_Date_W.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all()
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)











@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial)
    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside_Filter_GoodsName(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).\
        order_by('goods__name')

    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside_Filter_minValue(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).order_by('value')
    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside_Filter_maxValue(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).order_by('-value')
    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside_Filter_refferd(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial)\
        .order_by('profile__user__username')

    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside_Filter_dateAse(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).order_by('date')
    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_onside_Filter_dateDse(request):
    context = {}
    message = ''

    serial = models.ExitGoods.objects.all().values('id')
    context["dataset"] = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).order_by('-date')
    count = models.Requestgoods.objects.filter(result='1').exclude(serial__in=serial).count()
    if count == 0:
        message = "موردی یافت نشد"
    context["message"] = message
    context["filterdate"] = 'all_item_response'
    context["exclude"] = 'exclude'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_items_SearchByCode(request):
    context = {}
    message = ''

    form = forms.Requestgoods_all_items_SearchByCode_FORM(request.POST or None)

    if form.is_valid():
        s = form.cleaned_data['serial']
        context["dataset"] = models.Requestgoods.objects.filter(serial=s)
        count = models.Requestgoods.objects.filter(serial=s).count()
        if count == 0:
            message = "موردی یافت نشد"

        ######################22222222222222################
        ExitGoods = models.ExitGoods.objects.all().values('id')
        Exclude = models.Requestgoods.objects.filter(result='1').exclude(serial__in=ExitGoods)
        cuonter = 0
        for i in Exclude:
            if s == i.serial:
                cuonter = cuonter + 1

        if cuonter != 0:
            context["exclude"] = 'exclude'

        context["message"] = message

        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)
        return render(request, 'View_Requestgoods_By_Warehousekeeper.html', context)



    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Requestgoods_all_items_SearchByCode_Form.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_ByFilter_Filter_DateAsc(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('date')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_ByFilter_Filter_MaxValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('-value')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_ByFilter_Filter_MinValue(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('value')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_ByFilter_Filter_GoodsName(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('goods__name')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)











@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_ByFilter_Filter_Warehousekeeper(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('user__username')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_all_ByFilter_Filter_Applicant(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('profile__user__username')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_ByFilter_Filter_Resualt(request):
    context = {}
    message = ''

    context["dataset"] = models.Requestgoods.objects.all().order_by('result')
    count = models.Requestgoods.objects.all().count()
    if count == 0:
        message = "درخواست کالا وجود ندارد"
    context["message"] = message
    context["filterdate"] = 'all_item'

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "View_Requestgoods_By_Warehousekeeper.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Requestgoods_respond(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.Requestgoods, id=id)

    rand = random.sample(range(1, 11), 10)
    strings = [str(integer) for integer in rand]
    a_string = "".join(strings)
    an_integer = int(a_string)

    obj.serial = an_integer


    obj.user = models.User.objects.get(username=request.user.username)
    form = forms.Requestgoods_respondForm(request.POST or None, instance=obj)
    form.fields["user"].queryset = models.User.objects.filter(username=request.user.username)
    form.fields["profile"].queryset = models.Profile.objects.filter(national_code=obj.profile.national_code)

    if form.is_valid():
        ##############################
        goods_id = form.cleaned_data['goods'].id
        profilre_id = form.cleaned_data['profile'].id
        value_session = form.cleaned_data['value']
        address_session = form.cleaned_data['address']
        serial_session = form.cleaned_data['serial']
        request.session['goods_id'] = goods_id
        request.session['value_session'] = value_session
        request.session['profilre_id'] = profilre_id
        request.session['address_session'] = address_session
        request.session['serial_session'] = serial_session
        ##############################
        message = 'پاسخ درخواست کالا با موفعقیت ثبت شد.'
        form.save()


    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "Requestgoods_respond_W.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def Allgoods_ByName(request, GoodsName):
    context = {}
    message = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    context['dataset'] = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
        .filter(goods__name__exact=GoodsName)
    count = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
        .filter(goods__name__exact=GoodsName).count()
    if count == 0:
        message = "کالا وجود ندارد"

    goods = models.RegistrationOfGoods.objects.filter(warehouse_id=warehouse_name_top_page_id)\
        .filter(goods__name__exact=GoodsName)
    goods_count = 0
    for i in goods:
        goods_count = goods_count + i.value
    context['goods_count'] = goods_count

    context['alarm'] = 'نمایش اطلاعات کالا'
    context['message'] = message

    return render(request, 'GoodsView.html', context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ShowInfoDriver(request):
    context = {}
    message = ''
    context['dataset'] = models.Profile.objects.filter(post='4')
    count = models.Profile.objects.filter(post='4').count()
    if count == 0:
        message = 'راننده وجود ندارد'
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, 'ShowInfoDriver.html', context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def ShowInfoReferred(request):
    context = {}
    message = ''
    context['dataset'] = models.Profile.objects.filter(post='3')
    count = models.Profile.objects.filter(post='3').count()
    if count == 0:
        message = 'مراجعه کننده وجود ندارد'
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, 'ShowInfoReferred.html', context)













@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_Create(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name.id
    warehouse = models.Warehouse.objects.get(id=w_id)
    form = forms.WarehouseHandling_Form(request.POST or None, initial={'warehouse':warehouse,})
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=w_id)
    if form.is_valid():
        ################################
        WarehouseHandling = models.WarehouseHandling.objects.filter(warehouse=warehouse)
        i = 0
        for w in WarehouseHandling:
            if w.finish_date == None:
                i = 1
                break

        if i == 0:
        ###############################
            goods = models.RegistrationOfGoods.objects.filter(warehouse=warehouse)
            for g in goods:
                g.value_D = None
                g.value_Diff = None
                g.save()
            message = 'انبار گردانی با موفعقیت ایجاد شد'
            form.save()
        ##############################
        else:
            message = 'انبارگردانی قبلی به پایان نرسیده است.'

        ############################



    context['form'] = form
    context['message'] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_Create.html", context)











@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_view(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name.id
    warehouse = models.Warehouse.objects.get(id=w_id)

    context["dataset"] = models.WarehouseHandling.objects.filter(warehouse=warehouse)
    count = models.WarehouseHandling.objects.filter(warehouse=warehouse).count()
    if count == 0:
        message = "برای این انبار، انبارگردانی ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_view.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_view_FilterDate_Ase(request):
    context = {}
    message = ''

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name.id
    warehouse = models.Warehouse.objects.get(id=w_id)

    context["dataset"] = models.WarehouseHandling.objects.filter(warehouse=warehouse).order_by('start_date')
    count = models.WarehouseHandling.objects.filter(warehouse=warehouse).count()
    if count == 0:
        message = "برای این انبار، انبارگردانی ثبت نشده است"
    context["message"] = message
    context["filterdate"] = ''

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_view.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_delete(request, id):
    message = ''
    context = {}

    obj = get_object_or_404(models.WarehouseHandling, id=id)

    if request.method == "POST":
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'

        warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
        warehouse_name_top_page_id = warehouse_name_top_page.name.id
        context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_delete.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_update(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.WarehouseHandling, id=id)

    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name.id

    form = forms.WarehouseHandling_Form(request.POST or None, instance=obj)
    form.fields["warehouse"].queryset = models.Warehouse.objects.filter(id=w_id)
    if form.is_valid():
        ######################
        finish = form.cleaned_data['finish_date']
        if finish != None:
            goods_value = models.RegistrationOfGoods.objects.filter(warehouse_id=w_id)
            i = 0
            for g in goods_value:
                if g.value_D == None:
                    i = 1
                    break

            if i == 0:
                form.save()
                message = 'انبارگردانی با موفعقیت به اتمام رسید.'
                context['update'] = 'Yes'
            else:
                message = ' "موجودی انبار" بعضی از کالاها ثبت نشده است. تا زمانی که "موجودی انبار" ' \
                          '  تمام کالاهای انبار ثبت نشود، نمیتوانید پایان  انبار گردانی را ثبت کنید.'

        else:
        ###########################
            form.save()
            message = 'با موفعقیت ویرایش شد'
            context['update'] = 'Yes'


    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_update.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_view_ByFilter_date(request):
    context = {}
    message = ''
    form = forms.WarehouseHandling_FilterByDate_Form(request.POST or None)
    w = models.SelectWarehouse.objects.all()[0]
    w_id = w.name.id
    warehouse = models.Warehouse.objects.get(id=w_id)
    if form.is_valid():
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.WarehouseHandling.objects.filter(warehouse=warehouse)\
            .filter(start_date__range=[from_date, to_date])

        count = models.WarehouseHandling.objects.filter(warehouse=warehouse)\
            .filter(start_date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'
        return render(request, "WarehouseHandling_view.html", context)

    context["form"] = form

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_view_ByFilter_date.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_continue(request):
    context = {}
    message = ''
    sw = models.SelectWarehouse.objects.all()[0]
    sw_id = sw.name
    context["dataset"] = models.RegistrationOfGoods.objects.filter(warehouse=sw_id)
    count = models.RegistrationOfGoods.objects.filter(warehouse=sw_id).count()
    if count == 0:
        message = "کالایی در این انبار وجود ندارد"
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_continue.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def WarehouseHandling_GoodsValue(request, id):
    context = {}
    message = ''

    obj = models.RegistrationOfGoods.objects.get(id=id)


    form = forms.WarehouseHandling_GoodsValue(request.POST or None)


    if form.is_valid():
        GoodsValue = form.cleaned_data['GoodsValue']
        obj.value_D = GoodsValue
        obj.value_Diff = obj.value - obj.value_D
        obj.value = GoodsValue
        obj.save()
        message = 'با موفعقیت ویرایش شد'
        context["message"] = message
        return HttpResponseRedirect('/warehousekeeper/WarehouseHandling/continue/')


    context["form"] = form
    context["message"] = message

    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "WarehouseHandling_GoodsValue.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='WarehouseKeeper_Permissions') in u.groups.all())
def view_exitgoods_by_serial_w(request, id):
    context = {}
    message = ''
    try:
        context["dataset"] = models.ExitGoods.objects.filter(id=id)
    except:
        message = 'چیزی یافت نشد. لطفا شناسه خروج را به درستی وارد کنید'

    counter = models.ExitGoods.objects.filter(id=id).count()
    if counter == 0:
        context["reject"] = "reject"

    context["message"] = message
    warehouse_name_top_page = models.SelectWarehouse.objects.all()[0]
    warehouse_name_top_page_id = warehouse_name_top_page.name.id
    context["warehouse_name_top_page_id"] = models.Warehouse.objects.filter(id=warehouse_name_top_page_id)

    return render(request, "ExitGoods_view_W.html", context)














##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def referred(request):
    return render(request, 'Referred_Profile.html', {})






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def create_Requestgoods(request):
    context = {}
    message = ''

    u = models.User.objects.get(username=request.user.username)
    p = models.Profile.objects.get(user=u)
    form = forms.RequestgoodsForm(request.POST or None, initial={'profile':p})
    form.fields['profile'].queryset = models.Profile.objects.filter(user=u)

    if form.is_valid():
        message = 'درخواست کالا با موفعقیت ثبت شد'
        form.save()

    context['form'] = form
    context['message'] = message
    return render(request, "create_Requestgoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.Requestgoods.objects.filter(profile=p)
    if context["dataset"] == "":
        message = "شما درخواستی ثبت نکردید"
    context["message"] = message
    context["filterdate"] = ''

    return render(request, "view_Requestgoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods_Goodsname(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.Requestgoods.objects.filter(profile=p).order_by('goods__name')
    if context["dataset"] == "":
        message = "شما درخواستی ثبت نکردید"
    context["message"] = message
    context["filterdate"] = ''

    return render(request, "view_Requestgoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods_minValue(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.Requestgoods.objects.filter(profile=p).order_by('value')
    if context["dataset"] == "":
        message = "شما درخواستی ثبت نکردید"
    context["message"] = message
    context["filterdate"] = ''

    return render(request, "view_Requestgoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods_maxValue(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.Requestgoods.objects.filter(profile=p).order_by('-value')
    if context["dataset"] == "":
        message = "شما درخواستی ثبت نکردید"
    context["message"] = message
    context["filterdate"] = ''

    return render(request, "view_Requestgoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods_Result(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.Requestgoods.objects.filter(profile=p).order_by('result')
    if context["dataset"] == "":
        message = "شما درخواستی ثبت نکردید"
    context["message"] = message
    context["filterdate"] = ''

    return render(request, "view_Requestgoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods_Ace(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.Requestgoods.objects.filter(profile=p).order_by('date', 'result')
    if context["dataset"] == "":
        message = "شما درخواستی ثبت نکردید"
    context["message"] = message
    context["filterdate"] = ''

    return render(request, "view_Requestgoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def delete_Requestgoods(request, id):
    message = ''
    context = {}
    obj = get_object_or_404(models.Requestgoods, id=id)

    if request.method == "POST":
        obj.delete()
        message = 'با موفعقیت حذف شد'
        context['message'] = message
        context['delete'] = 'Yes'

    return render(request, "delete_Requestgoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def update_Requestgoods(request, id):
    context = {}
    message = ''
    obj = get_object_or_404(models.Requestgoods, id=id)

    form = forms.RequestgoodsForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        message = 'با موفعقیت ویرایش شد'
        context['update'] = 'Yes'

    context["form"] = form
    context["message"] = message
    return render(request, "update_Requestgoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_Requestgoods_ByFilter_Date(request):

    context = {}
    message = ''
    form = forms.Requestgoods_All_ByFilter_Date_Refferd_FORM(request.POST or None)
    p = models.Profile.objects.get(user=request.user)

    if form.is_valid():
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        context['dataset'] = models.Requestgoods.objects.filter(profile=p)\
            .filter(date__range=[from_date, to_date])

        count = models.Requestgoods.objects.filter(profile=p)\
            .filter(date__range=[from_date, to_date]).count()

        if count == 0:
            context["message"] = 'موردی یافت نشد'

        context["filterdate"] = 'yes'
        return render(request, "view_Requestgoods.html", context)

    context["form"] = form
    return render(request, "view_Form_Requestgoods_ByFilter_Date.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Referred_Permissions') in u.groups.all())
def view_exitgoods_by_serial_r(request, id):
    context = {}
    message = ''
    try:
        context["dataset"] = models.ExitGoods.objects.filter(id=id)
    except:
        message = 'چیزی یافت نشد. لطفا شناسه خروج را به درستی وارد کنید'


    counter = models.ExitGoods.objects.filter(id=id).count()
    if counter == 0:
        context["reject"] = 'reject'

    context["message"] = message


    return render(request, "ExitGoods_view_R.html", context)






##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
######################################################################################################



@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def driver(request):
    return render(request, 'Driver_Profile.html', {})






@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p)
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_refferd(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('receiver')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_minValule(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('value')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_maxvalue(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('-value')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_GoodsName(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).\
        order_by('registrationOfGoods__goods__name')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_Serialfordriver(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('SerialForDriver')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_serialExit(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('id')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Filter_warehouse(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('warehouse')
    count = models.ExitGoods.objects.filter(driver_receive=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_Ace(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).order_by('date')
    count = models.ExitGoods.objects.filter(driver_receive=p).order_by('date').count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_exitGoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p)
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_refferd(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('sender')
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)







@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_minValule(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('value')
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_maxvalue(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('-value')
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_GoodsName(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).\
        order_by('registrationOfGoods__goods__name')

    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_Serialfordriver(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('SerialForDriver')
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_serialExit(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('id')
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Filter_warehouse(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('warehouse')
    count = models.EntryGoods.objects.filter(driver_send=p).count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)











@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_EntryGoods_Ace(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).order_by('date')
    count = models.EntryGoods.objects.filter(driver_send=p).order_by('date').count()
    if count == 0:
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما یافت نشد"
    context["message"] = message
    context["SerialForDriver_Create"] = ''

    return render(request, "view_EntryGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def date_for_view_Exitgoods(request):
    return render(request, "view_Exit_goods_ByDate.html")










@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Exitgoods_ByDate(request):
    context = {}
    message = ''
    start_date = request.GET.get('start_date')
    finish_date = request.GET.get('finish_date')
    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.ExitGoods.objects.filter(driver_receive=p).filter(date__range=[start_date, finish_date])
    if context["dataset"] == "":
        message = "راننده محترم هیچ موردی درباره خروج کالا توسط شما در بازه تاریخی انتخاب شده یافت نشد"
    context["message"] = message

    return render(request, "view_exitGoods.html", context)









@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def date_for_view_Entergoods(request):
    return render(request, "view_Enter_goods_ByDate.html")











@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def view_Entergoods_ByDate(request):
    context = {}
    message = ''
    start_date = request.GET.get('start_date')
    finish_date = request.GET.get('finish_date')
    p = models.Profile.objects.get(user=request.user)
    context["dataset"] = models.EntryGoods.objects.filter(driver_send=p).filter(date__range=[start_date, finish_date])
    if context["dataset"] == "":
        message = "راننده محترم هیچ موردی درباره ورود کالا توسط شما در بازه تاریخی انتخاب شده یافت نشد"
    context["message"] = message

    return render(request, "view_EntryGoods.html", context)








@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def ExitGoods_view_ByFilter_SerialForDriver_DRIVER(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    p_id = p.id
    context["p_id"] = p_id

    form = forms.ExitGoods_view_ByFilter_SerialForDriver_DRIVER(request.POST or None)

    if form.is_valid():
        #######################

        SerialForDriver = form.cleaned_data['SerialForDriver']

        #######################
        context['dataset'] = models.ExitGoods.objects.filter(SerialForDriver=SerialForDriver)
        count = models.ExitGoods.objects.filter(SerialForDriver=SerialForDriver).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'

        context["SerialForDriver_Create"] = SerialForDriver
        return render(request, "view_exitGoods.html", context)

    context["form"] = form


    return render(request, "ExitGoods_view_ByFilter_SerialForDriver_DRIVER.html", context)












@login_required(login_url='/login/')
@user_passes_test(lambda u: Group.objects.get(name='Driver_Permissions') in u.groups.all())
def EntryGoods_view_ByFilter_SerialForDriver_DRIVER(request):
    context = {}
    message = ''

    p = models.Profile.objects.get(user=request.user)
    p_id = p.id
    context["p_id"] = p_id

    form = forms.EntryGoods_view_ByFilter_SerialForDriver_DRIVER(request.POST or None)

    if form.is_valid():
        #######################

        SerialForDriver = form.cleaned_data['SerialForDriver']

        #######################
        context['dataset'] = models.EntryGoods.objects.filter(SerialForDriver=SerialForDriver)
        count = models.EntryGoods.objects.filter(SerialForDriver=SerialForDriver).count()
        if count == 0:
            context["message"] = 'موردی یافت نشد'

        context["SerialForDriver_Create"] = SerialForDriver
        return render(request, "view_EntryGoods.html", context)

    context["form"] = form

    return render(request, "EntryGoods_view_ByFilter_SerialForDriver_DRIVER.html", context)







##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


