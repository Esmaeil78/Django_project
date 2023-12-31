from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin



admin.site.site_header = "پنل مدیریت"




@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('get_username', 'get_first_name', 'get_last_name',
                    'age', 'evidence', 'post',
                    )

    list_filter = ('evidence', 'post',)

    search_fields = ['age', 'user__username', 'user__first_name', 'user__last_name',
                     'national_code', 'phone', 'phone2',
                     ]

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'نام کاربری'
    get_username.admin_order_field = 'user'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'نام'
    get_first_name.admin_order_field = 'user'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'نام خانوادگی'
    get_last_name.admin_order_field = 'user'







class UserProfileInline(admin.StackedInline):
    model = models.Profile
    max_num = 1
    can_delete = False




class UserAccountAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAccountAdmin)









@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = ('name', 'address', 'phone', 'get_first_name', 'get_last_name',)

    search_fields = ['name', ]

    def get_first_name(self, obj):
        return obj.profile.user.first_name

    get_first_name.short_description = 'نام مدیر'
    get_first_name.admin_order_field = 'profile'

    def get_last_name(self, obj):
        return obj.profile.user.last_name

    get_last_name.short_description = 'نام خانوادگی مدیر'
    get_last_name.admin_order_field = 'profile'

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True








@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_company_name',)

    search_fields = ['name', ]

    def get_company_name(self, obj):
        return obj.company.name

    get_company_name.short_description = 'نام شرکت'
    get_company_name.admin_order_field = 'company'








@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse_name', 'name', )

    list_filter = ('warehouse__name',)

    search_fields = ['name', 'warehouse__name', ]

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'warehouse'







@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    pass








@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'number',)

    search_fields = ['name', 'number', ]









@admin.register(models.WarehouseHandling)
class WarehouseHandlingAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse_name', 'start_date', 'finish_date',)

    list_filter = ('warehouse__name',)

    search_fields = ['warehouse__name', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'warehouse'






@admin.register(models.Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_code',
                    'get_group', 'get_unit',
                    )

    list_filter = ('group__name', 'unit__name',)

    search_fields = ['name', 'code', ]


    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'نام'
    get_name.admin_order_field = 'name'

    def get_code(self, obj):
        return obj.code

    get_code.short_description = ' کد'
    get_code.admin_order_field = 'code'


    def get_unit(self, obj):
        return obj.unit.name

    get_unit.short_description = ' واحد'
    get_unit.admin_order_field = 'unit__name'

    def get_group(self, obj):
        return obj.group.name

    get_group.short_description = ' گروه'
    get_group.admin_order_field = 'group__name'








@admin.register(models.RegistrationOfGoods)
class RegistrationOfGoodsAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_code', 'get_group',
                    'get_unit', 'value', 'get_warehouse_name', 'get_location',
                    )

    list_filter = ('warehouse__name', 'goods__group__name', 'goods__unit__name',)

    search_fields = ['goods__name', 'goods__code', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'warehouse__name'

    def get_location(self, obj):
        return obj.location.name

    get_location.short_description = 'محل استقرار'
    get_location.admin_order_field = 'location__name'

    def get_name(self, obj):
        return obj.goods.name

    get_name.short_description = 'نام'
    get_name.admin_order_field = 'goods__name'

    def get_code(self, obj):
        return obj.goods.code

    get_code.short_description = ' کد'
    get_code.admin_order_field = 'goods__code'


    def get_unit(self, obj):
        return obj.goods.unit.name

    get_unit.short_description = ' واحد'
    get_unit.admin_order_field = 'goods__unit__name'

    def get_group(self, obj):
        return obj.goods.group.name

    get_group.short_description = ' گروه'
    get_group.admin_order_field = 'goods__group__name'








@admin.register(models.EntryGoods)
class EntryGoodsAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse_name', 'get_warehousekeeper_name', 'driver_username',
                    'sender_username', 'get_goods_name', 'date', 'SerialForDriver',
                    )

    list_filter = ('warehouse__name',
                   )

    search_fields = ['driver_send__user__username', 'user__username',
                     'sender__user__username', 'registrationOfGoods__goods__name', 'SerialForDriver',
                     ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'warehouse'

    def driver_username(self, obj):
        return obj.driver_send.user.username

    driver_username.short_description = 'نام کاربری راننده'
    driver_username.admin_order_field = 'driver_send'

    def sender_username(self, obj):
        return obj.sender.user.username

    sender_username.short_description = 'نام کاربری ارسال کننده'
    sender_username.admin_order_field = 'sender'


    def get_warehousekeeper_name(self, obj):
        return obj.user

    get_warehousekeeper_name.short_description = 'نام کاربری انباردار'
    get_warehousekeeper_name.admin_order_field = 'user'

    def get_goods_name(self, obj):
        return obj.registrationOfGoods.goods.name

    get_goods_name.short_description = 'نام کالا'
    get_goods_name.admin_order_field = 'registrationOfGoods__goods__name'







@admin.register(models.SerialGoods_ENG)
class SerialGoods_ENGAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse_name', 'get_goods_name', 'serial',
                    'get_date_entryGoodsID', 'get_date', )

    list_filter = ('entryGoods__warehouse__name',)
    search_fields = ['serial', 'entryGoods__registrationOfGoods__goods__name',
                     'entryGoods__id', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


    def get_warehouse_name(self, obj):
        return obj.entryGoods.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'entryGoods__warehouse__name'

    def get_goods_name(self, obj):
        return obj.entryGoods.registrationOfGoods.goods.name

    get_goods_name.short_description = 'نام کالا'
    get_goods_name.admin_order_field = 'entryGoods__registrationOfGoods__goods__name'

    def get_date(self, obj):
        return obj.entryGoods.date

    get_date.short_description = ' تاریخ'
    get_date.admin_order_field = 'entryGoods__date'

    def get_date_entryGoodsID(self, obj):
        return obj.entryGoods.id

    get_date_entryGoodsID.short_description = ' شناسه ورود'
    get_date_entryGoodsID.admin_order_field = 'entryGoods__id'




@admin.register(models.ExitGoods)
class ExitGoodsAdmin(admin.ModelAdmin):

    list_display = ('get_warehouse_name', 'get_warehousekeeper_name', 'receiver_username',
                    'get_goods_name', 'date', 'SerialForDriver',
                    )

    list_filter = ('warehouse__name',
                   )

    search_fields = ['driver_receive__user__username', 'user__username',
                     'receiver__user__username', 'registrationOfGoods__goods__name', 'SerialForDriver',
                     ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'warehouse'



    def receiver_username(self, obj):
        return obj.receiver.user.username

    receiver_username.short_description = 'نام کاربری دریافت کننده'
    receiver_username.admin_order_field = 'receiver'

    def get_warehousekeeper_name(self, obj):
        return obj.user.username

    get_warehousekeeper_name.short_description = 'نام کاربری انباردار'
    get_warehousekeeper_name.admin_order_field = 'user'

    def get_goods_name(self, obj):
        return obj.registrationOfGoods.goods.name

    get_goods_name.short_description = 'نام کالا'
    get_goods_name.admin_order_field = 'registrationOfGoods__goods__name'







@admin.register(models.SerialGoods)
class SerialGoodsAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse_name', 'get_goods_name', 'serial',
                    'get_date_entryGoodsID', 'get_date', )

    list_filter = ('exitGoods__warehouse__name',)
    search_fields = ['serial', 'exitGoods__registrationOfGoods__goods__name',
                     'exitGoods__id', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


    def get_warehouse_name(self, obj):
        return obj.exitGoods.warehouse.name

    get_warehouse_name.short_description = 'نام انبار'
    get_warehouse_name.admin_order_field = 'exitGoods__warehouse__name'

    def get_goods_name(self, obj):
        return obj.exitGoods.registrationOfGoods.goods.name

    get_goods_name.short_description = 'نام کالا'
    get_goods_name.admin_order_field = 'exitGoods__registrationOfGoods__goods__name'

    def get_date(self, obj):
        return obj.exitGoods.date

    get_date.short_description = ' تاریخ'
    get_date.admin_order_field = 'exitGoods__date'

    def get_date_entryGoodsID(self, obj):
        return obj.exitGoods.id

    get_date_entryGoodsID.short_description = ' شناسه ورود'
    get_date_entryGoodsID.admin_order_field = 'exitGoods__id'











@admin.register(models.Requestgoods)
class RequestgoodsAdmin(admin.ModelAdmin):
    list_display = ('profile_username', 'profile_firstname', 'profile_lastname',
                    'get_goods', 'value', 'date', 'get_user_username', 'result',
                    )

    list_filter = ('result', )

    search_fields = ['profile__user__username', 'goods__name', 'user__username', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def profile_username(self, obj):
        return obj.profile.user.username

    profile_username.short_description = 'نام کاربری درخواست کننده'
    profile_username.admin_order_field = 'profile'

    def profile_firstname(self, obj):
        return obj.profile.user.first_name

    profile_firstname.short_description = 'نام درخواست کننده'
    profile_firstname.admin_order_field = 'profile'

    def profile_lastname(self, obj):
        return obj.profile.user.last_name

    profile_lastname.short_description = 'نام خانوادگی درخواست کننده'
    profile_lastname.admin_order_field = 'profile'

    def get_user_username(self, obj):
        return obj.user

    get_user_username.short_description = 'نام انباردار'
    get_user_username.admin_order_field = 'user'


    def get_goods(self, obj):
        return obj.goods.name

    get_goods.short_description = 'نام کالا'
    get_goods.admin_order_field = 'goods__name'







