from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client
from .forms import ClientForm

def client_list(request):
    """Display list of all clients"""
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'clients/client_list.html', context)

def client_detail(request, pk):
    """Display details of a single client"""
    client = get_object_or_404(Client, pk=pk)
    context = {'client': client}
    return render(request, 'clients/client_detail.html', context)

def client_create(request):
    """Create a new client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.full_name} created successfully!')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'clients/client_form.html', context)

def client_update(request, pk):
    """Update an existing client"""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.full_name} updated successfully!')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    context = {'form': form, 'action': 'Update', 'client': client}
    return render(request, 'clients/client_form.html', context)

def client_delete(request, pk):
    """Delete a client"""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client_name = client.full_name
        client.delete()
        messages.success(request, f'Client {client_name} deleted successfully!')
        return redirect('client_list')

    context = {'client': client}
    return render(request, 'clients/client_confirm_delete.html', context)
