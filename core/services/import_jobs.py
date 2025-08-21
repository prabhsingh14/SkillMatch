from company.models import Job, Company
from core.services.jobs import fetch_jobs

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger(__name__)

def import_external_jobs_from_indianapi(limit=20, title=None, location=None):
    try:
        data = fetch_jobs(title=title, location=location, limit=limit)
        if isinstance(data, dict) and 'error' in data:
            logger.error(f"Error fetching jobs from IndiaAPI: {data['error']}")
            return {"error": data['error']}
        
        if not isinstance(data, list):
            logger.error("Unexpected data format received from IndiaAPI")
            return {"error": "Invalid data format"}

        jobs_data = data
        imported_jobs = 0

        external_company, created = Company.objects.get_or_create(
            name="IndianAPI External",
            user=None,  # Assuming no user is associated with this external company
            website="https://jobs.indianapi.in",
        )

        for job in jobs_data:
            try:
                job_title = job.get('title')
                company_name = job.get('company', 'Unknown')
                location_str = job.get('location', 'India')

                #parse posted date from API or use current time as fallback
                posted_at = job.get('posted_at')
                if posted_at:
                    try:
                        posted_date = parse_datetime(posted_at)
                        if not posted_date:
                            posted_date = timezone.now()
                    except(ValueError, TypeError):
                        logger.warning(f"Invalid posted date format for job {job_title}. Using current time.")
                        posted_date = timezone.now()
                else:
                    posted_date = timezone.now()

                job_type_mapping = {
                    'full_time': 'Full Time',
                    'part_time': 'Part Time',
                    'contract': 'Contract',
                    'internship': 'Internship',
                }

                employment_type = job_type_mapping.get(
                    job.get('employment_type', ""),
                    "full_time"
                )

                '''
                For IndianAPI, salary is not provided so will be null as set in company/models.py.
                For internal jobs, it will be set based on the job data.
                '''
                salary_value = None
                if "salary" in job and job['salary']:
                    try:
                        salary_value = Decimal(job['salary'])
                    except (ValueError, TypeError, InvalidOperation):
                        logger.warning(f"Invalid salary format for job {job_title}. Setting salary to None.")
                        salary_value = None
                if not job_title:
                    logger.warning("Job title is missing, skipping this job.")
                    continue
                
                #job record
                job_obj, created = Job.objects.get_or_create(
                    title=job_title,
                    company=external_company,
                    source="indianapi",
                    source_url=job.get("apply_link"),
                    defaults={
                        "description": job.get("description", ''),
                        "location": location_str,
                        "employment_type": employment_type,
                        "posted_at": posted_at,
                        "salary": salary_value,
                        "is_active": True,
                    }
                )

                if created:
                    imported_jobs += 1
                    logger.info(f"Created new job: {job_title} at {company_name}")
                else:
                    logger.info(f"Updated existing job: {job_title} at {company_name}")

            except Exception as e:
                logger.error(f"Error processing job {job_title}: {e}")
                continue

        return {"imported": imported_jobs, "total_processed": len(jobs_data)}

    except Exception as e:
        logger.error(f"Error in import_external_jobs_from_indianapi: {str(e)}")
        return {"error": f"Import failed: {str(e)}"}