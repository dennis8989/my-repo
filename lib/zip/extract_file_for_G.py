import os
import time
import zipfile
import pyzipper
import shutil
import requests
import traceback
from bs4 import BeautifulSoup
import subprocess
from multiprocessing import Pool
import re
filename_extension = ['.zip', '.rar','.7z']
def get_pwd():
    r = requests.get("https://renrenbear.com/fufeimimaben2-0/")
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.select("#tablepress-1")[0]
    list_video = table.select("tr")
    dict_video = {}
    for video in list_video[1:]:
        attr_video = video.select("td")
        name_video = attr_video[1].get_text()
        pwd_video = attr_video[2].get_text()
        dict_video[name_video] = pwd_video
    return dict_video


def scandir(path):
    list_path = []
    with os.scandir(path) as entries:
        for item in entries:
            list_path.append(item.path)
    return list_path


def scandir_recurse(path, list_path):
    # list_path = []
    with os.scandir(path) as entries:
        for item in entries:
            if item.is_dir():
                scandir_recurse(item.path, list_path)
            else:
                list_path.append(item.path)
    return list_path


# scandir_recurse(".\\", [])

def zip_list(path_file):
    zf = zipfile.ZipFile(path_file, 'r')
    list_unextract_files = zf.namelist()
    return list_unextract_files

def pyzipper_namelist(path_zipfile):
    # pwd = 'bear'
    with pyzipper.AESZipFile(path_zipfile, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
        # print(extracted_zip.namelist())
        # print(extracted_zip.infolist())
        return extracted_zip.namelist()

def pyzipper_extract(path_file, path_folder, pwd="bear"):
    # pwd = 'bear'
    with pyzipper.AESZipFile(path_file, 'r', compression=pyzipper.ZIP_DEFLATED,
                             encryption=pyzipper.WZ_AES) as extracted_zip:
        extracted_zip.extractall(pwd=str.encode(pwd), path=path_folder)
    print(f"{path_file} has been extracted")
    return
def pyzipper_extract_mp(member, path_zipfile, path_folder_extract_to, pwd):
    # pwd = 'bear'
    with pyzipper.AESZipFile(path_zipfile, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
        extracted_zip.extract(member,pwd=str.encode(pwd), path=path_folder_extract_to)
        print(f"{member} done")

def main():
    path = ".\\"
    list_path_zipfile = []
    list_path = scandir(path)
    dict_video = get_pwd()
    for path in list_path:
        if os.path.splitext(path)[-1] in filename_extension:
            list_path_zipfile.append(path)  # find all path from main folder

    for path_zipfile in list_path_zipfile:
        path_folder = ".\\temp\\"
        orginal_file = path_zipfile #.\example.py
        basename = os.path.basename(path_zipfile)  # example.py
        filename = os.path.splitext(basename)[0] # example
        filename_only = re.search("(?<=（).+|(?<=\().+", filename).group()[:-1]
        # filename_only = re.search("(?<=（).+(?=）)", filename).group()
        try:
            pwd = dict_video[filename_only]
        except:
            print(traceback.format_exc())
            pwd = 'unknown'
        if not os.path.isdir(path_folder):
            os.mkdir(path_folder)
        else:
            shutil.rmtree(path_folder)
            time.sleep(3)
            os.mkdir(path_folder)
            print(f"{path_folder} was created")

        text = fr'.\7-Zip64\7z.exe x -aoa  "{path_zipfile}" -o{path_folder} -pbear' #----------------- extract file 1 time
        os.system(fr"{text}")
        time.sleep(3)


        list_path_recursive = []
        list_path_recursive = scandir_recurse(path_folder, list_path_recursive)
        for path_recursive in list_path_recursive:
            if os.path.splitext(path_recursive)[-1] in filename_extension:

                path_zip_file = path_recursive
                path_zip_folder = os.path.dirname(path_zip_file)
                text = fr'.\7-Zip64\7z.exe x -aoa  "{path_zip_file}" -o"{path_zip_folder}" -pbear'#----- extract file 2 time
                result = os.system(fr"{text}")
                print(f"result is {result}")
                os.remove(fr"{path_zip_file}")
                break

        path_folder = path_zip_folder
        list_path_recursive = []
        list_path_recursive = scandir_recurse(path_folder, list_path_recursive)
        for path_recursive in list_path_recursive:
            if os.path.splitext(path_recursive)[-1] in filename_extension:
                path_zip_file = path_recursive
                path_zip_folder = os.path.dirname(path_zip_file)
                try:
                    if pwd == 'unknown':
                        # for key, pwd in dict_video.items():
                        #     print(f"now pwd is {pwd}")
                        #     start = time.time()
                        #     text = fr'.\7-Zip64\7z.exe x -aoa  "{path_zip_file}" -o"{path_zip_folder}" -p{pwd}'# extract file 3 time
                        #     print(text)
                        #     result = os.system(fr"{text}")
                        #     print((f"result is {result}"))
                        #     if result == 0:
                        #         break
                        #     result = ''
                        #     end = time.time()

                        with pyzipper.AESZipFile(path_zip_file, 'r') as f:
                            for key, pwd in dict_video.items():
                                f.pwd = str.encode(pwd)
                                try:
                                    print((f"try {pwd}"))
                                    f.extractall(path=f"{path_zip_folder}")
                                    print("\t密碼是:" + pwd)
                                    break
                                except Exception:
                                    pass
                    else:
                        print(f"now pwd is {pwd}")
                        start = time.time()
                        text = fr'.\7-Zip64\7z.exe x -aoa  "{path_zip_file}" -o"{path_zip_folder}" -p{pwd}'# extract file 3 time
                        print(text)
                        result = os.system(fr"{text}")  #
                        print((f"result is {result}"))
                        end = time.time()
                    # print(f"unzip time is {end - start}")
                    os.remove(fr'{path_zip_file}')
                    print(f'"{path_zip_file}" was removed')
                    shutil.move(fr'{path_zip_folder}',f".\\")
                    print(f'"{path_zip_folder}" was moved to main folder')
                    os.remove(f'{orginal_file}')
                    print(f'"{orginal_file}" was removed')
                    break
                except Exception as e:
                    print(e)
                    pass
if __name__ == '__main__':
    main()
#pyinstaller -F --name myapp3 getdriver_by_requests.py