from django.db import models

# Create your models here.
class Visiteur(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    structure = models.CharField(max_length=100)
    lieu_travail = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Soumission(models.Model):
    information = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(auto_now_add=True)
