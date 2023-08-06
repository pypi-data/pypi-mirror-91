import pandas as pd
import numpy as np
from IPython.display import display


class EDA:
    """
    This class will initialize Pandas Data frame

    Attributes:
        data    : Pandas Dataframe.
        target  : Target Feature String
        path    : Output Destiantion

    """

    def __init__(self, data, target, path):
        self.data = data
        self.target = target

        self.num_vars = [key for key in dict(data.dtypes) if dict(data.dtypes)[key]
                         in ['float64', 'float32', 'int32', 'int64'] and key != target]
        self.path = path

    def get_outliers_report(self):
        low_data = []
        high_data = []
        low_val = []
        high_val = []
        med_val = []
        name_list = []
        for item in self.num_vars:
            median_item = round(self.data[item][self.data[item].notnull()].median(), 2)
            q1_item = round(self.data[item][self.data[item].notnull()].quantile(0.25), 2)
            q3_item = round(self.data[item][self.data[item].notnull()].quantile(0.75), 2)
            iqr_item = q3_item - q1_item
            high_item = q3_item + 1.5 * iqr_item
            low_item = q1_item - 1.5 * iqr_item
            low_nos = np.sum(self.data[item][self.data[item].notnull()] < low_item)
            high_nos = np.sum(self.data[item][self.data[item].notnull()] > high_item)
            med_val.append(median_item)
            low_val.append(q1_item)
            high_val.append(q3_item)
            low_data.append(low_nos)
            high_data.append(high_nos)
            name_list.append(item)
        data_dict = {'Feature_Name': name_list, 'Median': med_val, 'Q1_Value': low_val, 'Q3_Value': high_val,
                     'Left_Outlier_Nos': low_data, 'Right_Outlier_Nos': high_data}

        data_outlier = pd.DataFrame(data_dict,
                                    columns=['Feature_Name', 'Median', 'Q1_Value',
                                             'Q3_Value', 'Left_Outlier_Nos', 'Right_Outlier_Nos'])

        display(data_outlier)
