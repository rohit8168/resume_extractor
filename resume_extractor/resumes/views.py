from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFilesForm
from .models import Resume
from .utils.extractors import extract_all_text, extract_structured
from .utils.remove_bad_words import censor_text
from django.views.decorators.http import require_http_methods
from django.db.models import Q

@require_http_methods(["GET","POST"])
def upload_view(request):#file upload api
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        # print(form)
        print("dfghjk")
        if form.is_valid:
            files = request.FILES.getlist('files')
            saved = []
            for f in files:
                raw_text = extract_all_text(f) #extractcing the text data
                censored_text = censor_text(raw_text) # replacing the bad words with ***
                struct = extract_structured(censored_text) 
                email = struct.get('email')
                phone = struct.get('phone')
                print(phone,"dfghjk")
                if phone and not (7 <= len(phone) <= 15):
                    phone = None
                r = Resume.objects.create(
                    file_name = f.name,
                    job_role = struct.get('job_role'),
                    qualification = struct.get('qualification'),
                    languages = struct.get('languages'),
                    phone = phone,
                    email = email,
                    address = struct.get('address'),
                    age = struct.get('dob_or_age'),
                    extracted_text = censored_text
                )
                # print(r,"gfdhjsksdj")
                saved.append(r.id)
            return render(request, 'result.html', {'saved_ids': saved})
        else:
            print(form.errors)
    else:
        form = UploadFilesForm()
    return render(request, 'upload.html', {'form': form})
#search api
def search_api(request):
    q = Resume.objects.all()
    job = request.GET.get('job_role')
    lang = request.GET.get('language')
    qual = request.GET.get('qualification')
    loc = request.GET.get('location')
    if job:
        q = q.filter(job_role__icontains=job)
    if lang:
        q = q.filter(languages__icontains=lang)
    if qual:
        q = q.filter(qualification__icontains=qual)
    if loc:
        q = q.filter(address__icontains=loc)
    results = []
    for r in q.order_by('-upload_date')[:200]:
        results.append({
            'id': r.id,
            'file_name': r.file_name,
            'job_role': r.job_role,
            'qualification': r.qualification,
            'languages': r.languages,
            'phone': r.phone,
            'email': r.email,
            'address': r.address,
            'age': r.age,
            'upload_date': r.upload_date.isoformat(),
        })
    return JsonResponse({'count': q.count(), 'results': results})
