import nibabel as nib
import numpy as np
import os
import pandas as pd

# 標籤區域的名稱和對應的編號
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

# NIfTI 文件所在資料夾
folder_path = r'C:\Users\Hikari20220126i712th\Downloads\IXI-T1\output'

# 創建一個空的 DataFrame 來儲存結果
df = pd.DataFrame(columns=["File"] + list(label_dict.values()))

# 遍歷資料夾中的每個 .nii.gz 文件
rows = []  # 用於儲存每個文件的數據行
for filename in os.listdir(folder_path):
    if filename.endswith('.nii.gz'):
        file_path = os.path.join(folder_path, filename)
        
        # 加載 NIfTI 文件
        nii_img = nib.load(file_path)
        data = nii_img.get_fdata()

        # 計算每個標籤的體素數量
        label_counts = {label: np.sum(data == label) for label in label_dict.keys()}

        # 計算體素體積
        voxel_volume = np.prod(nii_img.header.get_zooms()[:3])

        # 計算每個區域的體積並儲存到一行數據中
        row = {"File": filename}
        for label, count in label_counts.items():
            row[label_dict[label]] = count * voxel_volume

        # 添加行到列表中
        rows.append(row)

# 將所有行合併到 DataFrame
df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

# 將結果輸出為 Excel 文件
output_path = r'C:\Users\Hikari20220126i712th\Downloads\IXI-T1\output\nii_volume_data.xlsx'
df.to_excel(output_path, index=False)
print(f"Excel 文件已保存到: {output_path}")
