#!/jdfssz1/ST_HEALTH/P20Z10200N0206/ouyangkang/software/miniconda3/bin/python
import pandas as pd
import sys
import os
import re

print("#################### Start processing data ####################")

# for flexibly processing
raw_file_name = sys.argv[1]
clean_file_name = sys.argv[2]
file_location = sys.argv[3]

# read raw data
with open(raw_file_name, 'r') as rf:
    raw_data = rf.readlines()

# define a function to find total number of raw data
def find_total(file):
    with open(file, 'r') as f:
        _data = f.readlines()
    return int(_data[3].split('\t')[1].strip('\n'))

# get information
df_1 = pd.DataFrame(columns=['Sample', 'Path', 'Raw_Size(GB)'])
n = 0
for row in raw_data:
    sample_name = row.split('\t')[0] # sample name
    # print(sample_name)

    dir_path = '/'.join(row.split('\t')[-1].split('/')[0:-1]) # path
    # print(dir_path)

    files = os.listdir(dir_path)
    # print(files)
    pattern = re.compile(r".*report$")

    for i in files:
        if re.match(pattern, i) != None:
            file = re.match(pattern, i).group()

    total_num = round(find_total(dir_path + '/' + file)/1000000000, 2) # raw_data size (GB)
    df_1.loc[n] = [sample_name, dir_path, total_num]
    n += 1

df_2 = pd.DataFrame(columns=['Sample', 'R1_Clean_Size(GB)', 'R1_AVG'])
df_3 = pd.DataFrame(columns=['Sample', 'R2_Clean_Size(GB)', 'R2_AVG'])
m = 0
k = 0
with open(clean_file_name, 'r') as f:
    clean_data = f.readlines()
    for line in clean_data:
        if 'cleanreads_r1' in line:
            sample = line.split('\t')[0].split('/')[-2]
            # print(sample)
            # print(line.split('  '))
            r1_size = round(int(''.join(line.split('  ')[4].split(',')))/1000000000, 2)
            # print(r1_size)
            r1_avg = str(line.split('  ')[-4])
            # print(r1_avg)
            df_2.loc[m] = [sample, r1_size, r1_avg]
            m += 1
        else:
            sample = line.split('\t')[0].split('/')[-2]
            r2_size = round(int(''.join(line.split('  ')[4].split(',')))/1000000000, 2)
            r2_avg = str(line.split('  ')[-4])
            df_3.loc[k] = [sample, r2_size, r2_avg]
            k += 1

df_4 = pd.merge(df_2, df_3, on='Sample')
df_4['Clean_Size(GB)'] = df_4['R2_Clean_Size(GB)'] + df_4['R1_Clean_Size(GB)']

df_5 = pd.merge(df_4, df_1, on='Sample')
df_5['Ratio'] = round(df_5['Clean_Size(GB)']/df_5['Raw_Size(GB)'] , 2)

df_5[['Sample', 'Path', 'Raw_Size(GB)', 'Clean_Size(GB)', 'Ratio', 'R1_AVG', 'R2_AVG']].to_csv(file_location, index=None)

print("#################### End processing data ####################")
