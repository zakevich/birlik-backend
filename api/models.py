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


class Supplier(models.Model):
    """
    Таблица Поставщиков. Поставщик всегда один в системе.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название компании поставщика")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контактное лицо")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    # Специфичные поля для поставщика (пример)
    min_order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Минимальная сумма заказа"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'suppliers'
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class ShopProfile(models.Model):
    """
    Профиль/Аккаунт Магазинов (Юридическое лицо или кабинет владельца сети).
    У одного профиля может быть множество физических торговых точек (Shops).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название сети / Юрлица")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контактное лицо")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_profiles'
        verbose_name = 'Профиль магазинов (Сеть)'
        verbose_name_plural = 'Профили магазинов (Сети)'

    def __str__(self):
        return self.name


class Shop(models.Model):
    """
    Конкретная физическая торговая точка (магазин), куда доставляется товар.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        ShopProfile, 
        on_delete=models.CASCADE, 
        related_name='shops', 
        verbose_name="Родительский профиль/сеть"
    )
    name = models.CharField(max_length=255, verbose_name="Название конкретной точки")
    address = models.CharField(max_length=500, verbose_name="Фактический адрес")
    is_active = models.BooleanField(default=True, verbose_name="Точка работает")

    class Meta:
        db_table = 'shops'
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'

    def __str__(self):
        return f"{self.profile.name} - {self.name}"


class User(AbstractUser):
    """
    Единая таблица пользователей. Авторизация идет через нее.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Телефон")
    
    # Внутренняя роль (Админ платформы, Менеджер, Редактор каталога)
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


class SupplierUser(models.Model):
    """
    Промежуточная таблица: Пользователи Поставщиков и их роли.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplier_memberships')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='supplier_users')
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplier_users'
        unique_together = ('user', 'supplier')
        verbose_name = 'Сотрудник поставщика'
        verbose_name_plural = 'Сотрудники поставщиков'


class ShopUser(models.Model):
    """
    Промежуточная таблица: Пользователи Магазинов и их роли в рамках всей сети.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_memberships')
    shop_profile = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='shop_users')
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    # Опционально: можно привязать Продавца к конкретной торговой точке (Shop),
    # чтобы он видел заказы только своего магазина, а не всей сети Владельца.
    assigned_shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_staff',
        verbose_name="Закрепленная торговая точка"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def shop(self):
        return self.assigned_shop or self.shop_profile

    class Meta:
        db_table = 'shop_users'
        unique_together = ('user', 'shop_profile')
        verbose_name = 'Сотрудник магазина'
        verbose_name_plural = 'Сотрудники магазинов'