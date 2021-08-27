# import streamlit as st
# import numpy as np
# import pandas as pd
# from data.create_data import create_table

# def app():
#     st.title('Data Stats')

#     st.write("This is a sample data stats in the mutliapp.")
#     st.write("See `apps/data_stats.py` to know how to use it.")

#     st.markdown("### Plot Data")
#     df = create_table()

#     st.line_chart(df)

import streamlit as st
import numpy as np
import pandas as pd
from sklearn import datasets

def app():
    st.title('Data')

    st.write("This is the `Data` page of the multi-page app.")

    st.write("The following is the DataFrame of the `iris` dataset.")

    iris = datasets.load_iris()
    X = pd.DataFrame(iris.data, columns = iris.feature_names)
    Y = pd.Series(iris.target, name = 'class')
    df = pd.concat([X,Y], axis=1)
    df['class'] = df['class'].map({0:"setosa", 1:"versicolor", 2:"virginica"})

    st.write(df)