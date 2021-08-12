import numpy as np

def project_pc(pc, R, T, f, s_x, s_y, s_theta, theta_x, theta_y):
    # convert 3D pc to homogeneus coordinates and transpose it
    # pc_homog is then a 3xN matrix
    pc_homog = np.hstack((pc, np.ones((pc.shape[0], 1)))).T
    persp_proj = np.eye(3, 4)

    # se matrix containing rotation and tranlation of the camera (element of the special euclidean group)
    se = np.zeros((4, 4))
    se[:3, :3] = R
    se[-1,-1] = 1
    se[:3, -1] = -T # careful: T is the camera position in the origin frame, this is why we add a minus

    # Construct intrinsic parameter matrix K
    K = np.zeros((3, 3))
    K[0, 0] = f * s_x
    K[0, 1] = f * s_theta
    K[1, 1] = f * s_y
    K[0, 2] = theta_x
    K[1, 2] = theta_y
    K[2, 2] = 1

    K_all = K @ persp_proj @ se

    # get depths of points w.r.t camera
    pc_cam_frame = se @ pc_homog
    depths = pc_cam_frame[2, :]

    # project point clooud onto pixel coordinates of the image
    pc_pixel = (K_all @ pc_homog)/depths

    return np.rint(pc_pixel)[0:2, :].T


