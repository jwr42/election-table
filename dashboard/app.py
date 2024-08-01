# import libraries
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import pandas as pd
from shiny.ui import input_checkbox, markdown
import io

# import data from shared
from shared import app_dir, df

ui.page_opts(title="UK General Election Candidate Results", fillable=True)

with ui.sidebar(title="Filter Controls"):
    # Sidebar selection for the last four general elections
    ui.input_checkbox_group(
        "select_date",
        "",
        {
            "2024-07-04": "July 2024",
            "2019-12-12": "December 2019",
            "2017-06-08": "June 2017",
            "2015-05-07": "May 2015",
        },
        selected=["2024-07-04"],
    )
    ui.input_selectize(
        "select_constituencies",
        "Select Constituencies",
        {i: i for i in df["Constituency name"].unique().tolist()},
        multiple=True,
    )
    ui.input_slider(
        "select_result_position",
        "Result Positions",
        min=1,
        max=df["Candidate result position"].max(),
        value=df["Candidate result position"].max(),
    )
    ui.input_selectize(
        "select_parties",
        "Select Parties",
        {
            "Lab": "Labour",
            "Con": "Conservatives",
            "LD": "Liberal Democrats",
            "Green": "Green",
            "RUK": "Reform UK",
            "SNP": "Scottish National Party",
            "PC": "Plaid Cymru",
        },
        multiple=True,
    )
    ui.input_switch("select_speaker", "Include Speaker", value=True)

    @render.download(label="Download Table", filename="election_results.csv")
    def download():
        with io.BytesIO() as buf:
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
            filtered_df()[cols].to_csv(buf)
            yield buf.getvalue()

    ui.markdown("Data Source: [parliament.uk](https://electionresults.parliament.uk)")


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("people-group"), theme="text-black"):
        "Candidates, July 2024"

        @render.text
        def electorate():
            result = len(df[df["General election polling date"] == "2024-07-04"])
            return f"{result:,d}"

    with ui.value_box(showcase=icon_svg("check-to-slot"), theme="text-black"):
        "Ballots Cast, July 2024"

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
                "Surname",
                "First Name",
                "Constituency",
                "Party",
                "Polling Day",
                "Vote Count",
                "Vote Share (%)",
                "Position",
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
            "Candidate given name": "First Name",
            "Candidate family name": "Surname",
            "Constituency name": "Constituency",
            "Main party abbreviation": "Party",
            "General election polling date": "Polling Day",
            "Candidate vote count": "Vote Count",
            "Candidate result position": "Position",
            "Majority": "Majority",
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
    filt_df = filt_df[filt_df["Polling Day"].isin(input.select_date())]
    if input.select_constituencies() != ():
        filt_df = filt_df[filt_df["Constituency"].isin(input.select_constituencies())]
    filt_df = filt_df[filt_df["Position"] <= input.select_result_position()]
    if input.select_parties() != ():
        filt_df = filt_df[filt_df["Party"].isin(input.select_parties())]
    if input.select_speaker() != True:
        filt_df = filt_df[filt_df["Speaker"] != "Yes"]

    # filt_df = filt_df[filt_df["Candidate is standing as Commons Speaker"].isin(input.commons_speaker())]
    return filt_df
