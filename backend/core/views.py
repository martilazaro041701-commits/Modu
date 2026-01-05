from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Lightweight health endpoint to verify the API and database env vars are wired.
    """

    def get(self, request):
        return Response(
            {
                "service": "bark-api",
                "status": "ok",
            }
        )
