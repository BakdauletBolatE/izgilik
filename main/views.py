from django.shortcuts import render
from main.models import Needy,ExportationData
import xlsxwriter
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages




def change_status(request):
    print(request)
    return redirect('/main/needy/')

def file_save(request):
    status_id = request.GET.get('status__exact')
    data_in = request.GET.get('calendar_in')
    data_out = request.GET.get('calendar_out')

    if data_out == '' or data_in== '':
        messages.warning(request, 'Вы не выбрали дату')
        return redirect('/main/needy/')
        
    if status_id == 'null':
        needys = Needy.objects.all().filter(createdAt__range=[data_in, data_out])
    else:
        needys = Needy.objects.all().filter(status=status_id,createdAt__range=[data_in, data_out])
    

    str_name = f"/files/{str(data_in)}_{str(data_out)}_statusHome={status_id}.xlsx"

    print(settings.MEDIA_ROOT)
    workbook = xlsxwriter.Workbook(str(settings.MEDIA_ROOT)+str_name)
    worksheet = workbook.add_worksheet()

    ExportationData.objects.create(
        file=str_name,
        name=f"{str(data_in)}_{str(data_out)}_statusHome={status_id}",
        total=f"{str(needys.all().count())} - данных"
    )

    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '$#,##0'})

    # Write some data headers.
    worksheet.write('A2', 'Имя', bold)
    worksheet.write('B2', 'Фамилия', bold)
    worksheet.write('C2', 'Номер телефона', bold)
    worksheet.write('D2', 'Адрес', bold)
    worksheet.write('E2', 'ИИН', bold)
    worksheet.write('F2', 'Количество детей', bold)
    worksheet.write('G2', 'Статус дома', bold)
    worksheet.write('H2', 'Какую помощь получили', bold)
    worksheet.write('I2', 'Срок получение', bold)
    worksheet.write('J2', 'Какая помощь необходима', bold)
    worksheet.write('K2', 'Статус малоимущих', bold)

    row = 2
    col = 0
    for item in needys:        
        worksheet.write_string (row, col, item.name )
        worksheet.write_string  (row, col + 1, item.surName)
        worksheet.write_string (row, col+2, item.phone)
        worksheet.write_string (row, col+3, item.address)
        worksheet.write_string (row, col+4, item.iin)
        worksheet.write_number (row, col+5, item.childTotal)
        worksheet.write_string (row, col+6, item.statusHome.name)
        worksheet.write_string (row, col+7, item.getHelp)
        worksheet.write_string (row, col+8, item.period)
        worksheet.write_string (row, col+9, item.typeHelp)
        worksheet.write_number (row, col+10, item.status)
        row += 1
        


    workbook.close()
    messages.success(request, 'Успешно эскпортировано')
    return redirect('/main/needy/')
