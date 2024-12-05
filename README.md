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
For the image $V_{q,r,c}$, we utilize the 3D detection technique to obtain the type, length, width, height, the center location coordinates and the azimuth of each vehicle contained in the image. The adopted 3D detection method is [SMOKE](https://github.com/lzccccc/SMOKE). We use the detected data about vehicle type/size/location/azimuth to generate a label matrix $L_{q,r,c}\in\mathbb{R}^{O_{q,r,c}\times 8}$, where each row of $L_{q,r,c}$ corresponds to a vehicle contained in $V_{q,r,c}$ and $O_{q,r,c}$ is the total number of vehicles contained in $V_{q,r,c}$. The eight elements of a row of $L_{q,r,c}$ are the type index, length, width, height, three-dimensional center location coordinates and azimuth of the corresponding vehicle, respectively. There are three vehicle types, including car type, van type and bus type, in the environment. The type indices for the car type, van type and bus type are set as 0, 1 and 2 respectively. The $L_{q,r,c}$ is saved as the file: 'Results/Carla_{q-1}/Camera_{c}/{r-1}.npy'.

+ **Channel Generation**:
The Wireless Insite, a ray tracing software, is used to simulate the channel, as Fig. R3 shows. For the moment of taking image set $I_{q,r}$, the whole environment in CARLA will be synchronized to Wireless Insite to produce the coresponding channel $H_{q,r}\in\mathbb{C}^{K\times N_\mathrm{U}\times N_{\mathrel{B}}}$, where $N_\mathrm{B}=64$ and $N_{\mathrel{U}}=64$ are the number of antennas of BS and MS respectively, and $K=16$ is the number of subcarriers. The channel sequence $H_{q,r}$, $r=1,2,\dots,S_q$, are formed as a matrix $R_q\in \mathbb{C}^{S_q\times K \times N_\mathrm{U}\times N_{\mathrel{B}}}$, where the $r$ th row of $R_q$ is $H_{q,r}$. The $R_q$ is saved as the file: 'Channels/Carla_Channel_{q-1}.npy'.
<div align=center>
<img width="710" alt="WI_simu" src="https://user-images.githubusercontent.com/77795139/180575140-c43e0387-0f0b-40b8-8b2b-ecfd01f1f30f.png">
</div align=center>
 <div align=center>
 <center>Fig. R3. The synchronization simulation in Wireless Insite.</center>
  </div align=center>
