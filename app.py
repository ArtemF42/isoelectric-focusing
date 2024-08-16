import os
import io

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

import streamlit as st

PALETTE = ['#000000', '#AD150B', '#DA7F15', '#8CAD0B', '#2575D2', '#6448D5']


def add_custom_fonts() -> None:
    for filename in os.listdir('./fonts'):
        font_manager.fontManager.addfont(f'./fonts/{filename}')


def plot(data: pd.DataFrame, suptitle: str, width: float, height: float, offset: float) -> None:
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)
    fig.suptitle(suptitle)

    ax.set_xlabel(data.index.name)
    ax.set_xticks(data.index[::2])
    axs = [ax]

    for i in range(1, data.shape[1]):
        if i % 2:
            position = 'right'
            bias = 1 + offset * (i // 2)
        else:
            position = 'left'
            bias = 0 - offset * (i // 2)

        ax = axs[0].twinx()
        ax.yaxis.set_ticks_position(position)
        ax.yaxis.set_label_position(position)
        ax.spines[position].set_position(('axes', bias))

        axs.append(ax)

    for i, (ax, column) in enumerate(zip(axs, data.columns)):
        ax.plot(data.index, data[column], color=PALETTE[i])
        ax.set_ylabel(column, color=PALETTE[i])
        ax.tick_params(axis='y', colors=PALETTE[i])

    return fig

if file := st.file_uploader('Upload font', type=['otf', 'ttf']):
    font_data = file.getvalue()

    with open(f'./fonts/{file.name}', 'wb') as file:
        file.write(font_data)

add_custom_fonts()

with st.sidebar:
    suptitle = st.text_input('Title')
    width = st.number_input('Figure width', min_value=1.0, value=8.0, step=0.5)
    height = st.number_input('Figure height', min_value=1.0, value=4.0, step=0.5)
    offset = st.slider('Offset', min_value=0.1, max_value=0.2, value=0.15)
    plt.rcParams['font.family'] = st.selectbox('Font', font_manager.get_font_names())

if file := st.file_uploader('Upload data', type=['xls', 'xlsx']):
    data = pd.read_excel(file, index_col=0)
    st.dataframe(data.head())

    fig = plot(data, suptitle, width, height, offset)
    st.pyplot(fig)

    fig.savefig(fig_data := io.BytesIO(), dpi=400, format='png', bbox_inches='tight')
    st.download_button('Download figure', data=fig_data, file_name='plot.png', mime='image/png')
