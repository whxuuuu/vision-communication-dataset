import numpy as np

rotation_matrix = lambda thetaz: np.array(
    [[np.cos(thetaz), -np.sin(thetaz), 0], [np.sin(thetaz), np.cos(thetaz), 0], [0, 0, 1]])

#Selected cubic grid region
x_min=2
x_max=15
y_min=-5
y_max=0
#length, width, and height of each grid
L_grid=6
W_grid=2
H_grid=1
def trans_orientation(theta):
   theta_norm = (theta + np.pi) % (2 * np.pi) - np.pi
   if theta_norm>=-np.pi/2 and theta_norm<=np.pi/2:
       return theta_norm
   else:
       return np.arcsin(-np.sin(theta_norm))

H_max=3.326848
W_max=3.250588
L_max=11.076664

def vehicle_distribution(VL,VW,VH,VR,Vcenter_ori):
    VBALA_fea = np.zeros([y_max - y_min + 1, x_max - x_min + 1, 6,7])
    VBALA_fea_num=np.zeros([y_max - y_min + 1, x_max - x_min + 1,7])
    VR_t=trans_orientation(VR/180*np.pi)
    Vcenter = np.array([Vcenter_ori[0] - BS_coordinates[0], Vcenter_ori[1] - BS_coordinates[1], Vcenter_ori[2]])
    X_index = Vcenter[0] // W_grid
    Y_index = Vcenter[1] // L_grid
    Z_index=int((VH/2)//H_grid)
    if X_index >= x_min and X_index <= x_max:
        if Y_index >= y_min and Y_index <= y_max:
            X_spatial = int(min(max(X_index, x_min), x_max) - x_min)
            Y_spatial = int(-min(max(Y_index, y_min), y_max) + y_max)
            grid_coor = [(X_spatial + x_min + 1) * W_grid - 1 * W_grid, (y_max - Y_spatial + 1) * L_grid - 1 * L_grid]
            grid_coie=(Vcenter[0]-grid_coor[0])/W_grid,(Vcenter[1]-grid_coor[1])/L_grid
            VBALA_fea[Y_spatial,X_spatial,Z_index,:]=np.array([grid_coie[0],grid_coie[1],(VH/2-Z_index*H_grid)/H_grid,VW/W_max,VL/L_max,VH/H_max,VR_t/2/np.pi])#Normalized sizes and locations coordinates. The azimuths in the paper are also normalized by the factor 2pi.
            VBALA_fea_num[Y_spatial,X_spatial,Z_index]=1
    return VBALA_fea,VBALA_fea_num


samplenum_each_initialization = [50, 72, 122, 62, 116, 56, 60, 43, 62, 57, 55, 59, 45, 62, 100, 42, 71, 48, 57, 62, 45, 67, 40, 56, 44, 54, 46, 52, 60, 47, 93, 65, 57, 57, 42, 68, 64, 43, 60, 43, 67, 60, 57, 74, 56, 48, 41, 54, 51, 59, 44, 45, 46, 47, 60, 61, 61, 54, 46, 67, 158, 61, 51, 93, 58, 45, 45, 58, 47, 56, 68, 45, 63, 67, 54, 63, 41, 58, 60, 78, 56, 49, 53, 42, 45, 40, 65, 67, 43, 57, 46, 62, 60, 44, 60, 64, 64, 56, 38, 42, 42, 52, 61, 40, 60, 55, 62, 51, 96, 39, 59, 45, 62, 69, 67, 44, 56, 55, 42, 62, 72, 68, 59, 45, 54, 45, 64, 65, 48, 70, 59, 49, 54, 41, 73, 61, 65, 65, 59, 59, 59, 65, 59, 47, 46, 55, 41, 66, 68, 55, 43, 84, 73, 46, 56, 59, 69, 44, 41, 65, 67, 45, 57, 55, 51, 45, 56, 61, 63, 47, 39, 44, 55, 49, 60, 74, 40, 64, 54, 46, 57, 63, 47, 76, 38, 64, 58, 60, 55, 66, 72, 79, 42, 62, 76, 47, 48, 47, 51, 40, 65, 63, 98, 52, 54, 63, 40, 41, 69, 48, 46, 51, 48, 69, 56, 51, 50, 63, 41, 45, 60, 45, 45, 58, 41, 57, 46, 78, 63, 55, 47, 78, 41, 42, 43, 51, 67, 55, 54, 103, 53, 45, 45, 39, 49, 55, 47, 51, 111, 65, 59, 58, 52, 42, 51, 49, 52, 68, 44, 52, 47, 38, 41, 68, 37, 53, 58, 45, 42, 54, 40, 52, 41, 46, 45, 61, 60, 57, 54, 62, 58, 49, 131, 50, 55, 64, 47, 39, 68, 63, 52, 60, 41, 44, 41, 66, 40, 48, 57, 44, 47, 42, 67, 46, 54, 43, 41, 58, 73, 47, 54, 113, 63, 68, 39, 66, 57, 50, 79, 47, 51, 64, 68, 62, 63, 57, 59, 53, 59, 60, 47, 48, 40, 53, 50, 57, 63, 47, 59, 78, 43, 58, 66, 71, 54, 61, 65, 57, 58, 65, 39, 52, 47, 54, 45, 57, 45, 54, 58, 57, 57, 55, 55, 59, 54, 62, 60, 51, 41, 62, 44, 67, 62, 62, 62, 71, 43, 44, 72, 137, 67, 44, 45, 67, 64, 49, 55, 63, 52, 46, 65, 48, 54, 65, 64, 62, 57, 52, 57, 43, 52, 56, 49, 74, 44, 76, 69, 59, 81, 66, 44, 59, 74, 63, 47, 94, 81, 64, 42, 68, 62, 71, 41, 65, 67, 64, 39, 57, 79, 57, 58, 49, 43, 50, 72, 59, 42, 103, 59, 45, 76, 44, 73, 75, 57, 63, 58, 70, 41, 51, 59, 53, 60, 56, 63, 60, 66, 49, 50, 43, 71, 57, 65, 57, 47, 66, 68, 49, 53, 41, 45, 54, 56, 59, 62, 47, 61, 42, 49, 42, 74, 67, 58, 49, 48, 55, 45, 55, 63, 46, 66, 100, 101, 42, 44, 66, 51, 64, 44, 41, 40, 61, 69, 43, 45, 59, 60, 55, 64, 67, 62, 54, 54, 65, 58, 66, 66, 42, 43, 61, 57, 50, 70, 56, 52, 45, 47, 56, 57, 60, 53, 58, 58, 44, 46, 58, 51, 45, 49, 55, 48, 47, 60, 46, 51, 61, 83, 56, 51, 43, 40, 53, 62, 58, 76, 43, 61, 44, 57, 42, 56, 44, 73, 57, 58, 45, 46, 51, 48, 61, 66, 70, 104, 50, 56, 62, 48, 43, 64, 44, 44, 49, 42, 84, 74, 59, 65, 42, 58, 55, 63, 44, 67, 47, 57, 63, 56, 58, 55, 61]

scene_sample_num=int(np.sum(samplenum_each_initialization))

camera_index = 0

init_start = 0
init_end = 600
BS_coordinates=np.array([8,-16,3])
VBALA_Scene_all=np.zeros([int(np.sum(samplenum_each_initialization[init_start:init_end])),y_max-y_min+1,x_max-x_min+1,6,7])

for init_index in enumerate(range(init_start, init_end)):
    MS_locations=np.load(".//Locations//Carla_Location_%s.npy"%(init_index[1]))#Download from the link: https://github.com/whxuuuu/vision-communication-dataset/blob/main/Locations.zip
    for scene_index in range(MS_locations.shape[0]):
        camera_coordinates=np.array([MS_locations[scene_index,0]+BS_coordinates[0],MS_locations[scene_index,1]+BS_coordinates[1],1.547088+0.5])
        vehicles_dic_dect = []
        for camera_index in range(4):
            dect_results=np.load('.//Results//Carla_%s//Camera_%s//%s.npy' % (init_index[1], int(camera_index + 1), int(scene_index)))#Download from the link: https://cloud.tsinghua.edu.cn/f/ee892ab93e624b1a91d7/
            for dect_vehicle_index in range(dect_results.shape[0]):
                h, w, l = dect_results[dect_vehicle_index,3],dect_results[dect_vehicle_index,2],dect_results[dect_vehicle_index,1]
                move_trans =np.array([dect_results[dect_vehicle_index,4],dect_results[dect_vehicle_index,5],dect_results[dect_vehicle_index,6]])
                x, y, z = np.dot(rotation_matrix(camera_index * np.pi / 2), move_trans.reshape([3, 1])).reshape([3])
                rot_y =dect_results[dect_vehicle_index,7]- np.pi / 2 - camera_index * np.pi / 2
                vehicle_center = np.array([x, y, z]) + camera_coordinates
                vehicles_dic_dect.append({'type': None, 'id': None, 'center': vehicle_center,
                                                   'extent': np.array([w / 2, l / 2, h / 2]),
                                                   'rotation': (rot_y + np.pi / 2) / np.pi * 180})


        vehicle_weight_all = 0
        vehicle_weight_num_all=0
        vehicle_num_sta = 0
        for vehicle_piece in vehicles_dic_dect:
            if vehicle_piece['extent'][2] * 2 > 1.6860366083047085:#1.547088+0.05+(3-1.547088-0.05)*(1.788678/2)/(15-1.788678/2=1.6860366083047085 is the height that can block the MS antenna in the BS coverage area
                vehicle_weight,vehicle_weight_num = vehicle_distribution(vehicle_piece['extent'][1] * 2,
                                                    vehicle_piece['extent'][0] * 2,
                                                    vehicle_piece['extent'][2] * 2,
                                                    vehicle_piece['rotation'],
                                                    vehicle_piece['center'])
                vehicle_weight_all += vehicle_weight
                vehicle_weight_num_all+=vehicle_weight_num
                vehicle_num_sta +=1

        #Calculate the average of each parameter for all vehicles in a grid
        for ii in range(vehicle_weight_all.shape[0]):
            for jj in range(vehicle_weight_all.shape[1]):
                for zz in range(vehicle_weight_all.shape[2]):
                    if vehicle_weight_num_all[ii,jj,zz]!=0:
                        vehicle_weight_all[ii,jj,zz,:]=vehicle_weight_all[ii,jj,zz,:]/vehicle_weight_num_all[ii,jj,zz]

        #Embed MS location information into cubic VDF
        X_index = camera_coordinates[0] // W_grid
        Y_index = camera_coordinates[1] // L_grid
        Z_index = int((camera_coordinates[2]-0.45)//H_grid)

        if X_index >= x_min and X_index <= x_max:
            if Y_index >= y_min and Y_index <= y_max:
                X_spatial = int(min(max(X_index, x_min), x_max) - x_min)
                Y_spatial = int(-min(max(Y_index, y_min), y_max) + y_max)
                grid_coor = [(X_spatial + x_min + 1) * W_grid - 1 * W_grid,
                             (y_max - Y_spatial + 1) * L_grid - 1 * L_grid]
                grid_coie = (camera_coordinates[0] - grid_coor[0]) / W_grid, (camera_coordinates[1] - grid_coor[1]) / L_grid
                vehicle_weight_all[Y_spatial, X_spatial, Z_index, :] = np.array(
                    [-grid_coie[0], -grid_coie[1], -((camera_coordinates[2]-0.45)- Z_index*H_grid)/H_grid, 0,0,0,0])

        VBALA_Scene_all[int(np.sum(samplenum_each_initialization[init_start:init_index[1]])+scene_index),:]=vehicle_weight_all.copy()
        print('Load:', init_index[1], scene_index)


np.save('.//Cubic_VDF.npy',VBALA_Scene_all)



