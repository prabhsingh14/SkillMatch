from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.jobs import fetch_jobs

class JobFetchView(APIView):
    def get(self, request):
        title = request.query_params.get("title", "Software Engineer")
        location = request.query_params.get("location", "Bangalore")
        company = request.query_params.get("company", "Google")
        experience = request.query_params.get("experience", "2-5 years")
        job_type = request.query_params.get("job_type", "Full-time")
        limit = int(request.query_params.get("limit", 20))

        jobs_data = fetch_jobs(
            title=title,
            location=location,
            company=company,
            experience=experience,
            job_type=job_type,
            limit=limit
        )

        if isinstance(jobs_data, dict) and "error" in jobs_data:
            return Response({"error": jobs_data["error"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(jobs_data, status=status.HTTP_200_OK)
