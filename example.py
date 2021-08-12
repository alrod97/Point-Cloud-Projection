import pygltflib
from plyfile import PlyData, PlyElement
from matplotlib import pyplot as plt
from scipy.spatial.transform import Rotation as R
import open3d as o3d
from main import project_pc
import numpy as np

plydata = PlyData.read('point_cloud.ply')

x = np.asarray(plydata.elements[0].data['x'])
y = np.asarray(plydata.elements[0].data['y'])
z = np.asarray(plydata.elements[0].data['z'])

green = np.asarray(plydata.elements[0].data['green'])
red = np.asarray(plydata.elements[0].data['red'])
blue = np.asarray(plydata.elements[0].data['blue'])

pc = np.zeros((x.shape[0], 3))
colors = np.zeros((x.shape[0], 3))


pc[:, 0] = x
pc[:, 1] = y
pc[:, 2] = z

colors[:, 0] = red
colors[:, 1] = green
colors[:, 2] = blue

T = np.array([-5.6, -2.3, -20])
#R = np.eye(3)
Rot = np.array([[0, -1, 0],
              [1, 0, 0],
              [0, 0, 1]])

f = 1000*3
s_x = 1
s_y = 1
s_theta = 0.5
theta_x = 2000
theta_y = 2000

p_pixel = project_pc(pc, Rot, T, f, s_x, s_y, s_theta, theta_x, theta_y)
p_pixel = p_pixel.astype(int)
# image
img = np.zeros((p_pixel[:, 1].max()+1, p_pixel[:, 0].max()+1, 3))

for index, cur_pixel in enumerate(p_pixel):
    img[cur_pixel[1], cur_pixel[0], 0] = red[index]
    img[cur_pixel[1], cur_pixel[0], 1] = green[index]
    img[cur_pixel[1], cur_pixel[0], 2] = blue[index]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pc)
pcd.colors = o3d.utility.Vector3dVector(colors/255)

#o3d.visualization.draw_geometries([pcd])



plt.imshow(img.astype(np.uint8))
plt.show()