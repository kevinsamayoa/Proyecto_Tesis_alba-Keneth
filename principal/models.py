from django.db import models

# Create your models here.
class Alertas(models.Model):
    """Modelo y tipo de campo para tabla Alertas"""
    tweet_id = models.CharField(max_length=100)
    texto_tweet = models.TextField()
    nombre = models.CharField(max_length=100)
    edad = models.DecimalField(max_digits=20, decimal_places=2)
    ubicacion = models.CharField(max_length=200)
    fecha = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    longitud = models.DecimalField(max_digits=20, decimal_places=4)
    latitud = models.DecimalField(max_digits=20, decimal_places=4)
    imagen_link = models.CharField(max_length=200)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.tweet_id
