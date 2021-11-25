from cuser.models import AbstractCUser, CUserManager
from cuser.models import Group as CUserGroup
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_drf_filepond.models import StoredUpload
from djstripe.models import Customer, Subscription


class UserManager(CUserManager):
    """ Inherited UserManager to ensure that created superusers are active. """

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractCUser):
    """ This is our custom model for the user management. """

    objects = UserManager()
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    initial_setup_done = models.BooleanField(
        _("setup"),
        default=False,
        help_text=_(
            "Designates whether this user has been setup with additional "
            "information after their creation. This can be used for "
            "displaying a 'First Setup' page after login."
        ),
    )

    profile_picture = models.ForeignKey(
        StoredUpload,
        verbose_name="Profile picture",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT,
    )

    terms_and_conditions_accepted = models.BooleanField(
        _("Terms and Conditions accepted"),
        default=False,
        help_text=_(
            "Designates whether a user accepted the terms and conditions. "
            "Acceptance is required to use any functionality of the app."
        ),
    )

    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Referrer",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT,
    )


class Group(CUserGroup):
    """ Custom group model to replace standard group in admin dashboard """

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        proxy = True


class Workspace(models.Model):
    """ Company or Workspace that acts as customer and tenant for the user. """

    created_on = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    workspace_name = models.CharField(
        verbose_name="Workspace name", max_length=100, blank=False
    )

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The workspace's Stripe Customer object, if it exists",
    )
    subscription = models.ForeignKey(
        Subscription,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The workspace's Stripe Subscription object, if it exists",
    )

    members = models.ManyToManyField(
        User, verbose_name="Workspace Members", related_name="members"
    )
    admins = models.ManyToManyField(
        User, verbose_name="Workspace Admins", related_name="admins"
    )

    def __str__(self):
        return str(self.workspace_name)

    def add_member(self, user):
        """ Adds a member to a workspace """

        if user not in self.members.all():
            self.members.add(user.id)

    def add_admin(self, user):
        """ Adds an admin to a workspace """

        self.add_member(user)
        if user not in self.admins.all():
            self.admins.add(user.id)

    def remove_admin(self, user):
        """ Removes an admin from a workspace """

        if user in self.admins.all():
            self.admins.remove(user.id)

    def remove_member(self, user):
        """ Removes a member from a workspace """

        self.remove_admin(user)
        if user in self.members.all():
            self.members.remove(user.id)
