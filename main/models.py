from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
from django import forms
# Create your models here.




class StatusHome(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вид помощи дома'
        verbose_name_plural = 'Виды помощи домам'


class ExportationData(models.Model):
    file = models.FileField(upload_to='files/')
    name= models.CharField(max_length=255)
    total = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сохрененный данный'
        verbose_name_plural = 'Сохрененные данные'


class Needy(models.Model):

    status_type = (
        (0, 'Основные'),
        (1, 'Отроботонные'),
        (2,'Исключение')
    )

    name = models.CharField('Имя',max_length=255, )
    surName = models.CharField('Фамилия', max_length=255,)
    phone = models.CharField('Номер телефона', max_length=11)
    address = models.CharField('Адрес', max_length=255,)
    iin = models.CharField('ИИН', max_length=12)
    childTotal = models.IntegerField('Количество детей', null=True, blank=True)
    statusHome = models.ForeignKey(StatusHome, on_delete=models.CASCADE)
    getHelp = models.TextField('Какую помощь получили')
    period = models.CharField('Срок получение', max_length=255,)
    typeHelp = models.TextField('Какая помощь необходима')
    status = models.IntegerField('Статус малоимущих', choices=status_type,blank=True, null=True)
    createdAt = models.DateTimeField(auto_created=True)
    isDeadMan = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.name} {self.surName}'
        
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


    def save(self, *args,**kwargs):


        if self.status == 1:
            return super().save(*args,**kwargs)
        else:

            super().save(*args,**kwargs)
            
            self.childTotal = int(self.childs.count())
            dateYear = datetime.today().year
            dateMonth = datetime.today().month
            dateDay = datetime.today().day
            
            exceptIin = False
            print("save needs")
            for childIin in self.childs.all():
                iin = str(childIin.iin)
            
                year = iin[0:2]
                month = iin[2:4]
                if iin[2:3] == '0':
                    month = iin[3:4]
            
                day = iin[4:6]

                if iin[4:5] == '0':
                    month = iin[5:6]

                firstNumber = iin[0:1]
                if int(firstNumber) == 9:
                    self.status = 2
                    year = "19"+year
                    exceptIin = True
                    super().save(*args, **kwargs)
                    
                else:
                    year = "20"+year
                if dateYear - int(year) == 18 and exceptIin == False:
                    if dateMonth <= int(month) and exceptIin == False:
                        if dateDay < int(day) and exceptIin == False:
                            self.status = 0
                            super().save(*args, **kwargs)
                        else:
                            self.status = 2
                            super().save(*args, **kwargs)
                    else:
                        self.status = 2
                        super().save(*args, **kwargs)
                elif dateYear - int(year) < 18 and exceptIin == False:
                    self.status = 0
                    super().save(*args, **kwargs)
                else:
                    self.status = 2
                    exceptIin = True
                    super().save(*args, **kwargs)
                
                  

class Child(models.Model):

    name = models.CharField('Имя',max_length=255, )
    surName = models.CharField('Фамилия', max_length=255,)
    iin = models.CharField('ИИН', max_length=12)
    parents = models.ForeignKey(Needy, on_delete=models.CASCADE, related_name='childs')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("save childs")
        print(self.parents.childs.all())
        self.parents.save()
        

    def __str__(self):
        return f'{self.name} {self.surName}'

    class Meta:
        verbose_name = 'Детя'
        verbose_name_plural = 'Дети'


