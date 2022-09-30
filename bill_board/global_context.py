from allauth.account.admin import EmailAddress


def global_context(request):
    """Добавляем в "глобальный" контекст:
     - is_verified_email"""
    is_verified_email = False
    user = EmailAddress.objects.filter(user_id=request.user.id)
    if user.exists():
        is_verified_email = EmailAddress.objects.get(user_id=request.user.id).verified

    context = {
        'is_email_verified': is_verified_email,
    }
    return context
