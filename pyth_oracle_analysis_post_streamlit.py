# -------------------------------------------  IMPORTS   ------------------------------------------------------

import pandas as pd
import numpy as np
import time
import json
import altair as alt
import time
import datetime
import time
import base64
import datetime as dt
import streamlit as st


pool_market = 'HMVfAm6uuwnPnHRzaqfMhLNyrYHxaczKTbzeDcjBvuDo'
filename_seed_ = "pyth_oracle_xag_tx_details"

url_file="http://api.fibonacci.fi/get_demo_pyth/none"
previous_txs = pd.read_csv(url_file)
previous_txs.columns=["TxId","Slot","Blocktime","Publisher","PriceAccount","Price","Conf","Slot"]
previous_txs_relevant_price=previous_txs[previous_txs["PriceAccount"]=="HMVfAm6uuwnPnHRzaqfMhLNyrYHxaczKTbzeDcjBvuDo"]

unique_pulishers=list(set(previous_txs_relevant_price["Publisher"]))

dataframes_by_publisher={}
for publisher in unique_pulishers:
    dataframes_by_publisher[publisher]=previous_txs_relevant_price[previous_txs_relevant_price["Publisher"]==publisher]
import streamlit as st

st.write('EXAMPLE OF PYTH PROVIDERS ANALYSIS : Silver XAG over 24h (19/02/24) ')
st.write('Unique publishers found : ', unique_pulishers)
title = st.text_input('Provider to analyze', "2ehFijXkacypZL4jdfPm38BJnMKsN2nMHm8xekbujjdx")
lookback = st.text_input('Analizing over the last X hours : ', 24)
st.write('Analyzing new prices pushed by ', title," over the last ",lookback," hours")



if title in unique_pulishers:
    all_latencies=[]
    dff=title
    local_pd=dataframes_by_publisher[dff]
    local_pd=local_pd.sort_values("Blocktime",ascending=True)
    times_1=np.array(local_pd["Blocktime"][1:])
    times_2=np.array(local_pd["Blocktime"][:-1])
    time_diffs=times_1-times_2
    prices_diff=np.array(local_pd["Price"][:-1])/100000
    time_ui = [dt.datetime.fromtimestamp(ts) for ts in times_1]
    chart_data = pd.DataFrame(np.transpose([time_ui,prices_diff, time_diffs]))
    chart_data.columns = ["Time","Price in $", "Update Latency in seconds"]
    df=chart_data
    if False:
        chart_data=pd.DataFrame(np.transpose([prices_diff, time_diffs]))
        chart_data.columns=["Price($)","UpdateLatencyInSecs"]

        st.line_chart(chart_data)
    else:
        a = alt.Chart(chart_data, title="Price and latency").mark_line().encode(
            x=alt.X('Time:T', axis=alt.Axis(format='%m-%d %H:%M')),
            y=alt.Y('Update Latency in seconds',
                    scale=alt.Scale(domain=[np.min(chart_data["Update Latency in seconds"]), np.max(chart_data["Update Latency in seconds"])]),

                    ),
            color=alt.value("#FFAA00"),
        )
        b = alt.Chart(chart_data).mark_line().encode(
            x=alt.X('Time:T', axis=alt.Axis(format='%m-%d %H:%M')),
            y=alt.Y("Price in $", scale=alt.Scale(domain=[np.min(chart_data["Price in $"]), np.max(chart_data["Price in $"])]),

                    )
        )
        c = alt.layer(a, b).resolve_scale(
            y='independent'
        )
        st.altair_chart(c, use_container_width=True)




