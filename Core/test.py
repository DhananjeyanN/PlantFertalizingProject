import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta



# Current datetime for reference
now = datetime.now()

# Create figure
fig = go.Figure()

# Add trace
fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperature'], mode='lines+markers', name='Temperature'))

# Update layout with buttons
fig.update_layout(
    title='Temperature Data',
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            buttons=list([
                dict(
                    args=[{"xaxis.range": [now - timedelta(days=1), now]}],
                    label="Last Day",
                    method="relayout"
                ),
                dict(
                    args=[{"xaxis.range": [now - timedelta(days=30), now]}],
                    label="Last Month",
                    method="relayout"
                ),
                dict(
                    args=[{"xaxis.range": [now - timedelta(days=365), now]}],
                    label="Last Year",
                    method="relayout"
                ),
            ]),
        )
    ]
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                {"count": 1, "label": "1d", "step": "day", "stepmode": "backward"},
                {"count": 1, "label": "1m", "step": "month", "stepmode": "backward"},
                {"count": 1, "label": "1y", "step": "year", "stepmode": "backward"},
                {"step": "all"}
            ])
        ),
        type="date"
    )
)

fig.show()

