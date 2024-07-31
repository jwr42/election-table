# import libraries
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import pandas as pd
from shiny.ui import input_checkbox

# import data from shared
from shared import app_dir, df

ui.page_opts(title="🗳️ UK General Election Results", fillable=True)

with ui.sidebar(title="Filter Controls"):
    ui.input_checkbox_group(
        "select_year",
        "",
        {
            "2024-07-04": "July 2024",
            "2019-12-12": "December 2019",
            "2017-06-08": "June 2017",
            "2015-05-07": "May 2015",
        },
        selected=["2024-07-04", "2019-12-12", "2017-06-08", "2015-05-07"],
    )
    ui.input_selectize(
        "select_constituencies",
        "Select Constituencies",
        {i: i for i in df["Constituency name"].unique().tolist()},
        multiple=True,
    )
    ui.input_switch("select_speaker", "Include Speaker", value=True)


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("people-group"), theme="text-black"):
        "Electorate, July 2024"

        @render.text
        def electorate():
            result = df[df["General election polling date"] == "2024-07-04"][
                "Total electorate in general election"
            ].max()
            return f"{result:,d}"

    with ui.value_box(showcase=icon_svg("check-to-slot"), theme="text-black"):
        "Voters, July 2024"

        @render.text
        def voters():
            result = df[df["General election polling date"] == "2024-07-04"][
                "Total valid votes in general election"
            ].max()
            return f"{result:,d}"

    with ui.value_box(showcase=icon_svg("map-location-dot"), theme="text-black"):
        "Constituencies, July 2024"

        @render.text
        def constituencies():
            result = df[df["General election polling date"] == "2024-07-04"][
                "Constituency geographic code"
            ].nunique()
            return f"{result:,d}"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("UK General Election Candidates")

        @render.data_frame
        def table():
            cols = [
                "Polling Day",
                "Constituency",
                "Position",
                "Surname",
                "First Name",
                "Party",
                "Vote Count",
                "Vote Share (%)",
                "Majority",
            ]
            return render.DataGrid(filtered_df()[cols])


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    # select and name columns
    filt_df = df[
        [
            "General election polling date",
            "Constituency name",
            "Candidate result position",
            "Candidate family name",
            "Candidate given name",
            "Main party abbreviation",
            "Candidate vote count",
            "Candidate vote share",
            "Majority",
            "Candidate is standing as Commons Speaker",
        ]
    ].rename(
        columns={
            "General election polling date": "Polling Day",
            "Constituency name": "Constituency",
            "Candidate result position": "Position",
            "Majority": "Majority",
            "Candidate family name": "Surname",
            "Candidate given name": "First Name",
            "Main party abbreviation": "Party",
            "Candidate vote count": "Vote Count",
            "Candidate vote share": "Vote Share (%)",
            "Candidate is standing as Commons Speaker": "Speaker",
        }
    )

    # format individual columns
    filt_df["Vote Share (%)"] = filt_df["Vote Share (%)"].apply(
        lambda x: round(x * 100, 2)
    )
    filt_df["Speaker"] = filt_df["Speaker"].replace({True: "Yes", False: ""})

    # filter using conditions in sidebar
    if input.select_speaker() != True:
        filt_df = filt_df[filt_df["Speaker"] != "Yes"]

    # filt_df = filt_df[filt_df["Polling Day"].isin(input.select_date())]

    # filt_df = filt_df[filt_df["Candidate is standing as Commons Speaker"].isin(input.commons_speaker())]
    return filt_df
