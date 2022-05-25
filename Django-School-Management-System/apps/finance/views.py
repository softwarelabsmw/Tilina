from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import InvoiceItemFormset, InvoiceReceiptFormSet, Invoices
from .models import Invoice, InvoiceItem, Receipt

from apps.students.models import Student
from django.db.models import Sum


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = "__all__"
    success_url = "/finance/list"

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = InvoiceItemFormset(
                self.request.POST, prefix="invoiceitem_set"
            )
        else:
            context["items"] = InvoiceItemFormset(prefix="invoiceitem_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context["receipts"] = Receipt.objects.filter(invoice=self.object)
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
        return context


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ["student", "session", "term", "class_for", "balance_from_previous_term"]

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            context["items"] = InvoiceItemFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)
            context["items"] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["receipts"]
        itemsformset = context["items"]
        if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
            form.save()
            formset.save()
            itemsformset.save()
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice-list")


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("invoice-list")

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class ReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")


class ReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy("invoice-list")


@login_required
def bulk_invoice(request):
    return render(request, "finance/bulk_invoice.html")

@login_required
def fees_report_view(request):
    report = Invoice.objects.all()
    invoices = Invoice.objects.all().count()
    total_students = Student.objects.all().count()
    total_payable = InvoiceItem.objects.all().aggregate(total=Sum("amount"))['total']
    total_paid = Receipt.objects.all().aggregate(total=Sum("amount_paid"))['total']
    total_balance = total_payable - total_paid
    return render(request, "finance/fees_report.html",
                  {"reports": report,
                   "total_students": total_students,
                   "total_payable": total_payable,
                   "total_paid": total_paid,
                   "total_balance": total_balance,
                   "invoices": invoices}
                  )


