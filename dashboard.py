import pandas as pd
import numpy as np
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html

# ── LOAD DATA ────────────────────────────────────────────────────────────────
df = pd.read_csv("cleaned_data.csv")
df["avg_productivity"] = df[["productivity_home", "productivity_library", "productivity_class"]].mean(axis=1)

YEAR_ORDER  = ["Year 1", "Year 2", "Year 3", "Year 4", "Final Year", "PhD"]
HOURS_ORDER = ["<2 hrs", "2-4 hrs", ">4 hrs"]
LIB_ORDER   = ["Never", "Rarely", "Sometimes", "Regularly"]
EXAM_ORDER  = ["Less", "Same", "Slightly more", "Significantly more"]

def count_multi(series, top_n=8):
    items = []
    for val in series.dropna():
        items.extend([x.strip() for x in str(val).split(",")])
    return pd.Series(Counter(items)).nlargest(top_n)

# ── GOOGLE FONTS ─────────────────────────────────────────────────────────────
FONTS = "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap"

# ── THEME PER TOPIC: (plot_bg, paper_bg, font_color, [accent_colors]) ────────
THEMES = {
    1: ("#fdf6ec", "#fdf6ec", "#3b2a1a", ["#c0714f", "#e8a87c", "#f2c9a0", "#a0522d"]),
    2: ("#f2f7f2", "#f2f7f2", "#1e3a2f", ["#4a8c6f", "#76b593", "#a8d5b5", "#2e6b50"]),
    3: ("#2b2420", "#2b2420", "#f0e6d3", ["#d4845a", "#e8a87c", "#c06040", "#f0c090"]),
    4: ("#fef9f0", "#fef9f0", "#4a2c00", ["#c87941", "#e8a060", "#f0c080", "#a05020"]),
    5: ("#f7f0f0", "#f7f0f0", "#3d1515", ["#b54040", "#d47070", "#e8a0a0", "#8b2020"]),
    6: ("#f0f5f4", "#f0f5f4", "#1a3530", ["#3d7a70", "#5a9e94", "#7ec4ba", "#2a5a54"]),
    7: ("#f4f0f8", "#f4f0f8", "#2d1a4a", ["#7a52a8", "#9d78c8", "#bda0e0", "#5a3480"]),
    8: ("#f5f3ef", "#f5f3ef", "#2a2520", ["#7a6858", "#9e8878", "#c4b0a0", "#5a4838"]),
    9: ("#1e1a16", "#1e1a16", "#e8ddd0", ["#c8a878", "#e0c898", "#a88858", "#f0e0b8"]),
}

def fig_layout(fig, title, tid):
    bg, paper, fc, _ = THEMES[tid]
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=fc, family="Lora, Georgia, serif")),
        plot_bgcolor=bg, paper_bgcolor=paper,
        font=dict(color=fc, size=11, family="Source Sans 3, sans-serif"),
        margin=dict(l=40, r=20, t=48, b=36),
        showlegend=True,
    )
    return fig

def section_header(tid, title, subtitle):
    bg, _, fc, ac = THEMES[tid]
    return html.Div([
        html.Div(style={"width": "4px", "background": ac[0], "borderRadius": "2px",
                        "marginRight": "14px", "flexShrink": "0"}),
        html.Div([
            html.Span(f"0{tid}  ", style={
                "fontFamily": "Source Sans 3, sans-serif", "fontSize": "11px",
                "color": ac[0], "letterSpacing": "3px",
                "textTransform": "uppercase", "fontWeight": "600"
            }),
            html.H2(title, style={
                "margin": "4px 0 2px 0", "color": fc, "fontSize": "18px",
                "fontFamily": "Lora, Georgia, serif", "fontWeight": "600"
            }),
            html.P(subtitle, style={
                "margin": "0", "color": fc, "opacity": "0.6",
                "fontSize": "13px", "fontFamily": "Lora, Georgia, serif",
                "fontStyle": "italic"
            }),
        ])
    ], style={
        "display": "flex", "alignItems": "stretch", "background": bg,
        "padding": "16px 20px", "borderRadius": "6px", "marginBottom": "10px",
        "border": f"1px solid {ac[0]}33"
    })

def insight_box(points, tid):
    bg, _, fc, ac = THEMES[tid]
    return html.Div([
        html.Div("— Key Observations", style={
            "fontFamily": "Source Sans 3, sans-serif", "fontSize": "11px",
            "color": ac[0], "letterSpacing": "2px",
            "textTransform": "uppercase", "marginBottom": "10px", "fontWeight": "600"
        }),
        html.Ul([
            html.Li(p, style={
                "marginBottom": "7px", "fontFamily": "Source Sans 3, sans-serif",
                "fontSize": "13.5px", "lineHeight": "1.6", "color": fc
            }) for p in points
        ], style={"margin": "0", "paddingLeft": "18px"})
    ], style={
        "background": bg, "border": f"1px solid {ac[0]}44",
        "borderLeft": f"3px solid {ac[0]}", "borderRadius": "0 6px 6px 0",
        "padding": "16px 20px", "marginTop": "8px"
    })

def row(*figs, tid=1):
    bg = THEMES[tid][0]
    return html.Div([
        dcc.Graph(figure=f, style={"flex": "1", "minWidth": "0"}) for f in figs
    ], style={"display": "flex", "gap": "8px", "background": bg, "padding": "4px 0"})

# ── TOPIC 1 ───────────────────────────────────────────────────────────────────
_, _, _, T1C = THEMES[1]
prog = df["program"].value_counts()
fig1a = px.pie(values=prog.values, names=prog.index, color_discrete_sequence=T1C)
fig1a = fig_layout(fig1a, "Academic Program", 1)

year_counts = df["year"].value_counts().reindex([y for y in YEAR_ORDER if y in df["year"].values])
fig1b = px.bar(x=year_counts.index, y=year_counts.values, labels={"x": "", "y": "Count"},
               color=year_counts.index, color_discrete_sequence=T1C)
fig1b = fig_layout(fig1b, "Year of Study", 1)
fig1b.update_layout(showlegend=False)

gender = df["gender"].value_counts()
fig1c = px.pie(values=gender.values, names=gender.index, color_discrete_sequence=T1C)
fig1c = fig_layout(fig1c, "Gender", 1)

# ── TOPIC 2 ───────────────────────────────────────────────────────────────────
_, _, _, T2C = THEMES[2]
loc = df["primary_location"].value_counts()
fig2a = px.bar(x=loc.index, y=loc.values, labels={"x": "", "y": "Count"},
               color=loc.index, color_discrete_sequence=T2C)
fig2a = fig_layout(fig2a, "Primary Study Location", 2)
fig2a.update_layout(showlegend=False)

lib = df["library_usage"].value_counts().reindex(LIB_ORDER)
fig2b = px.bar(x=lib.index, y=lib.values, labels={"x": "", "y": "Count"},
               color=lib.index, color_discrete_sequence=T2C)
fig2b = fig_layout(fig2b, "Library Usage", 2)
fig2b.update_layout(showlegend=False)

hrs = df["daily_study_hours"].value_counts().reindex(HOURS_ORDER)
fig2c = px.bar(x=hrs.index, y=hrs.values, labels={"x": "", "y": "Count"},
               color=hrs.index, color_discrete_sequence=T2C)
fig2c = fig_layout(fig2c, "Daily Study Hours", 2)
fig2c.update_layout(showlegend=False)

routine = df["study_routine"].value_counts()
fig2d = px.pie(values=routine.values, names=routine.index, color_discrete_sequence=T2C)
fig2d = fig_layout(fig2d, "Study Routine", 2)

# ── TOPIC 3 ───────────────────────────────────────────────────────────────────
_, _, T3F, T3C = THEMES[3]
fig3a = go.Figure()
for col, label, color in zip(
    ["productivity_home","productivity_library","productivity_class"],
    ["Hostel","Library","Class"], T3C[:3]
):
    fig3a.add_trace(go.Box(y=df[col], name=label, marker_color=color, line_color=color))
fig3a = fig_layout(fig3a, "Productivity Distribution", 3)
fig3a.update_layout(yaxis=dict(range=[0,5], gridcolor="#443830"))

means = {"Hostel": df["productivity_home"].mean(),
         "Library": df["productivity_library"][df["productivity_library"] > 0].mean(),
         "Class": df["productivity_class"].mean()}
fig3b = px.bar(x=list(means.keys()), y=list(means.values()),
               color=list(means.keys()), color_discrete_sequence=T3C[:3],
               labels={"x": "", "y": "Mean Rating"})
# fig3b.update_traces(text=[f"{v:.2f}" for v in means.values()], textposition="outside",
#                     textfont=dict(color=T3F))
fig3b = fig_layout(fig3b, "Mean Productivity by Location", 3)
fig3b.update_layout(showlegend=False, yaxis=dict(range=[0,5], gridcolor="#443830"))

# ── TOPIC 4 ───────────────────────────────────────────────────────────────────
_, _, _, T4C = THEMES[4]
fig4_charts = []
for col, title in zip(
    ["productivity_home","productivity_library","productivity_class"],
    ["Hostel Productivity","Library Productivity","Class Productivity"]
):
    grp = df.groupby("primary_location")[col].mean().reset_index()
    fig = px.bar(grp, x="primary_location", y=col,
                 labels={"primary_location": "", col: "Mean Rating"},
                 color="primary_location", color_discrete_sequence=T4C)
    fig.update_layout(showlegend=False, yaxis=dict(range=[0,5]))
    fig = fig_layout(fig, title, 4)
    fig4_charts.append(fig)

# ── TOPIC 5 ───────────────────────────────────────────────────────────────────
_, _, _, T5C = THEMES[5]
dist = df["easily_distracted"].value_counts()
fig5a = px.pie(values=dist.values, names=dist.index, color_discrete_sequence=T5C)
fig5a = fig_layout(fig5a, "Easily Distracted?", 5)

top_dist = count_multi(df["main_distractions"]).sort_values()
fig5b = px.bar(x=top_dist.values, y=top_dist.index, orientation="h",
               labels={"x": "Count", "y": ""},
               color=top_dist.values, color_continuous_scale=["#f0d0d0","#b54040"])
fig5b = fig_layout(fig5b, "Top Distractors", 5)
fig5b.update_layout(coloraxis_showscale=False)

cross5 = pd.crosstab(df["primary_location"], df["easily_distracted"], normalize="index") * 100
fig5c = px.bar(cross5.reset_index().melt(id_vars="primary_location"),
               x="primary_location", y="value", color="easily_distracted",
               barmode="stack", labels={"primary_location": "", "value": "%"},
               color_discrete_sequence=T5C)
fig5c = fig_layout(fig5c, "Distraction by Location (%)", 5)

# ── TOPIC 6 ───────────────────────────────────────────────────────────────────
_, _, _, T6C = THEMES[6]
reasons_go = count_multi(df["library_visit_reasons"].replace("I don't go", np.nan)).sort_values()
fig6a = px.bar(x=reasons_go.values, y=reasons_go.index, orientation="h",
               labels={"x": "Count", "y": ""},
               color=reasons_go.values, color_continuous_scale=["#c8e0dc","#3d7a70"])
fig6a = fig_layout(fig6a, "Why Students Go to the Library", 6)
fig6a.update_layout(coloraxis_showscale=False)

reasons_avoid = count_multi(df["avoid_library_reasons"]).sort_values()
fig6b = px.bar(x=reasons_avoid.values, y=reasons_avoid.index, orientation="h",
               labels={"x": "Count", "y": ""},
               color=reasons_avoid.values, color_continuous_scale=["#c8e0dc","#3d7a70"])
fig6b = fig_layout(fig6b, "Why Students Avoid the Library", 6)
fig6b.update_layout(coloraxis_showscale=False)

grp6 = df.groupby("library_usage")["productivity_library"].mean().reindex(LIB_ORDER).reset_index()
fig6c = px.bar(grp6, x="library_usage", y="productivity_library",
               color="library_usage", color_discrete_sequence=T6C,
               labels={"library_usage": "", "productivity_library": "Mean Rating"})
fig6c.update_traces(text=grp6["productivity_library"].round(2), textposition="outside")
fig6c = fig_layout(fig6c, "Library Productivity vs Usage Frequency", 6)
fig6c.update_layout(showlegend=False, yaxis=dict(range=[0,5]))

# ── TOPIC 7 ───────────────────────────────────────────────────────────────────
_, _, _, T7C = THEMES[7]
exam_int = df["exam_study_intensity"].value_counts().reindex(EXAM_ORDER).dropna()
fig7a = px.bar(x=exam_int.values, y=exam_int.index, orientation="h",
               color=exam_int.index, color_discrete_sequence=T7C,
               labels={"x": "Count", "y": ""})
fig7a = fig_layout(fig7a, "Study Intensity During Exams", 7)
fig7a.update_layout(showlegend=False)

exam_loc = df["exam_location_change"].value_counts()
fig7b = px.pie(values=exam_loc.values, names=exam_loc.index, color_discrete_sequence=T7C)
fig7b = fig_layout(fig7b, "Location Change During Exams?", 7)

# ── TOPIC 8 ───────────────────────────────────────────────────────────────────
_, _, _, T8C = THEMES[8]
valid_years = [y for y in YEAR_ORDER if y in df["year"].values]
ct_yl = pd.crosstab(df["year"], df["primary_location"]).reindex(valid_years).reset_index()
fig8a = px.bar(ct_yl.melt(id_vars="year"), x="year", y="value", color="primary_location",
               barmode="group", labels={"year": "", "value": "Count"}, color_discrete_sequence=T8C)
fig8a = fig_layout(fig8a, "Location by Year", 8)

ct_gl = pd.crosstab(df["gender"], df["primary_location"]).reset_index()
fig8b = px.bar(ct_gl.melt(id_vars="gender"), x="gender", y="value", color="primary_location",
               barmode="group", labels={"gender": "", "value": "Count"}, color_discrete_sequence=T8C)
fig8b = fig_layout(fig8b, "Location by Gender", 8)

yr_prod = df.groupby("year")[["productivity_home","productivity_library","productivity_class"]].mean().reindex(valid_years)
yr_prod.columns = ["Home","Library","Class"]
fig8c = px.bar(yr_prod.reset_index().melt(id_vars="year"), x="year", y="value", color="variable",
               barmode="group", labels={"year": "", "value": "Mean Rating"}, color_discrete_sequence=T8C)
fig8c = fig_layout(fig8c, "Productivity by Year", 8)
fig8c.update_layout(yaxis=dict(range=[0,5]))

hrs_prod = df.groupby("daily_study_hours")[["productivity_home","productivity_library","productivity_class"]].mean().reindex(HOURS_ORDER)
hrs_prod.columns = ["Home","Library","Class"]
fig8d = px.bar(hrs_prod.reset_index().melt(id_vars="daily_study_hours"), x="daily_study_hours", y="value", color="variable",
               barmode="group", labels={"daily_study_hours": "", "value": "Mean Rating"}, color_discrete_sequence=T8C)
fig8d = fig_layout(fig8d, "Productivity by Study Hours", 8)
fig8d.update_layout(yaxis=dict(range=[0,5]))

# ── TOPIC 9 ───────────────────────────────────────────────────────────────────
enc = df.copy()
enc["year_num"]       = enc["year"].map({"Year 1":1,"Year 2":2,"Year 3":3,"Year 4":4,"Final Year":5,"PhD":6})
enc["lib_usage_num"]  = enc["library_usage"].map({"Never":1,"Rarely":2,"Sometimes":3,"Regularly":4})
enc["routine_num"]    = enc["study_routine"].map({"No":1,"During Exams":2,"Yes":3})
enc["distracted_num"] = enc["easily_distracted"].map({"No":1,"Sometimes":2,"Yes":3})

num_cols = ["year_num","lib_usage_num","routine_num",
            "productivity_home","productivity_library","productivity_class",
            "avg_productivity","distracted_num"]
labels   = ["Year","Lib Usage","Routine",
            "Prod Home","Prod Lib","Prod Class","Avg Prod","Distracted"]

corr = enc[num_cols].corr()
corr.index = corr.columns = labels

fig9 = px.imshow(corr, text_auto=".2f",
                 color_continuous_scale=["#3d2a1a","#8b6040","#c8a878","#f0e0b8","#faf4e8","#d0e8d8","#78a888","#3a6858","#1e3830"],
                 zmin=-1, zmax=1, aspect="auto")
fig9 = fig_layout(fig9, "Correlation Heatmap", 9)
fig9.update_layout(height=500)
# ═══════════════════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════════════════
app = Dash(__name__, external_stylesheets=[FONTS])

app.layout = html.Div([

    html.Div([
        html.P("SURVEY ANALYSIS  ·  N = 83 STUDENTS", style={
            "fontFamily": "Source Sans 3, sans-serif", "fontSize": "11px",
            "letterSpacing": "3px", "color": "#c8a878", "margin": "0 0 8px 0"
        }),
        html.H1("Study Location & Productivity", style={
            "fontFamily": "Lora, Georgia, serif", "fontSize": "28px",
            "color": "#f0e6d3", "margin": "0 0 6px 0", "fontWeight": "600"
        }),
        html.P("How ,where students study shapes how productive they feel.", style={
            "fontFamily": "Lora, Georgia, serif", "fontStyle": "italic",
            "fontSize": "14px", "color": "#c8b098", "margin": "0"
        }),
    ], style={
        "background": "#1e1a16", "padding": "32px 40px",
        "marginBottom": "24px", "borderBottom": "3px solid #c8a878"
    }),

    html.Div(style={"padding": "0 24px"}, children=[

        section_header(1, "Demographics", "Who took the survey?"),
        row(fig1a, fig1b, fig1c, tid=1),
        insight_box(["94% respondents are B.Tech students — results mainly reflect their habits.",
                     "72% are from Year 1 and Year 2 — senior student perspective is mostly missing.",
                     "76% are male. "], 1),
        html.Br(),

        section_header(2, "Study Behaviour", "Where, how long and how routinely do students study?"),
        row(fig2a, fig2b, tid=2),
        row(fig2c, fig2d, tid=2),
        insight_box(["67.5% of students primarily study at Hostel — most prefer comfort over discipline.",
                     "Only 18% visit the library regularly — 82% use it sometimes, rarely, or never.",
                     "59% study less than 2 hrs/day — overall study investment is quite low.",
                     "54% follow no fixed study routine."], 2),
        html.Br(),

        section_header(3, "Productivity Ratings by Location", "How productive do students feel at each location?"),
        row(fig3a, fig3b, tid=3),
        insight_box(["Library has the highest mean (~3), followed by Home (~2.5) and Class (~2).",
                     "Despite being the most productive space, majority still don't use the library regularly.",
                     "Box plot shows library ratings are consistently between 3–5 — students who go rarely rate it poorly.",
                     "0 values (not my spot) slightly pull averages down — real ratings skew even higher for library."], 3),
        html.Br(),

        section_header(4, "Primary Location vs Productivity", "Do students rate their own location higher?"),
        row(*fig4_charts, tid=4),
        insight_box(["Students consistently rate their own preferred location highest — classic comfort bias.",
                     "Even hostel students give library a decent rating, showing they know it works better.",
                     "Library students rate their location the highest overall.",
                     "Lab/Classroom gets low ratings across all groups — no one really favors it."], 4),
        html.Br(),

        section_header(5, "Distraction Analysis", "Who gets distracted, and by what?"),
        row(fig5a, fig5b, fig5c, tid=5),
        insight_box(["84% of students face distraction to some level — only 16% are truly focused.",
                     "Mobile phones and social media are the top distractors by a large margin.",
                     "Hostel students face the most distraction — as no extrenal pressure.",
                     "Library students show the least distraction — environment plays a big role in focus."], 5),
        html.Br(),

        section_header(6, "Library Usage Patterns", "Why do students go or not go to the library?"),
        row(fig6a, fig6b, tid=6),
        row(fig6c, tid=6),
        insight_box(["Students go to the library mainly for better focus and a quiet environment.",
                     "Main avoidance reasons: comfort of home, crowding, and time/distance issues.",
                     "Students who use the library more regularly rate their library productivity higher.",
                     "Low library usage is more about habit and comfort than the library being ineffective."], 6),
        html.Br(),

        section_header(7, "Exam Behaviour", "Does study intensity or location change during exams?"),
        row(fig7a, fig7b, tid=7),
        insight_box(["61% of students study more during exams — almost everyone ramps up effort.",
                     "51% don't change their study location even during exams.",
                     "Among those who shift, a good portion move to the library during exam time.",
                     "Exam pressure increases study time but not always the push to find a better environment."], 7),
        html.Br(),

        section_header(8, "Cross Analysis", "Year and gender vs location and productivity"),
        row(fig8a, fig8b, tid=8),
        row(fig8c, fig8d, tid=8),
        insight_box(["Year 1 & 2 mostly stick to hostel; Year 3 shows slightly more library usage.",
                     "Female students show higher tendency to study at the library compared to males.",
                     "Students who study more hours/day score higher productivity across all locations.",
                     "Year 3 students show slightly higher productivity — possibly better habits by then."], 8),
        html.Br(),

        section_header(9, "Correlation Heatmap", "How do all variables relate to each other?"),
        html.Div(dcc.Graph(figure=fig9), style={"background": THEMES[9][0]}),
        insight_box(["Library usage and library productivity are positively correlated — use it more, feel more productive.",
                     "Distraction level doesn't strongly correlate with productivity — a somewhat surprising finding.",
                     "No single variable strongly predicts productivity alone — it is a mix of habits and environment."], 9),

        html.Br(), html.Br(),
    ])
], style={"fontFamily": "Source Sans 3, sans-serif", "background": "#f5f0eb", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=True)