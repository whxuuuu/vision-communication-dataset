import numpy as np
import cv2

rotation_matrix = lambda thetaz: np.array(
    [[np.cos(thetaz), -np.sin(thetaz), 0], [np.sin(thetaz), np.cos(thetaz), 0], [0, 0, 1]])



image_size_x = 1280
image_size_y = 480
Hfov = 90


def camera_axis(vec):
    return np.array([vec[0], -vec[2], vec[1]])



def cal_slope(p1, p2):
    if np.linalg.norm(p2 - p1, 2)!=0:
        return (p2 - p1) / np.linalg.norm(p2 - p1, 2)
    else:
        return 0


L_max = 11.076664
W_max = 3.250588
H_max = 3.326848


def cubic_proj(Img, cubic_point, K, extent):
    cubic_point_proj = np.dot(K, cubic_point)
    cubic_point_proj = (cubic_point_proj / cubic_point_proj[2, :])[0:2, :]
    cubic_point_proj[0,:]=np.minimum(np.maximum(cubic_point_proj[0,:],0),image_size_x-1)
    cubic_point_proj[1,:] = np.minimum(np.maximum(cubic_point_proj[1,:], 0), image_size_y - 1)
    step = 0.5
    plane_list = []
    plane_list.append(np.array([[1, 5], [2, 6]]) - 1)
    plane_list.append(np.array([[4, 8], [3, 7]]) - 1)
    plane_list.append(np.array([[1, 5], [4, 8]]) - 1)
    plane_list.append(np.array([[5, 6], [8, 7]]) - 1)
    plane_list.append(np.array([[2, 6], [3, 7]]) - 1)
    plane_list.append(np.array([[1, 4], [2, 3]]) - 1)

    for plane in plane_list:
        slope1 = step * cal_slope(cubic_point_proj[:, plane[0, 0]], cubic_point_proj[:, plane[0, 1]])
        slope2 = step * cal_slope(cubic_point_proj[:, plane[1, 0]], cubic_point_proj[:, plane[1, 1]])

        max_length1 = np.linalg.norm(cubic_point_proj[:, plane[0, 0]] - cubic_point_proj[:, plane[0, 1]], 2)
        max_length2 = np.linalg.norm(cubic_point_proj[:, plane[1, 0]] - cubic_point_proj[:, plane[1, 1]], 2)
        if np.all(slope1==0):
            index1_max=1
        else:
            index1_max = int((max_length1 // step)+1)
        if np.all(slope2==0):
            index2_max=1
        else:
            index2_max = int((max_length2 // step)+1)
        index_spilit = index2_max / index1_max
        for index1 in range(index1_max):
            cubic_point1 = cubic_point_proj[:, plane[0, 0]] + index1 * slope1
            for index2 in range(int(index1 * index_spilit), int(np.ceil((index1 + 1) * index_spilit))):
                cubic_point2 = cubic_point_proj[:, plane[1, 0]] + index2 * slope2
                slope3 = step * cal_slope(cubic_point1, cubic_point2)
                max_length3 = np.linalg.norm(cubic_point1 - cubic_point2, 2)
                if np.all(slope3==0):
                    index3_max=1
                else:
                    index3_max = int((max_length3 // step)+1)
                cubic_point3_list = [cubic_point1 + index3 * slope3 for index3 in range(index3_max)]
                cubic_point3_1_list_all = [min(max(int(index_point[1]),0),image_size_y-1) for index_point in cubic_point3_list]
                cubic_point3_0_list_all = [min(max(int(index_point[0]),0),image_size_x-1) for index_point in cubic_point3_list]


                Img[cubic_point3_1_list_all, cubic_point3_0_list_all, :] = -np.array(
                    [min(extent[1] *2 / L_max,1), min(extent[0] *2 / W_max,1), min(extent[2]* 2  / H_max,1)]) * 255
        # print('this plane is over')

    return Img


def camera_plot_type(camera_coor, camera_angle, epoch_index, scene_index, camera_index, vehicle_boudingbox):
    img_comp = cv2.imread("ImgPath//Carla_%s//Carla_Camera%s//%d.png" % (epoch_index, camera_index + 1, scene_index))#Download from the link: https://cloud.tsinghua.edu.cn/d/06eb2d3f54c7406b9e4d/
    focal = image_size_x / (2.0 * np.tan(Hfov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = focal
    K[1, 1] = focal
    K[0, 2] = image_size_x / 2.0
    K[1, 2] = image_size_y / 2.0
    for vehicle_boudingbox_piece in vehicle_boudingbox[::-1]:
        corner_point = np.zeros([3, 8])
        point_index = 0
        for z_bias in [-1, 1]:
            for (y_bias, x_bias) in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
                corner_point[:, point_index] = vehicle_boudingbox_piece['extent'] * np.array([x_bias, y_bias, z_bias])
                point_index += 1
        corner_point = np.dot(rotation_matrix(-vehicle_boudingbox_piece['rotation'] / 180 * np.pi), corner_point)
        corner_point += vehicle_boudingbox_piece['center'].reshape([3, 1])
        img_select = np.zeros([3, 8])
        for i in range(8):
            abs_vec = np.dot(rotation_matrix(camera_angle / 180 * np.pi - camera_index * np.pi / 2),
                             (corner_point[:, i].reshape([3]) - camera_coor).reshape([3, 1]))
            img_select[:, i] = camera_axis(abs_vec)[:, 0]  # np.dot(K, camera_axis(abs_vec))[:,0]
        img_comp = cubic_proj(img_comp.astype(np.int16), img_select, K, vehicle_boudingbox_piece['extent'])

    return img_comp





samplenum_each_epoch = [50, 72, 122, 62, 116, 56, 60, 43, 62, 57, 55, 59, 45, 62, 100, 42, 71, 48, 57, 62, 45, 67, 40, 56, 44, 54, 46, 52, 60, 47, 93, 65, 57, 57, 42, 68, 64, 43, 60, 43, 67, 60, 57, 74, 56, 48, 41, 54, 51, 59, 44, 45, 46, 47, 60, 61, 61, 54, 46, 67, 158, 61, 51, 93, 58, 45, 45, 58, 47, 56, 68, 45, 63, 67, 54, 63, 41, 58, 60, 78, 56, 49, 53, 42, 45, 40, 65, 67, 43, 57, 46, 62, 60, 44, 60, 64, 64, 56, 38, 42, 42, 52, 61, 40, 60, 55, 62, 51, 96, 39, 59, 45, 62, 69, 67, 44, 56, 55, 42, 62, 72, 68, 59, 45, 54, 45, 64, 65, 48, 70, 59, 49, 54, 41, 73, 61, 65, 65, 59, 59, 59, 65, 59, 47, 46, 55, 41, 66, 68, 55, 43, 84, 73, 46, 56, 59, 69, 44, 41, 65, 67, 45, 57, 55, 51, 45, 56, 61, 63, 47, 39, 44, 55, 49, 60, 74, 40, 64, 54, 46, 57, 63, 47, 76, 38, 64, 58, 60, 55, 66, 72, 79, 42, 62, 76, 47, 48, 47, 51, 40, 65, 63, 98, 52, 54, 63, 40, 41, 69, 48, 46, 51, 48, 69, 56, 51, 50, 63, 41, 45, 60, 45, 45, 58, 41, 57, 46, 78, 63, 55, 47, 78, 41, 42, 43, 51, 67, 55, 54, 103, 53, 45, 45, 39, 49, 55, 47, 51, 111, 65, 59, 58, 52, 42, 51, 49, 52, 68, 44, 52, 47, 38, 41, 68, 37, 53, 58, 45, 42, 54, 40, 52, 41, 46, 45, 61, 60, 57, 54, 62, 58, 49, 131, 50, 55, 64, 47, 39, 68, 63, 52, 60, 41, 44, 41, 66, 40, 48, 57, 44, 47, 42, 67, 46, 54, 43, 41, 58, 73, 47, 54, 113, 63, 68, 39, 66, 57, 50, 79, 47, 51, 64, 68, 62, 63, 57, 59, 53, 59, 60, 47, 48, 40, 53, 50, 57, 63, 47, 59, 78, 43, 58, 66, 71, 54, 61, 65, 57, 58, 65, 39, 52, 47, 54, 45, 57, 45, 54, 58, 57, 57, 55, 55, 59, 54, 62, 60, 51, 41, 62, 44, 67, 62, 62, 62, 71, 43, 44, 72, 137, 67, 44, 45, 67, 64, 49, 55, 63, 52, 46, 65, 48, 54, 65, 64, 62, 57, 52, 57, 43, 52, 56, 49, 74, 44, 76, 69, 59, 81, 66, 44, 59, 74, 63, 47, 94, 81, 64, 42, 68, 62, 71, 41, 65, 67, 64, 39, 57, 79, 57, 58, 49, 43, 50, 72, 59, 42, 103, 59, 45, 76, 44, 73, 75, 57, 63, 58, 70, 41, 51, 59, 53, 60, 56, 63, 60, 66, 49, 50, 43, 71, 57, 65, 57, 47, 66, 68, 49, 53, 41, 45, 54, 56, 59, 62, 47, 61, 42, 49, 42, 74, 67, 58, 49, 48, 55, 45, 55, 63, 46, 66, 100, 101, 42, 44, 66, 51, 64, 44, 41, 40, 61, 69, 43, 45, 59, 60, 55, 64, 67, 62, 54, 54, 65, 58, 66, 66, 42, 43, 61, 57, 50, 70, 56, 52, 45, 47, 56, 57, 60, 53, 58, 58, 44, 46, 58, 51, 45, 49, 55, 48, 47, 60, 46, 51, 61, 83, 56, 51, 43, 40, 53, 62, 58, 76, 43, 61, 44, 57, 42, 56, 44, 73, 57, 58, 45, 46, 51, 48, 61, 66, 70, 104, 50, 56, 62, 48, 43, 64, 44, 44, 49, 42, 84, 74, 59, 65, 42, 58, 55, 63, 44, 67, 47, 57, 63, 56, 58, 55, 61]


samplenum_each_camera_write = []
part_index=0
total_epoch=600
total_part=1
epoch_start =int(part_index * (total_epoch/total_part))
epoch_end = int((part_index+1) * (total_epoch/total_part))
dataset_flag = 'training'
scene_sample_num=int(np.sum(samplenum_each_epoch))
Img_Scene_all=np.zeros([int(np.sum(samplenum_each_epoch[epoch_start:epoch_end])),4,120,320,3],dtype=np.int16)

def camera_axis(vec):
    return np.array([vec[0],-vec[2],vec[1]])

def sumo_axis(vec):
    return np.array([vec[0],vec[2],-vec[1]])
label_pattern='(.*?) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+) ([-Ee0-9.]+)'

for camera_index in range(4):
    samplenum_each_epoch_write = []
    camera_bias_index = np.sum(samplenum_each_camera_write[0:camera_index])

    for epoch_index in enumerate(range(epoch_start, epoch_end)):
        index_list=range(0,samplenum_each_epoch[epoch_index[1]])
        scene_index=0

        for index in index_list:
            vehicles_onepiece_dic=[]
            dect_results = np.load('.//Results//Carla_%s//Camera_%s//%s.npy' % (epoch_index[1], int(camera_index + 1),int(index)))  # Download from the link: https://cloud.tsinghua.edu.cn/f/ee892ab93e624b1a91d7/
            for dect_vehicle_index in range(dect_results.shape[0]):
                h, w, l = dect_results[dect_vehicle_index, 3], dect_results[dect_vehicle_index, 2], dect_results[
                    dect_vehicle_index, 1]
                move_trans = np.array([dect_results[dect_vehicle_index, 4], dect_results[dect_vehicle_index, 5],
                                       dect_results[dect_vehicle_index, 6]])
                x, y, z = np.dot(rotation_matrix(camera_index * np.pi / 2), move_trans.reshape([3, 1])).reshape([3])
                rot_y = dect_results[dect_vehicle_index, 7] - np.pi / 2 - camera_index * np.pi / 2
                vehicle_center = np.array([x, y, z])
                vehicles_onepiece_dic.append({'type': None, 'id': None, 'center': vehicle_center,
                                          'extent': np.array([w / 2, l / 2, h / 2]),
                                          'rotation': (rot_y + np.pi / 2) / np.pi * 180})
            vehicle_boudingbox = []
            vehicle_dis = np.zeros([len(vehicles_onepiece_dic)])
            for vehicles_onepiece in enumerate(vehicles_onepiece_dic):
                vehicle_dis[vehicles_onepiece[0]] = np.linalg.norm(
                    vehicles_onepiece[1]['center'], 2)
            argindex = np.argsort(vehicle_dis)

            for argi in argindex:
                vehicles_onepiece = vehicles_onepiece_dic[argi]
                vehicle_boudingbox.append(vehicles_onepiece)
            for vehicle_boudingbox_piece in vehicle_boudingbox:
                print(vehicle_boudingbox_piece)
            img_with_boundingbox = camera_plot_type(0, 0, epoch_index[1],scene_index, camera_index, vehicle_boudingbox)
            imgread = cv2.resize(img_with_boundingbox, dsize=(320, 120))
            Img_Scene_all[int(np.sum(samplenum_each_epoch[epoch_start:epoch_index[1]])+scene_index),camera_index,:,:,:]=imgread
            # cv2.namedWindow('img%s'%(scene_index), 0)
            # cv2.resizeWindow('img%s'%(scene_index), 320, 120)
            # cv2.imshow('img%s'%(scene_index), imgread.astype(np.uint8))
            # cv2.waitKey()

            vehicles_onepiece_dic = []
            camera_coordinates = np.zeros([3])
            camera_rotation = 0
            print('Loaded Index',int(np.sum(samplenum_each_epoch[epoch_start:epoch_index[1]]) + scene_index))
            scene_index += 1
            target_vehicle_found = 0


np.save('SIF.npy',Img_Scene_all)