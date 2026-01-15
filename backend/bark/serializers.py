from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from core.models import Customer
from .models import EstimateItem, Job, JobHistory, RepairJob, Status, Vehicle, InsuranceCompany

# 1. Simple serializers for related data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_uuid', 'full_name', 'contact_number', 'email']

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = ['id', 'name']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle 
        fields = ['id', 'model', 'plate_number']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'category', 'status_name', 'color_code', 'order']

# 2. The Super Serializer (The Engine)

class RepairJobSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    vehicle = VehicleSerializer()
    insurance = InsuranceSerializer(read_only=True)
    insurance_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    total_parts = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total_labor = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    service_tax = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    estimate_items = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
    estimate_items_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RepairJob
        fields = [
            'id', 'job_number', 'customer', 'vehicle', 'insurance',
            'insurance_name', 'priority', 'promised_date', 'current_status',
            'estimate_price', 'labor_cost', 'repair_order', 'job_order',
            'total_parts', 'total_labor', 'service_tax', 'grand_total',
            'estimate_items', 'estimate_items_detail'
        ]

    def get_estimate_items_detail(self, obj):
        return [
            {
                "id": item.id,
                "description": item.description,
                "part_cost": item.part_cost,
                "labor_cost": item.labor_cost,
            }
            for item in obj.estimate_items.all()
        ]

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        vehicle_data = validated_data.pop('vehicle')
        insurance_name = validated_data.pop('insurance_name', '').strip()
        estimate_items_data = validated_data.pop('estimate_items', [])
        validated_data.pop('estimate_price', None)
        validated_data.pop('labor_cost', None)
        total_parts = Decimal(validated_data.pop('total_parts', 0) or 0)
        total_labor = Decimal(validated_data.pop('total_labor', 0) or 0)

        if estimate_items_data:
            total_parts = sum(
                Decimal(str(item.get("part_cost", 0) or 0)) for item in estimate_items_data
            )
            total_labor = sum(
                Decimal(str(item.get("labor_cost", 0) or 0)) for item in estimate_items_data
            )
        service_tax = (total_labor * Decimal("0.12")).quantize(Decimal("0.01"))
        grand_total = (total_parts + total_labor + service_tax).quantize(Decimal("0.01"))

        with transaction.atomic():
            customer, _ = Customer.objects.get_or_create(**customer_data)

            insurance = None
            if insurance_name:
                insurance, _ = InsuranceCompany.objects.get_or_create(name=insurance_name)

            vehicle, _ = Vehicle.objects.get_or_create(owner=customer, **vehicle_data)

            repair_job = RepairJob.objects.create(
                customer=customer,
                vehicle=vehicle,
                insurance=insurance,
                total_parts=total_parts,
                total_labor=total_labor,
                service_tax=service_tax,
                grand_total=grand_total,
                estimate_price=total_parts + total_labor,
                labor_cost=total_labor,
                **validated_data
            )

            if estimate_items_data:
                EstimateItem.objects.bulk_create(
                    [
                        EstimateItem(
                            repair_job=repair_job,
                            description=item.get("description", ""),
                            part_cost=Decimal(str(item.get("part_cost", 0) or 0)),
                            labor_cost=Decimal(str(item.get("labor_cost", 0) or 0)),
                        )
                        for item in estimate_items_data
                    ]
                )

            return repair_job

    def update(self, instance, validated_data):
        estimate_items_data = validated_data.pop('estimate_items', None)
        validated_data.pop('estimate_price', None)
        validated_data.pop('labor_cost', None)
        total_parts = Decimal(validated_data.pop('total_parts', instance.total_parts) or 0)
        total_labor = Decimal(validated_data.pop('total_labor', instance.total_labor) or 0)

        if estimate_items_data is not None:
            total_parts = sum(
                Decimal(str(item.get("part_cost", 0) or 0)) for item in estimate_items_data
            )
            total_labor = sum(
                Decimal(str(item.get("labor_cost", 0) or 0)) for item in estimate_items_data
            )
            instance.estimate_items.all().delete()
            EstimateItem.objects.bulk_create(
                [
                    EstimateItem(
                        repair_job=instance,
                        description=item.get("description", ""),
                        part_cost=Decimal(str(item.get("part_cost", 0) or 0)),
                        labor_cost=Decimal(str(item.get("labor_cost", 0) or 0)),
                    )
                    for item in estimate_items_data
                ]
            )

        service_tax = (total_labor * Decimal("0.12")).quantize(Decimal("0.01"))
        grand_total = (total_parts + total_labor + service_tax).quantize(Decimal("0.01"))

        instance.total_parts = total_parts
        instance.total_labor = total_labor
        instance.service_tax = service_tax
        instance.grand_total = grand_total
        instance.estimate_price = total_parts + total_labor
        instance.labor_cost = total_labor

        return super().update(instance, validated_data)


class JobUpdateSerializer(serializers.ModelSerializer):
    target_status_id = serializers.IntegerField(write_only=True)
    is_overdue = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "customer",
            "vehicle_details",
            "current_status",
            "waiting_for_parts",
            "target_status_id",
            "is_overdue",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "customer",
            "vehicle_details",
            "current_status",
            "waiting_for_parts",
            "is_overdue",
            "created_at",
            "updated_at",
        ]

    def get_is_overdue(self, obj):
        return obj.is_overdue

    def validate_target_status_id(self, value):
        if not Status.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Target status does not exist.")
        return value

    def validate(self, attrs):
        instance = self.instance
        if not instance:
            return attrs

        target_status_id = attrs.get("target_status_id")
        target_status = Status.objects.get(pk=target_status_id)
        current_status = instance.current_status

        if target_status_id == 21 and instance.current_status_id not in (13, 14):
            raise serializers.ValidationError(
                {"target_status_id": "Scheduling requires Partial Parts Received or Parts Complete."}
            )

        if current_status:
            category_order = {
                "APPROVAL": 1,
                "PARTS": 2,
                "REPAIR": 3,
                "PICKUP": 4,
                "BILLING": 5,
                "DISMANTLE": 6,
            }
            current_order = category_order.get(current_status.category)
            target_order = category_order.get(target_status.category)
            if current_order and target_order and target_order - current_order > 1:
                raise serializers.ValidationError(
                    {"target_status_id": "Cannot skip phases (e.g., Phase 1 straight to Phase 4)."}
                )

        step_requirements = {
            25: 24,  # Ongoing Body Paint requires Ongoing Body Work completed.
        }
        required_status_id = step_requirements.get(target_status_id)
        if required_status_id:
            has_required = JobHistory.objects.filter(
                job=instance, status_id=required_status_id
            ).exists()
            if not has_required:
                raise serializers.ValidationError(
                    {"target_status_id": "Required step not completed for this transition."}
                )

        return attrs

    def update(self, instance, validated_data):
        target_status_id = validated_data["target_status_id"]

        if target_status_id == 21 and instance.current_status_id in (13, 14):
            return instance.advance_to_scheduling()

        instance.current_status_id = target_status_id
        instance.save(update_fields=["current_status", "updated_at"])
        return instance


class JobSerializer(serializers.ModelSerializer):
    status_color = serializers.SerializerMethodField(read_only=True)
    is_overdue = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "customer",
            "vehicle_details",
            "current_status",
            "waiting_for_parts",
            "status_color",
            "is_overdue",
            "created_at",
            "updated_at",
        ]

    def get_status_color(self, obj):
        if not obj.current_status:
            return None
        return obj.current_status.color_code

    def get_is_overdue(self, obj):
        return obj.is_overdue


class JobTransitionSerializer(serializers.ModelSerializer):
    target_status_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Job
        fields = ["id", "current_status", "target_status_id"]
        read_only_fields = ["id", "current_status"]

    def validate(self, attrs):
        instance = self.instance
        target_status_id = attrs.get("target_status_id")
        if not instance or not target_status_id:
            return attrs

        target_status = Status.objects.filter(pk=target_status_id).first()
        if not target_status:
            raise serializers.ValidationError({"target_status_id": "Target status does not exist."})

        if target_status.category == "REPAIR":
            has_loa_approved = JobHistory.objects.filter(
                job=instance, status_id=5
            ).exists()
            if not has_loa_approved:
                raise serializers.ValidationError(
                    {"target_status_id": "LOA Approved is required before moving to Repair."}
                )

        return attrs

    def update(self, instance, validated_data):
        target_status_id = validated_data["target_status_id"]
        instance.current_status_id = target_status_id
        instance.save(update_fields=["current_status", "updated_at"])
        return instance


class JobStatusUpdateSerializer(serializers.ModelSerializer):
    current_status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    scheduled_repair_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Job
        fields = ["current_status", "scheduled_repair_date"]

    def validate_current_status(self, value):
        instance = self.instance
        if not instance:
            return value

        target_status_id = value.pk
        repair_phase_ids = set(range(21, 28))
        scheduling_phase_ids = {21}

        if target_status_id in repair_phase_ids and not instance.has_reached_milestone(5):
            raise serializers.ValidationError(
                "LOA Approved (pk=5) is required before moving into Repair."
            )

        if target_status_id in scheduling_phase_ids and not instance.can_proceed_to_scheduling():
            raise serializers.ValidationError(
                "Scheduling is only allowed from Partial Parts or Parts Complete."
            )

        return value

    def validate(self, attrs):
        current_status = attrs.get("current_status")
        scheduled_repair_date = attrs.get("scheduled_repair_date")
        if current_status and current_status.pk == 22 and not scheduled_repair_date:
            raise serializers.ValidationError(
                {"scheduled_repair_date": "scheduled_repair_date is required for Scheduled for Repair."}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.current_status = validated_data["current_status"]
        if "scheduled_repair_date" in validated_data:
            instance.scheduled_repair_date = validated_data["scheduled_repair_date"]
        instance.save(update_fields=["current_status", "scheduled_repair_date", "updated_at"])
        return instance
        
        
