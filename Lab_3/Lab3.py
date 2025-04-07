import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('../Lab_2/Data/vhi_end.csv')


col1, col2 = st.columns([1, 2])

time_row = ['VCI', 'TCI', 'VHI']

if 'selected_time_row' not in st.session_state:
    st.session_state.selected_time_row = time_row[0]

with col1:
    st.session_state.selected_time_row = st.selectbox(
        "Оберіть часовий ряд для набору даних:",
        time_row,
        index=time_row.index(st.session_state.selected_time_row)
    )

    area_names = data['area'].unique()

    if 'selected_area' not in st.session_state:
        st.session_state.selected_area = area_names[0]

    st.session_state.selected_area = st.selectbox(
    "Оберіть область", options=area_names,
    index=list(area_names).index(st.session_state.selected_area)
    )

    if 'week_range' not in st.session_state:
        st.session_state.week_range = (1, 52)
    
    st.session_state.week_range = st.slider(
    "Виберіть інтервал тижнів", 1, 52, st.session_state.week_range
    )

    if 'year_range' not in st.session_state:
        st.session_state.year_range = (1982, 2024)

    st.session_state.year_range = st.slider(
    "Виберіть інтервал років", 1982, 2024, st.session_state.year_range
    )

    if st.button("Скинути фільтри"):
        st.session_state.selected_time_row = time_row[0]
        st.session_state.selected_area = area_names[0]
        st.session_state.week_range = (1, 52)
        st.session_state.year_range = (1982, 2024)
        st.session_state.ascending_order = False
        st.session_state.downward_order = False


    filtered_data_orig = data[(data['area'] == st.session_state.selected_area) 
                        & (data['week'].isin(range(st.session_state.week_range[0], st.session_state.week_range[1]+1))) 
                        & (data['year'].isin(range(st.session_state.year_range[0], st.session_state.year_range[1]+1)))]

    if 'ascending_order' not in st.session_state:
        st.session_state.ascending_order = False

    if 'downward_order' not in st.session_state:
        st.session_state.downward_order = False

    def ascending():
        st.session_state["ascending_order"] = not st.session_state["ascending_order"]
        if st.session_state.downward_order:
            st.session_state.downward_order = False

    def downward():
        st.session_state["downward_order"] = not st.session_state["downward_order"]
        if st.session_state.ascending_order:
            st.session_state.ascending_order = False

    ascending_order = st.checkbox(
        "Сортувати за зростанням",
        value=st.session_state["ascending_order"],
        on_change=ascending
    )

    downward_order = st.checkbox(
        "Сортувати за спаданням",
        value=st.session_state["downward_order"],
        on_change=downward
    )

    if st.session_state.ascending_order:
        filtered_data = filtered_data_orig.sort_values(by=st.session_state.selected_time_row)
    elif st.session_state.downward_order:
        filtered_data = filtered_data_orig.sort_values(by=st.session_state.selected_time_row, ascending=False)
    else:
        filtered_data = filtered_data_orig



with col2:
    tab1, tab2, tab3 = st.tabs(['Таблиця', 'Графік', 'Графік порівнянь даних по областях'])
    with tab1:
        st.write('Відфільтровані дані')
        st.write(filtered_data[['year', 'week', st.session_state.selected_time_row, 'area']])

    with tab2:
        plt.figure(figsize=(5, 5))
        sns.histplot(data=filtered_data, x='year', y=st.session_state.selected_time_row)
        plt.title(f'Відфільтровані дані')
        plt.xlabel('Рік')
        plt.ylabel(st.session_state.selected_time_row)
        st.pyplot(plt)

    with tab3:
        data_compare = data[(data['week'].isin(range(st.session_state.week_range[0], st.session_state.week_range[1]+1))) 
                            & (data['year'].isin(range(st.session_state.year_range[0], st.session_state.year_range[1]+1)))]
        data_compare['type'] = 'other'
        data_compare.loc[data_compare['area'] == st.session_state.selected_area, 'type'] = st.session_state.selected_area
        data_compare = data_compare[['year', st.session_state.selected_time_row, 'type']]

        color_palette = {st.session_state.selected_area:"b", "other":"yellow"}
        plt.figure(figsize=(5, 5))
        sns.histplot(data=data_compare, x='year', y=st.session_state.selected_time_row, hue='type', multiple="stack", palette=color_palette)
        plt.title('Графік порівнянь даних по областях')
        plt.xlabel('Рік')
        plt.ylabel(st.session_state.selected_time_row)
        st.pyplot(plt)
