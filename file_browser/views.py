from django.shortcuts import render
from django.http import HttpResponse, Http404

import os
import time

root = "/home/mihai/all/data/"
#root = "/media/pi/nas" 

def order(dir):
    dirs = []
    files = []
    all_items = []

    for item in os.listdir(dir):
        fullpath = os.path.join(dir, item)
        if os.path.isdir(fullpath):
            dirs.append(item)
        else:
            files.append(item)

    return sorted(dirs) + sorted(files)


def ls(dir):
    data  = []
    color = '1'
    
    for item in order(dir):

        fullpath = os.path.join(dir, item)

        info = os.stat(fullpath)
        last_modified = time.ctime(info.st_mtime)
        #print('last accesed',time.ctime(info.st_atime))

        if os.path.isdir(fullpath):
            size = str(len(os.listdir(fullpath)))
            data.append({'type':'D','href':'?dir='+fullpath,'name':item,'size':size + ' items','last_modified':last_modified})
        else:
            size = str(info.st_size) + " bytes"
            data.append({'type':'F','href':'?file='+fullpath,'name':item,'size':size,'last_modified':last_modified})

    return data


#time.struct_time(tm_year=2019, tm_mon=6, tm_mday=29, tm_hour=19, tm_min=50, tm_sec=11, tm_wday=5, tm_yday=180, tm_isdst=0)


import mimetypes
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

def download_file(the_file):
   filename = os.path.basename(the_file)
   chunk_size = 8192
   response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                    content_type=mimetypes.guess_type(the_file)[0])
   response['Content-Length'] = os.path.getsize(the_file)    
   response['Content-Disposition'] = "attachment; filename=%s" % filename
   return response


def index(request):
    global root

    if 'dir' in request.GET:
        data = ls(request.GET['dir'])
    elif 'file' in request.GET:
        data = download_file(request.GET['file'])
        #return HttpResponse(data)
        return data
    else:
        data = ls(root)

    return render(request, 'file_browser/list.html', {'data':data})
