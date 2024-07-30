
# import libraries
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import pandas as pd

# import data from shared
from shared import app_dir, df

ui.page_opts(title="UK General Election Results", fillable=True)

with ui.sidebar(title="Filter controls"):
    ""
    # ui.input_checkbox_group(
    #     "commons_speaker",
    #     "Standing as Common's Speaker",
    #     {
    #         "True": True,
    #         "False": False
    #     }
    # )


with ui.layout_column_wrap(fill=False):

    with ui.value_box(showcase=icon_svg("people-group")):
        "Electorate, July 2024"

        @render.text
        def electorate():
            result = df[
                df["General election polling date"]=="2024-07-04"]["Total electorate in general election"].max()
            return f"{result}"

    with ui.value_box(showcase=icon_svg("check-to-slot")):
        "Voters, July 2024"

        @render.text
        def voters():
            result = df[
                df["General election polling date"]=="2024-07-04"]["Total valid votes in general election"].max()
            return f"{result}"

    with ui.value_box(showcase=icon_svg("map-location-dot")):
        "Constituencies, July 2024"

        @render.text
        def constituencies():
            result = df[
                df["General election polling date"]=="2024-07-04"]["Constituency geographic code"].nunique()
            return f"{result}"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("UK General Election Candidates")

        @render.data_frame
        def summary_statistics():
            cols = [
                "General election polling date",
                "Constituency name",
                "Candidate result position",
                "Candidate family name",
                "Candidate given name",
                "Main party name",
                "Main party abbreviation",
                "Candidate vote count",
                "Candidate vote share",
                "Candidate vote change",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df
    # filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
