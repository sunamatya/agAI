import numpy as np
import deepxde as dde
import tensorflow as tf
import matplotlib as plt
'''
Current backend is based on tensorflow
Article based on Deep and Physics-Informed Neural Networks as a Substitute for Finite Element Analysis
'''

#governing equation base on  Equation 5 (calculation of strain vector with input which is the displacement caused in 2 Dimension)
def pde(x, y):
    """Defines the governing PDE for the FEA simulation."""
    u, v = y[:, 0:1], y[:, 1:2] # displacement in x = u, dispacement in y = v

    # First-order derivatives
    du_x = dde.grad.jacobian(y, x, i=0, j=0)  # ∂u/∂x
    dv_y = dde.grad.jacobian(y, x, i=1, j=1)  # ∂v/∂y
    du_y = dde.grad.jacobian(y, x, i=0, j=1)  # ∂u/∂y
    dv_x = dde.grad.jacobian(y, x, i=1, j=0)  # ∂v/∂x

    # Strain components
    epsilon_x = du_x
    epsilon_y = dv_y
    gamma_xy = du_y + dv_x

    # Material properties
    #TODO: check from the dataset material
    E, nu = 0.21, 0.3 # these are the young's modulus and the poission's ratio

    #equation 4 for he material consecutive
    D = (E / (1 - nu ** 2)) * np.array([
        [1, nu, 0],
        [nu, 1, 0],
        [0, 0, (1 - nu) / 2],
    ])

    # Convert to TensorFlow tensor
    D = tf.convert_to_tensor(D, dtype=tf.float32)

    # Stress components using the constitutive relation
    sigma_x = D[0, 0] * epsilon_x + D[0, 1] * epsilon_y
    sigma_y = D[1, 0] * epsilon_x + D[1, 1] * epsilon_y
    tau_xy = D[2, 2] * gamma_xy

    # Convert to TensorFlow tensor
    sigma_x = tf.convert_to_tensor(sigma_x, dtype=tf.float32)
    sigma_y = tf.convert_to_tensor(sigma_y, dtype=tf.float32)
    tau_xy = tf.convert_to_tensor(tau_xy, dtype=tf.float32)

    # Checking if the plane stress problem where inertial fores are zero
    sigma_x_x = dde.grad.jacobian(sigma_x, x, i=0, j=0)  # ∂σ_x/∂x
    sigma_y_y = dde.grad.jacobian(sigma_y, x, i=0, j=1)  # ∂σ_x/∂y
    tau_xy_x = dde.grad.jacobian(tau_xy, x, i=0, j=0)
    tau_xy_y = dde.grad.jacobian(tau_xy, x, i=0, j=1)  # Fixed indexing

    print("tau_xy_y shape:", tau_xy_y.shape)  # Debugging line

    # External forces (body forces)
    # WE see that the intertial forces are maximum of 3000N and 300 N
    #TODO: check from the requirement to get this material
    bx, by = 0.0, 1.0

    # PDE system (equilibrium equations)
    eq1 = sigma_x_x + tau_xy_y + bx
    eq2 = tau_xy_x + sigma_y_y + by

    return [eq1, eq2]

#PDE is accurate, check for bx and by

# Define the computational domain
#TODO: this should come from the stl file, may be not, can use the original formulation
geom = dde.geometry.Rectangle([0, 0], [1, 1])  # Ensure x is 2D

# Initial boundary conditions
#TODO: check the boundry condition for the setup
def boundary(_, on_boundary):
    return on_boundary

def bc_traction(x, on_boundary):
    return on_boundary and (np.isclose(x[0], 1) or np.isclose(x[1], 0) or np.isclose(x[1], 0.5))
#https://www.youtube.com/watch?v=Nsf5bmI54oc
'''
Dirichlet boundry condition to make sure that the elements at boundary are equal to zero
'''
#This is equation 7 and 8 for the initial displcement boundary condition and traction boundary condition
#TODO: check how to import boundary condition from the initial setup
bc_u = dde.DirichletBC(geom, lambda x: 0, boundary, component=0)
bc_v = dde.DirichletBC(geom, lambda x: 0, boundary, component=1)
bc3 = dde.NeumannBC(geom, lambda x: [0, 0, 0], bc_traction)


# Create the PDE data
data = dde.data.PDE(
    geom, pde, [bc_u, bc_v, bc3], num_domain=256, num_boundary=64
)

# Define the neural network architecture
net = dde.maps.FNN([2] + [20] * 3 + [2], "tanh", "Glorot uniform")

# Create the model
model = dde.Model(data, net)

# Compile and train
model.compile("adam", lr=0.001)
losshistory, train_state = model.train(iterations=10000)

# Save and plot results
dde.saveplot(losshistory, train_state, issave=True, isplot=True)


# def test_metric(model, geom, pde_func, num_test=100):
#     """
#     Evaluates the model using test points sampled from the domain.
#
#     Args:
#         model: Trained deepxde model.
#         geom: The geometry domain of the problem.
#         pde_func: Function that defines the PDE residual (must accept x as input).
#         num_test: Number of test points to sample.
#
#     Returns:
#         Dictionary of test metrics.
#     """
#     # Sample test points in the domain
#     x_test = geom.random_points(num_test)
#
#     # Compute PDE residuals using the same function from training
#     pde_residuals = np.abs(pde_func(x_test, model))  # Pass model instead of y_pred
#     mse_pde = np.mean(pde_residuals**2)
#
#     return {"MSE_PDE": mse_pde}
#
# def pde(x, model):
#     """
#     Computes PDE residual using the trained model.
#
#     Args:
#         x: Input points (tensor or array).
#         model: Trained deepxde model.
#
#     Returns:
#         Residual of the PDE at input points.
#     """
#     # Convert x to TensorFlow tensor if needed
#     x_tf = dde.backend.tf.convert_to_tensor(x)
#
#     # Predict y using the model
#     y = model.net(x_tf)
#
#     # Compute derivatives symbolically
#     du_x = dde.grad.jacobian(y, x_tf, i=0, j=0)  # ∂u/∂x
#     du_y = dde.grad.jacobian(y, x_tf, i=0, j=1)  # ∂u/∂y
#
#     # PDE residual (example: Laplace equation Δu = 0)
#     residual = du_x + du_y  # Modify based on your PDE
#
#     return dde.backend.tf.math.abs(residual)
#
# # Example usage after training
# metrics = test_metric(model, geom, pde)
# print(metrics)