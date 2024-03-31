import pandas as pd
import matplotlib.pyplot as plt

class PSM_analysis():
    def __init__(self) -> None:
        csv_file = "/Users/elio/Desktop/lookinup/PSMrawdata.csv"
        self.dataset = self.read_dataset(csv_file)
        # print(self.dataset)
        self.cheap_df = self.grouping_entries(dataset=self.dataset, column_name="安い",condition='>=')
        self.cheap_df = self.calculating_percentages(dataframe=self.cheap_df, column_name="安い",condition='>=')

        self.too_cheap_df = self.grouping_entries(dataset=self.dataset, column_name="安すぎる", condition='>=')
        self.too_cheap_df = self.calculating_percentages(dataframe=self.too_cheap_df, column_name="安すぎる", condition='>=')

        self.expensive_df = self.grouping_entries(dataset=self.dataset, column_name="高い", condition='<=')
        self.expensive_df = self.calculating_percentages(dataframe=self.expensive_df, column_name="高い", condition='<=')

        self.too_expensive_df = self.grouping_entries(dataset=self.dataset, column_name="高すぎる", condition='<=')
        self.too_expensive_df = self.calculating_percentages(dataframe=self.too_expensive_df, column_name="高すぎる", condition='<=')

        # self.graph = self.plotting_graph(dataframe=[self.cheap_df, self.too_cheap_df, self.expensive_df, self.too_expensive_df], label=["Cheap", "Too Cheap", "Expensive", "Too Expensive"])

        #Highest Price
        self.highest_price = self.intersection(dataframe1=self.too_expensive_df, dataframe2=self.cheap_df)
        #Compromise Price
        self.compromise_price = self.intersection(dataframe1=self.expensive_df, dataframe2=self.cheap_df)
        #Ideal Price
        self.ideal_price = self.intersection(dataframe1=self.too_expensive_df, dataframe2=self.too_cheap_df)
        #Lowest quality guaranteed price
        self.lowest_price = self.intersection(dataframe1=self.expensive_df, dataframe2=self.too_cheap_df)

        print("最高価格: ", round(self.highest_price, 0))
        print("理想価格: ", round(self.ideal_price, 0))
        print("妥協価格: ", round(self.compromise_price,0))
        print("最低品質保証価格: ", round(self.lowest_price, 0))


    def read_dataset(self, csv_file):
        dataset = pd.read_csv(csv_file)
        dataset.drop(columns="sample number", inplace=True)
        return dataset

    def grouping_entries(self, dataset, column_name, condition):
        count = {}
        ranges = list(range(50, 601, 50))
        for i in ranges:
            if condition == '>=':
                count[i] = dataset[dataset[column_name] >= i].shape[0]
            elif condition == '<=':
                count[i] = dataset[dataset[column_name] <= i].shape[0]
        return pd.DataFrame(list(count.items()), columns=['Subgroup', column_name+'('+condition+')'])

    def calculating_percentages(self, dataframe, column_name, condition):
        full_column_name = f"{column_name}({condition})"
        dataframe['Percentage'] = round((dataframe[full_column_name]/36) * 100, 1)
        return dataframe

    def plotting_graph(self, dataframe, label):
        plt.figure(figsize=(10, 7))
        plt.title('Percentage of Responses within Each Price Subgroup')
        plt.xlabel('Price Subgroups')
        plt.ylabel('Percentage of Responses (%)')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        for dataframe, label in zip(dataframe, label):
            plt.plot(dataframe['Subgroup'], dataframe['Percentage'], label=label, marker='o')
        plt.legend()
        return plt.show()
    
    #dataframe1 -> expensive ; dataframe2 -> cheap
    def intersection(self, dataframe1, dataframe2):
        compromise_df = pd.DataFrame({
            'Subgroup': dataframe1['Subgroup'],
            'Percentage_Expen': dataframe1['Percentage'],
            'Percentage_Cheap': dataframe2['Percentage']  
        })
        for i in range(len(compromise_df) - 1):
            if compromise_df['Percentage_Expen'].iloc[i] <= compromise_df['Percentage_Cheap'].iloc[i] and compromise_df['Percentage_Expen'].iloc[i + 1] > compromise_df['Percentage_Cheap'].iloc[i + 1]:
                lower_bound_idx = i
                upper_bound_idx = i+1
                break
        lower_bound = compromise_df['Subgroup'].iloc[lower_bound_idx]
        upper_bound = compromise_df['Subgroup'].iloc[upper_bound_idx]

        exp_lower = compromise_df['Percentage_Expen'].loc[lower_bound_idx]
        exp_upper = compromise_df['Percentage_Expen'].loc[upper_bound_idx]
        cheap_lower = compromise_df['Percentage_Cheap'].loc[lower_bound_idx]
        cheap_upper = compromise_df['Percentage_Cheap'].loc[upper_bound_idx]

        exact_intersection_subgroup = lower_bound + (upper_bound - lower_bound) * ((exp_lower - cheap_lower) / ((cheap_upper - cheap_lower) - (exp_upper - exp_lower)))

        return exact_intersection_subgroup
    
  
analysis = PSM_analysis()
analysis.__init__