import os, tempfile, sys
import shutil
import time

"""Usage: 

phoneungap(in_directory, out_directory, out_alias)

  in_directory is a directory containing your project and its files
  out_directory is the name of the directory you'd like them to go to
  out_alias is the string to replace "PhoneGap" with

Usually you would use this in the root PhoneGap directory 
(parent of "iphone")

Defaults:

  in_directory = "iphone"
  out_directory = "myapp"
  out_alias = "MyappName"
"""

def main(argv):
    now = int(time.time())

    in_directory = argv[1] if len(argv)>1 else "iphone"
    out_directory = argv[2] if len(argv)>2 else "phoneungap_%s" % now
    out_alias = argv[3] if len(argv)>3 else "Not%sPG"% now
    
    print copy_and_recursive_replace(in_directory, out_directory, 
    {"PhoneGap": out_alias,
    "phonegap": out_alias.lower()})

def replaceStrings(instring, mapping):
    for before, after in mapping.items():
        instring  = instring.replace(before, after)
    return instring

def replaceStringsInFile(filePath, mapping):
    "replaces all findStr by repStr in file filePath"

    input_file = open(filePath)
    input = input_file.read()
    input_file.close()

    if any(findStr in input for findStr in mapping.keys()):
        print("Changing %s " % filePath)
        tempName=filePath+'~~~'
        output = open(tempName,'w')

        output.write(replaceStrings(input, mapping))
        output.close()
        os.rename(tempName,filePath)

def replaceStringsInFilenameAndRename(path, mapping):
    parent, file = os.path.split(path)
    new_path = os.path.join(parent, replaceStrings(file, mapping))
    if new_path != path:
        print "Renaming %s" % new_path
        if os.path.exists(new_path): 
            raise IOError("File exists! %s" % new_path)
        os.rename(path, new_path)
    return new_path

def recursive_replace(filePath, mapping):
    for path, dirs, files in os.walk(filePath):
       if "/build/" in path:
            continue
       new_path = replaceStringsInFilenameAndRename(path, mapping)
       for file in files:
            filename = os.path.join(new_path, file)
            new_filename = replaceStringsInFilenameAndRename(filename, mapping)
            replaceStringsInFile(new_filename, mapping)
            
def copy_phonegap_js(out_directory):    
    shutil.copyfile("lib/iphone/phonegap.js", "lib/iphone/%s.js" % out_directory)
    shutil.copyfile("lib/iphone/phonegap-min.js", "lib/iphone/%s-min.js" % out_directory)
                
def copy_and_recursive_replace(source_directory, new_directory, mapping):
    shutil.copytree(source_directory, new_directory)
    recursive_replace(new_directory, mapping)
    copy_phonegap_js(new_directory)
    return new_directory
    
main(sys.argv)

