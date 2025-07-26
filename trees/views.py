# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseForbidden, JsonResponse
# from .models import PlantedTree
# from .forms import PlantedTreeForm

# @login_required
# def user_trees(request):
#     trees = PlantedTree.objects.filter(user=request.user)
#     return render(request, 'trees/user_trees.html', {'trees': trees})

# @login_required
# def tree_detail(request, pk):
#     tree = get_object_or_404(PlantedTree, pk=pk)

#     if tree.user != request.user:
#         return HttpResponseForbidden("You do not have permission to access this tree.")

#     return render(request, 'trees/tree_detail.html', {'tree': tree})

# @login_required
# def add_planted_tree(request):
#     if request.method == 'POST':
#         form = PlantedTreeForm(request.POST, user=request.user)
#         if form.is_valid():
#             planted_tree = form.save(commit=False)
#             planted_tree.user = request.user
#             planted_tree.save()
#             return redirect('user_trees')
#     else:
#         form = PlantedTreeForm(user=request.user)
#     return render(request, 'trees/add_tree.html', {'form': form})

# @login_required
# def account_trees(request):
#     user_accounts = request.user.accounts.all()
#     trees = PlantedTree.objects.filter(account__in=user_accounts).select_related('tree', 'user', 'account')
#     return render(request, 'trees/account_trees.html', {'trees': trees})

# @login_required
# def my_trees_api(request):
#     trees = PlantedTree.objects.filter(user=request.user).select_related('tree', 'account')

#     data = [
#         {
#             'id': t.id,
#             'tree_name': t.tree.name,
#             'account': t.account.name,
#             'lat': float(t.location_lat),
#             'lon': float(t.location_lon),
#             'planted_at': t.planted_at.strftime('%Y-%m-%d %H:%M'),
#         }
#         for t in trees
#     ]

#     return JsonResponse(data, safe=False)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from .models import PlantedTree
from .forms import PlantedTreeForm

# ✅ Lista de árvores do usuário logado
class UserTreeListView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'trees/user_trees.html'
    context_object_name = 'trees'

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)


# ✅ Detalhes de uma árvore (somente se for do usuário)
class TreeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PlantedTree
    template_name = 'trees/tree_detail.html'
    context_object_name = 'tree'

    def test_func(self):
        tree = self.get_object()
        return tree.user == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this tree.")


# ✅ Formulário para plantar nova árvore
class AddPlantedTreeView(LoginRequiredMixin, CreateView):
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = 'trees/add_tree.html'
    success_url = reverse_lazy('user_trees')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # passa o user para limitar contas
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ✅ Árvores das contas do usuário
class AccountTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'trees/account_trees.html'
    context_object_name = 'trees'

    def get_queryset(self):
        user_accounts = self.request.user.accounts.all()
        return PlantedTree.objects.filter(account__in=user_accounts).select_related('tree', 'user', 'account')


# ✅ API simples com árvores do usuário logado (mantida como FBV, mais direto)
from django.contrib.auth.decorators import login_required

@login_required
def my_trees_api(request):
    trees = PlantedTree.objects.filter(user=request.user).select_related('tree', 'account')

    data = [
        {
            'id': t.id,
            'tree_name': t.tree.name,
            'account': t.account.name,
            'lat': float(t.location_lat),
            'lon': float(t.location_lon),
            'planted_at': t.planted_at.strftime('%Y-%m-%d %H:%M'),
        }
        for t in trees
    ]

    return JsonResponse(data, safe=False)

