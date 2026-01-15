from django.contrib import admin



from .models import Customer, InsuranceCompany, Job, JobHistory, RepairJob, Status, StatusLog, Vehicle


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("status_name", "category", "color_code", "order")
    list_filter = ("category",)
    search_fields = ("status_name",)



@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ("repair_job", "status", "changed_at")
    list_filter = ("status", "changed_at")
    search_fields = ("repair_job__repairjob_uid", "status__status_name")
    list_select_related = ("repair_job", "status")


@admin.register(JobHistory)
class JobHistoryAdmin(admin.ModelAdmin):
    list_display = ("job", "status", "timestamp")
    list_filter = ("status", "timestamp")
    search_fields = ("job__id", "status__status_name")
    list_select_related = ("job", "status")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "current_status", "created_at")
    list_filter = ("current_status", "created_at")
    search_fields = ("customer__name", "vehicle_details", "id")
    list_select_related = ("customer", "current_status")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "email", "modu_customer_id", "synced_to_modu")
    search_fields = ("name", "phone_number", "email", "modu_customer_id")


@admin.register(RepairJob)
class RepairJobAdmin(admin.ModelAdmin):
    list_display = ("repairjob_uid", "customer", "estimate_price", "current_status", "estimate_date")
    list_filter = ("current_status", "estimate_date")
    search_fields = ("customer__full_name", "vehicle__model", "insurance__name", "repairjob_uid")
    readonly_fields = ("price_variance",)
    list_select_related = ("customer", "vehicle", "insurance", "current_status")



@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("model", "plate_number", "owner")
    search_fields = ("model", "plate_number", "owner__full_name")
