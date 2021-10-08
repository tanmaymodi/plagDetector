from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from auth_app.models import User
from .algorithms import plagiarism_detector
import os
from .document_parser import document_parser

#########################################################


def home(request):
    context = {'navigation': []}
    is_authenticated = request.user.is_authenticated
    notAuth = not is_authenticated
    username = ""
    if is_authenticated:
        username = request.user.username
    
    Matrix = [['x','a','b','c'],['a',1,3,5],['b', 4,7,34],['c',32,8,43]]
    context = {'is_authenticated': is_authenticated, 'username': username, "notAuth": notAuth, 'result':Matrix,}
    return render(request, 'plagDetector/home.html', context)


# test function to compare two texts -Tanmay/Aadarsh/Aayush
def get_similarity(doc_list):
    # str1 = ''.join(text1)
    # str2 = ''.join(text2)
    # doc_list = [str1, str2]
    pd = plagiarism_detector(doc_list)
    similarity = pd.get_results()
    return similarity


# test function two check two input texts
def search(request):
    # search goes here
    if request.method == 'POST':
        final_list = "cosine result"
        text1 = request.POST.get('text1', None)
        text2 = request.POST.get('text2', None)
        result = get_similarity([text1, text2])
        is_authenticated = request.user.is_authenticated
        username = ""
        if is_authenticated:
            username = request.user.username
        context = {'result': result, 'is_authenticated': is_authenticated, 'username': username}
        print(context)
        return render(request, 'plagDetector/home.html', context)
    else:
        return render(request, 'plagDetector/home.html')


# function to upload multiples files
# files are stored in the ./media folder of the directory
def upload(request):
    result = []
    doc_titles = []
    # list of students over threshold vaues

    doc_titles.append('___')
    if request.method == 'POST':
        assignment_name = request.POST['assignment_name']
        percentage_ = request.POST['percentage_']
        # for y, file in enumerate(request.FILES.getlist("document")):
        #     allowed_ext = ['txt', 'docx', 'doc']
        #     if file.name.split('.')[-1] not in allowed_ext:
        #         context = {'error': 'file extension not allowed, please upload a txt/doc/docx file!'}
        #         print("error occured")
        #         return render(request, 'plagDetector/home.html', context)

        for x, upload_file in enumerate(request.FILES.getlist("document")):
            print(upload_file.name)
            doc_titles.append(str(upload_file.name))
            print(upload_file.size)
            fs = FileSystemStorage()
            fs.save(upload_file.name, upload_file, max_length=None)

        doc_names, doc_list = get_doc_list()
        #print(doc_list)
        temp = get_similarity(doc_list)
        for cc in temp:
            result.append(cc)
    
        print(get_similarity(doc_list))

    #test list (to be removed)
    daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


    #rounding off values 
    Matrix = []
    Matrix.append(doc_titles)

    for x in result:
        temp = []
        for title in doc_titles:
            if title == "___":
                continue
            temp.append(title)
        
            for y in x:
            
                g = "{:.2f}".format(y)
                temp.append(g)

            break
        Matrix.append(temp)
    
    context = {"dow":daysOfWeek,"result":Matrix} 
    return render(request, 'plagDetector/home.html',context)


def parse_file(path):
    dp = document_parser(path)
    return dp.get_content()


def get_doc_list():
    d = os.getcwd()
    d1 = os.path.join(d, "media")
    media_dir = os.listdir(d1)
    print(media_dir)

    doc_list = []
    doc_names = []
    for file in media_dir:
        file_path = os.path.join(d1, file)
        # print("FF:", file_path)
        doc_content = parse_file(file_path)
        doc_list.append(doc_content)
        doc_names.append(file_path)

    return doc_names, doc_list


def find_color(x,n):
    if x == 0 or n ==0:
        return "green"
    if x>=n:
        return "red"
    if n<=10:
        if x <= n/2:
            return "green"
        else:
            return "yellow"
    