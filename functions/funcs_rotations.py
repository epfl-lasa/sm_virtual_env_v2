import numpy as np
from scipy.spatial.transform import Rotation
from scipy.spatial.transform import Rotation as R


def angle_between(v1, v2):
    # TODO modify such that it can deal with vectors or list of vectors (works currently but awfull)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)  # , axis=1
    cos_theta = dot_product / (norm_v1 * norm_v2)
    # cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    # return np.degrees(angle_rad)
    # Determine the sign of the angle using the cross product
    cross_product = np.cross(v2.T, v1)
    sign = np.sign(cross_product)
    signed_angle_rad = angle_rad * sign
    signed_angle_deg = np.degrees(signed_angle_rad)
    return signed_angle_deg


def compute_correct_angle(quat, vect=np.array((1, 0, 0))):
    quat = np.array(quat)
    rots = R.from_quat(quat.T)
    vect_rot = rots.as_matrix() @ vect
    if len(vect_rot.shape) == 1:
        vect_rot_theta = np.array([vect_rot[0], vect_rot[2]])
    else:
        vect_rot_theta = np.array([vect_rot[:, 0], vect_rot[:, 2]])
    vect_zero = np.array((0, -1))
    theta = angle_between(vect_zero, vect_rot_theta)
    return theta
