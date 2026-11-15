"""Plotly figure builders used by the Streamlit pages.

Colors follow a validated categorical palette (fixed slot order, separate light/dark
steps); ham/spam always use slots 1/2 so identity is consistent across pages.

Presentation polish only: function names, arguments and data are unchanged.
Entrance animations for these charts live in src/ui_theme.py (CSS).
"""

from __future__ import annotations

from typing import Any, Sequence

import plotly.graph_objects as go

LIGHT = {
    "series": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"],
    "seq": ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"],
    "grid": "rgba(82,81,78,0.12)",
    "muted": "#8a8984",
    "ink": "#252653",
}
DARK = {
    "series": ["#3987e5", "#d95926", "#199e70", "#c98500"],
    "seq": ["#0d366b", "#184f95", "#256abf", "#5598e7", "#9ec5f4"],
    "grid": "rgba(195,194,183,0.14)",
    "muted": "#9a998f",
    "ink": "#f0efec",
}
STATUS = {"good": "#0ca30c", "critical": "#d03b3b"}

FONT_FAMILY = "Inter, 'Source Sans Pro', system-ui, -apple-system, 'Segoe UI', sans-serif"


def palette(dark: bool) -> dict[str, Any]:
    return DARK if dark else LIGHT


def class_colors(dark: bool) -> dict[str, str]:
    s = palette(dark)["series"]
    return {"ham": s[0], "spam": s[1]}


def _layout(fig: go.Figure, dark: bool, *, height: int = 360, xtitle: str = "", ytitle: str = "", legend: bool = True) -> go.Figure:
    p = palette(dark)
    tooltip_bg = "#1b1f2e" if dark else "#FFFFFF"
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=36, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, size=12, color=p["ink"]),
        showlegend=legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=12),
        ),
        hovermode="closest",
        hoverlabel=dict(
            namelength=-1,
            bgcolor=tooltip_bg,
            bordercolor=p["grid"],
            font=dict(family=FONT_FAMILY, size=12, color=p["ink"]),
        ),
    )
    fig.update_xaxes(
        title_text=xtitle,
        title_font=dict(size=12, color=p["muted"]),
        tickfont=dict(color=p["muted"]),
        gridcolor=p["grid"],
        zeroline=False,
        linecolor=p["grid"],
    )
    fig.update_yaxes(
        title_text=ytitle,
        title_font=dict(size=12, color=p["muted"]),
        tickfont=dict(color=p["muted"]),
        gridcolor=p["grid"],
        zeroline=False,
        linecolor=p["grid"],
    )
    return fig


def probability_bar(prob: float, threshold: float, dark: bool) -> go.Figure:
    """Display spam probability with decision regions and a threshold marker."""
    colors = class_colors(dark)
    p = palette(dark)
    label = "spam" if prob >= threshold else "ham"

    ham_zone = "rgba(27,175,122,0.13)" if not dark else "rgba(25,158,112,0.17)"
    spam_zone = "rgba(235,104,52,0.13)" if not dark else "rgba(217,89,38,0.17)"

    fig = go.Figure()

    # Background regions reflect the current decision threshold.
    fig.add_vrect(x0=0, x1=threshold, fillcolor=ham_zone, line_width=0, layer="below")
    fig.add_vrect(x0=threshold, x1=1, fillcolor=spam_zone, line_width=0, layer="below")

    # Zone labels (only when the zone is wide enough to hold the text).
    if threshold >= 0.14:
        fig.add_annotation(
            x=threshold / 2, y=0.93, yref="paper", text="HAM ZONE", showarrow=False,
            font=dict(size=10, color=colors["ham"]),
        )
    if (1 - threshold) >= 0.14:
        fig.add_annotation(
            x=(1 + threshold) / 2, y=0.93, yref="paper", text="SPAM ZONE", showarrow=False,
            font=dict(size=10, color=colors["spam"]),
        )

    # Actual model probability.
    fig.add_trace(
        go.Bar(
            x=[prob],
            y=["Spam probability"],
            orientation="h",
            marker=dict(color=colors[label], cornerradius=8, line=dict(width=0)),
            width=0.42,
            hovertemplate="<b>Spam probability</b><br>%{x:.1%}<extra></extra>",
            showlegend=False,
        )
    )

    # Current classification threshold.
    fig.add_vline(x=threshold, line=dict(color=p["ink"], width=2, dash="dash"))

    fig.add_annotation(
        x=threshold,
        y=1.12,
        yref="paper",
        text=f"Threshold: {threshold:.2f}",
        showarrow=False,
        font=dict(size=12, color=p["ink"]),
        bgcolor="rgba(255,255,255,0.85)" if not dark else "rgba(20,25,35,0.85)",
        bordercolor=p["grid"],
        borderwidth=1,
        borderpad=4,
    )

    _layout(fig, dark, height=175, legend=False, xtitle="Spam probability")

    fig.update_xaxes(range=[0, 1], tickformat=".0%", dtick=0.2, showgrid=True)
    fig.update_yaxes(showgrid=False, showticklabels=False)
    fig.update_layout(margin=dict(l=8, r=12, t=42, b=38), bargap=0.35)

    return fig


def contribution_chart(
    contributions: Sequence[dict[str, Any]],
    dark: bool,
) -> go.Figure:
    """Display positive and negative feature contributions to the spam score."""
    colors = class_colors(dark)
    p = palette(dark)

    items = list(contributions)[::-1]

    labels = [
        f"{c['feature']} · {c['kind']}"
        + (" (absent)" if c["kind"] != "structured" and not c.get("value") else "")
        for c in items
    ]

    values = [c["contribution"] for c in items]
    bar_colors = [colors[c["direction"]] for c in items]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(color=bar_colors, cornerradius=6, line=dict(width=0)),
            width=0.68,
            customdata=[
                [c["direction"], c.get("description", ""), c.get("kind", "")]
                for c in items
            ],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Contribution: %{x:+.4f}<br>"
                "Direction: %{customdata[0]}<br>"
                "Description: %{customdata[1]}<br>"
                "Signal type: %{customdata[2]}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    _layout(
        fig,
        dark,
        height=max(300, 34 * len(items) + 75),
        xtitle="← Towards HAM     |     Towards SPAM →",
        legend=False,
    )

    fig.add_vline(x=0, line=dict(color=p["muted"], width=1.5))

    fig.update_xaxes(zeroline=False, showgrid=True, gridcolor=p["grid"], tickformat="+.2f", automargin=True)
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(size=11, color=p["ink"]), automargin=True)
    fig.update_layout(margin=dict(l=15, r=20, t=25, b=55), bargap=0.22)

    return fig


def confusion_matrix_chart(cm: dict[str, int], dark: bool) -> go.Figure:
    z = [[cm["tn"], cm["fp"]], [cm["fn"], cm["tp"]]]
    seq = palette(dark)["seq"]
    text = [[f"TN<br>{cm['tn']}", f"FP<br>{cm['fp']}"], [f"FN<br>{cm['fn']}", f"TP<br>{cm['tp']}"]]
    fig = go.Figure(
        go.Heatmap(
            z=z, x=["Predicted ham", "Predicted spam"], y=["Actual ham", "Actual spam"],
            colorscale=[[i / (len(seq) - 1), c] for i, c in enumerate(seq)], showscale=False,
            text=text, texttemplate="%{text}", textfont=dict(size=16), xgap=3, ygap=3,
            hovertemplate="%{y} / %{x}: %{z}<extra></extra>",
        )
    )
    _layout(fig, dark, height=320, legend=False)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig.update_xaxes(showgrid=False, side="top")
    return fig


def curve_chart(curves: list[dict[str, Any]], kind: str, dark: bool) -> go.Figure:
    """Overlay ROC ('roc') or precision-recall ('pr') curves; ``curves`` items: name, x, y, auc."""
    series = palette(dark)["series"]
    fig = go.Figure()
    for i, c in enumerate(curves):
        fig.add_trace(
            go.Scatter(
                x=c["x"], y=c["y"], mode="lines", name=f"{c['name']} (AUC {c['auc']:.4f})",
                line=dict(color=series[i % len(series)], width=2.5),
                hovertemplate=f"{c['name']}<br>%{{x:.3f}}, %{{y:.3f}}<extra></extra>",
            )
        )
    if kind == "roc":
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="chance",
                                 line=dict(color=palette(dark)["muted"], width=1, dash="dot"), hoverinfo="skip"))
        _layout(fig, dark, xtitle="False positive rate", ytitle="True positive rate")
    else:
        _layout(fig, dark, xtitle="Recall", ytitle="Precision")
    fig.update_xaxes(range=[0, 1])
    fig.update_yaxes(range=[0, 1.02])
    return fig


def threshold_chart(rows: Sequence[dict[str, float]], selected_threshold: float, dark: bool) -> go.Figure:
    series = palette(dark)["series"]
    fig = go.Figure()
    for i, (key, name) in enumerate((("precision", "Precision"), ("recall", "Recall"), ("f1", "F1"), ("f0_5", "F0.5"))):
        fig.add_trace(
            go.Scatter(
                x=[r["threshold"] for r in rows], y=[r[key] for r in rows], mode="lines+markers", name=name,
                line=dict(color=series[i], width=2.5), marker=dict(size=8),
                hovertemplate=f"{name} %{{y:.4f}} at threshold %{{x:.2f}}<extra></extra>",
            )
        )
    fig.add_vline(x=selected_threshold, line=dict(color=palette(dark)["ink"], width=1, dash="dot"))
    fig.add_annotation(x=selected_threshold, y=1, yref="paper", text=f"tuned {selected_threshold:.2f}",
                       showarrow=False, yanchor="bottom", xanchor="left")
    _layout(fig, dark, xtitle="Decision threshold", ytitle="Score")
    fig.update_xaxes(range=[0, 1])
    return fig


def calibration_chart(curves: list[dict[str, Any]], dark: bool, min_count: int = 5) -> go.Figure:
    """Reliability diagram. Bins with fewer than ``min_count`` emails are hidden (too noisy to read)."""
    series = palette(dark)["series"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="perfectly calibrated",
                             line=dict(color=palette(dark)["muted"], width=1, dash="dot"), hoverinfo="skip"))
    for i, c in enumerate(curves):
        keep = [j for j, n in enumerate(c.get("count") or []) if n >= min_count]
        fig.add_trace(
            go.Scatter(
                x=[c["x"][j] for j in keep], y=[c["y"][j] for j in keep], mode="lines+markers", name=c["name"],
                line=dict(color=series[i % len(series)], width=2.5), marker=dict(size=8),
                customdata=[c["count"][j] for j in keep],
                hovertemplate=f"{c['name']}<br>predicted %{{x:.2f}} → observed %{{y:.2f}}<br>n=%{{customdata}}<extra></extra>",
            )
        )
    _layout(fig, dark, xtitle="Mean predicted spam probability", ytitle="Observed spam fraction")
    fig.update_xaxes(range=[0, 1])
    fig.update_yaxes(range=[0, 1.02])
    return fig


def probability_histogram(hist: dict[str, list], dark: bool) -> go.Figure:
    colors = class_colors(dark)
    edges = hist["edges"]
    centers = [(a + b) / 2 for a, b in zip(edges[:-1], edges[1:])]
    fig = go.Figure()
    for cls in ("ham", "spam"):
        fig.add_trace(
            go.Bar(x=centers, y=hist[cls], name=f"Actual {cls}", marker=dict(color=colors[cls], cornerradius=5),
                   hovertemplate=f"Actual {cls}: %{{y}} emails<br>p≈%{{x:.3f}}<extra></extra>")
        )
    fig.update_layout(barmode="group", bargap=0.1)
    _layout(fig, dark, xtitle="Predicted spam probability (test set)", ytitle="Emails")
    fig.update_yaxes(type="log")
    return fig


def class_distribution_chart(spam: int, ham: int, dark: bool) -> go.Figure:
    colors = class_colors(dark)
    fig = go.Figure(
        go.Bar(
            x=[ham, spam], y=["Ham", "Spam"], orientation="h",
            marker=dict(color=[colors["ham"], colors["spam"]], cornerradius=6),
            text=[ham, spam], textposition="outside",
            hovertemplate="%{y}: %{x} predictions<extra></extra>",
        )
    )
    _layout(fig, dark, height=180, legend=False, xtitle="Predictions")
    return fig


def latency_chart(records: Sequence[dict[str, Any]], dark: bool) -> go.Figure:
    fig = go.Figure()
    for status, color, name in (("success", palette(dark)["series"][0], "Success"), ("error", STATUS["critical"], "Error")):
        pts = [r for r in records if r["status"] == status]
        if not pts:
            continue
        fig.add_trace(
            go.Scatter(
                x=[r["timestamp"] for r in pts], y=[r["latency_ms"] for r in pts], mode="markers", name=name,
                marker=dict(color=color, size=9, symbol="circle" if status == "success" else "x",
                            line=dict(width=2, color="rgba(0,0,0,0)")),
                customdata=[[r["request_id"], r.get("prediction") or r.get("error_type") or ""] for r in pts],
                hovertemplate="%{customdata[0]}<br>%{y:.1f} ms · %{customdata[1]}<extra></extra>",
            )
        )
    _layout(fig, dark, height=300, xtitle="Request time (UTC)", ytitle="Latency (ms)")
    return fig