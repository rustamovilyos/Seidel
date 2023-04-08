from django import forms
from django.shortcuts import render
from django.utils.safestring import mark_safe


def seidel(A, b, x0, tol=1e-10, max_iter=1000):
    n = len(A)
    x = list(x0)
    for k in range(max_iter):
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - s) / A[i][i]
        if all(abs(x[i] - x0[i]) < tol for i in range(n)):
            return x
        x0 = list(x)
    raise ValueError("Seidel method did not converge")


class SeidelForm(forms.Form):
    A = forms.CharField(label='A: матрица системы уравнений', widget=forms.Textarea(attrs={'rows': 5}))
    b = forms.CharField(label='b: вектор свободных членов',
                        widget=forms.TextInput(attrs={'placeholder': 'Введите список через пробел'}))
    x0 = forms.CharField(label=mark_safe('x<sub>0</sub>: начальное приближение'),
                         widget=forms.TextInput(attrs={'placeholder': 'Введите число'}))


def solve_system(request):
    if request.method == 'POST':
        form = SeidelForm(request.POST)
        if form.is_valid():
            A = [[int(x) for x in row.split()] for row in form.cleaned_data['A'].split('\n')]
            b = [int(x) for x in form.cleaned_data['b'].split()]
            x0 = [int(x) for x in form.cleaned_data['x0'].split()]
            x = seidel(A, b, x0)
            context = {
                'form': form,
                'solution': x,
            }
            return render(request, 'index.html', context)
    else:
        form = SeidelForm()
        context = {'form': form}
        return render(request, 'index.html', context)
