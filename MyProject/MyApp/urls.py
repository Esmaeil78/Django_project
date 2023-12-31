from django.urls import path
from . import views


app_name = 'MYApp'



urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('RegisterAdmin/', views.RegisterAdmin, name='RegisterAdmin'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('fa/admin', views.admin, name='admin'),

















##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
######################################################################################
    path('warehousekeeper/', views.warehousekeeper, name='warehousekeeper'),
    path('warehousekeeper/selectwarehouse/', views.selectwarehouse, name='selectwarehouse'),
    path('warehousekeeper/Goods/create/', views.GoodsCreate, name='GoodsCreate'),
    path('warehousekeeper/Goods/view/', views.Goodsview, name='Goodsview'),
    path('warehousekeeper/Goods/view/Filter_Name/', views.Goodsview_NAME, name='Goodsview_NAME'),
    path('warehousekeeper/Goods/view/Filter_CODE/', views.Goodsview_CODE, name='Goodsview_CODE'),
    path('warehousekeeper/Goods/view/Filter_MaxValue/', views.Goodsview_MaxValue, name='Goodsview_MaxValue'),
    path('warehousekeeper/Goods/view/Filter_MinValue/', views.Goodsview_MinValue, name='Goodsview_MinValue'),
    path('warehousekeeper/Goods/delete/<id>/', views.Goodsdelete, name='Goodsdelete'),
    path('warehousekeeper/Goods/update/<id>/', views.Goodsupdate, name='Goodsupdate'),
    path('warehousekeeper/Goods/alarm/expiration/', views.alarm_expiration, name='alarm_expiration'),
    path('warehousekeeper/Goods/alarm/min_value/', views.alarm_min_value, name='alarm_min_value'),
    path('warehousekeeper/Goods/alarm/max_value/', views.alarm_max_value, name='alarm_max_value'),

    path('warehousekeeper/Goods/viewByCode/', views.Goods_viewByCode,
         name='Goods_viewByCode'),
    path('warehousekeeper/Goods/viewByName/', views.Goods_viewByName, name='Goods_viewByName'),

    path('warehousekeeper/Goods/viewByName/AllWarehouse/',
         views.Goods_viewByName_AllWarehouse, name='Goods_viewByName_AllWarehouse'),


    path('warehousekeeper/DefineGoods/create/', views.DefineGoods_Create, name='DefineGoods_Create'),
    path('warehousekeeper/DefineGoods/view/', views.DefineGoods_view, name='DefineGoods_view'),
    path('warehousekeeper/DefineGoods/delete/<id>/', views.DefineGoods_delete, name='DefineGoods_delete'),
    path('warehousekeeper/DefineGoods/update/<id>/', views.DefineGoods_update, name='DefineGoods_update'),
    path('warehousekeeper/DefineGoods/viewByCode/', views.DefineGoods_viewByCode,
         name='DefineGoods_viewByCode'),

    path('warehousekeeper/DefineGoods/viewByName/', views.DefineGoods_viewByName, name='DefineGoods_viewByName'),




    path('warehousekeeper/Unit/create/', views.UnitCreate, name='UnitCreate'),
    path('warehousekeeper/Unit/view/', views.Unitview, name='Unitview'),
    path('warehousekeeper/Unit/delete/<id>/', views.Unitdelete, name='Unitdelete'),
    path('warehousekeeper/Unit/update/<id>/', views.Unitupdate, name='Unitupdate'),




    path('warehousekeeper/Group/create/', views.GroupCreate, name='GroupCreate'),
    path('warehousekeeper/Group/view/', views.Groupview, name='Groupview'),
    path('warehousekeeper/Group/delete/<id>/', views.Groupdelete, name='Groupdelete'),
    path('warehousekeeper/Group/update/<id>/', views.Groupupdate, name='Groupupdate'),






    path('warehousekeeper/EntryGoods/create/', views.EntryGoods_Create, name='EntryGoods_Create'),
    path('warehousekeeper/EntryGoods/view/', views.EntryGoods_view, name='EntryGoods_view'),

    path('warehousekeeper/EntryGoods/view/ByFilter/Filter_DateAse/', views.EntryGoods_ByFilter_Filter_DateAsc,
         name='EntryGoods_ByFilter_Filter_DateAsc'),

    path('warehousekeeper/EntryGoods/view/ByFilter/Filter_MaxValue/', views.EntryGoods_ByFilter_Filter_MaxValue,
         name='EntryGoods_ByFilter_Filter_MaxValue'),
    path('warehousekeeper/EntryGoods/view/ByFilter/Filter_MinValue/', views.EntryGoods_ByFilter_Filter_MinValue,
         name='EntryGoods_ByFilter_Filter_MinValue'),
    path('warehousekeeper/EntryGoods/view/ByFilter/Filter_Location/', views.EntryGoods_ByFilter_Filter_Location,
         name='EntryGoods_ByFilter_Filter_Location'),
    path('warehousekeeper/EntryGoods/view/ByFilter/Filter_Driver/', views.EntryGoods_ByFilter_Filter_Driver,
         name='EntryGoods_ByFilter_Filter_Driver'),
    path('warehousekeeper/EntryGoods/view/ByFilter/Filter_Sender/', views.EntryGoods_ByFilter_Filter_Sender,
         name='EntryGoods_ByFilter_Filter_Sender'),


    path('warehousekeeper/EntryGoods/delete/<id>/', views.EntryGoods_delete, name='EntryGoods_delete'),
    path('warehousekeeper/EntryGoods/update/<id>/', views.EntryGoods_update, name='EntryGoods_update'),

    path('warehousekeeper/EntryGoods/view/ByFilter/', views.EntryGoods_view_ByFilter,
         name='EntryGoods_view_ByFilter'),

    path('warehousekeeper/EntryGoods/view/ByFilter/WarehouseName/', views.EntryGoods_view_ByFilter_WarehouseName,
         name='EntryGoods_view_ByFilter_WarehouseName'),

    path('warehousekeeper/EntryGoods/view/ByFilter/DriverName/', views.EntryGoods_view_ByFilter_DriverName,
         name='EntryGoods_view_ByFilter_DriverName'),

    path('warehousekeeper/EntryGoods/view/ByFilter/ReferredName/',
         views.EntryGoods_view_ByFilter_ReferredName,
         name='EntryGoods_view_ByFilter_ReferredName'),

    path('warehousekeeper/EntryGoods/view/ByFilter/WarehouseName_Date/',
         views.EntryGoods_view_ByFilter_WarehouseName_Date,
         name='EntryGoods_view_ByFilter_WarehouseName_Date'),

    path('warehousekeeper/EntryGoods/view/ByFilter/WarehouseName_Date_DriverName/',
         views.EntryGoods_view_ByFilter_WarehouseName_Date_DriverName,
         name='EntryGoods_view_ByFilter_WarehouseName_Date_DriverName'),

    path('warehousekeeper/EntryGoods/ShowSerials/<id>/', views.EntryGoods_Serials, name='EntryGoods_Serials'),
    path('warehousekeeper/EntryGoods/SearchSerial/', views.SearchSerial_ENG,
         name='SearchSerial_ENG'),

    path('warehousekeeper/EntryGoods/view/ByFilter/FreightNumber', views.EntryGoods_view_ByFilter_SerialForDriver,
         name='EntryGoods_view_ByFilter_SerialForDriver'),


    path('warehousekeeper/EntryGoods/view/ByFilter/Serial/<str:serial>/',
         views.EntryGoods_view_ByFilter_serial,
         name='EntryGoods_view_ByFilter_serial'),

















    path('warehousekeeper/ExitGoods/create/', views.ExitGoods_Create, name='ExitGoods_Create'),


    path('warehousekeeper/ExitGoods/create/For_Referred/',
         views.ExitGoods_Create_For_Referred, name='ExitGoods_Create_For_Referred'),


    path('warehousekeeper/ExitGoods/create/For_Referred/id/<id>/',
         views.ExitGoods_Create_For_Referred_id, name='ExitGoods_Create_For_Referred_id'),



    path('warehousekeeper/ExitGoods/view/', views.ExitGoods_view, name='ExitGoods_view'),

    path('warehousekeeper/ExitGoods/view/ByFilter/Filter_DateAse/', views.ExitGoods_ByFilter_Filter_DateAsc,
         name='ExitGoods_ByFilter_Filter_DateAsc'),

    path('warehousekeeper/ExitGoods/view/ByFilter/Filter_MaxValue/', views.ExitGoods_ByFilter_Filter_MaxValue,
         name='ExitGoods_ByFilter_Filter_MaxValue'),
    path('warehousekeeper/ExitGoods/view/ByFilter/Filter_MinValue/', views.ExitGoods_ByFilter_Filter_MinValue,
         name='ExitGoods_ByFilter_Filter_MinValue'),
    path('warehousekeeper/ExitGoods/view/ByFilter/Filter_Location/', views.ExitGoods_ByFilter_Filter_Location,
         name='ExitGoods_ByFilter_Filter_Location'),
    path('warehousekeeper/ExitGoods/view/ByFilter/Filter_Driver/', views.ExitGoods_ByFilter_Filter_Driver,
         name='ExitGoods_ByFilter_Filter_Driver'),
    path('warehousekeeper/ExitGoods/view/ByFilter/Filter_Sender/', views.ExitGoods_ByFilter_Filter_Sender,
         name='ExitGoods_ByFilter_Filter_Sender'),


    path('warehousekeeper/ExitGoods/delete/<id>/', views.ExitGoods_delete, name='ExitGoods_delete'),
    path('warehousekeeper/ExitGoods/update/<id>/', views.ExitGoods_update, name='ExitGoods_update'),

    path('warehousekeeper/ExitGoods/view/ByFilter/', views.ExitGoods_view_ByFilter,
         name='ExitGoods_view_ByFilter'),

    path('warehousekeeper/ExitGoods/view/ByFilter/WarehouseName/', views.ExitGoods_view_ByFilter_WarehouseName,
         name='ExitGoods_view_ByFilter_WarehouseName'),

    path('warehousekeeper/ExitGoods/view/ByFilter/DriverName/', views.ExitGoods_view_ByFilter_DriverName,
         name='ExitGoods_view_ByFilter_DriverName'),

    path('warehousekeeper/ExitGoods/view/ByFilter/ReferredName/',
         views.ExitGoods_view_ByFilter_ReferredName,
         name='ExitGoods_view_ByFilter_ReferredName'),

    path('warehousekeeper/ExitGoods/view/ByFilter/WarehouseName_Date/',
         views.ExitGoods_view_ByFilter_WarehouseName_Date,
         name='ExitGoods_view_ByFilter_WarehouseName_Date'),

    path('warehousekeeper/ExitGoods/view/ByFilter/WarehouseName_Date_DriverName/',
         views.ExitGoods_view_ByFilter_WarehouseName_Date_DriverName,
         name='ExitGoods_view_ByFilter_WarehouseName_Date_DriverName'),


    path('warehousekeeper/ExitGoods/ShowSerials/<id>/', views.ExitGoods_Serials, name='ExitGoods_Serials'),
    path('warehousekeeper/ExitGoods/SearchSerial/', views.SearchSerial,
         name='SearchSerial'),


    path('warehousekeeper/ExitGoods/view/ByFilter/FreightNumber', views.ExitGoods_view_ByFilter_SerialForDriver,
         name='ExitGoods_view_ByFilter_SerialForDriver'),


    path('warehousekeeper/ExitGoods/view/ByFilter/FreightNumber/<str:serial>/',
         views.ExitGoods_view_ByFilter_SerialForDriver_Serial,
         name='ExitGoods_view_ByFilter_SerialForDriver_Serial'),






    path('warehousekeeper/Requestgoods/view/unanswered/', views.Requestgoods_unanswered,
         name='Requestgoods_unanswered'),

    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Filter_DateAse/',
         views.Requestgoods_ByFilter_Filter_DateAsc,
         name='Requestgoods_ByFilter_Filter_DateAsc'),

    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Filter_MaxValue/',
         views.Requestgoods_ByFilter_Filter_MaxValue,
         name='Requestgoods_ByFilter_Filter_MaxValue'),

    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Filter_MinValue/',
         views.Requestgoods_ByFilter_Filter_MinValue,
         name='Requestgoods_ByFilter_Filter_MinValue'),

    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Filter_GoodsName/',
         views.Requestgoods_ByFilter_Filter_GoodsName,
         name='Requestgoods_ByFilter_Filter_GoodsName'),

    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Filter_Warehousekeeper/',
         views.Requestgoods_ByFilter_Filter_Warehousekeeper,
         name='Requestgoods_ByFilter_Filter_Warehousekeeper'),

    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Filter_Applicant/',
         views.Requestgoods_ByFilter_Filter_Applicant,
         name='Requestgoods_ByFilter_Filter_Applicant'),






    path('warehousekeeper/Requestgoods/view/unanswered/respond/<id>/', views.Requestgoods_respond,
         name='Requestgoods_respond'),




    path('warehousekeeper/Requestgoods/view/accepted/', views.Requestgoods_accepted, name='Requestgoods_accepted'),

    path('warehousekeeper/Requestgoods/accepted/view/ByFilter/Filter_DateAse/',
         views.Requestgoods_accepted_ByFilter_Filter_DateAsc,
         name='Requestgoods_accepted_ByFilter_Filter_DateAsc'),

    path('warehousekeeper/Requestgoods/accepted/view/ByFilter/Filter_MaxValue/',
         views.Requestgoods_accepted_ByFilter_Filter_MaxValue,
         name='Requestgoods_accepted_ByFilter_Filter_MaxValue'),

    path('warehousekeeper/Requestgoods/accepted/view/ByFilter/Filter_MinValue/',
         views.Requestgoods_accepted_ByFilter_Filter_MinValue,
         name='Requestgoods_accepted_ByFilter_Filter_MinValue'),

    path('warehousekeeper/Requestgoods/accepted/view/ByFilter/Filter_GoodsName/',
         views.Requestgoods_accepted_ByFilter_Filter_GoodsName,
         name='Requestgoods_accepted_ByFilter_Filter_GoodsName'),

    path('warehousekeeper/Requestgoods/accepted/view/ByFilter/Filter_Warehousekeeper/',
         views.Requestgoods_accepted_ByFilter_Filter_Warehousekeeper,
         name='Requestgoods_accepted_ByFilter_Filter_Warehousekeeper'),

    path('warehousekeeper/Requestgoods/accepted/view/ByFilter/Filter_Applicant/',
         views.Requestgoods_accepted_ByFilter_Filter_Applicant,
         name='Requestgoods_accepted_ByFilter_Filter_Applicant'),





    path('warehousekeeper/Requestgoods/view/rejected/', views.Requestgoods_rejected, name='Requestgoods_rejected'),

    path('warehousekeeper/Requestgoods/rejected/view/ByFilter/Filter_DateAse/',
         views.Requestgoods_rejected_ByFilter_Filter_DateAsc,
         name='Requestgoods_rejected_ByFilter_Filter_DateAsc'),

    path('warehousekeeper/Requestgoods/rejected/view/ByFilter/Filter_MaxValue/',
         views.Requestgoods_rejected_ByFilter_Filter_MaxValue,
         name='Requestgoods_rejected_ByFilter_Filter_MaxValue'),

    path('warehousekeeper/Requestgoods/rejected/view/ByFilter/Filter_MinValue/',
         views.Requestgoods_rejected_ByFilter_Filter_MinValue,
         name='Requestgoods_rejected_ByFilter_Filter_MinValue'),

    path('warehousekeeper/Requestgoods/rejected/view/ByFilter/Filter_GoodsName/',
         views.Requestgoods_rejected_ByFilter_Filter_GoodsName,
         name='Requestgoods_rejected_ByFilter_Filter_GoodsName'),

    path('warehousekeeper/Requestgoods/rejected/view/ByFilter/Filter_Warehousekeeper/',
         views.Requestgoods_rejected_ByFilter_Filter_Warehousekeeper,
         name='Requestgoods_rejected_ByFilter_Filter_Warehousekeeper'),

    path('warehousekeeper/Requestgoods/rejected/view/ByFilter/Filter_Applicant/',
         views.Requestgoods_rejected_ByFilter_Filter_Applicant,
         name='Requestgoods_rejected_ByFilter_Filter_Applicant'),




    path('warehousekeeper/Requestgoods/view/all/', views.Requestgoods_all, name='Requestgoods_all'),


    path('warehousekeeper/Requestgoods/view/all_items/', views.Requestgoods_all_items, name='Requestgoods_all_items'),





    path('warehousekeeper/Requestgoods/view/all_items/onside',
         views.Requestgoods_all_items_onside, name='Requestgoods_all_items_onside'),




    path('warehousekeeper/Requestgoods/view/all_items/onside/Filter_GoodsName',
         views.Requestgoods_all_items_onside_Filter_GoodsName, name='Requestgoods_all_items_onside_Filter_GoodsName'),

    path('warehousekeeper/Requestgoods/view/all_items/onside/Filter_minValue',
         views.Requestgoods_all_items_onside_Filter_minValue, name='Requestgoods_all_items_onside_Filter_minValue'),

    path('warehousekeeper/Requestgoods/view/all_items/onside/Filter_maxValue',
         views.Requestgoods_all_items_onside_Filter_maxValue, name='Requestgoods_all_items_onside_Filter_maxValue'),

    path('warehousekeeper/Requestgoods/view/all_items/onside/Filter_refferd',
         views.Requestgoods_all_items_onside_Filter_refferd, name='Requestgoods_all_items_onside_Filter_refferd'),

    path('warehousekeeper/Requestgoods/view/all_items/onside/Filter_dateAse',
         views.Requestgoods_all_items_onside_Filter_dateAse, name='Requestgoods_all_items_onside_Filter_dateAse'),

    path('warehousekeeper/Requestgoods/view/all_items/onside/Filter_dateDse',
         views.Requestgoods_all_items_onside_Filter_dateDse, name='Requestgoods_all_items_onside_Filter_dateDse'),







    path('warehousekeeper/Requestgoods/view/all_items/SearchByCode',
         views.Requestgoods_all_items_SearchByCode, name='Requestgoods_all_items_SearchByCode'),





    path('warehousekeeper/Requestgoods/all/view/ByFilter/Filter_DateAse/',
         views.Requestgoods_all_ByFilter_Filter_DateAsc,
         name='Requestgoods_all_ByFilter_Filter_DateAsc'),

    path('warehousekeeper/Requestgoods/all/view/ByFilter/Filter_MaxValue/',
         views.Requestgoods_all_ByFilter_Filter_MaxValue,
         name='Requestgoods_all_ByFilter_Filter_MaxValue'),

    path('warehousekeeper/Requestgoods/all/view/ByFilter/Filter_MinValue/',
         views.Requestgoods_all_ByFilter_Filter_MinValue,
         name='Requestgoods_all_ByFilter_Filter_MinValue'),

    path('warehousekeeper/Requestgoods/all/view/ByFilter/Filter_GoodsName/',
         views.Requestgoods_all_ByFilter_Filter_GoodsName,
         name='Requestgoods_all_ByFilter_Filter_GoodsName'),

    path('warehousekeeper/Requestgoods/all/view/ByFilter/Filter_Warehousekeeper/',
         views.Requestgoods_all_ByFilter_Filter_Warehousekeeper,
         name='Requestgoods_all_ByFilter_Filter_Warehousekeeper'),

    path('warehousekeeper/Requestgoods/all/view/ByFilter/Filter_Applicant/',
         views.Requestgoods_all_ByFilter_Filter_Applicant,
         name='Requestgoods_all_ByFilter_Filter_Applicant'),


    path('warehousekeeper/Requestgoods/unanswered/view/ByFilter/Resualt/',
         views.Requestgoods_ByFilter_Filter_Resualt,
         name='Requestgoods_ByFilter_Filter_Resualt'),




    path('warehousekeeper/Allgoods/ByName/<str:GoodsName>/', views.Allgoods_ByName, name='Allgoods_ByName'),

    path('warehousekeeper/ShowInfoDriver/', views.ShowInfoDriver, name='ShowInfoDriver'),

    path('warehousekeeper/ShowInfoReferred/', views.ShowInfoReferred, name='ShowInfoReferred'),








    path('warehousekeeper/WarehouseHandling/create/', views.WarehouseHandling_Create,
         name='WarehouseHandling_Create'),

    path('warehousekeeper/WarehouseHandling/view/', views.WarehouseHandling_view,
         name='WarehouseHandling_view'),

    path('warehousekeeper/WarehouseHandling/view/FilterDate_Ase/', views.WarehouseHandling_view_FilterDate_Ase,
         name='WarehouseHandling_view_FilterDate_Ase'),

    path('warehousekeeper/WarehouseHandling/delete/<id>/', views.WarehouseHandling_delete,
         name='WarehouseHandling_delete'),

    path('warehousekeeper/WarehouseHandling/update/<id>/', views.WarehouseHandling_update,
         name='WarehouseHandling_update'),



    path('warehousekeeper/WarehouseHandling/view/ByFilter/date/', views.WarehouseHandling_view_ByFilter_date,
         name='WarehouseHandling_view_ByFilter_date'),

    path('warehousekeeper/WarehouseHandling/continue/', views.WarehouseHandling_continue,
         name='WarehouseHandling_continue'),

    path('warehousekeeper/WarehouseHandling/continue/GoodsValue/<id>/', views.WarehouseHandling_GoodsValue,
         name='WarehouseHandling_GoodsValue'),






    path('warehousekeeper/view_exitgoods_by_serial_w/<id>/', views.view_exitgoods_by_serial_w,
         name='view_exitgoods_by_serial_w'),













##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


    path('referred/', views.referred, name='referred'),
    path('referred/create_Requestgoods/', views.create_Requestgoods, name='create_Requestgoods'),
    path('referred/view_Requestgoods/', views.view_Requestgoods, name='view_Requestgoods'),


    path('referred/view_Requestgoods/Filter_Goodsname/', views.view_Requestgoods_Goodsname,
         name='view_Requestgoods_Goodsname'),

    path('referred/view_Requestgoods/Filter_minValue/', views.view_Requestgoods_minValue,
         name='view_Requestgoods_minValue'),

    path('referred/view_Requestgoods/Filter_maxValue/', views.view_Requestgoods_maxValue,
         name='view_Requestgoods_maxValue'),

    path('referred/view_Requestgoods/Filter_Result/', views.view_Requestgoods_Result,
         name='view_Requestgoods_Result'),



    path('referred/view_Requestgoods/Filter_Ascending/', views.view_Requestgoods_Ace, name='view_Requestgoods_Ace'),
    path('referred/delete_Requestgoods/<id>/', views.delete_Requestgoods, name='delete_Requestgoods'),
    path('referred/update_Requestgoods/<id>/', views.update_Requestgoods, name='update_Requestgoods'),
    path('referred/view_Requestgoods/ByFilter/Date', views.view_Requestgoods_ByFilter_Date,
         name='view_Requestgoods_ByFilter_Date'),




    path('referred/view_exitgoods_by_serial_r/<id>/', views.view_exitgoods_by_serial_r,
         name='view_exitgoods_by_serial_r'),















######################################################################################
######################################################################################
######################################################################################
######################################################################################




    path('driver/', views.driver, name='driver'),
    path('driver/view_Exitgoods/', views.view_Exitgoods, name='view_Exitgoods'),


    path('driver/view_Exitgoods/Filter_refferd/', views.view_Exitgoods_Filter_refferd,
         name='view_Exitgoods_Filter_refferd'),
    path('driver/view_Exitgoods/Filter_minValule/', views.view_Exitgoods_Filter_minValule,
         name='view_Exitgoods_Filter_minValule'),
    path('driver/view_Exitgoods/Filter_maxvalue/', views.view_Exitgoods_Filter_maxvalue,
         name='view_Exitgoods_Filter_maxvalue'),
    path('driver/view_Exitgoods/Filter_GoodsName/', views.view_Exitgoods_Filter_GoodsName,
         name='view_Exitgoods_Filter_GoodsName'),
    path('driver/view_Exitgoods/Filter_Serialfordriver/', views.view_Exitgoods_Filter_Serialfordriver,
         name='view_Exitgoods_Filter_Serialfordriver'),
    path('driver/view_Exitgoods/Filter_serialExit/', views.view_Exitgoods_Filter_serialExit,
         name='view_Exitgoods_Filter_serialExit'),
    path('driver/view_Exitgoods/Filter_warehouse/', views.view_Exitgoods_Filter_warehouse,
         name='view_Exitgoods_Filter_warehouse'),


    path('driver/view_Exitgoods/Filter_Ascending/', views.view_Exitgoods_Ace, name='view_Exitgoods_Ace'),
    path('driver/view_EntryGoods/', views.view_EntryGoods, name='view_EntryGoods'),


    path('driver/view_EntryGoods/Filter_refferd/', views.view_EntryGoods_Filter_refferd,
         name='view_EntryGoods_Filter_refferd'),
    path('driver/view_EntryGoods/Filter_minValule/', views.view_EntryGoods_Filter_minValule,
         name='view_EntryGoods_Filter_minValule'),
    path('driver/view_EntryGoods/Filter_maxvalue/', views.view_EntryGoods_Filter_maxvalue,
         name='view_EntryGoods_Filter_maxvalue'),
    path('driver/view_EntryGoods/Filter_GoodsName/', views.view_EntryGoods_Filter_GoodsName,
         name='view_EntryGoods_Filter_GoodsName'),
    path('driver/view_EntryGoods/Filter_Serialfordriver/', views.view_EntryGoods_Filter_Serialfordriver,
         name='view_EntryGoods_Filter_Serialfordriver'),
    path('driver/view_EntryGoods/Filter_serialExit/', views.view_EntryGoods_Filter_serialExit,
         name='view_EntryGoods_Filter_serialExit'),
    path('driver/view_EntryGoods/Filter_warehouse/', views.view_EntryGoods_Filter_warehouse,
         name='view_EntryGoods_Filter_warehouse'),


    path('driver/view_EntryGoods/Filter_Ascending/', views.view_EntryGoods_Ace, name='view_EntryGoods_Ace'),
    path('driver/view_Exitgoods/ByDate/', views.view_Exitgoods_ByDate, name='view_Exitgoods_ByDate'),
    path('driver/view_Exitgoods/InsertDate/', views.date_for_view_Exitgoods, name='date_for_view_Exitgoods'),
    path('driver/view_Entergoods/ByDate/', views.view_Entergoods_ByDate, name='view_Entergoods_ByDate'),
    path('driver/view_Entergoods/InsertDate/', views.date_for_view_Entergoods, name='date_for_view_Entergoods'),


    path('driver/EntryGoods/view/ByFilter/FreightNumber', views.EntryGoods_view_ByFilter_SerialForDriver_DRIVER,
         name='EntryGoods_view_ByFilter_SerialForDriver_DRIVER'),


    path('driver/ExitGoods/view/ByFilter/FreightNumber', views.ExitGoods_view_ByFilter_SerialForDriver_DRIVER,
         name='ExitGoods_view_ByFilter_SerialForDriver_DRIVER'),


]