# from rest_framework.permissions import BasePermission
#
#
#
# class AllowAnyWithAPIKey(BasePermission):
#     def has_permission(self, request, view):
#         api_key = request.headers.get("X-API-KEY")
#         return api_key in VALID_KEYS
#
#
#
# class IsAuthenticatedWithAPIKey(BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         api_key = request.headers.get("X-API-KEY")
#         return api_key in VALID_KEYS
#
