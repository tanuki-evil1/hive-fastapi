class User(AbstractUser):
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=50,
        blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=50,
        blank=True, null=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
