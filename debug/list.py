import os

def traverse(dir):
    print('<ul>')
    for item in os.listdir(dir):
        print('<li>%s</li>' % item)
        fullpath = os.path.join(dir, item)
        if os.path.isdir(fullpath):
            #if not ALL : print('<li>%s</li>' % item)
            if os.listdir(fullpath) != []:
                traverse(fullpath)
    print('</ul>')


#traverse("/home/mihai/all/data/django/")


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


traverse1("/home/mihai/all/data/django/")
print(my_list)

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


