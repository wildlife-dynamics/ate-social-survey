# ATE Social Survey — User Guide

This guide walks you through configuring and running the ATE Social Survey workflow (`social_survey`). It processes Amboseli Trust for Elephants community questionnaire responses from EarthRanger and produces an interactive dashboard of attitude, knowledge, and demographic charts, elephant sentiment scores with statistical comparisons, three maps of Amboseli, and a Word report.

Full documentation is also published as a site from the [`docs/`](docs/) folder: user guide, technical guide, and troubleshooting.

---

## Overview

The workflow delivers, for each run:

- **An interactive dashboard with 53 widgets**, combining everything below
- **11 pie charts** covering demographics and attitudes (age group, gender, tribe, education, marital status, land arrangement, threats to crops and livestock, feelings about wildlife, how often elephants are seen, reaction to elephants being harmed)
- **27 bar charts**:
  - 9 binned numeric questions (age, household size, cattle, dogs, donkeys, sheep/goats, other animals, land owned, land farmed)
  - 10 Yes/No behaviour questions
  - 8 True/False elephant-knowledge questions
- **1 Likert chart** showing Strongly Disagree → Strongly Agree responses across 9 attitude statements
- **An elephant sentiment score for each respondent**: the mean of 9 attitude statements scored 1–5, with negative statements reverse-scored
- **5 boxplots, 4 Tukey HSD plots, and 2 scatter plots with an OLS trendline** comparing sentiment across demographic groups
- **3 maps** (survey locations, respondent gender, and attitude category) drawn over Amboseli land-use zones, group-ranch boundaries, and the electric fence
- **1 Word report** (`social_survey_report.docx`) built from a template and filled with the chart PNGs and the demographic summary table

All outputs cover the whole dataset as one view. Grouping is fixed to none (`groupers: []`), so there is no per-group breakdown.

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with `atequestionnaire_rep` events recorded for the analysis period
- Internet access from the runner. The Amboseli map layers and the Word template are downloaded from Dropbox at run time, and the base map tiles come from ArcGIS Online

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/ate-social-survey.git
```

Then click **Add Template**.

![Add Workflow Template](data/screenshots/add_workflow.png)

---

### Step 2 — Add an EarthRanger Connection

Navigate to **Data Sources** and click **Connect**, then select **EarthRanger**. Fill in the connection form:

- **Data Source Name**: a label to identify this connection (e.g. `Amboseli Trust for Elephants`)
- **EarthRanger URL**: your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

![EarthRanger Connection](data/screenshots/er_connection.png)

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list. Click the card to open the workflow configuration form.

![Select Workflow Template](data/screenshots/select_workflow.png)

---

### Steps 4–6 — Set Workflow Details, Time Range, and Connect to EarthRanger

The configuration form has three sections, all on a single page. Base maps, map layers, grouping, and the report template are fixed in the workflow, so you don't configure them here.

**Step 4 — Set workflow details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes (e.g. survey round or site) |

**Step 5 — Set time range**

| Field | Description |
|-------|-------------|
| Since | Start date and time. All `atequestionnaire_rep` events from this point are fetched |
| Until | End date and time of the analysis window |
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Time Format | *Advanced.* Controls how dates appear in the report period (default `%d %b %Y %H:%M:%S`) |

**Step 6 — Connect to EarthRanger**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Amboseli Trust for Elephants`).

Once all three sections are filled, click **Submit**.

![Set Workflow Details, Time Range, and Connect to EarthRanger](data/screenshots/configure_workflow.png)

---

## Running the Workflow

Once submitted, the runner will:

1. Download the three Amboseli GeoPackages from Dropbox (land-use zones and conservancies, group-ranch boundaries with the electric fence, and group-ranch boundaries), reproject them to EPSG:4326, and style them as map layers.
2. Fetch `atequestionnaire_rep` events for the analysis period. The run fails if none are found.
3. Expand the event details into columns and strip the Maa translations from question headings (e.g. `What is your Age? (Kaja larin liata?)` becomes `What is your Age`).
4. Exclude invalid records: serial number `46283`, respondents aged 18 or under, and single-person households.
5. Fill missing values (`0` for numeric answers, `No Response` for text answers) and convert the numeric columns to integers.
6. Map raw answers to clean labels: Yes/No, True/False, Agree/Disagree, gender, age group, education, feelings about wildlife, how often elephants are seen, and marital status (many free-text spellings, including Maa words, map to *Married*, *Single*, or *Divorced*).
7. Draw 11 pie charts. Group the numeric answers into 5 natural-breaks bins and draw 9 bar charts, then draw 10 Yes/No and 8 True/False bar charts.
8. Build the demographic summary table (gender, age, tribe, household size, education).
9. Draw the Likert chart for the 9 agree/disagree statements.
10. Score each respondent's sentiment (1–5 for each statement, with negative statements reversed), take the mean, and put it into 5 attitude categories from *Strongly Disagree* to *Strongly Agree*.
11. Draw boxplots (gender, age group, education, tribe, marital status), Tukey HSD plots (gender, marital status, age group, education; `No Response` excluded), and scatter plots with an OLS trendline (household size and age against sentiment).
12. Render 3 maps: survey locations, gender, and attitude category.
13. Convert all 50 charts and the 3 maps to PNG.
14. Download the Word template from Dropbox and fill it with the chart PNGs, the demographic table, and the report period. It is saved as `social_survey_report.docx`.
15. Assemble the dashboard. All files are written to the directory set by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`. Every chart and map is saved as `.html` and converted to a `.png` with the same name.

### Data

| File | Description |
|------|-------------|
| `survey-events.gpkg` | Cleaned survey responses, one point per respondent |
| `demographic-data.parquet` | Demographic summary table (gender, age, tribe, household size, education); also used in the Word report |
| `elephant-sentiment-table.gpkg` | Per-respondent statement scores, `sentiment_score` (sum), `sentiment_score_mean`, and `sentiment_bins` (attitude category) |
| `social_survey_report.docx` | Final Word report |

### Pie charts (11)

| File | Question |
|------|----------|
| `what_is_your_age_group_pie_chart` | Age group |
| `what_is_the_land_arrangement_pie_chart` | Arrangement for the land farmed on |
| `highest_level_of_education_pie_chart` | Highest completed education |
| `what_is_your_tribe_pie_chart` | Tribe |
| `greatest_threat_to_crop_production_pie_chart` | Greatest threat to crop production |
| `greatest_threat_to_livestock_pie_chart` | Greatest threat to livestock |
| `what_is_your_marital_status_pie_chart` | Marital status |
| `overall_feeling_about_wildlife_pie_chart` | Overall feelings about wildlife |
| `how_often_have_you_seen_elephants_in_the_last_year_pie_chart` | How often elephants were seen in the last year |
| `how_do_you_feel_witnessing_elephant_harmed_pie_chart` | Feeling on hearing of or witnessing an elephant speared/poisoned |
| `gender_of_participant_pie_chart` | Gender |

### Bar charts — binned numeric answers (9)

`age_bins_bar_chart`, `other_people_bins_bar_chart` (household size), `cattle_bins_bar_chart`, `dog_bins_bar_chart`, `donkey_bins_bar_chart`, `sheep_goats_bins_bar_chart`, `other_animal_bins_bar_chart`, `land_grown_crops_bins_bar_chart`, `land_owned_bins_bar_chart`

Households with zero dogs or zero donkeys are left out of those two charts.

### Bar charts — Yes/No questions (10)

| File | Question |
|------|----------|
| `do_you_benefit_from_electric_fence_bar_chart` | Benefit from the KCCDT Big Life electric fence |
| `activities_altered_elephant_presence_bar_chart` | Choose routes/schedules/water fetching based on elephant presence |
| `protect_water_from_elephants_bar_chart` | Protect water sources from elephants |
| `more_eles_past_bar_chart` | See more elephants now than in the past |
| `family_protection_eles_bar_chart` | Use measures to prevent crop damage by elephants |
| `ffamily_protection_eles_livestock_bar_chart` | Use measures to prevent injury to livestock |
| `illness_wild_bar_chart` | Noticed signs of illness in wild animals |
| `elephant_harmed_bar_chart` | Involved in or witnessed an elephant being harmed |
| `report_elephant_conflict_bar_chart` | Report elephant conflict |
| `elephant_community_dialogue_bar_chart` | Interested in a future community dialogue |

### Bar charts — True/False knowledge questions (8)

`male_elephant_secretion_bar_chart`, `elephant_human_awareness_bar_chart`, `elephant_shake_head_bar_chart`, `elephant_smell_far_away_bar_chart`, `elephants_move_seasonally_bar_chart`, `female_elephants_protective_bar_chart`, `female_elephants_family_groups_bar_chart`, `witness_elephant_harm_bar_chart`

### Sentiment and statistics

| File | Description |
|------|-------------|
| `ele_sentiment_chart` | Likert chart of the 9 agree/disagree statements |
| `gender_boxplot_chart`, `age_group_boxplot_chart`, `education_level_boxplot_chart`, `tribe_boxplot_chart`, `marital_status_boxplot_chart` | Sentiment score distribution by group |
| `gender_tukey_chart`, `marital_status_tukey_chart`, `age_group_tukey_chart`, `education_tukey_chart` | Tukey HSD pairwise comparisons (95% confidence) |
| `household_sentiment_scatter_chart`, `age_sentiment_scatter_chart` | Sentiment against household size and age, with an OLS trendline |

### Maps

| File | Description |
|------|-------------|
| `survey_event_map` | All survey locations (crimson points) |
| `gender_event_map` | Survey points coloured by gender |
| `sentiment_event_map` | Survey points coloured by attitude category |

---

## More documentation

- [Technical Guide (PDF)](technical_guide/ate_survey_technical_guide.pdf): how each step works, the scoring method, and version pins
- [Troubleshooting](docs/troubleshooting.html): common errors and how to fix them
