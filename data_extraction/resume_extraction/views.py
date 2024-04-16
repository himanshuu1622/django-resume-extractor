from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import os
import PyPDF2
from openpyxl import Workbook as work
import re

def index(request):
    return render(request, 'index.html', {'header': 'HOME'})

def upload(request):
    folder_path = 'C:/Users/daksh/PycharmProjects/sample/data_extraction/media/'
    print("",request.FILES["fileToUpload"])
    uploaded_file = request.FILES["fileToUpload"]
    resume_folder = FileSystemStorage(location=folder_path)
    filename = resume_folder.save(uploaded_file.name.replace(' ', '_').lower(), uploaded_file)
    file_url = resume_folder.url(filename)
    print(file_url)
    name = 'C:/Users/daksh/PycharmProjects/sample/data_extraction'+file_url
    a = PyPDF2.PdfReader(name)
    page = a.pages[0]
    text = page.extract_text()
    email, Ph_numbers = Generators(text)

    output_file = 'output.xlsx'
    text_to_xls(email, Ph_numbers, output_file)
    print(f"Excel file '{output_file}' has been created.")
    return download_file(request)


def text_to_xls(email,Ph_numbers, output_file):
    workbook = work()
    sheet = workbook.active

    lines = email,Ph_numbers

    for row_idx, line in enumerate(lines, start=1):
        columns = line
        for col_idx, value in enumerate(columns, start=1):
            sheet.cell(row=row_idx, column=col_idx, value=value)
        workbook.save(output_file)


def Generators(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    phone_pattern = r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b'

    email = re.findall(email_pattern, text)

    Ph_numbers = re.findall(phone_pattern, text)

    formatted_Ph_numbers = [''.join(number) for number in Ph_numbers]

    return email, formatted_Ph_numbers


def download_file(request):
    file_path = 'output.xlsx'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='sample/output.xlsx')
            response['Content-Disposition'] = 'attachment; filename="resume_data.xlsx"'
            return response
    else:
        return HttpResponse("File not found", status=404)




