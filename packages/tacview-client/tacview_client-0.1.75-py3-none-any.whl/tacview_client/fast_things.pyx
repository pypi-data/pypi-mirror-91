from libc.math cimport sqrt
from libc.math cimport cos
from libc.math cimport radians

cpdef list get_cartesian_coord(float lat, float lon, float h):
    cdef float a = 6378137.0
    cdef float rf = 298.257223563

    cdef float lat_rad = radians(lat)
    cdef float lon_rad = radians(lon)
    cdef float N = sqrt(a / (1 - (1 - (1 - 1 / rf) ** 2) * (sin(lat_rad)) ** 2))
    cdef float X = (N + h) * cos(lat_rad) * cos(lon_rad)
    cdef float Y = (N + h) * cos(lat_rad) * sin(lon_rad)
    cdef float Z = ((1 - 1 / rf) ** 2 * N + h) * sin(lat_rad)
    return [X, Y, Z]


# cdef cy_cosine(np.ndarray[np.float64_t] x, np.ndarray[np.float64_t] y):
#     cdef double xx=0.0
#     cdef double yy=0.0
#     cdef double xy=0.0
#     cdef Py_ssize_t i
#     for i in range(len(x)):
#         xx+=x[i]*x[i]
#         yy+=y[i]*y[i]
#         xy+=x[i]*y[i]
#     return 1.0-xy/sqrt(xx*yy)

# def get_cartesian_coord(lat: float, lon: float, h: float) -> Sequence:
#     """Convert coords from geodesic to cartesian."""
#     a = 6378137.0
#     rf = 298.257223563
#     lat_rad = radians(lat)
#     lon_rad = radians(lon)
#     N = sqrt(a / (1 - (1 - (1 - 1 / rf) ** 2) * (sin(lat_rad)) ** 2))
#     X = (N + h) * cos(lat_rad) * cos(lon_rad)
#     Y = (N + h) * cos(lat_rad) * sin(lon_rad)
#     Z = ((1 - 1 / rf) ** 2 * N + h) * sin(lat_rad)
#     return X, Y, Z