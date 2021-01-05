import json
import subprocess
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.staticfiles.utils import get_files
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os
import os.path

# Create your views here.
from django.template import RequestContext
from django.template.loader import render_to_string

from djangoProject import settings


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def register(request):
    return render(request, 'keygen/register.html')

@login_required
def register_submit(request):
    print(request.POST)
    jsonData = request.POST.get('json', None)
    jsonD = json.loads(jsonData)
    # print(jsonD)

    array = []
    input_str = ""
    for (k, v) in jsonD.items():
        array.append(v)
    i = 0
    # print (array)
    # print(array[1])
    # print(len(array))
    # print(array)
    for i in range(0, int((len(array))), 2):  # num of rows in table'
        print(array[i+1])
        if array[i + 1] == "":
            # print('Line ' + str(i) + ' NO number')
            input_str = input_str + (array[i].replace("'", ""))
            input_str = input_str + " "
            # print("input:" + input_str)
        else:
            # print('Line ' + str(i) + ' number')
            temp_str = array[i] + ' = ' + array[i + 1]
            temp_str = temp_str.replace("'", "")
            temp_str = "'" + temp_str + "'"
            # print(temp_str)
            input_str += temp_str
            input_str += " "
    print(input_str.strip())
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    arguments=PROJECT_PATH + "/graphene/Runtime/pal_loader"
    arguments += " cpabe-keygen.manifest pub_key master_key "+input_str.strip()
    print(arguments)

    print(PROJECT_PATH + "/graphene/Runtime/pal_loader")
    res = subprocess.call([arguments], cwd=settings.GRAPHENE_DIR, shell=True)
    print (res)
    return JsonResponse({"response": "success"})




def graphene_setup_check(self):
    if os.path.exists(os.path.join(settings.GRAPHENE_DIR, 'pub_key')):
        return JsonResponse({'success': 'true'})
    else:
        return JsonResponse({'success': 'false'})


def download_pubkey(self):
    file_path = os.path.join(settings.GRAPHENE_DIR, 'pub_key')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def setup(self):
    print('Running Setup')
    res = subprocess.call(["../../Runtime/pal_loader", "cpabe-setup.manifest","SGX=1"], cwd=settings.GRAPHENE_DIR)
    return JsonResponse({"response": "success"}, safe=False)


def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def profileView(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.get_username()
    s = FileSystemStorage()
    # checkIfFolderExistOrCreate(s.location, username)
    files = list(get_files(s, location=username))

    return render(request, 'index.html', {
        'files': files,
    })


def usersView(request):
    User = get_user_model()
    users = User.objects.all()

    return render(request, 'users.html', {
        'users': users
    })


def userView(request, user):
    s = FileSystemStorage()
    # checkIfFolderExistOrCreate(s.location, user)
    files = list(get_files(s, location=user))
    return render(request, 'user.html', {
        'user': user,
        'files': files,
    })


def uploadView(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.get_username()

    s = FileSystemStorage()
    checkIfFolderExistOrCreate(s.location, username)

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=FileSystemStorage().location + '/' + username)
        filename = fs.save(myfile.name, myfile)

        return render(request, 'upload.html', {
            'uploaded_file': filename
        })
    return render(request, 'upload.html')


def checkIfFolderExistOrCreate(location, folder):
    if not os.path.isdir(location + '/' + folder):
        os.mkdir(location + '/' + folder)


def revokeView(request):
    myfile = request.POST['filename']
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    data_file = open(PROJECT_PATH + '/revoked.txt', 'r')
    users = []
    for line in data_file:
        line.strip().split('/n')
        if line.startswith(myfile):
            users.append(line.split(',')[1])
    data_file.close()
    myRender = render_to_string('modal.html', {'revokedUsers': users, 'filename': myfile}, request=request)
    context = {'context': myRender}
    return JsonResponse(context)


def revokeSaveView(request):
    myfile = request.POST['filename']
    user = request.POST['user']
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    with open(PROJECT_PATH+'/revoked.txt', "a") as data_file:
        data_file.write(myfile+','+user+'\n')
    data_file.close()

    data = {
        'names': "S",
    }
    return JsonResponse(data)


def revokeRemoveView(request):
    myfile = request.POST['filename']
    user = request.POST['user']
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    data_file = open(PROJECT_PATH + '/revoked.txt', 'r')
    lineToDel=None;
    lines=[]
    for line in data_file:
        lines.append(line)
        line.strip().split('/n')
        parts = line.split(',')
        if parts[0] == myfile and parts[1].rstrip("\n") == user:
            lineToDel=line
    data_file.close()
    # print(lines)
    # print(lineToDel)
    with open(PROJECT_PATH + '/revoked.txt', "w") as f:
        for line in lines:
           line.strip().split('/n')
           if line!=lineToDel:
               f.write(line)
    f.close()

    data = {
        'names': "S",
    }
    return JsonResponse(data)