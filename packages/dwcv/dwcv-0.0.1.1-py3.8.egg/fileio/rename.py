
import hashlib
import time
import os


def _createmd5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()), encoding='utf-8'))
    return m.hexdigest()



def md5rename1(org_movie_path, org_txt_path, rename_movie_path, rename_txt_path):
    """

    :param org_movie_path:
    :param org_txt_path:
    :param rename_movie_path:
    :param rename_txt_path:
    :return: None
    """

    for root, dirs, files in os.walk(org_txt_path):
        for file in files:
            dotpos = file.rfind('_')
            if dotpos < 0:
                file = file
            else:
                file = file[:dotpos]
            name = file + '.mp4'
            org_movie_file_path = os.path.join(org_movie_path, name)
            new_name = _createmd5()
            rename_movie_file_path = os.path.join(rename_movie_path, new_name + '.pm4')
            org_txt_file_path = os.path.join(org_txt_path, file + '_gt.txt')
            rename_txt_file_path = os.path.join(rename_txt_path, new_name + '.txt')
            os.rename(org_movie_file_path, rename_movie_file_path)
            os.rename(org_txt_file_path, rename_txt_file_path)





