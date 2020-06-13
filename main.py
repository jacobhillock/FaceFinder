import face_recognition as fr
import platform, os
from shutil import copy2

file_del = '/'
if platform.system() == 'Windows':
    file_del = '\\'

image_ext = ['jpg', 'jpeg', 'png']
knowns = []
knowns_dir = f'known{file_del}'

for file in os.listdir(knowns_dir):
    if file.split(".")[-1] in image_ext:
        # print(file)
        temp = fr.load_image_file(os.path.join(knowns_dir, file))
        for face in fr.face_encodings(temp):
            knowns.append(face)

confirmed = []
search_base = input("Enter full searching path, defaukt 'C:\'")
if search_base == '':
    search_base = 'C:\\'
for root, dir, files in os.walk():
    print(root)
    for file in files:
        if file.split(".")[-1] in image_ext:
            # print(file)
            photo = fr.face_encodings(
                        fr.load_image_file(os.path.join(root, file))
                    )
            for face in photo:
                add = False
                for boo in fr.compare_faces(knowns, face):
                    if boo:
                        add = True
                if add:
                    confirmed.append(os.path.join(root, file))

print(confirmed)

base = ''
path = str(__file__).split(file_del)
for p in path[:-2]:
    base = os.path.join(base, p)
base = os.path.join(base, f'found{file_del}')
if platform.system() != 'Windows':
    base = '/' + base

for c in confirmed:
    copy2(c, base)
