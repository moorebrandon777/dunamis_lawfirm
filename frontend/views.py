import json
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Attorney, Service
from .utils import build_breadcrumbs
from .forms import ContactForm
from notification.async_email import send_email_async

def home(request):
    # Structured data for homepage (LegalService)
    structured_data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "Dunamis Law Firm",
        "url": request.build_absolute_uri(),
        "logo": request.build_absolute_uri('/static/frontend/images/logo.png'),
        "image": request.build_absolute_uri('/static/frontend/images/office.jpg'),
        "description": "Trusted legal services in family, criminal, and corporate law. Book a free consultation today.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "950 3rd Ave",
            "addressLocality": "New York",
            "addressRegion": "NY",
            "postalCode": "10022",
            "addressCountry": "USA"
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
        "logo": request.build_absolute_uri('/static/frontend/images/logo.png'),
        "image": request.build_absolute_uri('/static/frontend/images/office.jpg'),
        "description": "Dunamis Law Firm offers expert legal services in family law, criminal defense, and corporate law.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "950 3rd Ave",
            "addressLocality": "New York",
            "addressRegion": "NY",
            "postalCode": "10022",
            "addressCountry": "USA"
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


from django.urls import reverse
from .models import Attorney
from .utils import build_breadcrumbs

def attorneys_list(request):
    attorneys = Attorney.objects.all()

    breadcrumbs = build_breadcrumbs(request, [
        ("Home", reverse("frontend:home")),
        ("Our Legal Team", request.path)
    ])

    context = {
        "attorneys": attorneys,
        "breadcrumbs": breadcrumbs
    }

    return render(request, "frontend/attorneys/list.html", context)



def attorney_detail(request, slug):
    attorney = get_object_or_404(Attorney, slug=slug)

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
            "url": request.build_absolute_uri('/')
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
        'structured_data_json': json.dumps(structured_data)
    }

    return render(request, 'frontend/attorneys/detail.html', context)


def services_list(request):
    services = Service.objects.all()

    structured_data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "provider": {
            "@type": "LegalService",
            "name": "Dunamis Law Firm",
            "url": request.build_absolute_uri('/')
        },
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

    context = {
        'services': services,
        'meta': {
            'title': 'Our Legal Services | Dunamis Law Firm',
            'description': 'Explore our expert legal services ranging from family law to corporate defense.',
            'keywords': 'legal services, family law, corporate law, criminal defense'
        },
        'structured_data': structured_data,
        'breadcrumbs': breadcrumbs
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
        "provider": {
            "@type": "LegalService",
            "name": "Dunamis Law Firm",
            "url": request.build_absolute_uri('/')
        },
        "url": request.build_absolute_uri(),
        # Optional:
        # "areaServed": service.area_served,
        # "serviceType": service.service_type,
    }

    context = {
        "service": service,
        "services": related_services,
        "meta": {
            "title": service.seo_title or service.name,
            "description": service.seo_description or service.description[:160],
            "keywords": service.seo_keywords or ''
        },
        "structured_data": structured_data,
        "breadcrumbs": breadcrumbs
    }

    return render(request, "frontend/service_detail.html", context)


def contact(request):
    structured_data = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Dunamis Law Firm",
        "url": request.build_absolute_uri(),
        "description": "Contact Dunamis Law Firm for expert legal representation and consultations.",
        "publisher": {
            "@type": "LegalService",
            "name": "Dunamis Law Firm",
            "url": request.build_absolute_uri('/')
        }
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
        receiver = email
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
        'structured_data': [structured_data, breadcrumbs],
        'form':form,
        'scroll_to_contact_area': scroll_to_contact_area if 'scroll_to_contact_area' in locals() else False,
    }
    return render(request, 'frontend/contact.html', context)

