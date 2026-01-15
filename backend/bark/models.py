import uuid
import datetime
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_bark_job_number():
    year = datetime.date.today().year
    last_job = RepairJob.objects.filter(job_number__contains=f"BARK-{year}").order_by('-id').first()
    if not last_job:
        return f"BARK-{year}-0001"
    
   
    last_number = int(last_job.job_number.split('-')[-1])
    new_number = str(last_number + 1).zfill(4)
    return f"BARK-{year}-{new_number}"

class AuditModel(models.Model):
    """Abstract base class to provide audit fields automatically."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True

class Status(models.Model):
    CATEGORY_CHOICES = [
        ('APPROVAL', 'LOA & INSURANCE'),
        ('PARTS', 'Parts Procurement'),
        ('REPAIR', 'Repair Shop Stage'),
        ('PICKUP', 'Releasing Stage'),
        ('BILLING', 'Insurance Claims'),
        ('DISMANTLE', 'Total Wreck'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, default="#3498db")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.status_name}"


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    modu_customer_id = models.CharField(max_length=100, blank=True, null=True)
    synced_to_modu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def upsert_by_phone(cls, *, phone_number, name, email=""):
        customer = None
        if phone_number:
            customer = cls.objects.filter(phone_number=phone_number).first()

        if customer:
            updates = {}
            if name and customer.name != name:
                updates["name"] = name
            if email and customer.email != email:
                updates["email"] = email
            if updates:
                for field, value in updates.items():
                    setattr(customer, field, value)
                customer.save(update_fields=[*updates.keys(), "updated_at"])
            return customer, False

        customer = cls.objects.create(
            name=name,
            phone_number=phone_number or "",
            email=email or "",
            synced_to_modu=False,
        )
        return customer, True

    def __str__(self):
        return self.name


class Job(models.Model):
    customer = models.ForeignKey("bark.Customer", on_delete=models.PROTECT, related_name="jobs")
    vehicle_details = models.TextField()
    current_status = models.ForeignKey("bark.Status", on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_repair_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_with_customer_autofill(cls, *, customer_name, phone_number="", email="", **job_fields):
        customer, _created = Customer.upsert_by_phone(
            phone_number=phone_number, name=customer_name, email=email
        )
        return cls.objects.create(customer=customer, **job_fields)

    def advance_to_scheduling(self):
        if self.current_status_id not in (13, 14):
            raise ValueError("Advance to scheduling requires Partial Parts Received or Parts Complete.")
        self.current_status = Status.objects.get(pk=21)
        self.save(update_fields=["current_status", "updated_at"])
        return self

    def can_proceed_to_scheduling(self):
        return self.current_status_id in (13, 14)

    @property
    def waiting_for_parts(self):
        return self.current_status_id == 13

    def has_reached_milestone(self, status_pk):
        return self.history.filter(status_id=status_pk).exists()

    def get_available_transitions(self):
        if self.current_status and self.current_status.category == "PARTS":
            return [21] if self.can_proceed_to_scheduling() else []
        return []

    @property
    def is_overdue(self):
        if not self.current_status:
            return False
        if self.current_status.category != "BILLING" or self.current_status.status_name != "Pending":
            return False
        last_entry = self.history.filter(status=self.current_status).order_by("-timestamp").first()
        if not last_entry:
            return False
        overdue_threshold = timezone.now() - datetime.timedelta(days=30)
        return last_entry.timestamp <= overdue_threshold

    def __str__(self):
        return f"Job {self.id}"


class JobHistory(models.Model):
    job = models.ForeignKey("bark.Job", on_delete=models.CASCADE, related_name="history")
    status = models.ForeignKey("bark.Status", on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job} -> {self.status} @ {self.timestamp}"


class RepairJob(models.Model):
    job_number = models.CharField(
        max_length=20, 
        unique=True, 
        default=generate_bark_job_number, 
        editable=False
    )
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]


    # LINK TO CUSTOMER
    customer = models.ForeignKey("core.Customer", on_delete=models.PROTECT, related_name="bark_jobs")
    vehicle = models.ForeignKey("bark.Vehicle", on_delete=models.PROTECT, related_name="repair_jobs")
    insurance = models.ForeignKey("bark.InsuranceCompany", on_delete=models.PROTECT, related_name="repair_jobs")
    repairjob_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_number = models.CharField(max_length=20, unique=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    promised_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ----- LIVE TRACKER -------
    current_status = models.ForeignKey(
        "bark.Status",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # ----- PHASE 1 (ESTIMATE PHASE) ------
    estimate_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimate_date = models.DateTimeField(auto_now_add=True)
    repair_order = models.TextField()
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)
    job_order = models.TextField()
    total_labor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_parts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # ------- PHASE 2 (APPROVED PHASE) ------
    approved_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approved_repair_order = models.TextField(null=True, blank=True)
    approved_job_order = models.TextField(null=True, blank=True)
    loa_date = models.DateTimeField(null=True, blank=True)

    # ------ PHASE 3 (GAP/DIFFERENCE) -----
    @property
    def price_variance(self):
        if self.approved_estimate is not None:
            return self.approved_estimate - self.estimate_price
        return Decimal("0.00")

    def __str__(self):
        return f"RepairJob {self.repairjob_uid}"


class StatusLog(models.Model):
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name="history")
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)  # "Parts are late"

    def __str__(self):
        return f"{self.repair_job} -> {self.status} @ {self.changed_at}"
    

class InsuranceCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    owner = models.ForeignKey("core.Customer", on_delete=models.PROTECT, related_name="vehicles")
    model = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model} ({self.plate_number})" if self.plate_number else self.model
    
class JobMedia(models.Model):
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to="repair_damages/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class EstimateItem(models.Model):
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name="estimate_items")
    description = models.CharField(max_length=255)
    part_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
