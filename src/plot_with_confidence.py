import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


"""Plot dataframe with confidence interval"""

# ===== create data (mock) =====
df = pd.DataFrame(
    dict(
        algorithm=[
            "a", "b", "c", "d", "a", "b", "c", "d", "a", "b", "c", "d",
            "a", "b", "c", "d", "a", "b", "c", "d", "a", "b", "c", "d",
            "a", "b", "c", "d", "a", "b", "c", "d", "a", "b", "c", "d",
        ],
        seed=[
            0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
            0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
            0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
        ],
        trial=[
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        ],
        objective=np.random.rand(36),
    )
)


# ===== figure =====

# color sequence
hex_colors: list[str] = px.colors.qualitative.Plotly  # TODO: Enable manually selection.

# base figure
fig = go.Figure()

# add plot per legend group
algorithm: str  # TODO: Generalizing
group: pd.DataFrame
for (algorithm, group), hex_color in zip(df.groupby('algorithm'), hex_colors):
    print(f'===== {algorithm} =====')
    print(type(group))
    print(group)

    x: list
    y: list
    y_lb: list
    y_ub: list

    # create variance data per trial  # TODO: This should be the default behavior if the y_error is not passed.
    trial = np.array(tuple(group.groupby('trial').groups.keys()))
    mean = group.groupby('trial').mean(numeric_only=True)['objective'].values
    std = group.groupby('trial').std(numeric_only=True)['objective'].values

    x = list(trial)
    y = list(mean)
    y_lb = list(mean - std)
    y_ub = list(mean + std)

    fig.add_trace(
        go.Scatter(
            # data
            x=x, y=y,
            # line
            line=dict(color=hex_color),
            # marker
            marker=dict(),
            # fill
            fill=None,
            # legend
            name=algorithm,
            legendgroup=algorithm,
            # # hover
            # hovertemplate=f"algorithm={algorithm}<br>x=%{{x}}<br>y=%{{y}}<extra></extra>",
        )
    )


    def convert_color(alpha):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f'rgba({r}, {g}, {b}, {alpha})'


    fig.add_trace(
        go.Scatter(
            # data
            x=x + x[::-1],
            y=y_lb + y_ub[::-1],
            # style
            mode='lines',
            # line
            line=dict(color=convert_color(0.5), width=0.2),
            # marker
            marker=dict(),
            # fill
            fill='toself',
            fillcolor=convert_color(0.2),
            # legend
            legendgroup=algorithm,
            showlegend=False,
            # hover
            # hovertemplate=f"algorithm={algorithm}<br>x=%{{x}}<br>y=%{{y}}<extra></extra>",
        )
    )

# TODO: Enable to specify these
fig.update_layout(legend_title_text="Legend")
fig.update_layout(title_text="Title")
fig.update_layout(
    autosize=False,
    # minreducedwidth=250,
    # minreducedheight=250,
    width=450,
    height=450,
    yaxis=dict(
        title=dict(
            text="Y-axis Title",
            font=dict(
                size=30
            )
        ),
        ticktext=["Label", "Very long label", "Other label", "Very very long label"],
        tickvals=[0, 0.25, 0.75, 1],
        tickmode="array",
        range=[0, 1],
    )
)
fig.update_xaxes(title_text="x axis title")
fig.show()
