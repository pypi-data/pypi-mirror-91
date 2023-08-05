from pysplines.bsplines import Bspline

el_size = 0.142#0.05
control_points_0 = [[9.1, -0.2], [9.1, 0.0]]


spline = Bspline(cv=control_points_0, degree=1, n=20)
spline.plot(linetype="x-")
