from django.db import models

class NameEntry(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    order_number = models.IntegerField(verbose_name="Порядковый номер")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order_number']
    
    def __str__(self):
        return f"{self.order_number}. {self.name}"