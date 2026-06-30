import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    Таблица ролей (Глобальный админ, Владелец поставщика, Продавец и т.д.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name="Системное имя (код)")
    description = models.TextField(blank=True, null=True, verbose_name="Описание роли")

    class Meta:
        db_table = 'roles'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Company(models.Model):
    """
    Таблица компаний (Поставщики и Магазины)
    """
    class CompanyType(models.TextChoices):
        SUPPLIER = 'supplier', 'Поставщик'
        SHOP = 'shop', 'Магазин'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название компании")
    company_type = models.CharField(
        max_length=20, 
        choices=CompanyType.choices, 
        verbose_name="Тип бизнеса"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = 'companies'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f"{self.name} ({self.get_company_type_display()})"


class User(AbstractUser):
    """
    Единая таблица пользователей для всех сущностей (Внутренние, Поставщики, Магазины).
    Наследуется от AbstractUser для сохранения механизмов авторизации Django.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Телефон")
    
    # Связь "Многие-ко-Многим" через промежуточную таблицу CompanyUser
    companies = models.ManyToManyField(
        Company, 
        through='CompanyUser', 
        related_name='users',
        verbose_name="Компании"
    )

    # Поля для внутренних пользователей (Глобальный админ, Менеджер, Редактор)
    # Для них привязка к компании будет отсутствовать, а роль задается здесь напрямую
    internal_role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='internal_users',
        verbose_name="Внутренняя роль платформы"
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"


class CompanyUser(models.Model):
    """
    Промежуточная таблица связывающая Пользователя, Компанию и его Роль в этой компании.
    Реализует Multi-tenancy (один пользователь может состоять в разных компаниях с разными ролями).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_memberships')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_memberships')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='company_users')
    
    is_active = models.BooleanField(default=True, verbose_name="Активен в компании")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company_users'
        # Уникальный индекс: пользователь может иметь только одну роль в рамках конкретной компании
        unique_together = ('user', 'company')
        verbose_name = 'Сотрудник компании'
        verbose_name_plural = 'Сотрудники компаний'

    def __str__(self):
        return f"{self.user.username} -> {self.company.name} ({self.role.name})"