import streamlit as st
import pandas as pd
import requests
from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import io
from datetime import datetime, timedelta


dune = DuneClient(
    api_key=st.secrets["api_keys"]["dune_key"],
    base_url="https://api.dune.com",
    request_timeout=300 # request will time out after 300 seconds
)

query_result = dune.get_latest_result(3917119)

query = QueryBase(
    query_id=3917119,
)
gas_fee = dune.run_query_dataframe(
  query=query
)

url = "https://open-api-v3.coinglass.com/api/bitcoin/etf/flow-history"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["api_keys"]["coinglass_key"]
}

response = requests.get(url, headers=headers)
data = response.json()['data']
df = pd.DataFrame(data)
# 将日期转换为可读格式
df['date'] = pd.to_datetime(df['date'], unit='ms')
btc_etf_data = df[df['changeUsd'] != 0]

url = "https://open-api-v3.coinglass.com/api/ethereum/etf/flow-history"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["api_keys"]["coinglass_key"]
}

response = requests.get(url, headers=headers)
data = response.json()['data']
df = pd.DataFrame(data)
# 将日期转换为可读格式
df['date'] = pd.to_datetime(df['date'], unit='ms')
eth_etf_data = df[df['changeUsd'] != 0]

url = "https://open-api-v3.coinglass.com/api/index/fear-greed-history"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["api_keys"]["coinglass_key"]
}

response = requests.get(url, headers=headers)
data = response.json()['data']
df = pd.DataFrame(data)
df['dates'] = pd.to_datetime(df['dates'], unit='ms')
fear_greed = df.tail(360)



url = "https://open-api-v3.coinglass.com/api/index/bitcoin-bubble-index"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["api_keys"]["coinglass_key"]
}

response = requests.get(url, headers=headers)
data = response.json()['data']
df = pd.DataFrame(data)
bubble_index = df.tail(360)


url = "https://open-api-v3.coinglass.com/api/index/ahr999"

headers = {
    "accept": "application/json",
    "CG-API-KEY": st.secrets["api_keys"]["coinglass_key"]
}
response = requests.get(url, headers=headers)
data = response.json()['data']
df = pd.DataFrame(data)
arh999 = df.tail(360)

# Function to convert DataFrame to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to convert multiple DataFrames to a single CSV file
def convert_multiple_dfs_to_csv(dfs, names):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for df, name in zip(dfs, names):
            df.to_excel(writer, sheet_name=name, index=False)
    return output.getvalue()

# Streamlit app
st.title('Download Multiple DataFrames')

# Display DataFrames
st.write("DataFrame Gas Fee")
st.dataframe(gas_fee)

st.write("DataFrame BTC ETF Data")
st.dataframe(btc_etf_data)

st.write("DataFrame ETH ETF Data")
st.dataframe(eth_etf_data)

st.write("DataFrame fear greed Data")
st.dataframe(fear_greed)

st.write("DataFrame BTC RAINBOW")
st.dataframe(bubble_index)

st.write("DataFrame BTC AHR999")
st.dataframe(arh999)

# Convert DataFrames to CSV
csv1 = convert_df_to_csv(gas_fee)
csv2 = convert_df_to_csv(btc_etf_data)
csv3 = convert_df_to_csv(eth_etf_data)
csv4 = convert_df_to_csv(fear_greed)
csv5 = convert_df_to_csv(bubble_index)
csv6 = convert_df_to_csv(arh999)

# Create a button to download each CSV
st.download_button(
    label="Download DataFrame Gas Fee as CSV",
    data=csv1,
    file_name='gas_fee.csv',
    mime='text/csv',
)

st.download_button(
    label="Download DataFrame ETF Data as CSV",
    data=csv2,
    file_name='btc_etf_data.csv',
    mime='text/csv',
)

st.download_button(
    label="Download DataFrame AHR999 as CSV",
    data=csv3,
    file_name='eth_etf_data.csv',
    mime='text/csv',
)

st.download_button(
    label="Download DataFrame AHR999 as CSV",
    data=csv4,
    file_name='fear_greed.csv',
    mime='text/csv',
)

st.download_button(
    label="Download DataFrame AHR999 as CSV",
    data=csv5,
    file_name='bubble_index.csv',
    mime='text/csv',
)

st.download_button(
    label="Download DataFrame AHR999 as CSV",
    data=csv6,
    file_name='arh999.csv',
    mime='text/csv',
)

# Convert multiple DataFrames to a single Excel file
excel_data = convert_multiple_dfs_to_csv([gas_fee, btc_etf_data, eth_etf_data,fear_greed,bubble_index, arh999], ['Sheet1', 'Sheet2','Sheet3','Sheet4', 'Sheet5','Sheet6'])

# Create a button to download the Excel file
st.download_button(
    label="Download both DataFrames as Excel",
    data=excel_data,
    file_name='dataframes.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)
