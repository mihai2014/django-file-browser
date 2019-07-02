#from wsgiref.util import FileWrapper
import os, tempfile, zipfile

def send_file(request):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """
    filename = __file__ # Select your file here.                                
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def send_zipfile(request):
    """                                                                         
    Create a ZIP file on disk and transmit it in chunks of 8KB,                 
    without loading the whole file into memory. A similar approach can          
    be used for large dynamic PDF files.                                        
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(10):
        filename = __file__ # Select your files here.                           
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response



#display tree
my_list = ""
def traverse1(dir):
    global my_list

    my_list += '<ul>'

    for item in os.listdir(dir):

        fullpath = os.path.join(dir, item)

        if os.path.isdir(fullpath):
            my_list += '<li>%s</li>' % item
            #data.append({'type':'D','href':'#','name':item})
        else:
            my_list += '<li><a href="%s">%s</a></li>' % (''+fullpath ,item)
            #data.append({'type':'F','href':'/static'+fullpath,'name':item})

        if os.path.isdir(fullpath):
            if os.listdir(fullpath) != []:
                traverse1(fullpath)

    my_list += '</ul>'



#display tree with links
data = []
def traverse2(rootDir):
    global data

    #my_list += '<ul>'
    for dirName, subdirList, fileList in os.walk(rootDir):
        #type = 'D'
        #href = '#'
        #name = '/static'+dirName+'/'
        if len(fileList) == 0:
            data.append({'type':'D','href':'#','name':''+dirName})
        for fname in fileList:
            #my_list += '<li><a href="%s">%s</a></li>' % ('/static'+dirName+'/'+fname ,'/static'+dirName+'/'+fname)
            data.append({'type':'F','href':''+dirName+'/'+fname,'name':dirName+'/'+fname})
    #my_list += '<ul>'

