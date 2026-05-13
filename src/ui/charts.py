import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


DEFAULT_HEIGHT = 520
PRIMARY_COLOR = "#00C2FF"
SECONDARY_COLOR = "#FFB703"


def _base_layout(title, x_axis_title=None, y_axis_title=None, height=DEFAULT_HEIGHT):
    return {
        "template": "plotly_dark",
        "height": height,
        "title": {
            "text": title,
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 22,
            },
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {
            "l": 40,
            "r": 24,
            "t": 72,
            "b": 96,
        },
        "xaxis_title": x_axis_title,
        "yaxis_title": y_axis_title,
        "hoverlabel": {
            "bgcolor": "#111827",
            "font_size": 13,
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
        "bargap": 0.28,
        "font": {
            "family": "Inter, Segoe UI, Arial, sans-serif",
        },
    }


def _series_to_frame(data, x_name="Category", y_name="Value"):
    if isinstance(data, pd.Series):
        return data.rename(y_name).reset_index().rename(columns={"index": x_name})

    return data.copy()


def create_bar_chart(
    data,
    x=None,
    y=None,
    title="Bar Chart",
    x_axis_title=None,
    y_axis_title=None,
    color=None,
    height=DEFAULT_HEIGHT,
):
    chart_data = _series_to_frame(data)
    x_col = x or chart_data.columns[0]
    y_col = y or chart_data.columns[1]

    fig = px.bar(
        chart_data,
        x=x_col,
        y=y_col,
        color=color,
        template="plotly_dark",
        text_auto=True,
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
            "#8B5CF6",
            "#22C55E",
            "#F97316",
        ],
    )

    fig.update_traces(
        marker_line_width=0,
        opacity=0.92,
        hovertemplate=f"<b>%{{x}}</b><br>{y_axis_title or y_col}: %{{y}}<extra></extra>",
    )
    fig.update_layout(
        **_base_layout(
            title,
            x_axis_title or x_col,
            y_axis_title or y_col,
            height,
        )
    )
    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.18)",
    )

    return fig


def create_line_chart(
    data,
    x=None,
    y=None,
    title="Line Chart",
    x_axis_title=None,
    y_axis_title=None,
    height=DEFAULT_HEIGHT,
):
    chart_data = _series_to_frame(data)
    x_col = x or chart_data.columns[0]
    y_col = y or chart_data.columns[1]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=chart_data[x_col],
            y=chart_data[y_col],
            mode="lines+markers",
            line={
                "color": PRIMARY_COLOR,
                "width": 3,
                "shape": "spline",
            },
            marker={
                "size": 9,
                "color": SECONDARY_COLOR,
                "line": {
                    "width": 1,
                    "color": "#0F172A",
                },
            },
            hovertemplate=f"<b>%{{x}}</b><br>{y_axis_title or y_col}: %{{y}}<extra></extra>",
        )
    )

    fig.update_layout(
        **_base_layout(
            title,
            x_axis_title or x_col,
            y_axis_title or y_col,
            height,
        )
    )
    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.18)",
    )

    return fig


def create_multi_line_chart(
    data,
    x,
    y,
    color,
    title="Line Chart",
    x_axis_title=None,
    y_axis_title=None,
    height=DEFAULT_HEIGHT,
):
    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        markers=True,
        template="plotly_dark",
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
            "#8B5CF6",
            "#22C55E",
            "#F97316",
        ],
    )

    fig.update_traces(
        line={
            "width": 3,
            "shape": "spline",
        },
        marker={
            "size": 8,
            "line": {
                "width": 1,
                "color": "#0F172A",
            },
        },
        hovertemplate="<b>%{fullData.name}</b><br>%{x}<br>%{y}<extra></extra>",
    )
    fig.update_layout(
        **_base_layout(
            title,
            x_axis_title or x,
            y_axis_title or y,
            height,
        )
    )
    fig.update_xaxes(
        showgrid=False,
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.18)",
    )

    return fig


def create_scatter_chart(
    data,
    x,
    y,
    title="Scatter Chart",
    x_axis_title=None,
    y_axis_title=None,
    color=None,
    size=None,
    height=DEFAULT_HEIGHT,
):
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        size=size,
        template="plotly_dark",
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
            "#8B5CF6",
            "#22C55E",
            "#F97316",
        ],
    )

    fig.update_traces(
        marker={
            "opacity": 0.86,
            "line": {
                "width": 1,
                "color": "#0F172A",
            },
        }
    )
    fig.update_layout(
        **_base_layout(
            title,
            x_axis_title or x,
            y_axis_title or y,
            height,
        )
    )
    fig.update_xaxes(
        showgrid=False,
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.18)",
    )

    return fig


def create_radar_chart(
    data,
    title="Radar Chart",
    height=DEFAULT_HEIGHT,
):
    fig = go.Figure()

    categories = list(data.columns)
    closed_categories = categories + [categories[0]]

    for player, row in data.iterrows():
        values = row.tolist()
        closed_values = values + [values[0]]
        fig.add_trace(
            go.Scatterpolar(
                r=closed_values,
                theta=closed_categories,
                fill="toself",
                name=str(player),
                hovertemplate="<b>%{fullData.name}</b><br>%{theta}: %{r:.2f}<extra></extra>",
            )
        )

    fig.update_layout(
        **_base_layout(
            title,
            height=height,
        ),
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "gridcolor": "rgba(255,255,255,0.12)",
            },
            "angularaxis": {
                "gridcolor": "rgba(255,255,255,0.10)",
            },
        },
    )

    return fig


def create_gauge_chart(
    value,
    title="Gauge",
    suffix="%",
    height=360,
):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={
                "suffix": suffix,
                "font": {
                    "size": 34,
                },
            },
            title={
                "text": title,
                "font": {
                    "size": 20,
                },
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "rgba(255,255,255,0.55)",
                },
                "bar": {
                    "color": PRIMARY_COLOR,
                },
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
                "steps": [
                    {
                        "range": [0, 35],
                        "color": "rgba(239,68,68,0.28)",
                    },
                    {
                        "range": [35, 65],
                        "color": "rgba(245,158,11,0.28)",
                    },
                    {
                        "range": [65, 100],
                        "color": "rgba(34,197,94,0.28)",
                    },
                ],
            },
        )
    )

    fig.update_layout(
        **_base_layout(
            title,
            height=height,
        )
    )

    return fig
