import magpylib as mag
import numpy as np

#Hollow Cylinder
def get_hollow_cylinder(r_in, r_out, h, B_z, location,grid_size = 0.0001,grid = True  ):

    outer_cyl = mag.magnet.Cylinder(
        polarization=(0,0,B_z),
        dimension=(r_out * 2, h) 
    )
    inner_cyl = mag.magnet.Cylinder(
        polarization=(0, 0, -B_z),
        dimension=(r_in * 2, h)
    )

    full_cyl = mag.Collection(outer_cyl, inner_cyl)
    full_cyl.move(location)

    if grid:
        dis_x,dis_y,dis_z = location
        xs = np.arange(dis_x - r_out, dis_x + r_out + grid_size, grid_size)
        ys = np.arange(dis_y - r_out, dis_y + r_out + grid_size, grid_size)
        zs = np.arange(dis_z - h, dis_z + h + grid_size, grid_size)
        X, Y, Z = np.meshgrid(xs, ys, zs)
        positions = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T

        r_sq = (positions[:, 0] - dis_x)**2 + (positions[:, 1]-dis_y)**2
        mask = (r_sq >= r_in**2) & (r_sq <= r_out**2)
        valid_positions = positions[mask]

        mu_0 = 4 * np.pi * 1e-7
        M_z_Am = B_z / mu_0            
        dV_m3 = grid_size**3             
        magt = M_z_Am * dV_m3

        return full_cyl, valid_positions, magt

    return full_cyl