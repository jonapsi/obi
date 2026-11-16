from django.contrib.auth import hashers
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone

from core.models import TimeStampedModel, UUIDModel


class AccountStatus(models.TextChoices):
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class AccountManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email__iexact=email, deleted_at__isnull=True)


class Account(UUIDModel, TimeStampedModel, AbstractBaseUser):
    # El hash vive en AccountCredential; se elimina el campo heredado.
    password = None
    last_login = models.DateTimeField(null=True, blank=True, db_column="last_login_at")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # E.164
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    professional_license = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING_VERIFICATION,
    )
    privacy_notice_version = models.CharField(max_length=20, null=True, blank=True)
    privacy_notice_accepted_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = AccountManager()

    class Meta:
        db_table = "accounts"
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                condition=Q(deleted_at__isnull=True),
                name="accounts_email_uniq",
            ),
            models.UniqueConstraint(
                fields=["phone_number"],
                condition=Q(phone_number__isnull=False, deleted_at__isnull=True),
                name="accounts_phone_uniq",
            ),
            models.CheckConstraint(
                condition=Q(status__in=AccountStatus.values),
                name="accounts_status_valid",
            ),
        ]

    @property
    def is_active(self):
        return self.status == AccountStatus.ACTIVE and self.deleted_at is None


class AccountCredential(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="credentials",
    )
    password_hash = models.CharField(max_length=255)  # Argon2id
    password_changed_at = models.DateTimeField(default=timezone.now)
    mfa_totp_secret_encrypted = models.BinaryField(null=True, blank=True)  # cifrado con KMS
    mfa_enabled_at = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "account_credentials"

    def __str__(self):
        # Nunca mostrar el hash ni el secreto MFA.
        return f"Credenciales de {self.account_id}"

    def set_password(self, raw_password):
        self.password_hash = hashers.make_password(raw_password)
        self.password_changed_at = timezone.now()

    def check_password(self, raw_password):
        return hashers.check_password(raw_password, self.password_hash)
