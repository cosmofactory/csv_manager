from django.db import models


class Deal(models.Model):
    """Deal model."""

    customer = models.CharField('Покупатель', max_length=60)
    item = models.CharField('Товар',  max_length=256)
    total = models.IntegerField('Сумма')
    quantity = models.IntegerField('Количество товара')
    date = models.DateTimeField('Дата сделки')

    def __str__(self):
        return f'{self.customer} {self.item} {self.date}'

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'date'],
                name='deal-already-registered')
        ]
