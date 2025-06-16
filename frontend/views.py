import json
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

from .models import Attorney, Service
from .utils import build_breadcrumbs
from .forms import ContactForm
from notification.async_email import send_email_async


def get_legal_service_schema(request):
    return {
        "@type": "LegalService",
        "name": "Dunamis Law Firm",
        "url": request.build_absolute_uri('/'),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "950 3rd Ave",
            "addressLocality": "New York",
            "addressRegion": "NY",
            "postalCode": "10022",
            "addressCountry": "US"
        }
    }

def home(request):
    # Structured data for homepage (LegalService)
    structured_data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "Dunamis Law Firm",
        "url": request.build_absolute_uri(),
        "logo": request.build_absolute_uri('/static/frontend/images/logo.svg'),
        "image": request.build_absolute_uri('/static/frontend/images/office.jpg'),
        "description": "Trusted legal services in family, criminal, and corporate law. Book a free consultation today.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "950 3rd Ave",
            "addressLocality": "New York",
            "addressRegion": "NY",
            "postalCode": "10022",
            "addressCountry": "US"
        },
        "telephone": "+1-516-286-3799",
        "email": "contact@dunamislawfirm.com",
        "sameAs": [
            "https://www.facebook.com/dunamislaw",
            "https://twitter.com/dunamislaw",
            "https://www.linkedin.com/company/dunamislaw"
        ]
    }

    # Breadcrumb structured data
    breadcrumbs = build_breadcrumbs(request, [
        ("Home", "/"),
    ])

    context = {
        'meta': {
            'title': 'Experienced Law Firm in New York | Dunamis Law Firm',
            'description': 'Trusted legal services in family, criminal, and corporate law. Book a free consultation today.',
            'keywords': 'law firm, family lawyer, criminal defense, corporate law, New York'
        },
        'structured_data': json.dumps([structured_data, breadcrumbs])
    }

    return render(request, 'frontend/index.html', context)


def about(request):
    structured_data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "Dunamis Law Firm",
        "url": request.build_absolute_uri(),
        "logo": request.build_absolute_uri('/static/frontend/images/logo.svg'),
        "image": request.build_absolute_uri('/static/frontend/images/office.jpg'),
        "description": "Dunamis Law Firm offers expert legal services in family law, criminal defense, and corporate law.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "950 3rd Ave",
            "addressLocality": "New York",
            "addressRegion": "NY",
            "postalCode": "10022",
            "addressCountry": "US"
        },
        "telephone": "+1-516-286-3799",
        "email": "contact@dunamislawfirm.com",
        "sameAs": [
            "https://www.facebook.com/dunamislaw",
            "https://twitter.com/dunamislaw",
            "https://www.linkedin.com/company/dunamislaw"
        ],
        "founder": {
            "@type": "Person",
            "name": "Rurl Amos, Esq."
        }
    }

    breadcrumbs = build_breadcrumbs(request, [
        ("Home", "/"),
        ("About Us", request.path),
    ])

    context = {
        'meta': {
            'title': 'About Dunamis Law Firm | Trusted Law Firm in New York',
            'description': 'Learn more about our mission, values, and the experienced legal team behind Dunamis Law Firm.',
            'keywords': 'about Dunamis Law Firm, law firm New York, legal team, Rurl Amos'
        },
        'structured_data': json.dumps([structured_data, breadcrumbs])
    }
    return render(request, 'frontend/about.html', context)


def robots_txt(request):
    return render(request, 'frontend/robots.txt', content_type='text/plain')


def attorneys_list(request):
    attorneys = Attorney.objects.all()

    breadcrumbs = build_breadcrumbs(request, [
        ("Home", reverse("frontend:home")),
        ("Our Legal Team", request.path)
    ])

    breadcrumbs_json = json.dumps(breadcrumbs)

    context = {
        "attorneys": attorneys,
        "breadcrumbs_data_json": breadcrumbs_json
    }

    return render(request, "frontend/attorneys/list.html", context)



def attorney_detail(request, slug):
    attorney = get_object_or_404(Attorney, slug=slug)

    form = ContactForm()

    person_data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": attorney.name,
        "image": request.build_absolute_uri(attorney.photo.url) if attorney.photo else "",
        "jobTitle": attorney.title,
        "url": request.build_absolute_uri(),
        "email": attorney.email,
        "telephone": attorney.phone,
        "sameAs": [attorney.linkedin_url] if attorney.linkedin_url else [],
        "worksFor": {
            "@type": "LegalService",
            "name": "Dunamis Law Firm",
            "url": request.build_absolute_uri('/'),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "950 3rd Ave",
                "addressLocality": "New York",
                "addressRegion": "NY",
                "postalCode": "10022",
                "addressCountry": "US"
            }
        }
    }

    breadcrumb_items = [
        ("Home", "/"),
        ("Attorneys", "/attorneys/"),
        (attorney.name, request.path),
    ]
    breadcrumb_data = build_breadcrumbs(request, breadcrumb_items)

    structured_data = {
        "@context": "https://schema.org",
        "@graph": [
            person_data,
            breadcrumb_data
        ]
    }

    context = {
        'attorney': attorney,
        'meta': {
            'title': attorney.meta_title or attorney.name,
            'description': attorney.meta_description or (attorney.bio[:160] if attorney.bio else ''),
        },
        'structured_data_json': json.dumps(structured_data),
        'form':form,
    }

    return render(request, 'frontend/attorneys/detail.html', context)


def services_list(request):
    services = Service.objects.all()

    structured_data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "provider": get_legal_service_schema(request),
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Legal Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": service.name,
                        "description": service.description[:160]  # Truncate for brevity
                    }
                } for service in services
            ]
        }
    }

    breadcrumbs = build_breadcrumbs(request, [
        ("Home", reverse("frontend:home")),
        ("Services", reverse("frontend:services_list"))
    ])

    breadcrumbs_json = json.dumps(breadcrumbs)
    context = {
        'services': services,
        'meta': {
            'title': 'Our Legal Services | Dunamis Law Firm',
            'description': 'Explore our expert legal services ranging from family law to corporate defense.',
            'keywords': 'legal services, family law, corporate law, criminal defense'
        },
        'structured_data': json.dumps(structured_data),
        'breadcrumbs_data_json': breadcrumbs_json
    }

    return render(request, 'frontend/services_list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.exclude(id=service.id)  # Optional: show others

    # Breadcrumbs for structured data
    breadcrumbs = build_breadcrumbs(request, [
        ("Home", reverse("frontend:home")),
        ("Services", reverse("frontend:services_list")),
        (service.name, request.path)
    ])

    # Structured data for individual service
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service.name,
        "description": service.description[:160],
        "provider": get_legal_service_schema(request),
        "url": request.build_absolute_uri(),
    }

    context = {
        "service": service,
        "services": related_services,
        "meta": {
            "title": service.seo_title or service.name,
            "description": service.seo_description or service.description[:160],
            "keywords": service.seo_keywords or ''
        },
        "structured_data": json.dumps(structured_data),
        "breadcrumbs": json.dumps(breadcrumbs)
    }

    return render(request, "frontend/service_detail.html", context)


def contact(request):
    structured_data = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Dunamis Law Firm",
        "url": request.build_absolute_uri(),
        "description": "Contact Dunamis Law Firm for expert legal representation and consultations.",
        "publisher": get_legal_service_schema(request)
    }

    breadcrumbs = build_breadcrumbs(request, [
        ("Home", "/"),
        ("Contact", request.path),
    ])

    form = ContactForm(request.POST or None)
    
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']
        message = form.cleaned_data['message']

        # send email
        subject = f"Email From {name}"
        template = "notification/customer_care_email.html"
        context = {
            "name": name,
            'email':email,
            'phone': phone,
            'address': address,
            'message': message
        }
        receiver = "contact@dunamislawfirm.com"
        send_email_async(subject, template, context, receiver)

        messages.success(request, 'Form is submitted successfuly, we will get back to you as soon as possible.')
        url = reverse('frontend:contact')
        return redirect(f"{url}#contact-area-me")
    else:
        # On POST with invalid form, enable scroll flag
        scroll_to_contact_area = request.method == 'POST'

    context = {
        'meta': {
            'title': 'Contact Dunamis Law Firm | Schedule a Consultation',
            'description': 'Get in touch with Dunamis Law Firm. Call, email, or visit our NYC office to schedule a consultation with an experienced attorney.',
            'keywords': 'contact Dunamis Law Firm, schedule consultation, NYC law firm, Rurl Amos'
        },
        'structured_data': json.dumps([structured_data, breadcrumbs]),
        'form':form,
        'scroll_to_contact_area': scroll_to_contact_area if 'scroll_to_contact_area' in locals() else False,
    }
    return render(request, 'frontend/contact.html', context)


@require_POST
def contact_attorney(request):
    form = ContactForm(request.POST)
    redirect_url = request.POST.get('next', '/')
    slug = request.POST.get('attorney_slug')
    attorney = get_object_or_404(Attorney, slug=slug)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']
        message = form.cleaned_data['message']

        # Email sending logic
        subject = f"Email From {name}"
        template = "notification/customer_care_email.html"
        context = {
            "name": name,
            'email': email,
            'phone': phone,
            'address': address,
            'message': message
        }
        receiver = "contact@dunamislawfirm.com"
        send_email_async(subject, template, context, receiver)


        messages.success(request, 'Message sent successfully. We will be in touch shortly.')
        return HttpResponseRedirect(redirect_url)

    else:
        messages.error(request, 'There was an error with your submission. Please correct the error below and try again.')
        context = {
            'attorney': attorney,
            'form': form,
            'scroll_to_contact_area': True,
        }
        return render(request, 'frontend/attorneys/detail.html', context)
    
# @require_POST
# def contact_attorney(request):
#     form = ContactForm(request.POST)

#     # Get return URL to redirect after success/failure
#     redirect_url = request.POST.get('next', '/')

#     if form.is_valid():
#         name = form.cleaned_data['name']
#         email = form.cleaned_data['email']
#         phone = form.cleaned_data['phone']
#         address = form.cleaned_data['address']
#         message = form.cleaned_data['message']

#         # Email sending logic
#         subject = f"Email From {name}"
#         template = "notification/customer_care_email.html"
#         context = {
#             "name": name,
#             'email': email,
#             'phone': phone,
#             'address': address,
#             'message': message
#         }
#         receiver = email
#         send_email_async(subject, template, context, receiver)

#         messages.success(request, 'Message sent successfully. We will be in touch shortly.')

#     else:
#         messages.error(request, 'There was an error with your submission. Please check and try again.')

#     return HttpResponseRedirect(redirect_url)
