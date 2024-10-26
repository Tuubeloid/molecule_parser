import numpy as np

def parse_xyz_data(xyz_data):
    """Parse the pasted .xyz data and return a list of atom data (type, x, y, z)."""
    atoms = []
    lines = xyz_data.strip().split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue  # Skip malformed lines
        atom_type = parts[0]
        x, y, z = map(float, parts[1:4])
        atoms.append((atom_type, np.array([x, y, z])))
    return atoms

def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two 3D points."""
    return np.linalg.norm(point2 - point1)

def normalize(vector):
    """Normalize a 3D vector."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def determine_bond_threshold(atom_type1, atom_type2):
    """Determine the bond threshold based on atom types."""
    # Default bond threshold for common covalent bonds
    default_threshold = 1.6
    # Increase threshold for phosphorus-oxygen bonds
    if (atom_type1 == 'P' and atom_type2 == 'O') or (atom_type1 == 'O' and atom_type2 == 'P'):
        return 1.8  # Increase threshold for P-O bond
    return default_threshold

def generate_map_content(atoms):
    """Generate the ray tracer map content based on atom positions."""
    content = []

    # Write ambient light, camera, and light information
    content.append("A 0.2 255,255,255")
    content.append("C -50.0,0.0,20.0 0.0,0.0,1.0 70")
    content.append("L -40.0,50.0,0.0 0.6 10,0,255")

    # Write spheres for each atom
    sphere_radius = 1.0  # Default sphere radius, can be adjusted
    for atom_type, position in atoms:
        r, g, b = (255, 255, 255)  # Default color for spheres
        if atom_type == 'C':
            r, g, b = (128, 128, 128)  # Carbon: grey
        elif atom_type == 'N':
            r, g, b = (0, 0, 255)       # Nitrogen: blue
        elif atom_type == 'O':
            r, g, b = (255, 0, 0)      # Oxygen: red
        elif atom_type == 'H':
            r, g, b = (255, 255, 255)  # Hydrogen: white
        elif atom_type == 'P':
            r, g, b = (255, 165, 0)    # Phosphorus: orange
        content.append(f"sp {position[0]:.4f},{position[1]:.4f},{position[2]:.4f} {sphere_radius*1:.2f} {r},{g},{b}")

    # Write cylinders for bonds between atoms based on distance thresholds
    cylinder_radius = 0.2  # Default cylinder radius
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            atom_type1, position1 = atoms[i]
            atom_type2, position2 = atoms[j]
            distance = calculate_distance(position1, position2)

            # Determine the bond threshold based on the atom types
            bond_threshold = determine_bond_threshold(atom_type1, atom_type2)
            if distance < bond_threshold:
                # Create a cylinder only if the atoms are within the bond threshold
                center = (position1 + position2) / 2
                height = distance
                direction = normalize(position2 - position1)

                # Default color for cylinders
                r, g, b = (200, 200, 200)
                content.append(f"cy {center[0]:.4f},{center[1]:.4f},{center[2]:.4f} "
                               f"{direction[0]:.4f},{direction[1]:.4f},{direction[2]:.4f} "
                               f"{cylinder_radius * 2:.2f} {height:.2f} {r},{g},{b}")

    # Join the content into a single string
    return "\n".join(content)

# Example usage:
xyz_data = """C         -0.95200        0.65960       -0.65320
C         -0.56930       -0.80850       -0.88900
C         -0.91730        0.42510        0.86370
C         -0.53460       -1.04310        0.62790
C          0.53460        1.04310       -0.62790
C          0.91730       -0.42510       -0.86360
C          0.56920        0.80840        0.88890
C          0.95190       -0.65960        0.65320
H         -1.72680        1.19660       -1.18500
H         -1.03260       -1.46660       -1.61270
H         -1.66390        0.77120        1.56680
H          0.96980        1.89210       -1.13910
H          1.66390       -0.77120       -1.56670
H         -0.96980       -1.89210        1.13900
H          1.72680       -1.19660        1.18500
H          1.03260        1.46650        1.61260"""

# Parse the pasted .xyz data
atoms = parse_xyz_data(xyz_data)

# Generate map content
map_content = generate_map_content(atoms)

# Output the generated map content
if map_content:
    print(map_content)
else:
    print("No map content was generated. Please check the input data.")
