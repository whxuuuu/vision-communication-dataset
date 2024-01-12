# Computer Vision Aided mmWave Beam Alignment in V2X Communications

The dataset is released for the ***vision perception aided wireless communication***, such as the beam alignment task. The dataset is collected in the V2X communication scenario. The communication environment and vehicles are simulated in the CARLA, an autonomous driving simulation platform, to realize the vision information gathering, as Fig. R1 shows. This dataset includes four components: images, locations, 3D detection results and channels. Here is the detailed generation steps:
<div align=center>
<img width="710" alt="communication_environment" src="https://user-images.githubusercontent.com/77795139/180574989-53fc1151-6525-48b8-b2d9-74ae4453c368.PNG">
 </div align=center>
 <div align=center>
 <center>Fig. R1. The communication environment in CARLA.</center>
  </div align=center>
 
+ **Image Generation**:
The images are taken by the four cameras above the roof center of MS, as shown in Fig. R2. The heights of the four cameras are set to be $0.5\mathrm{m}$ higher than the roof of MS. The frame rate of all the cameras are set as 20. We repeat making the MS running through the RSU's coverage area under different traffic conditions for 600 times. For the $q$ th repetition, $q=1,2,\cdots,600$, the MS can obtain four images at each shooting moment to form an image set, and thereby collect an image set sequence $I_{q,r}$, $r=1,2,\cdots,S_q$, in the RSU's coverage area, where $S_q$ is the length of the image set sequence, $I_{q,r}=\lbrace V_{q,r,c}\ |\ c=1,2,3,4 \rbrace$ and $V_{q,r,c}$ is the image taken by the $c$ th camera with the azimuth $\frac{-\pi (c-1)}{2}$. The image $V_{q,r,c}$ is saved as the file: 'Images/Carla_{q-1}/Camera_{c}/{r-1}.png'.

<div align=center>
<img width="710" alt="MS_camera" src="https://user-images.githubusercontent.com/77795139/180578713-01cad0ee-3576-45c4-a502-9cb33d44912d.png">
</div align=center>
 <div align=center>
 <center>Fig. R2. The RSU coverage area.</center>
  </div align=center>
  
+ **Location Generation**:
For the moment of taking image set $I_{q,r}$, the MS's plane location coordinates $u_{q,r}\in\mathbb{R}^{2}$ relative to RSU are recorded. Specifically, we record the MS's location coordinates $u_{q,r}$, $r=1,2,\cdots,S_q$, to form a location matrix $U_q\in\mathbb{R}^{S_q\times 2}$, where the $r$ th row of $U_q$ is $u_{q,r}$, and save $U_q$ as the file: 'Locations/Carla_Location_{q-1}.npy'.

+ **3D Detection Result Generation**:
For the image $V_{q,r,c}$, we utilize the 3D detection technique to obtain the type, length, width, height, the center location coordinates and the azimuth of each vehicle contained in the image. The adopted 3D detection method is SMOKE (https://github.com/lzccccc/SMOKE). Then, we use the detected data about vehicle type/size/location/azimuth to generate a label matrix $L_{q,r,c}\in\mathbb{R}^{O_{q,r,c}\times 8}$, where each row of $L_{q,r,c}$ corresponds to a vehicle contained in $V_{q,r,c}$ and $O_{q,r,c}$ is the total number of vehicles contained in $V_{q,r,c}$. The eight elements of a row of $L_{q,r,c}$ are the type index, length, width, height, three-dimensional center location coordinates and azimuth of the corresponding vehicle, respectively. There are three vehicle types, including car type, van type and bus type, in the environment. The type indices for the car type, van type and bus type are set as 0, 1 and 2 respectively. The $L_{q,r,c}$ is saved as the file: 'Results/Carla_{q-1}/Camera_{c}/{r-1}.npy'.

+ **Channel Generation**:
The Wireless Insite, a ray tracing software, is used to simulate the channel, as Fig. R3 shows. For the moment of taking image set $I_{q,r}$, the whole environment in CARLA will be synchronized to Wireless Insite to produce the coresponding channel $H_{q,r}\in\mathbb{C}^{K\times N_\mathrm{U}\times N_{\mathrel{B}}}$, where $N_\mathrm{B}=64$ and $N_{\mathrel{U}}=64$ are the number of antennas of BS and MS respectively, and $K=16$ is the number of subcarriers. The channel sequence $H_{q,r}$, $r=1,2,\dots,S_q$, are formed as a matrix $R_q\in \mathbb{C}^{S_q\times K \times N_\mathrm{U}\times N_{\mathrel{B}}}$, where the $r$ th row of $R_q$ is $H_{q,r}$. The $R_q$ is saved as the file: 'Channels/Carla_Channel_{q-1}.npy'.
<div align=center>
<img width="710" alt="WI_simu" src="https://user-images.githubusercontent.com/77795139/180575140-c43e0387-0f0b-40b8-8b2b-ecfd01f1f30f.png">
</div align=center>
 <div align=center>
 <center>Fig. R3. The synchronization simulation in Wireless Insite.</center>
  </div align=center>

# Corrigendum and Addendum

We are frightfully sorry for few defective details about the proposed vision based beam alignment method. Specifically, due to the limitations of the adopted training steps for the deep neural networks (DNN), the obtained simulation results of both the proposed and compared beam alignment methods do not fully demonstrate their achievable performance. Thus, we slightly correct the design of the vehicle distribution feature (VDF). The vehicle locations are used to expand the VDF. The utilized maximum vehicle size in each grid is replace by the average vehicle size. Then, we modify the training approach and add some simulation results to enhance the persuasiveness. All the conclusions remain unchanged.

**Corrigendum**:
![fig1_00](https://github.com/whxuuuu/vision-communication-dataset/assets/77795139/72054766-e712-4c2f-89f5-8fa4c2a1546a)
<div align=center>
<center>Fig. R4. The diagram of the proposed VBALA.</center>
</div align=center>

Fig.~1 shows the diagram of the proposed vision based beam alignment when the MS location is available (VBALA). The maximum length $l_{\mathrm{max},g}$, width $w_{\mathrm{max},g}$ and height $h_{\mathrm{max},g}$ of the vehicles in $\bm{\mathcal{V}}_g$ should be replaced with the average length $l_{\mathrm{ave},g}$, width $w_{\mathrm{ave},g}$ and height $h_{\mathrm{ave},g}$ of the vehicles in $\bm{\mathcal{V}}_g$. Moreover, for the $g$th grid, we set a local coordinate system (LCS) with $\mathrm{X}_{\mathrm{L}}$-axis, $\mathrm{Y}_{\mathrm{L}}$-axis, and $\mathrm{Z}_{\mathrm{L}}$-axis, where the origin is the vertex $(i^{\mathrm{X}}_g L_{\mathrm{G}}, i^{\mathrm{Y}}_g W_{\mathrm{G}}, 0)$ and the $\mathrm{X}_{\mathrm{L}}-\mathrm{Y}_{\mathrm{L}}-\mathrm{Z}_{\mathrm{L}}$ axis is parallel to the $\mathrm{X}_{\mathrm{R}}-\mathrm{Y}_{\mathrm{R}}-\mathrm{Z}_{\mathrm{R}}$ axis. Thus, under the LCS of the $g$th grid, we obtain the average plane location coordinates
of the vehicles in $\bm{\mathcal{V}}_g$ as $(x_{\mathrm{L}}^{g},y_{\mathrm{L}}^g)$.

The VDF is defined as a $G\times 6$ dimensional matrix $\bm{F}\in \mathbb{R}^{G\times 6}$, and the $g$th row of $\bm{F}$ is set as $[\frac{l_{\mathrm{ave},g}}{L_{\mathrm{max}}}, \frac{w_{\mathrm{ave},g}}{W_{\mathrm{max}}}, \frac{h_{\mathrm{ave},g}}{H_{\mathrm{max}}}, \frac{\theta_{\mathrm{R}}^{g}}{2\pi},\frac{x_{\mathrm{L}}^{g}}{L_{\mathrm{G}}},\frac{y_{\mathrm{L}}^{g}}{W_{\mathrm{G}}}]$.

**Addendum**:
We modify the training approach to the usual mode with dataset shuffle at every epoch. Then, we obtain the corrected simulation results in Fig.~R5, Fig.~R6, Fig.~R7, and Fig.~R8, which corresponds to the Fig.~11, Fig.~12, Fig.~13, and Fig.~14, respectively in the paper. All the conclusions from Fig.~R6, the Fig.~R7, and Fig.~R8 are consistent with that from Fig.~12, Fig.~13, and Fig.~14 in the paper. For more details, please read the document: https://github.com/whxuuuu/vision-communication-dataset/blob/main/Corrigendum%20and%20Addendum%20to%20%E2%80%9CComputer%20Vision%20Aided%20mmWave%20Beam%20Alignment%20in%20V2X%20Communications%E2%80%9D.pdf.

![results1](https://github.com/whxuuuu/vision-communication-dataset/assets/77795139/ba0df752-d9ad-4b02-9ae8-8903503095e6)
<div align=center>
<center>Fig. R5-R7. The corrected simulation results.</center>
</div align=center>

