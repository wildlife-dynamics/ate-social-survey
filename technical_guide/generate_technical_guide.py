"""
Generate the ATE Social Survey Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: ate_survey_technical_guide.pdf (written next to this script and copied to docs/assets/)
"""

import shutil
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = str(Path(__file__).with_name("ate_survey_technical_guide.pdf"))

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

TH       = _style("TableHeader", fontSize=9, leading=14, textColor=WHITE,
                  fontName="Helvetica-Bold")

def c(text, style=BODY):
    return Paragraph(str(text), style)

def make_table(data, col_widths, header_row=True):
    # Paragraph cells ignore TableStyle TEXTCOLOR, so the header row gets its own style
    wrapped = [[c(cell, TH if header_row and i == 0 else BODY) if isinstance(cell, str) else cell
                for cell in row]
               for i, row in enumerate(data)]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"ATE Social Survey — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("ATE Social Survey", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Community attitude, knowledge, and sentiment analysis towards elephants", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>social_survey</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>social_survey</b> workflow processes Amboseli Trust for Elephants (ATE) "
      "community questionnaire responses recorded as <b>atequestionnaire_rep</b> events "
      "in EarthRanger. It cleans and relabels the survey answers, produces demographic, "
      "attitude, and knowledge charts, computes a per-respondent elephant sentiment "
      "score, compares sentiment across demographic groups, maps respondents over "
      "Amboseli context layers, and assembles everything into an interactive dashboard "
      "and a Word report."),
    sp(4),
    p("This guide is written directly from <b>spec.yaml</b>. The workflow is compiled "
      "with <b>wt-compiler</b> (see <b>pixi.toml</b>) into the "
      "<b>ecoscope-workflows-social-survey-workflow/</b> package."),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Dashboard",              "1",  "53 widgets: 50 charts and 3 maps (gather_dashboard)"],
            ["Pie charts",             "11", "Demographics, threats, feelings about wildlife, elephant encounters"],
            ["Bar charts (binned)",    "9",  "Age, household size, livestock counts, land owned and farmed"],
            ["Bar charts (Yes/No)",    "10", "Behaviour and mitigation questions"],
            ["Bar charts (True/False)","8",  "Elephant knowledge questions"],
            ["Likert chart",           "1",  "9 agree/disagree attitude statements"],
            ["Boxplots",               "5",  "Sentiment by gender, age group, education, tribe, marital status"],
            ["Tukey HSD plots",        "4",  "Pairwise sentiment comparisons by gender, marital status, age group, education"],
            ["Scatter plots (OLS)",    "2",  "Sentiment against household size and age"],
            ["Maps",                   "3",  "Survey locations, gender, attitude category"],
            ["Data files",             "3",  "survey-events.gpkg, demographic-data.parquet, elephant-sentiment-table.gpkg"],
            ["Word report",            "1",  "social_survey_report.docx"],
        ],
        [4.5*cm, 1.8*cm, W - 6.3*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies & Configuration"),
    hr(),
    h2("2.1  User-configurable form"),
    p("Only three sections appear in the run form; everything else is fixed "
      "in <b>spec.yaml</b> via <b>partial</b> arguments."),
    make_table(
        [
            ["Section", "Task", "Fields"],
            ["Workflow Details", "set_workflow_details", "Workflow Name (required), Workflow Description"],
            ["Time Range", "set_time_range",
             "Since, Until (required), Timezone, Time Format (advanced; default %d %b %Y %H:%M:%S)"],
            ["Connect to EarthRanger", "set_er_connection", "Data Source"],
        ],
        [4*cm, 3.8*cm, W - 7.8*cm],
    ),
    sp(6),
    h2("2.2  Groupers"),
    p("<b>set_groupers</b> is fixed to <b>groupers: []</b>. All survey records are "
      "processed as a single dataset, with no per-group split. The empty grouper list "
      "is passed through to the dashboard only."),
    sp(6),
    h2("2.3  Base maps"),
    p("Two tile layers are fixed via <b>set_base_maps_pydeck</b>:"),
    make_table(
        [
            ["Layer", "URL (abbreviated)", "Opacity"],
            ["ArcGIS World Hillshade",
             "server.arcgisonline.com/…/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}",
             "1.0"],
            ["ArcGIS World Street Map",
             "server.arcgisonline.com/…/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
             "0.15"],
        ],
        [4*cm, W - 6.5*cm, 2.5*cm],
    ),
    p("Both layers use max_zoom: 20."),
    sp(6),
    h2("2.4  Files downloaded at runtime"),
    p("Four files are downloaded from Dropbox with "
      "<b>ecoscope_workflows_ext_ste.tasks.io.fetch_and_persist_file</b> "
      "(overwrite_existing: false, retries: 3, unzip: false) into "
      "<b>ECOSCOPE_WORKFLOWS_RESULTS</b>:"),
    make_table(
        [
            ["Task id", "File", "Purpose"],
            ["ambo_ranch_layers", "amboseli_ranch_conservancies_layers.gpkg",
             "Land-use zones, coloured by the land_use column"],
            ["ambo_bound_fence", "amboseli_group_ranch_boundaries_x_electric_fence.gpkg",
             "Filtered into two layers: land_use == 'Ranch boundaries' and land_use == 'Electric Fence'"],
            ["ambo_conservancies", "amboseli_group_ranch_boundaries.gpkg",
             "Loaded and reprojected. Not currently drawn on any map"],
            ["download_word_template", "ate_survey_template_280857_updated.docx",
             "docxtpl/Jinja Word template for the report"],
        ],
        [3.6*cm, 5.8*cm, W - 9.4*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. SURVEY DATA PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Survey Data Pipeline"),
    hr(),
    h2("3.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",              "get_events"],
            ["Event type",        "atequestionnaire_rep"],
            ["Columns retained",  "id, time, event_type, event_category, reported_by, "
                                  "serial_number, geometry, created_at, event_details"],
            ["raise_on_empty",    "true (the run fails if no events are found)"],
            ["include_details",   "true"],
            ["include_display_values", "true"],
            ["force_point_geometry", "true"],
            ["include_null_geometry", "false"],
            ["include_updates / include_related_events", "false / false"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("3.2  Flattening and renaming"),
    make_table(
        [
            ["Step (task id)", "Task", "What it does"],
            ["extract_event_date", "extract_column_as_type",
             "Adds a <b>date</b> column from <b>time</b>"],
            ["process_survey_details", "process_events_details (ext-custom)",
             "Replaces event_details choice values with their EarthRanger display titles "
             "(map_to_titles: true, ordered: true)"],
            ["normalize_survey_events", "normalize_json_column",
             "Flattens event_details into event_details__* columns "
             "(skip_if_not_exists, sort_columns)"],
            ["drop_survey_prefix", "drop_column_prefix (ext-custom)",
             "Strips the event_details__ prefix (duplicate_strategy: keep_original)"],
            ["map_survey_columns", "map_columns",
             "Drops event_type and event_type_display; renames about 80 bilingual question "
             "headings to English only (e.g. <i>What is your Age? (Kaja larin liata?)</i> "
             "→ <i>What is your Age</i>). raise_if_not_found: false"],
        ],
        [3.8*cm, 4.2*cm, W - 8*cm],
    ),
    note("Because <b>raise_if_not_found</b> is false, a question whose heading changes "
         "in EarthRanger won't fail the run. Its column simply keeps the "
         "original bilingual heading, and any downstream chart that expects the English "
         "name is skipped."),
    sp(6),
    h2("3.3  Record exclusion"),
    p("Rows are filtered with <b>ecoscope_workflows_ext_ste.tasks.filter.filter_rows</b> "
      "(reset_index: true), in this order:"),
    make_table(
        [
            ["Task id", "Column", "Rule", "Keeps"],
            ["exclude_invalid_serial", "serial_number", "ne 46283", "Everything except the known invalid entry"],
            ["exclude_invalid_age", "What is your Age", "gt 18", "Respondents older than 18"],
            ["exclude_invalid_household", "How many People are there in your Household",
             "gt 1", "Households of 2 or more people"],
        ],
        [4*cm, 4.2*cm, 2*cm, W - 10.2*cm],
    ),
    note("These filters run before missing values are filled, so rows with a blank "
         "age or household size are also dropped."),
    sp(6),
    h2("3.4  Missing values and type conversion"),
    make_table(
        [
            ["Task id", "Task", "Columns", "Behaviour"],
            ["fill_missing_columns", "fill_missing_values (ext-mnc)",
             "11 numeric columns: livestock counts (cattle, dogs, donkeys, sheep/goats, "
             "other animals), household size, land owned and farmed, age, "
             "participant_num_cows, participant_num_shoats", "fill 0"],
            ["convert_cols_numeric", "convert_column_values_to_numeric", "Same 11", "to numeric"],
            ["fill_string_columns", "fill_missing_values (ext-mnc)",
             "About 75 text/choice columns", "fill 'No Response'"],
            ["convert_num_int", "convert_columns_to_int (ext-mnc)", "Same 11 numeric",
             "errors: coerce, fill_value: 0"],
        ],
        [3.4*cm, 3.8*cm, W - 9.6*cm, 2.4*cm],
    ),
    sp(6),
    h2("3.5  Answer relabelling"),
    p("A chain of <b>replace_column_values</b> tasks (inplace: true, errors: ignore) "
      "strips the Maa translation from each answer and merges variants:"),
    make_table(
        [
            ["Task id", "Columns", "Mapping (raw → label)"],
            ["replace_yes_no", "11 Yes/No questions",
             "Yes (ee)→Yes, No (aa)→No, I Don’t Know (Mayolo)→I Don’t Know; "
             "No Response and Not Applicable unchanged"],
            ["replace_true_false", "7 knowledge statements",
             "True, False, I Don’t Know, No Response (unchanged)"],
            ["replace_agree_disagree", "11 attitude statements",
             "Strongly Agree (tipat ake)→Strongly Agree, Agree (tipat)→Agree, "
             "Neutral (tipat nemetipat)→Neutral, Disagree (meetipat)→Disagree, "
             "Strongly Disagree (meetipat pi)→Strongly Disagree, I Don’t Know (mayolo)→I Don’t Know"],
            ["replace_gender_participant", "Gender of Participant", "Unknown→No Response"],
            ["replace_ele_area", "Having Elephants in this Area is",
             "Very Good / Good / Neutral / Bad / Very Bad / I Don’t Know / Prefer not to Answer"],
            ["replace_how_often", "How often seen elephants in the last year",
             "Every Day / Week / Month / Few Months / Year, Never, I Don’t Know"],
            ["replace_overall_wildlife", "Overall feelings about wildlife",
             "Strongly Like / Like / Neutral / Dislike / Strongly Dislike, I Don’t Know, Prefer not to Answer"],
            ["replace_age_groups", "What is your Age Group",
             "Senior Elder, Junior Elder, Elder → Elder; Moran, Kidemi Mamas unchanged"],
            ["replace_highest_level", "Highest level of completed education",
             "None→No Response; Primary, Secondary, University, Post Grad unchanged"],
            ["replace_marital_status", "What is your marital status",
             "About 90 free-text spellings (English and Maa: iama, iamishe, eamishe, itu …) "
             "→ Married, Single, Divorced, or No Response. Widowed → Single; "
             "Separated → Married"],
        ],
        [3.8*cm, 4.2*cm, W - 8*cm],
    ),
    sp(4),
    p("The cleaned table is saved as <b>survey-events.gpkg</b> (task events_gpkg)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. PIE CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Pie Charts"),
    hr(),
    p("Task: <b>ecoscope_workflows_ext_wwf_virunga.tasks.plot._plot.draw_pie_chart</b>, "
      "one per question, with value_column = label_column = the question. "
      "textinfo: percent+label+value, font_size 10, legend shown. Each is saved with "
      "<b>persist_text</b>."),
    make_table(
        [
            ["Widget", "Question", "Output file (.html / .png)"],
            ["0",  "What is your Age Group", "what_is_your_age_group_pie_chart"],
            ["1",  "What is your Arrangement for the Land that You are Farming On", "what_is_the_land_arrangement_pie_chart"],
            ["2",  "What is your Highest Level of Completed Education", "highest_level_of_education_pie_chart"],
            ["3",  "What is your Tribe", "what_is_your_tribe_pie_chart"],
            ["4",  "Greatest Threat to Successful Crop Production", "greatest_threat_to_crop_production_pie_chart"],
            ["5",  "Greatest Threat to your Livestock", "greatest_threat_to_livestock_pie_chart"],
            ["6",  "What is your marital status", "what_is_your_marital_status_pie_chart"],
            ["7",  "Overall feelings about wildlife", "overall_feeling_about_wildlife_pie_chart"],
            ["8",  "How often seen elephants in the last year", "how_often_have_you_seen_elephants_in_the_last_year_pie_chart"],
            ["9",  "How do you feel when an elephant is speared or poisoned in retaliation", "how_do_you_feel_witnessing_elephant_harmed_pie_chart"],
            ["10", "Gender of Participant", "gender_of_participant_pie_chart"],
        ],
        [1.4*cm, 7*cm, W - 8.4*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. BINNING & BAR CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Binning & Bar Charts"),
    hr(),
    h2("5.1  Numeric binning"),
    p("Nine chained <b>apply_classification</b> tasks add a bin column for each numeric "
      "answer using <b>natural_breaks, k = 5</b>. <b>order_categorical_by_number</b> "
      "then orders every bin column numerically so the bars sort correctly."),
    make_table(
        [
            ["Input column", "Bin column", "Labels"],
            ["What is your Age", "age_bins", "ranges, 0 dp"],
            ["How many Cattle does Your Household Own", "cattle_bins", "ranges, 0 dp"],
            ["How many Dogs does Your Household Own", "dog_bins", "fixed: 0, 0 - 1, 1 - 2, 2 - 4, 4 - 8"],
            ["How many Donkey does Your Household Own", "donkey_bins", "fixed: 0, 0 - 3, 3 - 7, 7 - 25, 25 - 56"],
            ["How many Other Animals does Your Household Own", "other_animals_bins", "ranges, 0 dp"],
            ["How many People are there in your Household", "other_people_bins", "ranges, 0 dp"],
            ["How many Sheep/Goats does Your Household Own", "sheep_goats_bins", "ranges, 0 dp"],
            ["How much Land do you Grow Crops on each Season (in Acres)", "land_grown_crops_bins", "ranges, 0 dp"],
            ["How much Land do you Own (in Acres)", "land_owned_bins", "ranges, 0 dp"],
        ],
        [7*cm, 3.6*cm, W - 10.6*cm],
    ),
    note("The dog and donkey labels are hard-coded from the current data distribution. "
         "For those two charts, the '0' bin is filtered out (filter_df ne '0') and the "
         "column is converted back to string so the unused category disappears."),
    sp(6),
    h2("5.2  Bar chart settings"),
    p("Task: <b>ecoscope_workflows_ext_wwf_virunga.tasks.plot.draw_bar_chart</b>. Every "
      "bar chart counts respondents (column id, agg_func: count) per category, in grouped "
      "mode, with marker colour #6495ed, labels shown, background #f5f5f5, "
      "and no legend."),
    sp(6),
    h2("5.3  Bar chart inventory"),
    make_table(
        [
            ["Widget", "Source", "Category", "Output file"],
            ["11", "binned", "age_bins", "age_bins_bar_chart"],
            ["12", "binned", "cattle_bins", "cattle_bins_bar_chart"],
            ["13", "binned", "dog_bins (non-zero)", "dog_bins_bar_chart"],
            ["14", "binned", "donkey_bins (non-zero)", "donkey_bins_bar_chart"],
            ["15", "binned", "other_animals_bins", "other_animal_bins_bar_chart"],
            ["16", "binned", "other_people_bins", "other_people_bins_bar_chart"],
            ["17", "binned", "sheep_goats_bins", "sheep_goats_bins_bar_chart"],
            ["18", "binned", "land_grown_crops_bins", "land_grown_crops_bins_bar_chart"],
            ["19", "binned", "land_owned_bins", "land_owned_bins_bar_chart"],
            ["20", "Yes/No", "Benefit from the KCCDT Big Life Electric Fence", "do_you_benefit_from_electric_fence_bar_chart"],
            ["21", "Yes/No", "Choose routes/schedules/water based on elephant presence", "activities_altered_elephant_presence_bar_chart"],
            ["22", "Yes/No", "Protect where you get water from elephants", "protect_water_from_elephants_bar_chart"],
            ["23", "Yes/No", "See more elephants now compared to the past", "more_eles_past_bar_chart"],
            ["24", "Yes/No", "Measures to prevent crop damage", "family_protection_eles_bar_chart"],
            ["25", "Yes/No", "Measures to prevent injuring livestock", "ffamily_protection_eles_livestock_bar_chart"],
            ["26", "Yes/No", "Signs of illness in wild animals", "illness_wild_bar_chart"],
            ["27", "Yes/No", "Involved in or witnessed an elephant being harmed", "elephant_harmed_bar_chart"],
            ["28", "Yes/No", "Report conflict with elephants", "report_elephant_conflict_bar_chart"],
            ["29", "Yes/No", "Interested in a community dialogue", "elephant_community_dialogue_bar_chart"],
            ["30", "True/False", "Male with facial secretion may be more aggressive", "male_elephant_secretion_bar_chart"],
            ["31", "True/False", "Raised trunk means aware of a person", "elephant_human_awareness_bar_chart"],
            ["32", "True/False", "Head shaking means annoyed", "elephant_shake_head_bar_chart"],
            ["33", "True/False", "Can smell and hear from far away", "elephant_smell_far_away_bar_chart"],
            ["34", "True/False", "Move seasonally for food and water", "elephants_move_seasonally_bar_chart"],
            ["35", "True/False", "Females are protective of their young", "female_elephants_protective_bar_chart"],
            ["36", "True/False", "Females live in family groups", "female_elephants_family_groups_bar_chart"],
            ["37", "True/False", "Involved in or witnessed an elephant being harmed", "witness_elephant_harm_bar_chart"],
        ],
        [1.4*cm, 1.9*cm, 6.4*cm, W - 9.7*cm],
    ),
    note("Widget 37 charts the same question as widget 27. It sits in the True/False "
         "group, but the answers are Yes/No."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. DEMOGRAPHIC TABLE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Demographic Table"),
    hr(),
    p("Task: <b>format_demographic_table</b>, run on the binned table with these "
      "columns of interest:"),
    bullet("Gender of Participant"),
    bullet("What is your Age"),
    bullet("What is your Tribe"),
    bullet("How many People are there in your Household"),
    bullet("What is your Highest Level of Completed Education"),
    sp(4),
    p("The result is saved with <b>persist_df</b> (filetype: geoparquet) as "
      "<b>demographic-data.parquet</b>. The Word report reads it back from the results "
      "directory by that exact name."),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. LIKERT & SENTIMENT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Likert Chart & Elephant Sentiment Score"),
    hr(),
    h2("7.1  Statements used"),
    p("<b>retain_agree_disagree</b> keeps id, time, serial_number, geometry, five "
      "demographic columns (age group, education, tribe, marital status, gender), "
      "household size, age, and the nine statements below. The two 'I Receive Benefits…' "
      "statements are relabelled in section 3.5 but are <b>not</b> used here."),
    make_table(
        [
            ["Direction", "Statement"],
            ["Negative", "Elephants Hurt Members of my Community"],
            ["Negative", "Elephants should only Live Inside the Parks"],
            ["Negative", "It is Acceptable to Harm Elephants if they have Damaged Physical Property or Livestock"],
            ["Negative", "It is Acceptable to Harm Elephants if they have Hurt People"],
            ["Negative", "Elephants have a Negative Effect on my Income/Livelihood"],
            ["Negative", "Elephants Negatively Impact my Emotional Wellbeing"],
            ["Positive", "Elephants are Important for a Healthy Ecosystem"],
            ["Positive", "It is Important for Elephants to Live in this Area"],
            ["Positive", "It is Possible for both Humans and Elephants to Live Together in this Area"],
        ],
        [2.6*cm, W - 2.6*cm],
    ),
    sp(6),
    h2("7.2  Likert chart (widget 38)"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task", "draw_likert_chart"],
            ["response_order", "Strongly Disagree → Disagree → Neutral → Agree → Strongly Agree"],
            ["Colours", "Strongly Disagree #2c5282, Disagree #4299e1, Neutral / No Response / "
                        "I Don’t Know #a0aec0, Agree #ed8936, Strongly Agree #c05621"],
            ["show_percentage / sort_questions / sort_by", "true / false / positive"],
            ["Output", "ele_sentiment_chart.html / .png"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("7.3  Scoring"),
    make_table(
        [
            ["Answer", "Negative statements", "Positive statements"],
            ["Strongly Disagree", "5", "1"],
            ["Disagree", "4", "2"],
            ["Neutral", "3", "3"],
            ["Agree", "2", "4"],
            ["Strongly Agree", "1", "5"],
            ["I Don’t Know / No Response", "0", "0"],
        ],
        [5.5*cm, (W - 5.5*cm) / 2, (W - 5.5*cm) / 2],
    ),
    sp(4),
    p("Higher scores always mean a more positive attitude towards elephants. The steps "
      "that follow:"),
    make_table(
        [
            ["Task id", "Task", "Result"],
            ["replace_negative / replace_positive", "replace_column_values", "Answers → scores (table above)"],
            ["convt_ele_int", "convert_columns_to_int", "Scores as int (coerce, fill 0)"],
            ["create_sentiment_score", "apply_arithmetic_operation_over_rows (ext-mnc)",
             "sentiment_score = sum of the 9 scores"],
            ["sentiment_score_mean", "apply_arithmetic_operation_over_columns",
             "sentiment_score_mean = mean of the 9 scores"],
            ["round_sentiment_score", "round_column_values", "Rounded to 1 decimal place"],
            ["sentiment_bins", "apply_classification",
             "sentiment_bins: equal_interval, k = 5, range labels, 0 dp"],
            ["replace_bins_mapping", "replace_column_values",
             "0 - 1 → Strongly Disagree, 1 - 2 → Disagree, 2 - 3 → Neutral, "
             "3 - 4 → Agree, 4 - 5 → Strongly Agree"],
        ],
        [4.4*cm, 5*cm, W - 9.4*cm],
    ),
    note("'I Don’t Know' and 'No Response' score 0 and are <b>included</b> in the mean, "
         "so respondents who skip statements are pulled towards the low "
         "(negative) end of the scale."),
    note("The equal-interval bins are fitted to the observed range of "
         "sentiment_score_mean, not a fixed 0–5 scale. The category mapping only "
         "matches when the rounded bin labels come out as 0 - 1 … 4 - 5. Any other "
         "label is left unmapped and appears grey on the attitude map."),
    sp(4),
    p("The scored table (after category mapping) is saved as "
      "<b>elephant-sentiment-table.gpkg</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. STATISTICAL COMPARISONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Statistical Comparisons"),
    hr(),
    p("Every comparison uses <b>sentiment_score_mean</b> from the "
      "<b>sentiment_bins</b> output."),
    sp(4),
    h2("8.1  Boxplots"),
    p("Task: <b>ecoscope_workflows_ext_big_life.tasks.results.draw_boxplot</b> "
      "(vertical, boxmode group, no points, colour #7eb0d5)."),
    make_table(
        [
            ["Widget", "x-axis", "Output file"],
            ["39", "Gender of Participant", "gender_boxplot_chart"],
            ["40", "What is your Age Group", "age_group_boxplot_chart"],
            ["41", "What is your Highest Level of Completed Education", "education_level_boxplot_chart"],
            ["42", "What is your Tribe", "tribe_boxplot_chart"],
            ["43", "What is your marital status", "marital_status_boxplot_chart"],
        ],
        [1.6*cm, 8*cm, W - 9.6*cm],
    ),
    sp(6),
    h2("8.2  Tukey HSD"),
    p("For each factor, <b>filter_df</b> removes 'No Response'. "
      "<b>compute_tukey_comparisons</b> (confidence_level 0.95) then runs the pairwise test and "
      "<b>ecoscope_workflows_ext_ate.tasks.results.draw_tukey_chart</b> plots the "
      "mean differences (significant #ff6b6b, non-significant #4ecdc4)."),
    make_table(
        [
            ["Widget", "Group column", "Output file"],
            ["44", "Gender of Participant", "gender_tukey_chart"],
            ["45", "What is your marital status", "marital_status_tukey_chart"],
            ["46", "What is your Age Group", "age_group_tukey_chart"],
            ["47", "What is your Highest Level of Completed Education", "education_tukey_chart"],
        ],
        [1.6*cm, 8*cm, W - 9.6*cm],
    ),
    note("A Tukey comparison needs at least two groups with more than one "
         "respondent each. With a narrow time range this can fail or skip."),
    sp(6),
    h2("8.3  Scatter plots with OLS trendline"),
    p("Task: <b>ecoscope_workflows_ext_ate.tasks.results.draw_scatter_chart</b>, "
      "markers only, with a red solid OLS trendline (width 2)."),
    make_table(
        [
            ["Widget", "x-axis", "Output file"],
            ["48", "How many People are there in your Household", "household_sentiment_scatter_chart"],
            ["49", "What is your Age", "age_sentiment_scatter_chart"],
        ],
        [1.6*cm, 8*cm, W - 9.6*cm],
    ),
    note("The previous version's Type II ANOVA table (anova_results.csv) is no "
         "longer produced."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. MAPS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Maps"),
    hr(),
    h2("9.1  Static context layers"),
    p("Built with <b>ecoscope_workflows_ext_custom.tasks.results.create_geojson_layer</b> "
      "after reprojecting to EPSG:4326. <b>combine_deckgl_map_layers</b> adds all "
      "three to every map as static layers."),
    make_table(
        [
            ["Layer", "Style", "Legend"],
            ["Land use (apply_color_map on land_use)",
             "filled + stroked, line width 0.85, opacity 0.75. Rangeland #a39c91, "
             "Rangeland and settlement #ffa07a, Settlement and agriculture #2f4f4f, "
             "Conservancies #8fbc8b, National parks and reserves #4d6600",
             "Map Layers (5 entries)"],
            ["Ranch boundaries", "outline only, black, width 0.95, opacity 0.55", "Ranch boundaries"],
            ["Electric fence", "outline only, #2d62b1, width 5.5, opacity 1.0", "Electric fence"],
        ],
        [4.4*cm, W - 8.4*cm, 4*cm],
    ),
    sp(6),
    h2("9.2  Viewport"),
    p("Task group <b>Map Zoom &amp; Extent</b>: <b>envelope_gdf</b> "
      "(expansion_factor 1.05) is applied to the <b>ranch boundaries</b> layer, and "
      "<b>compute_view_state_from_gdf</b> (pitch 0, bearing 0, max_zoom 15) builds the view. "
      "The viewport is therefore always Amboseli, not the extent of the survey points. "
      "All three maps use <b>draw_map</b> with max_zoom 10, static: false, "
      "and the legend at bottom-right."),
    sp(6),
    h2("9.3  Point layers"),
    p("Each map adds one <b>create_scatterplot_layer</b> built from the "
      "<b>replace_bins_mapping</b> table (radius 4, opacity 0.75, black outline 0.25)."),
    make_table(
        [
            ["Widget", "Map", "Colouring", "Output file"],
            ["50", "Survey events", "Single colour [220, 20, 60] (#dc143c), legend 'Survey Location'",
             "survey_event_map"],
            ["51", "Gender", "map_column_value on Gender of Participant: Female #e9967a, Male #0000ff, "
             "No Response / other #cfcfc4; add_rgba_columns_from_hex → gender_colors_rgba",
             "gender_event_map"],
            ["52", "Attitude", "map_column_value on sentiment_bins: Strongly Disagree #dc143c, "
             "Disagree #d2691e, Neutral #ffff00, Agree #7fff00, Strongly Agree #0000ff, "
             "other #cfcfc4 → sentiment_colors_rgba", "sentiment_event_map"],
        ],
        [1.4*cm, 2.4*cm, W - 7.8*cm, 4*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. PNG CONVERSION, WORD REPORT & DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. PNG Conversion, Word Report & Dashboard"),
    hr(),
    h2("10.1  PNG conversion"),
    make_table(
        [
            ["Task id", "Inputs", "Config"],
            ["convert_charts_to_png", "All 50 chart HTML files (one call)",
             "1280 × 720, device_scale_factor 2.0, wait_for_timeout 1 ms, "
             "max_concurrent_pages 10"],
            ["convert_survey_map_png / convert_gender_map_png / convert_sent_map_png",
             "One map each", "device_scale_factor 2.0, wait_for_timeout 40 000 ms (tile loading), "
             "max_concurrent_pages 1"],
        ],
        [5.2*cm, 4.4*cm, W - 9.6*cm],
    ),
    p("Each PNG is written to ECOSCOPE_WORKFLOWS_RESULTS with the same stem as its HTML file."),
    sp(6),
    h2("10.2  Word report"),
    p("Task: <b>generate_survey_report</b> (ecoscope-workflows-ext-ate). The Dropbox "
      "template is rendered with docxtpl:"),
    bullet("<b>Images</b>: every .png/.jpg/… found anywhere under the results "
           "directory is exposed as a template variable named after its file stem (e.g. "
           "<b>{{ what_is_your_age_group_pie_chart }}</b>), inserted at 11.11 × 6.5 cm."),
    bullet("<b>Demographics</b>: demographic-data.parquet (or .csv) is read into "
           "<b>demographics</b> and <b>total_responses</b>."),
    bullet("<b>Metadata</b>: report_period (since–until in the chosen time format), "
           "time_generated, and prepared_by = 'Ecoscope'."),
    sp(4),
    p("The output is <b>social_survey_report.docx</b>."),
    note("In the task graph, generate_survey_doc depends only on the template download "
         "and the time range, <b>not</b> on the PNG conversion tasks. The report only "
         "contains the images that exist when it runs, so run the workflow sequentially "
         "(or make the report depend on the PNG tasks) to guarantee a complete report. "
         "Renaming a chart's filename in spec.yaml also breaks its template tag."),
    sp(6),
    h2("10.3  Dashboard"),
    p("Charts are wrapped with <b>create_plot_widget_single_view</b> (widgets 0–49) and "
      "maps with <b>create_map_widget_single_view</b> (widgets 50–52). "
      "<b>gather_dashboard</b> combines the 53 widgets with the workflow details, time "
      "range, and groupers. The grid positions live in <b>layout.json</b> "
      "(53 entries, 10 × 10 units each)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>. Every chart and "
      "map exists as .html and .png. Sections 4, 5, 8 and 9 list the individual chart "
      "file names."),
    make_table(
        [
            ["File", "Description"],
            ["survey-events.gpkg", "Cleaned, relabelled survey responses"],
            ["demographic-data.parquet", "Demographic summary table (used by the report)"],
            ["elephant-sentiment-table.gpkg", "Statement scores, sentiment_score, sentiment_score_mean, sentiment_bins"],
            ["*_pie_chart.html / .png (×11)", "Pie charts"],
            ["*_bar_chart.html / .png (×27)", "Bar charts"],
            ["ele_sentiment_chart.html / .png", "Likert chart"],
            ["*_boxplot_chart.html / .png (×5)", "Sentiment boxplots"],
            ["*_tukey_chart.html / .png (×4)", "Tukey HSD plots"],
            ["*_sentiment_scatter_chart.html / .png (×2)", "Scatter plots with OLS trendline"],
            ["survey_event_map / gender_event_map / sentiment_event_map (.html / .png)", "Maps"],
            ["amboseli_*.gpkg (×3), ate_survey_template_280857_updated.docx", "Downloaded inputs"],
            ["social_survey_report.docx", "Final Word report"],
        ],
        [7.5*cm, W - 7.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Workflow Execution Logic"),
    hr(),
    h2("12.1  Skip conditions"),
    p("Every task inherits <b>task-instance-defaults</b>. The map scatterplot layers and "
      "draw_map tasks also declare the same conditions explicitly:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip the task if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip the task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("A single empty result (for example, no households with dogs) skips that "
      "chart, its PNG, and its widget. The rest of the run continues."),
    sp(6),
    h2("12.2  Data flow summary"),
    make_table(
        [
            ["Stage", "Main table", "Feeds"],
            ["Clean & relabel", "replace_marital_status", "Pie charts, survey-events.gpkg, binning"],
            ["Bin", "order_bins", "Binned bar charts, demographic table, retain_* subsets"],
            ["Subset", "retain_yes_no / retain_true_false / retain_agree_disagree",
             "Yes/No bars, True/False bars, Likert chart + scoring"],
            ["Score", "sentiment_bins → replace_bins_mapping", "Boxplots, Tukey, scatter / maps, sentiment gpkg"],
            ["Publish", "persist_* → html_to_png → generate_survey_report; widget_* → gather_dashboard",
             "PNG files, Word report, dashboard"],
        ],
        [3*cm, 6.5*cm, W - 9.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml", "Channel"],
            ["ecoscope-platform",                  "2.18.0",           "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",      "0.1.0rc14.*",      "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",         "0.0.0rc1.*",       "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",         "1.0.5.*",          "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-wwf-virunga", "0.0.0rc9.*",       "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",    "1.0.2.*",          "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ate",         "1.0.3.*",          "ecoscope-workflows-custom"],
            ["pydeck",                             "0.9.2",            "conda-forge"],
            ["opentelemetry-sdk",                  ">=1.20.0,<2.0.0",  "conda-forge"],
        ],
        [6*cm, 4.5*cm, W - 10.5*cm],
    ),
    sp(6),
    p("Build tooling (<b>pixi.toml</b>): wt-compiler &gt;=0.8.2,&lt;0.9, graphviz, go-yq. "
      "Compiled package version: <b>ecoscope-workflows-social-survey-workflow/VERSION.yaml</b>."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")

# Keep the GitHub Pages copy in sync
DOCS_ASSETS = Path(__file__).resolve().parent.parent / "docs" / "assets"
if DOCS_ASSETS.is_dir():
    shutil.copy2(OUTPUT_FILE, DOCS_ASSETS / Path(OUTPUT_FILE).name)
    print(f"Copied → {DOCS_ASSETS / Path(OUTPUT_FILE).name}")
