from django.db.models import (
    Avg,
    Count,
    DurationField,
    ExpressionWrapper,
    F,
    Max,
    Min,
    OuterRef,
    Subquery,
    Sum,
)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Job, JobHistory, RepairJob, Status, StatusLog
from .serializers import (
    JobSerializer,
    JobStatusUpdateSerializer,
    JobTransitionSerializer,
    RepairJobSerializer,
    StatusSerializer,
)


class BarkHealthView(APIView):
    """
    Lightweight BARK-specific health/ping endpoint.
    """

    def get(self, request):
        return Response({"service": "bark", "status": "ok"})
    
class RepairJobViewSet(viewsets.ModelViewSet):
    queryset = RepairJob.objects.all().order_by('-created_at')
    serializer_class = RepairJobSerializer

    #Adding Filters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['job_number', 'customer__first_name', 'vehicle__plate_number']

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all().order_by('category', 'order')
    serializer_class = StatusSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer

    @action(detail=True, methods=["patch"])
    def transition(self, request, pk=None):
        job = self.get_object()
        serializer = JobStatusUpdateSerializer(instance=job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(JobSerializer(job).data, status=status.HTTP_200_OK)


class JobStatusUpdateView(APIView):
    def patch(self, request, pk):
        job = Job.objects.filter(pk=pk).first()
        if not job:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        target_status_id = request.data.get("target_status_id")
        if not target_status_id:
            return Response(
                {"detail": "target_status_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target_status = Status.objects.filter(pk=target_status_id).first()
        if not target_status:
            return Response(
                {"detail": "Target status does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if target_status.category == "REPAIR":
            approval_complete = JobHistory.objects.filter(
                job=job, status__category="APPROVAL", status__order=6
            ).exists()
            if not approval_complete:
                return Response(
                    {"detail": "Approval phase is not completed for this job."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        job.current_status = target_status
        job.save(update_fields=["current_status", "updated_at"])
        return Response(JobSerializer(job).data, status=status.HTTP_200_OK)


class JobTransitionUpdateView(APIView):
    def patch(self, request, pk):
        job = Job.objects.filter(pk=pk).first()
        if not job:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobTransitionSerializer(instance=job, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(JobSerializer(job).data, status=status.HTTP_200_OK)


class UnsyncedCustomerView(APIView):
    def get(self, request):
        customers = Customer.objects.filter(synced_to_modu=False).order_by("created_at")
        payload = [
            {
                "id": customer.id,
                "name": customer.name,
                "phone_number": customer.phone_number,
                "email": customer.email,
                "modu_customer_id": customer.modu_customer_id,
                "synced_to_modu": customer.synced_to_modu,
            }
            for customer in customers
        ]
        return Response(payload)


class AnalyticsDashboardView(APIView):
    def get(self, request):
        estimate_done_subquery = StatusLog.objects.filter(
            repair_job=OuterRef("pk"), status_id=1
        ).order_by("changed_at").values("changed_at")[:1]
        released_subquery = StatusLog.objects.filter(
            repair_job=OuterRef("pk"), status_id=33
        ).order_by("changed_at").values("changed_at")[:1]

        cycle_time_queryset = RepairJob.objects.annotate(
            estimate_done_at=Subquery(estimate_done_subquery),
            released_at=Subquery(released_subquery),
        ).exclude(estimate_done_at__isnull=True, released_at__isnull=True)

        average_cycle = cycle_time_queryset.annotate(
            cycle_time=ExpressionWrapper(
                F("released_at") - F("estimate_done_at"), output_field=DurationField()
            )
        ).aggregate(average_cycle_time=Avg("cycle_time"))["average_cycle_time"]

        average_cycle_time_days = (
            average_cycle.total_seconds() / 86400 if average_cycle else None
        )

        revenue_rows = (
            RepairJob.objects.values("insurance__name")
            .annotate(
                approved_cost_total=Sum("approved_estimate"),
                job_count=Count("repairjob_uid"),
            )
            .order_by("insurance__name")
        )
        revenue_by_insurance = [
            {
                "insurance_provider": row["insurance__name"] or "Unknown",
                "approved_cost_total": row["approved_cost_total"] or 0,
                "job_count": row["job_count"],
            }
            for row in revenue_rows
        ]

        partial_count = (
            StatusLog.objects.filter(status_id=13)
            .values("repair_job")
            .distinct()
            .count()
        )
        complete_count = (
            StatusLog.objects.filter(status_id=14)
            .values("repair_job")
            .distinct()
            .count()
        )
        total_parts_branch = partial_count + complete_count
        parts_delay_rate = (
            (partial_count / total_parts_branch) * 100 if total_parts_branch else 0
        )

        return Response(
            {
                "average_cycle_time": average_cycle_time_days,
                "revenue_by_insurance": revenue_by_insurance,
                "parts_delay_rate": parts_delay_rate,
            }
        )


class JobAnalyticsView(APIView):
    def get(self, request):
        estimate_done_subquery = StatusLog.objects.filter(
            repair_job=OuterRef("pk"), status_id=1
        ).order_by("changed_at").values("changed_at")[:1]
        released_subquery = StatusLog.objects.filter(
            repair_job=OuterRef("pk"), status_id=33
        ).order_by("changed_at").values("changed_at")[:1]

        cycle_time_queryset = RepairJob.objects.annotate(
            estimate_done_at=Subquery(estimate_done_subquery),
            released_at=Subquery(released_subquery),
        ).exclude(estimate_done_at__isnull=True, released_at__isnull=True)

        average_cycle = cycle_time_queryset.annotate(
            cycle_time=ExpressionWrapper(
                F("released_at") - F("estimate_done_at"), output_field=DurationField()
            )
        ).aggregate(average_cycle_time=Avg("cycle_time"))["average_cycle_time"]

        average_cycle_time_days = (
            average_cycle.total_seconds() / 86400 if average_cycle else None
        )

        phase_duration_queryset = (
            StatusLog.objects.values("repair_job", "status__category")
            .annotate(
                first_seen=Min("changed_at"),
                last_seen=Max("changed_at"),
            )
            .annotate(
                phase_duration=ExpressionWrapper(
                    F("last_seen") - F("first_seen"), output_field=DurationField()
                )
            )
            .values("status__category")
            .annotate(average_duration=Avg("phase_duration"))
            .order_by("status__category")
        )

        phase_bottlenecks = [
            {
                "category": row["status__category"],
                "average_days": (
                    row["average_duration"].total_seconds() / 86400
                    if row["average_duration"]
                    else None
                ),
            }
            for row in phase_duration_queryset
        ]

        partial_count = (
            StatusLog.objects.filter(status_id=13)
            .values("repair_job")
            .distinct()
            .count()
        )
        complete_count = (
            StatusLog.objects.filter(status_id=14)
            .values("repair_job")
            .distinct()
            .count()
        )
        total_parts_branch = partial_count + complete_count
        partial_rate = (partial_count / total_parts_branch) * 100 if total_parts_branch else 0
        complete_rate = (complete_count / total_parts_branch) * 100 if total_parts_branch else 0

        paid_jobs = RepairJob.objects.filter(history__status_id=42).distinct()
        total_approved_cost = paid_jobs.aggregate(
            total_approved_cost=Sum("approved_estimate")
        )["total_approved_cost"] or 0
        revenue_by_insurance = (
            paid_jobs.values("insurance__name")
            .annotate(total=Sum("approved_estimate"))
            .order_by("insurance__name")
        )
        revenue_breakdown = [
            {
                "insurance_provider": row["insurance__name"] or "Unknown",
                "approved_cost_total": row["total"] or 0,
            }
            for row in revenue_by_insurance
        ]

        return Response(
            {
                "average_cycle_time_days": average_cycle_time_days,
                "phase_bottlenecks": phase_bottlenecks,
                "parts_efficiency": {
                    "partial_parts_percentage": partial_rate,
                    "parts_complete_percentage": complete_rate,
                },
                "total_approved_cost_paid": total_approved_cost,
                "revenue_by_insurance": revenue_breakdown,
            }
        )


class ShopAnalyticsView(APIView):
    def get(self, request):
        estimate_done_subquery = JobHistory.objects.filter(
            job=OuterRef("pk"), status_id=1
        ).order_by("timestamp").values("timestamp")[:1]
        released_subquery = JobHistory.objects.filter(
            job=OuterRef("pk"), status_id=33
        ).order_by("timestamp").values("timestamp")[:1]

        cycle_time_queryset = Job.objects.annotate(
            estimate_done_at=Subquery(estimate_done_subquery),
            released_at=Subquery(released_subquery),
        ).exclude(estimate_done_at__isnull=True, released_at__isnull=True)

        average_cycle = cycle_time_queryset.annotate(
            cycle_time=ExpressionWrapper(
                F("released_at") - F("estimate_done_at"), output_field=DurationField()
            )
        ).aggregate(average_cycle_time=Avg("cycle_time"))["average_cycle_time"]

        average_cycle_time_days = (
            average_cycle.total_seconds() / 86400 if average_cycle else None
        )

        next_timestamp_subquery = JobHistory.objects.filter(
            job=OuterRef("job_id"), timestamp__gt=OuterRef("timestamp")
        ).order_by("timestamp").values("timestamp")[:1]

        phase_duration_queryset = (
            JobHistory.objects.annotate(next_timestamp=Subquery(next_timestamp_subquery))
            .exclude(next_timestamp__isnull=True)
            .annotate(
                phase_duration=ExpressionWrapper(
                    F("next_timestamp") - F("timestamp"), output_field=DurationField()
                )
            )
            .values("status__category")
            .annotate(average_duration=Avg("phase_duration"))
            .order_by("status__category")
        )

        phase_bottlenecks = [
            {
                "category": row["status__category"],
                "average_days": (
                    row["average_duration"].total_seconds() / 86400
                    if row["average_duration"]
                    else None
                ),
            }
            for row in phase_duration_queryset
        ]

        partial_count = (
            JobHistory.objects.filter(status_id=13)
            .values("job")
            .distinct()
            .count()
        )
        complete_count = (
            JobHistory.objects.filter(status_id=14)
            .values("job")
            .distinct()
            .count()
        )
        total_parts_branch = partial_count + complete_count
        partial_rate = (partial_count / total_parts_branch) * 100 if total_parts_branch else 0
        complete_rate = (complete_count / total_parts_branch) * 100 if total_parts_branch else 0

        paid_jobs = RepairJob.objects.filter(
            current_status__category="BILLING", current_status__status_name="Paid"
        )
        total_approved_cost = paid_jobs.aggregate(
            total_approved_cost=Sum("approved_estimate")
        )["total_approved_cost"] or 0
        revenue_by_insurance = (
            paid_jobs.values("insurance__name")
            .annotate(total=Sum("approved_estimate"))
            .order_by("insurance__name")
        )
        revenue_breakdown = [
            {
                "insurance_provider": row["insurance__name"] or "Unknown",
                "approved_cost_total": row["total"] or 0,
            }
            for row in revenue_by_insurance
        ]

        return Response(
            {
                "average_cycle_time_days": average_cycle_time_days,
                "phase_bottlenecks": phase_bottlenecks,
                "parts_efficiency": {
                    "partial_parts_percentage": partial_rate,
                    "parts_complete_percentage": complete_rate,
                },
                "total_approved_cost_paid": total_approved_cost,
                "revenue_by_insurance": revenue_breakdown,
            }
        )
