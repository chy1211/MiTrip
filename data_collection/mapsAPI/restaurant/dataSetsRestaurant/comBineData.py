import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
from glob import glob
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


# 讀取檔案
def read_csv(file):
    df = pd.read_csv(file, encoding="utf-8")
    return df


# 指定要列出所有檔案的目錄 並僅列出字節數為>2的檔案
files = glob("E:\\temp\\code\\data\\result\\googlemap_restaurant_*.csv")
ckecked_files = []
for f in files:
    if os.path.getsize(f) > 2:
        ckecked_files.append(f)

# 使用多線程讀取檔案
dfs = []
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = []
    for f in ckecked_files:
        futures.append(executor.submit(read_csv, f))
    for future in tqdm(futures):
        dfs.append(future.result())
merge_df = pd.concat(dfs, ignore_index=False)

# 依照id列出重複的資料之欄位"name"與"place_id" 並列出每筆資料的重複數量
print("重複數量：", merge_df[merge_df.duplicated(subset=["place_id"], keep=False)].shape)
print(
    merge_df[merge_df.duplicated(subset=["place_id"], keep=False)][["name", "place_id"]]
)
print(
    merge_df[merge_df.duplicated(subset=["place_id"], keep=False)][["name", "place_id"]]
    .groupby("place_id")
    .count()
    .sort_values(by="name", ascending=False)
)

# 依照place_id去重複
print("去重複前：", merge_df.shape)
merge_df = merge_df.drop_duplicates(subset=["place_id"], keep="first")
print("去重複後：", merge_df.shape)

# 輸出成csv
merge_df.to_csv(
    f"{DATA_DIR}/googlemap_restaurant.csv", encoding="utf-8-sig", index=False
)
