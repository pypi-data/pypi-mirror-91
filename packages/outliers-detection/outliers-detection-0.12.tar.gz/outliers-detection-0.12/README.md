It takes the dataframe and returns the outliers and other outliers related stats
 

Installation
pip install detect-outliers

How to use it?



This class will initialize Pandas Data frame
    
    from EdaFirstPhase.eda import EDA

    get_outliers_report() --> This method will print the outliers report
    
    from EdaFirstPhase.eda import EDA
    
    data = EDA(data="train_data","y",path = "/")
    
You need to pass data="train_data","y",path = "/"
    
