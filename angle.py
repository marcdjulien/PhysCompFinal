import numpy as np
def three_point_angle(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return np.arccos( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

p1 = np.array([[0,0]])
p2 = np.array([[1,0]])
p3 = np.array([[2,1]])
print 180*three_point_angle(p3,p1,p2)/np.pi