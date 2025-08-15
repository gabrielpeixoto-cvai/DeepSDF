from mesh_to_sdf import sample_sdf_near_surface

import trimesh
import pyrender
import numpy as np
import os
import sys
import tqdm


def compute_normalization_parameters(mesh: trimesh.Trimesh, buffer: float = 1.03):
    """
    Equivalent of the C++ ComputeNormalizationParameters function,
    but using trimesh instead of pangolin.

    Returns:
        translation (np.ndarray of shape (3,)): -center
        scale (float): 1 / max_distance (with buffer applied)
    """
    vertices = mesh.vertices  # shape: (num_vertices, 3)
    faces = mesh.faces  # shape: (num_faces, 3)

    num_vertices = vertices.shape[0]

    # Only consider vertices used in faces
    vertices_used = np.zeros(num_vertices, dtype=bool)
    vertices_used[faces.flatten()] = True

    used_vertices = vertices[vertices_used]

    # Compute min and max per axis
    x_min, y_min, z_min = used_vertices.min(axis=0)
    x_max, y_max, z_max = used_vertices.max(axis=0)

    # Compute center
    center = np.array(
        [(x_max + x_min) / 2.0, (y_max + y_min) / 2.0, (z_max + z_min) / 2.0],
        dtype=np.float32,
    )

    # Compute max distance from center
    dists = np.linalg.norm(used_vertices - center, axis=1)
    max_distance = dists.max()

    # Apply buffer
    max_distance *= buffer

    # Translation (negative center) and scale
    translation = -center
    scale = 1.0 / max_distance

    return translation, scale


source_folder = "/home/gabriel/phd_repos/DeepSDF/data/ShapeNetCore.v2/04256520/"
save_folder = "/home/gabriel/phd_repos/DeepSDF/data/SurfaceSamples/ShapeNetV2/04256520/"
normparsave_folder = (
    "/home/gabriel/phd_repos/DeepSDF/data/NormalizationParameters/ShapeNetV2/04256520/"
)
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
    savepath = os.path.join(save_folder, f"{folder}.ply")
    normparamsavepath = os.path.join(normparsave_folder, f"{folder}.npz")
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

    # 2. Sample points on the surface
    num_samples = 30000  # Number of points to sample
    sampled_points = mesh.sample(count=num_samples)

    # 3. Create a PointCloud object
    point_cloud = trimesh.points.PointCloud(sampled_points)
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    os.makedirs(os.path.dirname(normparsave_folder), exist_ok=True)

    offset, scale = compute_normalization_parameters(mesh=mesh)

    # 4. Save the PointCloud as a PLY file
    point_cloud.export(savepath)
    np.savez(normparamsavepath, offset=offset, scale=scale)

    print(f"Successfully sampled {num_samples} points and saved to {savepath}")
