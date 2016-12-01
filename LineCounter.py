import fnmatch, os, sys, getopt

extValueDict = {}

def file_len(fname):
    try:
        return sum(1 for line in open(fname))
    except Exception, e:
        return 0
    
def extensionMatch(root, filenames, ext):
    lines = 0
    for filename in fnmatch.filter(filenames, '*' + ext):
        extValueDict[ext] += file_len(os.path.join(root, filename))

def getCount(folder, extensions):
    # initialize the dictionary
    global extValueDict
    for ext in extensions:
        extValueDict[ext] = 0

    for root, dirnames, filenames in os.walk(folder):
        for ext in extensions:
            extensionMatch(root, filenames, ext)

    print "Lines of code in \"%s\" are:" % folder
    for ext in extValueDict.keys():
        print "%s : %s" % (ext, extValueDict[ext])

def exitWithCode(code):
    print 'LineCounter.py -d <targetDirectory> -ext <fileExtensions>'
    print 'Example: LineCounter.py -d /Users -ext .h:.cpp:.js'
    sys.exit(code)

def main(argv):
    targetDirectory = ''
    extensions = []
    try:
        opts, args = getopt.getopt(argv, "hd:e:", ["targetDirectory=", "fileExtensions="])
    except getopt.GetoptError:
      exitWithCode(2)

    getDir = False
    getExt = False
    for opt, arg in opts:
        if opt == '-h':
            exitWithCode(0)
        elif opt in ("-d", "--targetDirectory"):
            targetDirectory = arg
            getDir = True
        elif opt in ("-e", "--fileExtensions"):
            extensions = arg.split(':')
            getExt = True

    if (getDir and getExt):
        getCount(targetDirectory, extensions)
    else:
        exitWithCode(2)
   
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        exitWithCode(2)
    main(sys.argv[1:])


