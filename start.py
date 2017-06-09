from optparse import OptionParser
from os.path import exists, isfile, dirname, join
from os import walk, mkdir
import shutil
import face_recognition
import imghdr

file_types = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr']

opt = OptionParser()
opt.add_option('-f', '--folder', dest='folder', help='Folder to perform')
opt.add_option('-r', '--recursive', dest='recursive', help='Recursive search of folders', action="store_true")

(options, args) = opt.parse_args()

def get_files_from_folder(folder, recursive):
    files = []
    if exists(dirname(folder)):
        for (dirpath, dirnames, filenames) in walk(folder):
            files.extend([fname for fname in filenames if imghdr.what(join(dirpath, fname)) in file_types])
            if not recursive:
                break
    else:
        print "FOLDER DOESN'T EXIST"
    
    no_faces = []
    len_files = len(files)
    index = 1
    print "%d images to process. Facial recognition starting." % (len_files)
    for file_name in files:
        print '[%d/%d] Reading %s' % (index, len_files, file_name)
        file_path = join(folder, file_name)
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) < 1:
            no_faces.append((file_name, file_path))
        index = index + 1
    
    if len(no_faces) > 0:
        dumps_folder = join(folder, 'no_face_dumps')
        print "%d images without faces detected. Moving them to %s" % (len(no_faces), dumps_folder)
        if not exists(dumps_folder):gi
            mkdir(dumps_folder)
        for file_name, file_path in no_faces:
            shutil.move(file_path, join(dumps_folder, file_name))

    return files
    

if hasattr(options, 'folder') and options.folder is not None:
    files = []
    if hasattr(options, 'recursive') and options.recursive is not None:
        get_files_from_folder(options.folder, True)
    else:
        get_files_from_folder(options.folder, False)
else:
    print "NO FOLDER SUPPLIED"
