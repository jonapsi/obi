from django.contrib.auth import hashers

from .models import Account


class CredentialBackend:
    """Autentica contra account_credentials en lugar de accounts.password."""

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            account = Account.objects.select_related("credentials").get(
                email__iexact=email, deleted_at__isnull=True
            )
        except Account.DoesNotExist:
            # Mismo costo de tiempo que un login real, para no revelar
            # qué correos existen.
            hashers.make_password(password)
            return None

        credential = getattr(account, "credentials", None)
        if credential is None or not credential.check_password(password):
            return None
        return account if account.is_active else None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id, deleted_at__isnull=True)
        except Account.DoesNotExist:
            return None
