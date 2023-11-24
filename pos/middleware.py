from django.shortcuts import redirect
from .models import LockScreen
#
# class LockScreenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#
#         # Check if the user is authenticated and the lock screen is active
#         if request.user.is_authenticated:
#             lock_screen = LockScreen.objects.get_or_create(user=request.user)[0]
#             if lock_screen.is_locked and request.path_info != '/lock-screen/':
#                 return redirect('lock_screen')
#
#         return response