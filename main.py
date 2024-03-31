import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

scv_file = "/Users/elio/Desktop/lookinup/PSMrawdata.csv"

dataset = pd.read_csv(scv_file)
dataset.drop(columns="sample number", inplace=True)
# print(dataset.head)

totalLength = len(dataset)

ranges = list(range(50, 601, 50))
#counting cheap (>=)
cheap_count = {}
for i in ranges:
    cheap_count[i] = dataset[dataset['安い'] >= i].shape[0]
counts_df = pd.DataFrame(list(cheap_count.items()), columns=['Subgroup', '安い(>=)'])
counts_df['Percentage'] = round((counts_df['安い(>=)']/36)*100, 1)

#Counting too cheap (>=)
too_cheap_count = {}
for i in ranges:
    too_cheap_count[i] = dataset[dataset['安すぎる'] >= i].shape[0]
tcounts_df = pd.DataFrame(list(too_cheap_count.items()), columns=['Subgroup', '安すぎる(>=)'])
tcounts_df['Percentage'] = round((tcounts_df['安すぎる(>=)']/36)*100, 1)

#Counting expensive (<=)
expensive_count = {}
for i in ranges:
    expensive_count[i] = dataset[dataset['高い'] <= i].shape[0]
exp_data = pd.DataFrame(list(expensive_count.items()), columns=['Subgroup', '高い(<=)'])
exp_data['Percentage'] = round((exp_data['高い(<=)']/36)*100, 1)

#Counting too expensive (<=)
too_exp_count = {}
for i in ranges:
    too_exp_count[i] = dataset[dataset['高すぎる'] <= i].shape[0]
too_exp_data = pd.DataFrame(list(too_exp_count.items()), columns=['Subgroup', '高すぎる(<=)'])
too_exp_data['Percentage'] = round((too_exp_data['高すぎる(<=)']/36)*100, 1)

# print(counts_df)

#plot -> Graph
plt.figure(figsize=(10, 7))
plt.title('Percentage of Responses within Each Price Subgroup')
plt.xlabel('Price Subgroups')
plt.ylabel('Percentage of Responses (%)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

#Plotting values
plt.plot(counts_df['Subgroup'], counts_df['Percentage'], label="Cheap", marker='o')
plt.plot(tcounts_df['Subgroup'], tcounts_df['Percentage'], label="Too Cheap", marker='o')
plt.plot(exp_data['Subgroup'], exp_data['Percentage'], label="Expensive", marker='o')
plt.plot(too_exp_data['Subgroup'], too_exp_data['Percentage'], label="Too Expensive", marker='o')

plt.legend()
# plt.show() 

#Intersection

#a. Compromise Price
compromise_df = pd.DataFrame({
    'Subgroup': counts_df['Subgroup'],
    'Percentage_Expensive': exp_data['Percentage'],
    'Percentage_Cheap': counts_df['Percentage']
})
# print(compromise_df)

# Finding the precise intersection when it's not exactly on a predefined subgroup

# Identifying the brackets (subgroup ranges) where the intersection might lie
for i in range(len(compromise_df) - 1):
    if compromise_df['Percentage_Expensive'].iloc[i] <= compromise_df['Percentage_Cheap'].iloc[i] and compromise_df['Percentage_Expensive'].iloc[i + 1] > compromise_df['Percentage_Cheap'].iloc[i + 1]:
        lower_bound_idx = i
        upper_bound_idx = i+1
        break

# Linear interpolation to find the exact intersection point
# Formula: x = x1 + (x2 - x1) * ((y - y1) / (y2 - y1))
# Where (x1, y1) and (x2, y2) are points on the line, and y is the known value we're solving for x
# We know the y values are equal at the intersection, so we can simplify this to finding when House and Land percentages are equal

# Extracting the relevant percentages
lower_bound = compromise_df['Subgroup'].iloc[lower_bound_idx]
upper_bound = compromise_df['Subgroup'].iloc[upper_bound_idx]

house_lower = compromise_df['Percentage_Expensive'].loc[lower_bound_idx]
house_upper = compromise_df['Percentage_Expensive'].loc[upper_bound_idx]
land_lower = compromise_df['Percentage_Cheap'].loc[lower_bound_idx]
land_upper = compromise_df['Percentage_Cheap'].loc[upper_bound_idx]

# Assuming linear progression between points, solve for the exact subgroup where House = Land
exact_intersection_subgroup = lower_bound + (upper_bound - lower_bound) * ((house_lower - land_lower) / ((land_upper - land_lower) - (house_upper - house_lower)))

# Interpolating to get the percentage at this exact intersection
exact_intersection_percentage = np.interp(exact_intersection_subgroup, [lower_bound, upper_bound], [house_lower, house_upper])

print("Compromise Price: ",exact_intersection_subgroup)
