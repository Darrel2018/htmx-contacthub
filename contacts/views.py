from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from contacts.forms import ContactForm



@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {
        'contacts': contacts,
        'form': ContactForm()
    }
    return render(request, 'contacts.html', context)


@login_required
def search_contacts(request):
    import time
    time.sleep(2)
    query = request.GET.get('search', '')

    # use the query to filter contacts by name or email
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    )

    return render(request, 'partials/contact-list.html', {'contacts': contacts})

@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST, request.FILES, initial={'user': request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()

        context = {'contact': contact}
        response = render(request, 'partials/contact-row.html', context)
        response['HX-Trigger'] = 'success'
        return response
    else:
        response = render(request, 'partials/add-contact-modal.html', {'form': form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response


@login_required
@require_http_methods(["DELETE"])
def contact_delete(request, contact_id):
    contact = get_object_or_404(request.user.contacts, id=contact_id)
    contact_name = contact.name
    contact.delete()
    
    # Return success message that will replace the deleted row
    return HttpResponse(
        f'''<tr id="success-message-{contact_id}">
            <td colspan="5" class="text-center py-4">
                <div class="alert alert-success">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span><strong>{contact_name}</strong> : has been deleted successfully.</span>
                </div>
            </td>
        </tr>
        <script>
            setTimeout(function() {{
                const element = document.getElementById('success-message-{contact_id}');
                if (element) {{
                    element.style.transition = 'opacity 0.5s ease-out';
                    element.style.opacity = '0';
                    setTimeout(function() {{
                        element.remove();
                    }}, 500);
                }}
            }}, 3000);
        </script>'''
    )
