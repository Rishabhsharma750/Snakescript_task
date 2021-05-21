from django.db import models


class Profession(models.Model):
    description=models.CharField(max_length=50)

    def __str__(self):
        return self.description

class DataSheet(models.Model):
    description=models.CharField(max_length=50)
    historical_data=models.TextField()

    def __str__(self):
        return self.description

class Customer(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    professions=models.ManyToManyField(Profession)
    data_Sheet=models.OneToOneField(DataSheet,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    doc_num=models.CharField(max_length=12,unique=True)

    @property
    def status_message(self):
        if self.active:
            return "Customer active"
        else:
            return "Customer inactive"

    def num_professions(self):
        return self.professions.all().count()

    def __str__(self):
        return self.name

class Document(models.Model):
    PP='PP'
    ID ='ID'
    OT='OT'

    DOC_TYPE=(
        (PP,'Passport'),
        (ID,'Identity Card'),
        (OT,'Other')
    )

    dtype=models.CharField(choices=DOC_TYPE,max_length=2)
    doc_number=models.CharField(max_length=50)
    customers=models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number
