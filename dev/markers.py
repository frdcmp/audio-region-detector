import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import GridUpdateMode, DataReturnMode
import pandas as pd

vpth = "./"  # path that contains the csv file
csvfl = "markers.csv"  # I used a small csv file containing 2 columns: Name & Amt
tdf = pd.read_csv(vpth + csvfl)  # load csv into dataframe

gb = GridOptionsBuilder.from_dataframe(tdf)
gb.configure_column("Name", header_name=("F Name"), editable=True)
gb.configure_column("Amt", header_name=("Amount"), editable=True, type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0)

gridOptions = gb.build()
dta = AgGrid(
    tdf,
    gridOptions=gridOptions,
    reload_data=False,
    height=200,
    editable=True,
    theme="streamlit",
    data_return_mode=DataReturnMode.AS_INPUT,
    update_mode=GridUpdateMode.MODEL_CHANGED
)

tdf = dta['data']    # overwrite df with revised aggrid data; complete dataset at one go
tdf.to_csv(vpth + 'file1.csv', index=False)  # re/write changed data to CSV if/as required
st.dataframe(tdf)    # confirm changes to df
