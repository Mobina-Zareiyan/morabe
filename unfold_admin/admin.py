# Django Built-in modules
from django.db.models import PositiveBigIntegerField, Sum, F, FileField
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.utils import timezone

# Local Apps
from .widgets import NumberInput, ImagePreviewFileInput
from account.models import User
from investments.models import Investment, InvestmentSale
from payment.models import Wallet, Transaction, WithdrawRequest
from project.models import Project
from contractor.models import Contractor, RegistrationContractor

# Third_party apps
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.components import BaseComponent, register_component


class ModelAdmin(UnfoldModelAdmin):
    formfield_overrides = {
        PositiveBigIntegerField: {'widget': NumberInput(attrs={'filter': 'number_format'})},
        FileField: {'widget': ImagePreviewFileInput()},
        #NOTE: template not found error
    }

    def get_list_display(self, request):
        list_display = list(self.list_display)
        return list(map(lambda x: x.replace('ticket_number', 'display_ticket_number'), list_display))

    def get_fieldsets(self, request, obj=None):
        """ Add tabs for each fieldset """
        fieldsets = super(ModelAdmin, self).get_fieldsets(request, obj)                    
       
        model = super(ModelAdmin, self)
        
        if fieldsets[0][0] is None: #prevents Models that don't have fieldsets to return an empty page
            return fieldsets 

        for fieldset in fieldsets:
            fieldset[1]['classes'] = fieldset[1].get('classes', ()) + ('tab',)
            
        return fieldsets
    
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
        
    #     for field in list(form.base_fields):
    #         if field.endswith('_ru'):
    #             print(field)
    #             form.base_fields.pop(field)
    #     return form
     

# Components and synthetic Data for Admin page charts, bars, etc 

# generate data automatically taking header number and row number
def generate_cohort_data(num_headers=7, num_rows=7):
    data = {
        "headers": [],
        "rows": []
    }

    # Build headers
    for h in range(1, num_headers + 1):
        data["headers"].append({
            "title": f"Header {h}",
            "subtitle": f"Subtitle {h}"
        })

    # Build rows
    for r in range(1, num_rows + 1):
        row = {
            "header": {
                "title": f"Row {r}",
                "subtitle": f"Row {r} subtitle"
            },
            "cols": []
        }
        for c in range(1, num_headers + 1):
            row["cols"].append({
                "value": f"R{r}C{c}",  # row/col identifier
                "subtitle": f"Value {r}-{c}",
                "color": f"bg-primary-400 dark:bg-primary-{(r+c)}00"
            })
        data["rows"].append(row)

    return data

DATA = generate_cohort_data(5, 7)

# Registers classes as a class component that unfold can use {%component with component_class=%} tag
@register_component
class MyCohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "data": DATA
        })
        return context


TDATA = [
    {
        "color": "bg-primary-400 dark:bg-primary-500",
        "tooltip": "Custom value 1",
    },
    {
        "color": "bg-primary-400 dark:bg-primary-600",
        "tooltip": "Custom value 2",
    },
        {
        "color": "bg-primary-600 dark:bg-primary-700",
        "tooltip": "Custom value 2",
    },
    {
        "color": "bg-primary-200 dark:bg-primary-800",
        "tooltip": "Custom value 2",
    },
        {
        "color": "bg-primary-200 dark:bg-primary-900",
        "tooltip": "Custom value 2",
    },
        {
        "color": "bg-primary-200 dark:bg-primary-1000",
        "tooltip": "Custom value 2",
    },
]

@register_component
class MyTrackerComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "data": TDATA
        })
        return context

#
# import json
# def dashboard_callback(request, context):
#     context = context or {}
#
#     # ─────────────────────────────
#     # USERS & KYC
#     # ─────────────────────────────
#     context["total_users"] = User.objects.count()
#     context["verified_users"] = User.objects.filter(is_authenticate=True).count()
#
#     # ─────────────────────────────
#     # PROJECTS
#     # ─────────────────────────────
#     projects = Project.objects.all()
#     context["total_projects"] = projects.count()
#     context["featured_projects"] = projects.filter(is_featured=True).count()
#     context["total_project_budget"] = projects.aggregate(total=Sum("total_budget"))["total"] or 0
#     context["total_project_funding"] = projects.aggregate(total=Sum("current_funding"))["total"] or 0
#     context["funded_projects"] = projects.filter(current_funding__gte=F("total_budget")).count()
#
#     # ─────────────────────────────
#     # INVESTMENTS
#     # ─────────────────────────────
#     context["total_investments"] = Investment.objects.count()
#     context["paid_investments"] = Investment.objects.filter(status="paid").count()
#     context["total_invested_area"] = Investment.objects.filter(status="paid").aggregate(total=Sum("area"))["total"] or 0
#     context["pending_sale_listings"] = InvestmentSale.objects.filter(status="selling").count()
#
#     # ─────────────────────────────
#     # WALLET
#     # ─────────────────────────────
#     context["total_wallet_balance"] = Wallet.objects.aggregate(total=Sum("balance"))["total"] or 0
#     context["transactions_today"] = Transaction.objects.filter(created__date=timezone.now().date()).count()
#     context["failed_transactions"] = Transaction.objects.filter(status="FAILED").count()
#     context["pending_withdraws"] = WithdrawRequest.objects.filter(status="PENDING").count()
#
#     # ─────────────────────────────
#     # CONTRACTORS
#     # ─────────────────────────────
#     context["total_contractors"] = Contractor.objects.count()
#     context["pending_contractors"] = RegistrationContractor.objects.filter(is_checked=False).count()
#
#     # ─────────────────────────────
#     # TABLE
#     # ─────────────────────────────
#     recent_investments = Investment.objects.select_related("user", "project").order_by("-created")[:10]
#     context["table_data"] = {
#         "headers": [_("کاربر"), _("پروژه"), _("متراژ"), _("مبلغ"), _("وضعیت")],
#         "rows": [
#             [
#                 inv.user.fullname if inv.user else "-",
#                 inv.project.title if inv.project else "-",
#                 inv.area,
#                 inv.base_amount,
#                 inv.status,
#             ]
#             for inv in recent_investments
#         ],
#     }
#
#     # ─────────────────────────────
#     # NAVIGATION (این بخش حیاتی است)
#     # ─────────────────────────────
#     context["navigation_items"] = []
#
#     for app in admin.site.get_app_list(request):
#         context["navigation_items"].append({
#             "title": app["name"],
#             "icon": "apps",
#             "children": [
#                 {
#                     "title": model["name"],
#                     "link": model["admin_url"],
#                 }
#                 for model in app["models"]
#             ]
#         })
#
#     return context
