#!/usr/bin/python3
import os
import sys


def getFiles():
    '''A helper function to get the list of file names.'''
    path = os.getcwd()
    files = []

    with os.scandir() as d:
        for entry in d:
            if entry.name.endswith('adoc') and entry.is_file():
                files.append(entry.name)

    return(files)

def getId(files):
    '''A function to realize the lowest possible free ID.'''
    ids = []
    for file in files:
        with open(file) as fdata:
            data = fdata.readlines()
        for line in data:
            #print(line)
            if ":rh-id:" in line:
                line = line.strip()
                split = line.split('#')
                idnum = split[1]
                ids.append(int(idnum))
    ids.sort()
    idLen = len(ids)
    nums = [x for x in range(ids[0],ids[-1]+1)]
    a = set(ids)
    compare = list(a^set(nums))

    try:
        idnum = compare[0]
    except IndexError:
        idnum = idLen+1
        
    return(str(idnum))

    
def parseArg():
    '''Parse CLI options.'''
    data = sys.argv
    options = {}
    while len(data) > 1:
        try:
            opt1 = data.pop(1)
            opt2 = data.pop(1)
            options[opt1]=opt2
        except IndexError:
            if opt1 != '-h':
                print('Not a valid command. Use -h for help.')
            else:
                options[opt1]='Help me!'
    return(options)

def solveOpt(options,option):
    try:
        value = options[option]
    except KeyError:
       print('Something went wrong.')
    return(value)   
       
options = (parseArg())


if '-h' in options.keys():
    data = ['============================================',
            'Module Creator (proof-of-concept)',
            '--------------------------------------------',
            'Usage: ModuleCreator.py [option] [argument] [option2] [argument2] ...',
            '-h: displays this help message',
            '-t: title (For more words use quotation marks.)',
            '-b: book acronym, such as odl, nfv, ...',
            '-p: product acronym, such as rhosp, rhel, rhev, ...',
            '-f: function (concept or reference or procedure)',
            '------------------------------------------------',
            'If you run the command without options, or you skip an option, the script will become interactive.',
            '================================================']
    text = '\n'.join(data)
    print(text)

else:
    if '-t' not in options.keys():
        title = input('Write the module title: ')
        ntitle = title.lower()
        ntitle = ntitle.split(' ')
        ntitle = '-'.join(ntitle)
    else:
        title = solveOpt(options,'-t')
        print(title)
        ntitle = title.lower()
        ntitle = ntitle.split(' ')
        ntitle = '-'.join(ntitle)

    if '-p' not in options.keys():
        product = input("Write the acronym of the product (rhosp, rhel, rhev, ...): ")
        product = product.lower()
    else:
        product = solveOpt(options,'-p')
        
    if '-b' not in options.keys():
        book = input("Write the acronym of the guide (odl, nfv, ...): ")
        book = book.lower()
    else:
        book = solveOpt(options,'-b')
        
    if '-f' not in options.keys():
        function = input("Write the function of the module (concept, reference, procedure): ")
        print(function)
        function = function.lower()
    else:    
        function = solveOpt(options,'-f')
        
    flist = getFiles()
    fID = getId(flist)

    fname = [function,fID,product,book,ntitle]
    fname = '_'.join(fname)
    fname = fname+'.adoc'

    lineId = ':rh-id: #'+fID
    linePr = ':rh-provides: '
    lineUs = ':rh-used-by: '
    lineTg = ':rh-tags: '
    lineTi = '= '+title

    ftext = [lineId,linePr,lineUs,lineTg,' ',lineTi]

    if fname not in flist:
        with open(fname,'w') as outfile:
            for line in ftext:
                outfile.write(line)
                outfile.write('\n')
        print('File %s was succesfully created.' %fname)
    else:
        print('File %s already exists which is strange. Resolve the conflict first!' %fname)

