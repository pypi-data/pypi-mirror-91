import os
from fileio import write_csv



def txt2ava1(txt_path, label_dict, ava_file, ava_obj_file):
    """
    convert sigle txt format file to ava
    surport txt format : frame#,n[id,x1,y1,x2,y2,label]
    """
    annotation_person_arr = []
    annotation_obj_arr = []
    for root, dirs, files in os.walk(txt_path):
        for file in files:
            print(file)
            file_path = os.path.join(txt_path, file)
            video_id = file[:-4]
            with open(file_path) as f:
                txtes = f.readlines()
                for txt in txtes:
                    txt = txt.strip('\n')
                    arr = txt.split(',')
                    frame = arr[0]
                    if int(arr[0]) % 5 == 0:
                        count = int(arr[1])
                        for num in range(count):
                            idx = 2 + num * 6
                            axis = arr[idx+1:idx+5]
                            str = arr[idx+5]
                            labels = str.split('@')
                            idx = labels[0]
                            if labels[1] == 'a':
                                if len(labels) > 2:
                                    for k in labels[2:]:
                                        action_id = label_dict[k]
                                        re_arr = [video_id, int(frame), int(axis[0]), int(axis[1]), int(axis[2]), int(axis[3]), action_id, idx]
                                        annotation_person_arr.append(re_arr)
                                # else:
                                #     re_arr = [video_id, int(frame), int(axis[0]), int(axis[1]), int(axis[2]),
                                #               int(axis[3]), -1, idx]
                                #     annotation_person_arr.append(re_arr)

                            else:
                                label = label_dict[labels[1]]
                                annotation_obj_arr.append([video_id, int(frame), int(axis[0]), int(axis[1]), int(axis[2]), int(axis[3]), label, idx])


    write_csv(annotation_person_arr, ava_file, 'a+')
    write_csv(annotation_obj_arr, ava_obj_file, 'a+')









