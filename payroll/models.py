from django.db import models


class Salary(models.Model):

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='salaries'
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    allowances = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    effective_from = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        self.net_salary = (
            self.basic_salary
            + self.allowances
            - self.deductions
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.net_salary}"

class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'

    class PaymentMethod(models.TextChoices):
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
        CASH = 'CASH', 'Cash'
        UPI = 'UPI', 'UPI'

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    salary = models.ForeignKey(
        Salary,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True
    )

    processed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_payments'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.username} - ₹{self.amount}"


class BankStatement(models.Model):

    class TransactionType(models.TextChoices):
        CREDIT = 'CREDIT', 'Credit'
        DEBIT = 'DEBIT', 'Debit'

    transaction_date = models.DateField()

    transaction_reference = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.CharField(
        max_length=255
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bank_name = models.CharField(
        max_length=100
    )

    reconciled = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.transaction_reference} - ₹{self.amount}"


class Insurance(models.Model):

    employee = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='insurance'
    )

    insurance_provider = models.CharField(
        max_length=100
    )

    policy_number = models.CharField(
        max_length=100,
        unique=True
    )

    coverage_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee.username} - {self.policy_number}"


class InsuranceClaim(models.Model):

    class ClaimStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='insurance_claims'
    )

    claim_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    claim_reason = models.TextField()

    medical_certificate = models.FileField(
        upload_to='medical_certificates/'
    )

    status = models.CharField(
        max_length=20,
        choices=ClaimStatus.choices,
        default=ClaimStatus.PENDING
    )

    reviewed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_insurance_claims'
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee.username} - ₹{self.claim_amount}"