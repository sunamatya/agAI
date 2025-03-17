import deepxde as dde
import numpy as np
import tensorflow as tf


# Define the PDE system
def pde(x, y):
    u, v = y[:, 0:1], y[:, 1:2]

    du_x = dde.grad.jacobian(y, x, i=0, j=0)
    dv_y = dde.grad.jacobian(y, x, i=1, j=1)
    du_y = dde.grad.jacobian(y, x, i=0, j=1)
    dv_x = dde.grad.jacobian(y, x, i=1, j=0)

    # Strain components
    epsilon_x = du_x
    epsilon_y = dv_y
    gamma_xy = du_y + dv_x

    # Stress components using the constitutive relation
    E, nu = 0.21, 0.3
    D = (E / (1 - nu ** 2)) * np.array([
        [1, nu, 0],
        [nu, 1, 0],
        [0, 0, (1 - nu) / 2],
    ])

    # Convert to TensorFlow tensor
    D = tf.convert_to_tensor(D, dtype=tf.float32)

    sigma_x = D[0, 0] * epsilon_x + D[0, 1] * epsilon_y
    sigma_y = D[1, 0] * epsilon_x + D[1, 1] * epsilon_y
    tau_xy = D[2, 2] * gamma_xy

    # Equilibrium equations
    sigma_x_x = dde.grad.jacobian(sigma_x, x, i=0, j=0)
    sigma_y_y = dde.grad.jacobian(sigma_y, x, i=1, j=1)
    tau_xy_x = dde.grad.jacobian(tau_xy, x, i=0, j=1)
    tau_xy_y = dde.grad.jacobian(tau_xy, x, i=1, j=0)



    bx, by = 0.0, 1.0
    eq1 = sigma_x_x + tau_xy_y + bx
    eq2 = tau_xy_x + sigma_y_y + by

    return [eq1, eq2]


# # Define the geometry
# geometry = dde.geometry.Rectangle([0, 0], [1, 0.5])
# Define the computational domain (2D)
geom = dde.geometry.Rectangle(xmin=[0, 0], xmax=[1, 1])
# Define boundary conditions
def boundary(x, on_boundary):
    return on_boundary

bc_u = dde.DirichletBC(geom, lambda x: 0, boundary, component=0)
bc_v = dde.DirichletBC(geom, lambda x: 0, boundary, component=1)

# Define the problem
data = dde.data.PDE(
    geom, pde, [bc_u, bc_v], num_domain=256, num_boundary=64, solution=None
)

# Define the neural network
net = dde.nn.FNN([2] + [50] * 3 + [2], "tanh", "Glorot uniform")

# Create the model
model = dde.Model(data, net)

# Compile and train
model.compile("adam", lr=0.001)
losshistory, train_state = model.train(epochs=5000)

# Plot results
dde.saveplot(losshistory, train_state, issave=True, isplot=True)
# # Define boundary conditions
# def bc_displacement(x, on_boundary):
#     return on_boundary and np.isclose(x[0], 0)
#
#
# def bc_traction(x, on_boundary):
#     return on_boundary and (np.isclose(x[0], 1) or np.isclose(x[1], 0) or np.isclose(x[1], 0.5))
#
#
# bc1 = dde.DirichletBC(geometry, lambda x: [0, 0], bc_displacement, component=0)
# bc2 = dde.DirichletBC(geometry, lambda x: [0, 0], bc_displacement, component=1)
# bc3 = dde.NeumannBC(geometry, lambda x: [0, 0, 0], bc_traction)
#
# # Define the PINN model
# data = dde.data.PDE(geometry, pde, [bc1, bc2, bc3], num_domain=10000, num_boundary=2000)
#
# # Define the neural network architecture
# layer_size = [2] + [64] * 3 + [2]
# activation = "tanh"
# initializer = "Glorot uniform"
# net = dde.nn.FNN(layer_size, activation, initializer)
#
# # Define the model
# model = dde.Model(data, net)
#
# # Compile and train the model
# model.compile("adam", lr=0.001)
# loss_history, train_state = model.train(epochs=100000, callbacks=[dde.callbacks.EarlyStopping(patience=10000)])
#
# # Save and evaluate the model
# model.save("pinn_cantilever_plate")
