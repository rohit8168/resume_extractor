from django.db import models

class Resume(models.Model):
    file_name = models.CharField(max_length=512)
    job_role = models.CharField(max_length=200, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    languages = models.CharField(max_length=512, blank=True, null=True)  
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    extracted_text = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.job_role or 'Unknown'})"
