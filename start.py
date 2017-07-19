from optparse import OptionParser
from os.path import exists, dirname, join
from os import walk, mkdir
import shutil
import face_recognition
import imghdr

file_types = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr']

opt = OptionParser()
opt.add_option('-f', '--folder', dest='folder', help='Folder to perform')
opt.add_option('-r', '--recursive', dest='recursive', help='Recursive search of folders', action="store_true")

(options, args) = opt.parse_args()

def process_folder(folder, recursive):
    no_faces = []
    number_of_files = 0
    number_of_images = 0
    number_of_images_processed = 0
    number_of_images_with_faces = 0
    number_of_images_without_faces = 0

    if exists(dirname(folder)):
        print 'Starting facial recognition check on folder %s' % (folder)
        for (dirpath, dirnames, filenames) in walk(folder):
            print 'Checking files on folder %s' % (dirpath)
            # files.extend([fname for fname in filenames if imghdr.what(join(dirpath, fname)) in file_types])
            for file_name in filenames:
                number_of_files = number_of_files + 1
                if imghdr.what(join(dirpath, file_name)) in file_types:
                    number_of_images = number_of_images + 1
                    print 'Reading image %s' % (file_name)
                    file_path = join(dirpath, file_name)
                    image = face_recognition.load_image_file(file_path)
                    face_locations = face_recognition.face_locations(image)
                    if len(face_locations) < 1:
                        print 'Image %s contains no faces' % (file_name)
                        number_of_images_without_faces = number_of_images_without_faces + 1
                        no_faces.append((file_name, file_path))
                    else:
                        print 'Image %s contains at least one face' % (file_name)
                        number_of_images_with_faces = number_of_images_with_faces + 1
                else:
                    print 'Skipping file %s for facial recognition processing' % (file_name)

            if not recursive:
                break
    else:
        print "FOLDER DOESN'T EXIST"
    
    if len(no_faces) > 0:
        dumps_folder = join(folder, 'no_face_dumps')
        print "%d images without faces detected. Moving them to %s" % (len(no_faces), dumps_folder)
        if not exists(dumps_folder):
            mkdir(dumps_folder)
        for file_name, file_path in no_faces:
            shutil.move(file_path, join(dumps_folder, file_name))

    print 'Done processing folder %s' % (folder)
    print 'Number of files: %s' % (number_of_files)
    print 'Number of images: %s' % (number_of_images)
    print 'Number of images processed: %s' % (number_of_images_processed)
    print 'Number of images with faces: %s' % (number_of_images_with_faces)
    print 'Number of images without faces: %s' % (number_of_images_without_faces)

if hasattr(options, 'folder') and options.folder is not None:
    files = []
    if hasattr(options, 'recursive') and options.recursive is not None:
        process_folder(options.folder, True)
    else:
        process_folder(options.folder, False)
else:
    print "NO FOLDER SUPPLIED"
