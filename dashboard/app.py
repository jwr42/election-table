# import libraries
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import pandas as pd
from shiny.ui import input_checkbox

# import data from shared
from shared import app_dir, df

ui.page_opts(title="UK General Election Results", fillable=True)

with ui.sidebar(title="Filter Controls"):
    ui.input_checkbox_group(
        "year",
        "Select Elections",
        {"2024": "", "2019": "", "2017": ""},
        selected=["2024", "2019"],
    )
    ui.input_selectize("constituencies", "Select Constituencies", {}, selected=[])
    ui.input_switch("speaker", "Include Speaker", value=True)


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("people-group")):
        "Electorate, July 2024"

        @render.text
        def electorate():
            result = df[df["General election polling date"] == "2024-07-04"][
                "Total electorate in general election"
            ].max()
            return f"{result}"

    with ui.value_box(showcase=icon_svg("check-to-slot")):
        "Voters, July 2024"

        @render.text
        def voters():
            result = df[df["General election polling date"] == "2024-07-04"][
                "Total valid votes in general election"
            ].max()
            return f"{result}"

    with ui.value_box(showcase=icon_svg("map-location-dot")):
        "Constituencies, July 2024"

        @render.text
        def constituencies():
            result = df[df["General election polling date"] == "2024-07-04"][
                "Constituency geographic code"
            ].nunique()
            return f"{result}"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("UK General Election Candidates")

        @render.data_frame
        def table():
            return render.DataGrid(filtered_df())


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = (
        df[
            [
                "General election polling date",
                "Constituency name",
                "Candidate result position",
                "Majority",
                "Candidate family name",
                "Candidate given name",
                "Main party abbreviation",
                "Candidate vote count",
                "Candidate vote share",
            ]
        ].rename(
            columns={
                "General election polling date": "Date",
                "Constituency name": "Constituency",
                "Candidate result position": "Result Position",
                "Majority": "Majority",
                "Candidate family name": "Surname",
                "Candidate given name": "First Name",
                "Main party abbreviation": "Party",
                "Candidate vote count": "Vote Count",
                "Candidate vote share": "Vote Share",
            }
        )
        # .fillna("")
    )
    # filt_df = filt_df[filt_df["Candidate is standing as Commons Speaker"].isin(input.commons_speaker())]
    return filt_df
