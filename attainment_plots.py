# %%
# import libraries
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag


LAs = [ 'National','Birmingham', 'Coventry', 'Dudley', 'Sandwell', 'Solihull', 'Walsall',
       'Wolverhampton', 'Worcestershire', 'Herefordshire, County of', 'Warwickshire']

# mapping for different measures
measure_map = {"Attainment 8": {"column": "attainment8_average",
                                "sum_col": "attainment8_sum",
                                "denominator": "pupil_count",
                                "multiplier": 1,
                                "y_title": "Average Attainment 8 Score"},
                "4 or above in English and maths GCSEs": {"column":"engmath_94_percent",
                                                          "sum_col": "engmath_94_total",
                                                          "denominator": "pupil_count",
                                                          "multiplier": 100,
                                                          "y_title": "% Pupils"},
                "5 or above in English and maths GCSEs": {"column":"engmath_95_percent",
                                                          "sum_col": "engmath_95_total",
                                                          "denominator": "pupil_count",
                                                          "multiplier": 100,
                                                          "y_title": "% Pupils"}
}

# mapping for different groups of students
group_map = {
    "Sex": {"column": "sex",
            "labels": ["Boys","Girls"]},
    "Sex by ethnicity": {"x_col":"ethnicity_major",
                         "comparison_col": "sex",
                         "labels": ["Boys","Girls"],
                         "x_title": "Ethnicity"},
    "Sex by ethnicity by FSM status":{"category_col":"ethnicity_major",
                                      "group_col":"sex",
                                      "comparison_col": "fsm_status",
                                      "group_labels": ["Boys", "Girls"],
                                      "comparison_labels": ["FSM eligible", "Not known to be FSM eligible"],
                                      "category_title": "Ethnicity"},
    "FSM status": {"column": "fsm_status"},
    "Young carer": {"column": "young_carer",
                    "labels": ["Young carer", "Not known to be a young carer"]}
}


# plots
def line_plot(df, group, selected_la, att_measure, selected_time):

    selected_measure = measure_map[att_measure]
    selected_group = group_map[group]
    
    filtered_df = df[(df['la_name'] == selected_la) &
                     (df['breakdown_topic'] == group)]
    
    fig = px.line(
            filtered_df,
            x="time_period", 
            y=selected_measure["column"], 
            color=selected_group["column"])
    
    fig.update_yaxes(title_text=selected_measure["y_title"])
    fig.update_xaxes(title_text='Academic Year')
    fig.update_legends(title_text='Local Authority')

    return fig

#def line_plot_3wayint(df, group, selected_la, att_measure, selected_time):

    selected_measure = measure_map[att_measure]
    selected_group = group_map[group]

    x_col = selected_group["x_col"]
    group1_col = selected_group["group1_col"]
    group2_col = selected_group["group2_col"]

    filtered_df = df[
        (df["time_period"] == "202425") &
        (df["la_name"] == selected_la) &
        (df["breakdown_topic"] == group)
        ].copy()

    # create labels for each condition
    filtered_df["interaction"] = (filtered_df[group1_col].astype(str) + " | " + filtered_df[group2_col].astype(str))

    fig = px.line(
        filtered_df,
        x=x_col,
        y=selected_measure["column"],
        color="interaction",
        markers=True)

    fig.update_xaxes(title_text=selected_group["x_title"])
    fig.update_yaxes(title_text=selected_measure["y_title"])
    fig.update_layout(template="simple_white",legend_title_text="")
       
    return fig


def dumbbell_plot(df, group, selected_la, att_measure, selected_time):

    selected_measure = measure_map[att_measure]
    selected_group = group_map[group]

    group_col = selected_group["column"]
    label1, label2 = selected_group["labels"]

    filtered_df = df[df['time_period'] == '202425']
    filtered_df = filtered_df[filtered_df["breakdown_topic"] == group]
    
    fig = go.Figure()

    # Draw connecting lines
    for la in LAs:

        la_df = filtered_df[filtered_df["la_name"] == la]

        value1 = la_df.loc[
            la_df[group_col] == label1,
            selected_measure["column"]
        ].iloc[0]

        value2 = la_df.loc[
            la_df[group_col] == label2,
            selected_measure["column"]
        ].iloc[0]

        fig.add_trace(
            go.Scatter(
                x=[la, la],
                y=[value1, value2],
                mode="lines",
                line=dict(color="#0B4F9C", width=3),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # Marker trace for first group
    group1_df = filtered_df[
        filtered_df[group_col] == label1
    ]

    fig.add_trace(
        go.Scatter(
            x=group1_df["la_name"],
            y=group1_df[selected_measure["column"]],
            mode="markers",
            name=label1,
            text=group1_df[selected_measure["column"]],
            textposition="top center",
            marker=dict(
                size=12,
                color="#0B4F9C"
            )
        )
    )

    # Marker trace for second group
    group2_df = filtered_df[
        filtered_df[group_col] == label2
    ]

    fig.add_trace(
        go.Scatter(
            x=group2_df["la_name"],
            y=group2_df[selected_measure["column"]],
            mode="markers",
            name=label2,
            text=group2_df[selected_measure["column"]],
            textposition="bottom center",
            marker=dict(
                size=12,
                color="#BFDDF6"
            )
        )
    )

    fig.update_layout(
        template="simple_white",
        xaxis_title="Local Authority",
        yaxis_title=selected_measure["y_title"]
    )

    return fig

def dumbbell_plot_timeline(df, group, selected_la, att_measure, selected_time):

    selected_measure = measure_map[att_measure]
    selected_group = group_map[group]

    x_col = selected_group["x_col"]
    comparison_col = selected_group["comparison_col"]
    label1, label2 = selected_group["labels"]

    filtered_df = df[
        (df["time_period"] == selected_time) &
        (df["la_name"] == selected_la) &
        (df["breakdown_topic"] == group)
        ].copy()

    plot_df = (filtered_df.groupby([x_col, comparison_col],
                                  as_index = False).agg({
                                    selected_measure["sum_col"]:"sum",
                                    selected_measure["denominator"]:"sum",          
                                  })
    )

    plot_df["value"] = (
        plot_df[selected_measure["sum_col"]]
        / plot_df[selected_measure["denominator"]]
        * selected_measure["multiplier"]
                
    )
                                
    fig = go.Figure()

    for category in plot_df[x_col].unique():

        category_df = plot_df[plot_df[x_col] == category]       

        value1 = category_df.loc[
            category_df[comparison_col] == label1,
            "value"
        ].iloc[0]

        value2 = category_df.loc[
            category_df[comparison_col] == label2,
            "value"
        ].iloc[0]

        fig.add_trace(
            go.Scatter(
                x=[category, category],
                y=[value1, value2],
                mode="lines",
                line=dict(
                    color="#0B4F9C",
                    width=3
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # First group
    group1_df = plot_df[
        plot_df[comparison_col] == label1
    ]

    fig.add_trace(
        go.Scatter(
            x=group1_df[x_col],
            y=group1_df["value"],
            mode="markers",
            name=label1,
            marker=dict(
                size=12,
                color="#0B4F9C"
            )
        )
    )

    # Second Sex group
    group2_df = plot_df[
        plot_df[comparison_col] == label2
    ]

    fig.add_trace(
        go.Scatter(
            x=group2_df[x_col],
            y=group2_df["value"],
            mode="markers",
            name=label2,
            marker=dict(
                size=12,
                color="#BFDDF6"
            )
        )
    )

    fig.update_layout(
        template="simple_white",
        xaxis_title=selected_group["x_title"],
        yaxis_title=selected_measure["y_title"]
    )

    return fig

def dumbbell_plot_3wayint(df, group, selected_la, att_measure, selected_time):
    selected_measure = measure_map[att_measure]
    selected_group = group_map[group]

    category_col = selected_group["category_col"]
    group_col = selected_group["group_col"]
    comparison_col = selected_group["comparison_col"]

    group1, group2 = selected_group["group_labels"]
    label1, label2 = selected_group["comparison_labels"]

    filtered_df = df[
        (df["time_period"] == "202425") &
        (df["la_name"] == selected_la) &
        (df["breakdown_topic"] == group)
        ].copy()
    

    plot_df = (filtered_df.groupby(
        [category_col, group_col, comparison_col],
        as_index=False).agg({
            selected_measure["sum_col"]: "sum",
            selected_measure["denominator"]: "sum"})
    )

    # Calculate attainment measure
    plot_df["value"] = (
    plot_df[selected_measure["sum_col"]]/ plot_df[selected_measure["denominator"]]* selected_measure["multiplier"])

    fig = go.Figure()

    categories = plot_df[category_col].unique()

    y_positions = {category: i 
                   for i, category in enumerate(categories)}

    # Plot the two groups slightly above/below each ethnicity
    groups = [{"label": group1,
               "offset": 0.15,
               "colour": "#0B4F9C"},
              {"label": group2,
               "offset": -0.15,
               "colour": "#BFDDF6"}
            ]


    for group_info in groups:
        group_value = group_info["label"]
        offset = group_info["offset"]
        colour = group_info["colour"]

        group_df = plot_df[plot_df[group_col] == group_value]

        for category in categories:
            category_df = group_df[group_df[category_col] == category]

            value1 = category_df.loc[category_df[comparison_col] == label1,"value"]
            value2 = category_df.loc[category_df[comparison_col] == label2,"value"]

            y = y_positions[category] + offset

            # Connecting line
            fig.add_trace(go.Scatter(
                x=[value1.iloc[0],
                    value2.iloc[0]],
                y=[y, y],
                mode="lines",
                line=dict(color=colour,
                          width=3),
                showlegend=False,
                hoverinfo="skip"
                )
            )

    # Add markers separately
    for group_info in groups:
        group_value = group_info["label"]
        offset = group_info["offset"]
        colour = group_info["colour"]

        group_df = plot_df[plot_df[group_col] == group_value]

        label1_df = group_df[group_df[comparison_col] == label1]

        fig.add_trace(go.Scatter(
            x=label1_df["value"],
            y=[y_positions[category] + offset
                for category in label1_df[category_col]],
            mode="markers",
            name=f"{group_value} - {label1}",
            marker=dict(size=12,
                        color=colour,
                        symbol="circle"
                        )
                    )
                )

        label2_df = group_df[group_df[comparison_col] == label2]

        fig.add_trace(go.Scatter(
            x=label2_df["value"],
            y=[y_positions[category] + offset
                for category in label2_df[category_col]],
            mode="markers",
            name=f"{group_value} - {label2}",
            marker=dict(size=12,
                        color=colour,
                        symbol="circle-open"
                        )
                    )
                )   

    # Format axes 
    fig.update_layout(
        template="simple_white",
        xaxis_title=selected_measure["y_title"],
        yaxis=dict(title=selected_group["category_title"],
               tickmode="array",
               tickvals=list(y_positions.values()),
               ticktext=list(y_positions.keys())),
        legend_title_text="")

    return fig

def table_plot (df, group, selected_la, att_measure, selected_time):

    selected_measure = measure_map[att_measure]
    selected_group = group_map[group]

    measure_col = selected_measure["column"]
    group_col = selected_group["column"]
    label1, label2 = selected_group["labels"]

    filtered_df = df[(df["breakdown_topic"] == group) &
                     (df["time_period"] == "202425")].copy()

    # Keep only the cols we need
    filtered_df = filtered_df[["la_name", group_col, measure_col]]

    # reshape
    table_df = filtered_df.pivot(
        index="la_name",
        columns=group_col,
        values=measure_col
        ).reset_index()

    # Calculate difference
    table_df["Gap"] = (table_df[label1] - table_df[label2]).round(1)

    # National difference
    national_difference = table_df.loc[
        table_df["la_name"] == "National", "Gap"
        ].iloc[0]

    # Difference compared with National
    table_df["Gap to National"] = (table_df["Gap"] - national_difference).round(1)

    table_df = table_df[["la_name", label1, label2,
                         "Gap", "Gap to National"]]
    table_df = table_df.rename(columns={"la_name": "Local Authority"})
                    

    table =  dag.AgGrid(
             id="att-table",
             columnDefs=[
                 {"field": "Local Authority"},
                 {"field": label1},
                 {"field": label2},
                 {"field": "Gap"},
                 {"field": "Gap to National",
                  "cellStyle":{"styleConditions":[{
                      "condition": "params.value < 0",
                      "style": {
                          "backgroundColor":"#F8D7DA",
                          "color": "#842029"}
                      },
                      {"condition": "params.value > 0",
                      "style": {
                          "backgroundColor":"#D1E7DD",
                           "color": "#0F5132"}
                  }]}}
            ],
            rowData=table_df.to_dict("records"),
            defaultColDef={
                "sortable": True,
                "filter": True,
                "resizable": True
            },
            columnSize="sizeToFit"
        )

    return table

PLOT_FUNCTIONS = {
    "FSM status": line_plot,
    "Sex": dumbbell_plot,
    "Sex by ethnicity":dumbbell_plot_timeline,
    "Young carer": table_plot,
    "Sex by ethnicity by FSM status": dumbbell_plot_3wayint
    }

# %%