# Education Retention & Welfare Efficacy Tracker

## About the Project

This project is developed by our team for the **TransOrg AgentIQ Datathon** under the **Education & EdTech** track.

The main purpose of our project is to bring different school-related datasets together and understand what is happening with student attendance, attendance integrity, school infrastructure, mid-day meal procurement and learning outcomes.

Instead of looking at each dataset separately, we cleaned and integrated the data and built an interactive **Streamlit dashboard** where users can explore the results at district, block and school level.

---

# Problem We Are Trying to Solve

The datasets provided for the problem contained different data quality issues such as duplicate records, different formats for school IDs, mixed date formats, inconsistent Yes/No values and some attendance records that were not logically possible.

Our first step was therefore to clean and standardize the data.

After cleaning the individual datasets, we integrated them and created analytical datasets which are used by our dashboard.

The dashboard helps in identifying:

- Schools with lower attendance
- Possible attendance anomalies
- Districts with higher infrastructure gaps
- Differences in learning outcomes
- Mid-day meal procurement trends
- Schools that may need closer attention based on multiple indicators

---

# Datasets Used

We worked with five datasets provided for the project.

| Dataset | What it contains |
|---|---|
| School Master | School name, district, block, enrollment, school type and medium |
| Student Attendance | Attendance records by school, date and grade |
| Mid-Day Meal Procurement | Procurement quantity, cost, vendor and payment information |
| School Infrastructure | Availability of basic school facilities |
| Test Scores | Assessment scores by school, grade and subject |

The raw data is kept separately from the cleaned data so that the cleaning process can be checked and reproduced.

---

# Data Cleaning

## 1. School Master

The School Master dataset had duplicate records and some missing district and block values.

We removed exact duplicate records and standardized the text fields and school IDs.

| Metric | Result |
|---|---:|
| Raw records | 618 |
| Cleaned records | 600 |
| Duplicate records removed | 18 |
| Missing values after cleaning | 0 |
| Duplicate school IDs after cleaning | 0 |

---

## 2. Student Attendance

The attendance dataset required the most cleaning.

Some of the issues we found were:

- Duplicate attendance records
- Different formats of school IDs
- Mixed date formats
- Different values for teacher presence
- Different values for who marked attendance
- Present students greater than total students
- Sunday attendance records
- Missing record IDs

We standardized the school IDs, dates and grades and converted the different teacher presence and attendance-marker values into common categories.

For impossible attendance records, we did not simply delete them. Instead, we created a flag so that these records could still be investigated.

We also created a proxy attendance flag for suspicious patterns such as attendance recorded on Sundays.

### Attendance Cleaning Results

| Metric | Result |
|---|---:|
| Raw records | 20,800 |
| Cleaned records | 20,000 |
| Duplicate records removed | 800 |
| Impossible attendance records flagged | 806 |
| Proxy attendance records flagged | 979 |
| Missing record IDs | 405 |

---

## 3. Mid-Day Meal Procurement

For the mid-day meal data, we standardized the school IDs, dates, vendor names and grain types.

The quantity values were converted into kilograms and different measurement units were handled during the cleaning process.

We also cleaned the cost values so they could be used for numerical analysis.

After cleaning, the data was converted into a monthly analytical dataset for the dashboard.

---

## 4. School Infrastructure

The infrastructure dataset contains information about facilities available in schools.

We standardized the values used for facilities such as:

- Electricity
- Drinking water
- Functional toilet
- Boundary wall
- Playground

Values such as `Yes`, `1`, `Hai` and `Functional` were treated as available, while values such as `No`, `0`, `Nahi`, `Kharab` and `Broken` were treated as unavailable.

Unknown values were not automatically treated as unavailable.

We also calculated an infrastructure deficit percentage based on the amenities checked for each school.

---

## 5. Test Scores

The test score dataset contained different grading formats.

We converted the different formats into a common percentage-based score so that they could be compared.

The grading formats included:

- Percentage
- Raw Marks
- Letter Grade
- CGPA

For CGPA, we used:

`CGPA × 10`

Letter grades were also converted into percentage values using a consistent mapping.

### Test Score Results

| Metric | Result |
|---|---:|
| Raw records | 8,000 |
| Cleaned records | 8,000 |
| Duplicate records | 0 |

---

# Data Integration

After cleaning the individual datasets, we integrated them using the standardized `school_id`.

The final analytical datasets are:


data/analytical/
│
├── school_dim.csv
├── attendance_monthly.csv
├── mdm_monthly.csv
├── infrastructure_monthly.csv
└── test_scores_analysis.csv


# Dashboard

We developed an interactive **Streamlit dashboard** to bring the cleaned and
integrated datasets into one place.

The dashboard is designed to help users explore school performance and welfare
indicators at different levels, from district-level analysis down to individual
schools.

The dashboard follows a simple flow:

**Overview → Attendance → Mid-Day Meal → Infrastructure → Learning → 
Cross-Domain Analysis → Priority Schools**

---

## Dashboard Features

### 1. Interactive Filters

The dashboard provides cascading filters that allow users to explore the data
according to their requirements.

Available filters:

- District
- Block
- School
- Month

The filters work together. For example, selecting a district updates the
available blocks, and selecting a block updates the available schools.

This allows the same dashboard to be used for both high-level district
analysis and detailed school-level analysis.

---

## 2. Executive Overview

The Executive Overview provides a quick summary of the selected data.

### Key Performance Indicators

- **Total Schools** – Number of schools included in the selected view.
- **Average Attendance** – Overall attendance rate calculated using student
  presence and observed student counts.
- **Proxy Attendance Rate** – Percentage of attendance records flagged as
  possible proxy/suspicious attendance.
- **Total MDM Cost** – Total mid-day meal procurement cost for the selected
  period.
- **Infrastructure Deficit** – Percentage of checked infrastructure amenities
  that are unavailable.
- **Average Test Score** – Average standardized test score expressed as a
  percentage.

These KPIs provide a quick understanding of the current education and welfare
situation before moving into detailed analysis.

---

## 3. Key Findings

The Key Findings section automatically summarizes important observations from
the currently selected filters.

It focuses on:

- Attendance performance
- Possible attendance anomalies
- Learning outcomes

This section helps users understand the most important patterns without
having to inspect every chart individually.

---

## 4. Areas Requiring Attention

This section highlights areas that may require further investigation.

It identifies:

- District with the lowest attendance
- District with the highest infrastructure deficit
- District with the lowest learning outcome

This gives decision-makers a quick way to identify where further attention
may be required.

---

## 5. Attendance & Retention Analysis

The Attendance section focuses on student attendance patterns and attendance
integrity.

### Visualizations

- **Monthly Attendance Trend**
- **Proxy Attendance Trend**
- **District-wise Attendance Comparison**

The monthly attendance trend helps identify changes in attendance over time,
while the proxy attendance trend highlights periods with a higher number of
flagged attendance records.

The district comparison helps identify areas with relatively lower attendance.

---

## 6. Mid-Day Meal & Welfare Analysis

The Mid-Day Meal section focuses on procurement activity and expenditure.

### KPIs

- Total MDM Quantity
- Total Procurement Cost
- Procurement Records
- Vendor Instances

### Visualizations

- **Monthly MDM Cost Trend**
- **Monthly MDM Quantity Trend**

This section helps users understand procurement volume and expenditure
patterns over time.

The current analysis focuses on **procurement data** available in the
provided dataset and does not directly estimate actual meal consumption or
wastage.

---

## 7. Infrastructure Analysis

The Infrastructure section provides an overview of basic facilities
available across schools.

The dashboard analyses:

- Electricity
- Drinking Water
- Functional Toilets
- Boundary Wall
- Playground

### Visualizations

- **Infrastructure Deficit Trend**
- **Facility Availability**
- **Infrastructure Deficit by District**

The Infrastructure Deficit metric is calculated using the amenities that were
actually checked. Unknown facility statuses are not automatically treated as
unavailable.

---

## 8. Learning Outcomes Analysis

The Learning Outcomes section focuses on student assessment performance.

### Visualizations

- **Average Score by Subject**
- **Average Score by Grade**
- **Average Score by District**

Different grading formats from the original test-score data were converted
into a common percentage scale before analysis.

This makes scores from Percentage, Raw Marks, Letter Grade and CGPA formats
comparable.

---

## 9. Cross-Domain Analysis

The dashboard also combines indicators from different datasets to look for
relationships between school conditions and student outcomes.

One of the current analyses compares:

**Attendance Rate vs Infrastructure Deficit**

at the school level.

A correlation value and scatter plot are provided to show the relationship
between the two variables.

This analysis is **descriptive only**. Correlation does not establish that
infrastructure directly causes changes in attendance.

---

## 10. District Performance Summary

The District Performance Summary provides a consolidated view of district
performance.

For each district, users can compare:

- Attendance %
- Test Score %
- Infrastructure Deficit %
- Proxy Attendance %

This makes it easier to compare districts across multiple education and
welfare indicators rather than looking at only one metric.

---

## 11. Priority Schools

The Priority Schools section is designed to help identify schools that may
require closer review.

We created a rule-based priority screening score using four indicators:

| Indicator | Weight |
|---|---:|
| Attendance Risk | 35% |
| Learning Risk | 30% |
| Infrastructure Risk | 25% |
| Proxy Attendance Risk | 10% |

The combined score is used to classify schools into:

- 🔴 **High Priority**
- 🟠 **Medium Priority**
- 🟢 **Low Priority**

The dashboard displays the highest-priority schools along with:

- School ID
- School Name
- District
- Block
- Priority Level
- Priority Score
- Attendance %
- Test Score %
- Infrastructure Deficit %
- Proxy Attendance %

The priority score is intended as a **screening and prioritization tool**. It
is not a trained machine learning prediction model and should not be
interpreted as a prediction of student retention or school failure.

---

## 12. Light / Dark Theme

The dashboard also includes a **Light/Dark Mode toggle**.

This allows users to switch between themes depending on their viewing
preference while keeping the dashboard readable and consistent.

---

## Dashboard Design

We kept the dashboard design simple and information-focused.

The dashboard uses:

- Clear KPI cards
- Interactive filters
- Line charts for trends
- Bar charts for comparisons
- Scatter plots for relationships
- Tables for detailed school-level information
- Semantic priority indicators

The objective was to make the dashboard useful for both quick decision-making
and deeper exploration of the data.


education-retention-tracker/
│
├── dashboard/
│   ├── .gitkeep
│   └── app.py
│
├── data/
│   ├── analytical/
│   │   ├── school_dim.csv
│   │   ├── attendance_monthly.csv
│   │   ├── mdm_monthly.csv
│   │   ├── infrastructure_monthly.csv
│   │   └── test_scores_analysis.csv
│   │
│   ├── cleaned/
│   │   ├── school_master_cleaned.csv
│   │   ├── student_attendance_cleaned.csv
│   │   ├── mid_day_meal_procurement_cleaned.csv
│   │   ├── infrastructure_cleaned.csv
│   │   └── test_scores_cleaned.csv
│   │
│   └── raw/
│       ├── track4_school_master.csv
│       ├── track4_student_attendance.csv
│       ├── track4_mid_day_meal_procurement.xlsx
│       ├── track4_school_infrastructure.csv
│       └── track4_test_scores.json
│
├── docs/
│   └── dataset_notes.txt
│
├── notebooks/
│   ├── 01_eda_and_cleaning.ipynb
│   ├── 02_eda_cleaning_mid_day_meal_procurement.ipynb
│   ├── 03_eda_cleaning_school_infrastructure.ipynb
│   ├── 04_cleaning_test_scores.ipynb
│   └── 05_data_integration.ipynb
│
├── .gitignore
├── README.md
└── requirements.txt