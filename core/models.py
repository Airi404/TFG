from django.db import models

class Mascota(models.Model):
    TIPO_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('hámster', 'Hámster'),
        ('conejo', 'Conejo'),
        ('pajaro', 'Pájaro'),
        ('otro', 'Otro'),
    ]

    CARACTER_CHOICES = [
        ('tranquilo', 'Tranquilo'),
        ('jugueton', 'Juguetón'),
        ('agresivo', 'Agresivo'),
        ('timido', 'Tímido'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    raza = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    años = models.PositiveIntegerField()
    caracter = models.CharField(max_length=20, choices=CARACTER_CHOICES)
    foto = models.ImageField(upload_to='mascotas/')

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre