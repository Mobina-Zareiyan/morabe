# Django Built-in modules
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UnfoldAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'unfold_admin'
    verbose_name = _("ادمین آنفولد")
    
    # def ready(self):
    #     """Override admin index view when app is ready."""
    #     from django.contrib import admin
    #     from django.contrib.auth import get_user_model
    #     from kyc.models import KYCLevel2Request, VerificationStatus
    #     from transactions.models import Transaction
    #
    #     try:
    #         from helpdesk.models import Ticket
    #     except ImportError:
    #         Ticket = None
    #
    #     User = get_user_model()
    #
    #     # Store original index method
    #     original_index = admin.site.index
    #
    #     def custom_index(request, extra_context=None):
    #         """
    #         Custom admin index view that provides dashboard data.
    #         """
    #         extra_context = extra_context or {}
    #
    #         try:
    #             # Initialize statistics with default values
    #             pending_kyc_count = 0
    #             pending_transactions_count = 0
    #             open_tickets_count = 0
    #             total_users_count = 0
    #             recent_kyc_requests = []
    #             recent_transactions = []
    #
    #             # Get KYC statistics only if user has permission
    #             if request.user.has_perm('kyc.view_kyclevel2request') or request.user.has_perm('kyc.view_kyclevel3request'):
    #                 if request.user.has_perm('kyc.view_kyclevel2request'):
    #                     pending_kyc_count = KYCLevel2Request.objects.filter(
    #                         status=VerificationStatus.PENDING
    #                     ).count()
    #
    #             # Get transactions statistics only if user has permission
    #             if (request.user.has_perm('transactions.view_transaction') or
    #                 request.user.has_perm('transactions.view_cryptodeposit') or
    #                 request.user.has_perm('transactions.view_fiatdeposit')):
    #                 if request.user.has_perm('transactions.view_transaction'):
    #                     pending_transactions_count = Transaction.objects.filter(
    #                         status__in=['pending', 'awaiting_admin']
    #                     ).count()
    #
    #             # Get tickets count only for superusers
    #             if request.user.is_superuser and Ticket:
    #                 open_tickets_count = Ticket.objects.filter(
    #                     status__in=[1, 2]  # Open, Reopened
    #                 ).count()
    #
    #             # Get users count only if user has permission
    #             if request.user.has_perm('account.view_user') or request.user.is_superuser:
    #                 total_users_count = User.objects.count()
    #
    #             # Get recent KYC requests only if user has permission
    #             if request.user.has_perm('kyc.view_kyclevel2request'):
    #                 kyc_requests = KYCLevel2Request.objects.select_related('user').order_by('-created')[:10]
    #                 for req in kyc_requests:
    #                     recent_kyc_requests.append({
    #                         'id': req.id,
    #                         'user': req.user.username if req.user else '-',
    #                         'full_name': req.full_name or '-',
    #                         'status': req.status,
    #                         'created': req.created.strftime('%Y/%m/%d %H:%M') if req.created else '-',
    #                     })
    #
    #             # Get recent transactions only if user has permission
    #             if request.user.has_perm('transactions.view_transaction'):
    #                 transactions = Transaction.objects.select_related('user', 'asset').order_by('-created')[:10]
    #
    #                 # Map transaction types to Persian
    #                 tx_type_map = {
    #                     'deposit_crypto': 'واریز رمزارز',
    #                     'withdraw_crypto': 'برداشت رمزارز',
    #                     'deposit_fiat': 'واریز فیات',
    #                     'withdraw_fiat': 'برداشت فیات',
    #                     'deposit_voucher': 'واریز ووچر',
    #                     'withdraw_voucher': 'برداشت ووچر',
    #                     'deposit_broker': 'واریز بروکر',
    #                     'withdraw_broker': 'برداشت بروکر',
    #                     'internal_transfer': 'انتقال داخلی',
    #                     'trade': 'معامله',
    #                 }
    #
    #                 for tx in transactions:
    #                     recent_transactions.append({
    #                         'id': str(tx.id),
    #                         'user': tx.user.username if tx.user else '-',
    #                         'tx_type': tx_type_map.get(tx.tx_type, tx.tx_type),
    #                         'amount': f"{tx.amount} {tx.asset.symbol}" if tx.asset else str(tx.amount),
    #                         'status': tx.status,
    #                         'created': tx.created.strftime('%Y/%m/%d %H:%M') if tx.created else '-',
    #                     })
    #
    #             # Add dashboard data to context
    #             extra_context.update({
    #                 'pending_kyc_count': pending_kyc_count,
    #                 'pending_transactions_count': pending_transactions_count,
    #                 'open_tickets_count': open_tickets_count,
    #                 'total_users_count': total_users_count,
    #                 'recent_kyc_requests': recent_kyc_requests,
    #                 'recent_transactions': recent_transactions,
    #             })
    #
    #         except Exception as e:
    #             # In case of any error, provide empty data
    #             extra_context.update({
    #                 'pending_kyc_count': 0,
    #                 'pending_transactions_count': 0,
    #                 'open_tickets_count': 0,
    #                 'total_users_count': 0,
    #                 'recent_kyc_requests': [],
    #                 'recent_transactions': [],
    #             })
    #
    #         return original_index(request, extra_context)
    #
    #     # Override the admin index method
    #     admin.site.index = custom_index
