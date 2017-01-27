import numpy as np
from skimage import transform, exposure
import random
import matplotlib.image as mpimg
import warnings
import os


# Cameras we will use
cameras = ['left', 'center', 'right']
cameras_steering_correction = [0.2, 0., -0.2]

def preprocess(image):
    top = int((60 / 160) * image.shape[0])
    bottom = int((20 / 160) * image.shape[0])
    image = image[top:-bottom, :]
    image = transform.resize(image, (66, 200, 3))
    # with warnings.catch_warnings():
    #     warnings.simplefilter("ignore")
    #     image = exposure.equalize_hist(image)
    return image - 0.5

def generate_samples(data, root_path):
    while 1:
        # Generate random batch of indices
        indices = np.random.permutation(data.count()[0])
        batch_size = 128
        for batch in range(0, len(indices), batch_size):
            batch_indices = indices[batch:(batch + batch_size)]
            # Output arrays
            x = np.empty([0, 66, 200, 3], dtype=np.float32)
            y = np.empty([0], dtype=np.float32)
            # Read in and preprocess a batch of images
            for i in batch_indices:
                # Randomly select camera
                #camera = np.random.choice(len(cameras), p=[.25, .5, .25])
                camera = np.random.randint(len(cameras))
                # Read and preprocess image + steering angle
                image = mpimg.imread(os.path.join(root_path, data[cameras[camera]].values[i].strip()))
                angle = data.steering.values[i] + cameras_steering_correction[camera]
                # Append to batch
                x = np.append(x, [preprocess(image)], axis=0)
                y = np.append(y, [angle])
            # Randomly flip half of images in the batch
            flip_indices = random.sample(range(x.shape[0]), int(x.shape[0] / 2))
            x[flip_indices] = x[flip_indices, :, ::-1, :]
            y[flip_indices] = -y[flip_indices]
            yield (x, y)
