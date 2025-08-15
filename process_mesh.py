from mesh_to_sdf import sample_sdf_near_surface

import trimesh
import pyrender
import numpy as np
import os
import sys
import tqdm

source_folder = "/home/gabriel/phd_repos/DeepSDF/data/ShapeNetCore.v2/04256520/"
save_folder = "/home/gabriel/phd_repos/DeepSDF/data/SdfSamples/ShapeNetV2/04256520/"
folders = [
    name
    for name in os.listdir(source_folder)
    if os.path.isdir(os.path.join(source_folder, name))
]
print(folders)
skip_processed_files = True

for index in tqdm.tqdm(range(len(folders))):
    folder = folders[index]
    folderpath = os.path.join(source_folder, folder)
    modelpath = os.path.join(folderpath, "models")
    filepath = os.path.join(modelpath, f"model_normalized.obj")
    savepath = os.path.join(save_folder, f"{folder}.npz")
    if os.path.exists(filepath):
        print(f"Processing file: {filepath}")

    # skip already processed files
    if os.path.exists(savepath) and skip_processed_files:
        print(f"Skipping file: {savepath}")
        continue

    mesh = trimesh.load(filepath)

    # Convert to single mesh if it's a scene or list of meshes
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(mesh.dump())
    elif isinstance(mesh, list):
        mesh = trimesh.util.concatenate(mesh)

    points, sdf = sample_sdf_near_surface(mesh, number_of_points=500000)

    pos = []
    neg = []
    for point in range(len(points)):
        if sdf[point] < 0:
            for index in range(len(points[point])):
                neg.append(points[point][index])
            neg.append(sdf[point])
        else:
            for index in range(len(points[point])):
                pos.append(points[point][index])
            pos.append(sdf[point])

    # colors = np.zeros(points.shape)
    # colors[sdf < 0, 2] = 1
    # colors[sdf > 0, 0] = 1
    # cloud = pyrender.Mesh.from_points(points, colors=colors)
    # scene = pyrender.Scene()
    # scene.add(cloud)
    # viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)
    print(f"Saving file to: {savepath}")
    # Reshape like in C++: rows = len(pos) / 4, columns = 4
    pos_array = np.array(pos, dtype=np.float64).reshape(-1, 4)
    neg_array = np.array(neg, dtype=np.float64).reshape(-1, 4)

    np.savez(savepath, pos=pos_array, neg=neg_array)
