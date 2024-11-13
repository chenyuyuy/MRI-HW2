import nibabel as nib
import numpy as np
import os
import pandas as pd

# Names and corresponding numbers of labeled regions
label_dict = {
    1: "Left-Thalamus-Proper",
    2: "Right-Thalamus-Proper",
    3: "Left-Caudate",
    4: "Right-Caudate",
    5: "Left-Putamen",
    6: "Right-Putamen",
    7: "Left-Pallidum",
    8: "Right-Pallidum",
    9: "Left-Hippocampus",
    10: "Right-Hippocampus",
    11: "Left-Amygdala",
    12: "Right-Amygdala"
}

# Folder containing NIfTI files
folder_path = r'C:\Users\Hikari20220126i712th\Downloads\IXI-T1\output'

# Create an empty DataFrame to store results
df = pd.DataFrame(columns=["File"] + list(label_dict.values()))

# Iterate over each .nii.gz file in the folder
rows = []  # To store data row for each file
for filename in os.listdir(folder_path):
    if filename.endswith('.nii.gz'):
        file_path = os.path.join(folder_path, filename)
        
        # Load the NIfTI file
        nii_img = nib.load(file_path)
        data = nii_img.get_fdata()

        # Calculate the voxel count for each label
        label_counts = {label: np.sum(data == label) for label in label_dict.keys()}

        # Calculate voxel volume
        voxel_volume = np.prod(nii_img.header.get_zooms()[:3])

        # Calculate the volume for each region and store it in a data row
        row = {"File": filename}
        for label, count in label_counts.items():
            row[label_dict[label]] = count * voxel_volume

        # Append row to the list
        rows.append(row)

# Combine all rows into the DataFrame
df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

# Output the results to an Excel file
output_path = r'C:\Users\Hikari20220126i712th\Downloads\IXI-T1\output\nii_volume_data.xlsx'
df.to_excel(output_path, index=False)
print(f"Excel file has been saved to: {output_path}")
