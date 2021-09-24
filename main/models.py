from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
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


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Needy(models.Model):

    status_type = (
        (0, 'Помощь не полученные'),
        (1, 'Полученные'),
        (2,'Исключение'),
        (3,'Заново не полученные')
    )

    name = models.CharField('Имя',max_length=255, )
    surName = models.CharField('Фамилия', max_length=255,)
    phone = models.CharField('Номер телефона', max_length=11)
    address = models.CharField('Адрес', max_length=255,)
    iin = models.CharField('ИИН', max_length=12)
    childTotal = models.IntegerField('Количество детей', null=True, blank=True)
    statusHome = models.ForeignKey(StatusHome, verbose_name="Статус дома", on_delete=models.CASCADE, blank=True, null=True)
    getHelp = models.TextField('Какую помощь получили',null=True,blank=True)
    period = models.CharField('Срок получение', max_length=255,null=True,blank=True)
    typeHelp = models.TextField('Какая помощь необходима',null=True,blank=True)
    status = models.IntegerField('Статус малоимущих', choices=status_type,blank=True, null=True)
    comment = models.TextField('Комментарий', null=True, blank=True)
    created_at = models.DateTimeField("Дата создания",default=timezone.now)
    updated_at = models.DateTimeField("Дата изменения",auto_now=True)
    isDeadMan = models.BooleanField("Статус вдовы",default=False)
    helped = models.BooleanField("Помощь получили",default=False)
    region = models.ForeignKey(Region,verbose_name='Регион', on_delete=models.CASCADE,blank=True,null=True)
    owner = models.ForeignKey(User, verbose_name="Создатель заявки", null=True, blank=True,on_delete=models.CASCADE,related_name="owner")
    changed_onwer = models.ForeignKey(User,null=True, verbose_name="Изменитель заявки", blank=True,on_delete=models.CASCADE,related_name="changed_owner")


    def __str__(self):
        return f'{self.name} {self.surName}'
        
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


    def save(self,*args,**kwargs):

        
        

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
                if childIin.gender == "Девочка":
                    if self.status == 2:
                        return super().save(*args,**kwargs)
                    self.status = 0
                    return super().save(*args,**kwargs)
                        

                else:
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
                                if self.helped == True:     
                                    self.status = 3
                                    
                                else:
                                    self.status = 0
                            else:
                                self.status = 2
                        else:
                            self.status = 2

                    elif dateYear - int(year) < 18 and exceptIin == False:
                        if self.helped == True:
                            self.status = 3
                        else:
                            if self.status == 2:
                                return super().save(*args,**kwargs)
                            self.status = 0
                            
                    else:
                        self.status = 2
                        exceptIin = True
                    super().save(*args, **kwargs)
                                
                  

class Child(models.Model):

    gend = (
        ('Мальчик', 'Мальчик'),
        ('Девочка', 'Девочка')
    )

    name = models.CharField('Имя',max_length=255, )
    surName = models.CharField('Фамилия', max_length=255,)
    iin = models.CharField('ИИН', max_length=12)
    parents = models.ForeignKey(Needy, on_delete=models.CASCADE, related_name='childs')
    gender = models.CharField('Пол ребенка', max_length=255, choices=gend, blank=True, null=True )

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


