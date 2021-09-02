import pyzipper
import time
from multiprocessing import Pool
def pyzipper_namelist(path_zipfile, path_folder_extract_to, pwd = "bear"):
    # pwd = 'bear'
    with pyzipper.AESZipFile(path_zipfile, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
        print(extracted_zip.namelist())
        print(extracted_zip.infolist())

        # extracted_zip.extract('收费部分/123man+ phamcuong/123Men phamcuonng/',pwd=str.encode(pwd), path=path_folder_extract_to)
        # extracted_zip.extractall(pwd=str.encode(pwd),path=path_folder_extract_to)
    # print(f"{path_zipfile} has been extracted")
    return extracted_zip.namelist()

# def pyzipper_extract(member, path_zipfile = ".\\abc.zip", path_folder_extract_to=".\\", pwd = "relax"):
def pyzipper_extract(member, path_zipfile, path_folder_extract_to, pwd):
    # pwd = 'bear'
    with pyzipper.AESZipFile(path_zipfile, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
        extracted_zip.extract(member,pwd=str.encode(pwd), path=path_folder_extract_to)
        print(f"{member} done")
        # extracted_zip.extractall(pwd=str.encode(pwd),path=path_folder_extract_to)
    # print(f"{path_zipfile} has been extracted")


# start = time.time()
# pyzipper_extract(".\\abc.zip",".\\",pwd="relax")
# end = time.time()
# print(end-start)

if __name__ == '__main__':
    with Pool(2) as p:
        start = time.time()
        namelist = pyzipper_namelist(".\\abc.zip",".\\",pwd="relax")
        len_namelist = len(namelist)
        path_zipfile = [".\\abc.zip"]*len_namelist
        path_folder_extract_to = [".\\"]*len_namelist
        pwd = ["relax"] * len_namelist
        tasks = [*zip(namelist,path_zipfile, path_folder_extract_to, pwd)]
        p.starmap(pyzipper_extract, iterable=tasks)
        # p.map(pyzipper_extract, [namelist,path_zipfile, path_folder_extract_to, pwd])
        end = time.time()
        print(end-start)