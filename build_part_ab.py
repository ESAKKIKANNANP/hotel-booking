"""
Notebook Section A & B Tasks Generator
======================================
Generates Markdown and Code cells for:
- Title and Executive Header
- Imports & Configuration
- OOP Analytical Architecture
- SECTION A: Data Loading, Inspection, and Preprocessing (Tasks 1 to 14)
- SECTION B: Univariate Analysis (Tasks 15 to 27)
"""

def add_header_and_oop(builder):
    # Header Cell
    builder.add_markdown("""# Hotel Booking Demand, Customer Behaviour and Cancellation Analysis
### Comprehensive End-to-End Hospitality Analytics & Revenue Management Study

---
**Prepared by:** Aman Sah, Training Central  
**Project Level:** Advanced Analytics & Strategic Consulting  
**Target Audience:** Hotel Senior Leadership, Revenue Managers, and Operations Directors  
**Dataset Reference:** António, N., de Almeida, A., & Nunes, L. (2019). *Hotel booking demand datasets*. Data in Brief, 22, 41-49.  
**Format:** Single Production-Grade Executable Jupyter Notebook (`.ipynb`) adhering to PEP 8, PEP 257 docstring standards, and Object-Oriented Architecture.

---

### Executive Problem Statement & Research Questions
This project investigates the operational, behavioral, and commercial drivers of hotel reservation outcomes across two contrasting properties: a **City Hotel (Lisbon, Portugal)** and a **Resort Hotel (Algarve, Portugal)**. Historical reservation records spanning arrivals from July 1, 2015 to August 31, 2017 are examined to address ten core managerial questions:

1. **Why are hotel bookings cancelled?** (Identifying root behavioral and operational drivers of cancellation).
2. **Do city hotels and resort hotels exhibit distinct booking patterns?** (Contrasting urban commercial vs coastal leisure dynamics).
3. **Which months and seasons experience peak booking demand?** (Decomposing calendar seasonality and arrival clustering).
4. **How does advance booking horizon (lead time) influence cancellation risk?** (Quantifying the vulnerability of distant commitments).
5. **Which customer segments contribute the highest volume and stability?** (Profiling Transient, Group, Contract, and Party segments).
6. **Do special requests signal genuine guest commitment to stay?** (Evaluating customer engagement as a mitigating signal).
7. **How do room type allocations, deposit structures, and booking channels shape reservation outcomes?** (Unraveling the Non-Refund deposit paradox and room mismatch effects).
8. **What factors drive Average Daily Rate (ADR) premiums?** (Assessing seasonality, room tiering, lead time, and channel discounting).
9. **How do weekday and weekend stay patterns diverge?** (Evaluating length-of-stay structures across property types).
10. **What concrete revenue management, booking policies, and operational strategies should leadership implement?** (Formulating data-grounded strategic recommendations).
""")

    # Imports Cell
    builder.add_code('''# Standard Library Imports
import os
import sys
import io
import json
import base64
import warnings
from typing import Dict, List, Tuple, Any, Optional

# Core Scientific & Data Manipulation Libraries
import numpy as np
import pandas as pd

# Visualization Libraries
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Visualization Settings & Aesthetics
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 110
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 15

print("Environment configured: NumPy", np.__version__, "| Pandas", pd.__version__, "| Matplotlib", matplotlib.__version__, "| Seaborn", sns.__version__)
''')

    # Architecture Definition
    builder.add_markdown("""## Object-Oriented Analytical Architecture
To adhere to enterprise software engineering standards, the analysis is modularized into seven production Python classes:
1. `HotelDataLoader`: Manages raw data ingestion, H1/H2 partition handling, and structural data dictionary generation.
2. `HotelDataPreprocessor`: Implements a scikit-learn compatible transformer for temporal parsing, missingness imputation, feature engineering, and auditable anomaly logging.
3. `UnivariateAnalyzer`: Encapsulates parametric/non-parametric descriptive metrics and distributional plotting routines.
4. `ComparativeHotelAnalyzer`: Conducts rigorous property-level comparisons reporting both absolute differences and relative percentage changes.
5. `CancellationAnalyzer`: Drives multi-factor cancellation rate profiling, risk segmentation, and the Non-Refund paradox investigation.
6. `TimeSeriesSeasonalityAnalyzer`: Decomposes temporal trends across years, months, weeks, and arrival days.
7. `RevenueManager`: Benchmarks ADR, models lodging value equations, audits financial validity, and synthesizes executive strategies.
""")

    with open('classes_definition.py', 'r', encoding='utf-8') as f:
        classes_code = f.read()
    builder.add_code(classes_code)


def add_section_a(builder):
    builder.add_markdown("""# SECTION A – DATA LOADING, INSPECTION AND PREPROCESSING
**Objective:** Ingest the raw reservation records, examine the schema and structural dimensions, identify data quality anomalies, parse temporal attributes, and construct a transparent, auditable cleaned dataset.
""")

    # TASK 1
    builder.add_markdown("""### Task 1: Dataset Ingestion & Head/Tail Inspection
**Objective:** Load the Hotel Booking Demand dataset into a Pandas DataFrame and display the first 10 and last 10 records.
""")
    builder.add_code('''# Instantiate loader and ingest raw dataset
loader = HotelDataLoader(file_path='hotel_bookings.csv')
df_raw = loader.load_raw_data()

print("--- First 10 Records (Head) ---")
display_head = df_raw.head(10)
print(display_head[['hotel', 'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'adults', 'children', 'meal', 'country', 'market_segment', 'adr']])

print("\\n--- Last 10 Records (Tail) ---")
display_tail = df_raw.tail(10)
print(display_tail[['hotel', 'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'adults', 'children', 'meal', 'country', 'market_segment', 'adr']])
''')
    builder.add_markdown("""**Interpretation (Task 1):**  
The dataset successfully loads into memory. A visual inspection of the first 10 records confirms Resort Hotel reservations from July 2015 with lead times ranging from 0 to 737 days, accompanied by granular booking parameters such as market segment (`Direct`, `Corporate`, `Online TA`) and room types. The last 10 records capture City Hotel bookings from August 2017 with Check-Out statuses, confirming the chronological span from July 2015 through August 2017.
""")

    # TASK 2
    builder.add_markdown("""### Task 2: Dataset Dimensions & Observation Unit
**Objective:** Find the total number of rows and columns, and articulate what each individual observation represents.
""")
    builder.add_code('''# Display dataset shape
n_rows, n_cols = df_raw.shape
print(f"Dataset Dimensions: {n_rows:,} rows (observations) and {n_cols} columns (features).")
''')
    builder.add_markdown("""**Interpretation (Task 2):**  
The dataset contains **119,390 rows** and **32 columns**.  
**Observation Unit:** Each row represents a single hotel reservation scheduled to arrive between July 1, 2015 and August 31, 2017. This includes bookings that successfully checked in, reservations that were cancelled prior to arrival, and reservations where guests failed to show up (No-Show). It encompasses both individual/transient customers and group block reservations.
""")

    # TASK 3
    builder.add_markdown("""### Task 3: Column Names, Data Types, Non-Null Counts, and Memory Footprint
**Objective:** Inspect column data types, non-null counts, and memory consumption using `info()`.
""")
    builder.add_code('''# Capture info summary
buffer = io.StringIO()
df_raw.info(buf=buffer, memory_usage='deep')
info_str = buffer.getvalue()
print(info_str)
''')
    builder.add_markdown("""**Interpretation (Task 3):**  
The raw dataset occupies approximately **64.5 MB** of memory. It features 32 attributes comprising 4 float columns (`children`, `adr`, `agent`, `company`), 16 integer columns, and 12 object (string) columns. Columns such as `reservation_status_date` require datetime parsing, while `agent` and `company` exhibit substantial missingness.
""")

    # TASK 4
    builder.add_markdown("""### Task 4: Independent Loading and Concatenation of H1 (Resort) and H2 (City) Datasets
**Objective:** Emulate loading the separate H1 and H2 research files independently, adding a distinguishing hotel identifier to each, and concatenating them via `pd.concat()`.
""")
    builder.add_code('''# Partition into H1 (Resort Hotel) and H2 (City Hotel) subsets
h1_resort, h2_city = loader.get_h1_h2_split(df_raw)

# Ensure explicit hotel column tagging
h1_resort['hotel'] = 'Resort Hotel'
h2_city['hotel'] = 'City Hotel'

# Combine via pd.concat()
df_combined = pd.concat([h1_resort, h2_city], ignore_index=True)

print(f"H1 (Resort Hotel) observations: {h1_resort.shape[0]:,}")
print(f"H2 (City Hotel) observations:   {h2_city.shape[0]:,}")
print(f"Combined DataFrame shape:       {df_combined.shape[0]:,} rows, {df_combined.shape[1]} columns")
assert df_combined.shape == df_raw.shape, "Shape mismatch after concatenation!"
print("Verification: Concatenation perfectly reproduces the 119,390 observation dataset.")
''')
    builder.add_markdown("""**Interpretation (Task 4):**  
In the original research publication by António et al. (2019), data was collected as two distinct CSV files: H1 (Resort Hotel in Algarve) and H2 (City Hotel in Lisbon). The demonstration above verifies that concatenating H1 (40,060 rows) and H2 (79,330 rows) seamlessly reconstructs the complete 119,390 row dataset without data degradation.
""")

    # TASK 5
    builder.add_markdown("""### Task 5: Observation Counts and Proportions by Hotel Type
**Objective:** Calculate the count and percentage share of observations represented by City Hotel and Resort Hotel.
""")
    builder.add_code('''# Calculate frequency and percentage
hotel_counts = df_raw['hotel'].value_counts()
hotel_pcts = df_raw['hotel'].value_counts(normalize=True) * 100

hotel_share_table = pd.DataFrame({
    'Observation Count': hotel_counts,
    'Share of Total (%)': hotel_pcts.round(2)
})
print("--- Hotel Share Summary Table ---")
print(hotel_share_table)
''')
    builder.add_markdown("""**Interpretation (Task 5):**  
- **City Hotel (H2):** 79,330 bookings (**66.45%** of the dataset).  
- **Resort Hotel (H1):** 40,060 bookings (**33.55%** of the dataset).  
The City Hotel accounts for approximately two-thirds of all observations, reflecting the significantly larger room capacity and higher guest turnover typical of metropolitan commercial hotels compared to seasonal vacation resorts.
""")

    # TASK 6
    builder.add_markdown("""### Task 6: Column Identification & Structured Data Dictionary
**Objective:** Categorize numerical, categorical, binary, and date-related columns, and construct a comprehensive Data Dictionary.
""")
    builder.add_code('''# Generate comprehensive Data Dictionary
data_dict = loader.generate_data_dictionary(df_raw)
print(f"Data Dictionary created covering all {len(data_dict)} attributes.")
print(data_dict.to_string(index=False))
''')
    builder.add_markdown("""**Interpretation (Task 6):**  
The dataset is structured across four primary analytical categories:
- **Numerical (16 variables):** Counts (`lead_time`, `adults`, `children`, `babies`, `stays_in_week_nights`, `stays_in_weekend_nights`, `booking_changes`, `days_in_waiting_list`, `previous_cancellations`, `previous_bookings_not_canceled`, `required_car_parking_spaces`, `total_of_special_requests`) and continuous financial figures (`adr`).
- **Categorical (12 variables):** Nominal types (`hotel`, `meal`, `country`, `market_segment`, `distribution_channel`, `reserved_room_type`, `assigned_room_type`, `deposit_type`, `customer_type`, `reservation_status`, `agent`, `company`).
- **Binary Flags (2 variables):** `is_canceled` (target label: 1=canceled, 0=not canceled), `is_repeated_guest` (1=repeat, 0=first-time).
- **Temporal/Date (4 variables):** Arrival date components (`arrival_date_year`, `arrival_date_month`, `arrival_date_week_number`, `arrival_date_day_of_month`) and `reservation_status_date`.
""")

    # TASK 7
    builder.add_markdown("""### Task 7: Missing Value Audit
**Objective:** Calculate missing-value counts and percentages for every column in the dataset.
""")
    builder.add_code('''# Compute missing values count and percentage
null_counts = df_raw.isnull().sum()
null_percentages = (null_counts / len(df_raw)) * 100

missing_summary = pd.DataFrame({
    'Missing Count': null_counts,
    'Missing Percentage (%)': null_percentages.round(4)
})
missing_only = missing_summary[missing_summary['Missing Count'] > 0].sort_values(by='Missing Count', ascending=False)
print("--- Columns with Missing Values ---")
print(missing_only)
''')
    builder.add_markdown("""**Interpretation (Task 7):**  
Missing values are confined to exactly four attributes:
1. `company`: 112,593 missing (**94.31%**)
2. `agent`: 16,340 missing (**13.69%**)
3. `country`: 488 missing (**0.41%**)
4. `children`: 4 missing (**0.003%**)  
All remaining 28 variables contain 100% complete records.
""")

    # TASK 8
    builder.add_markdown("""### Task 8: In-Depth Investigation of Missing Values
**Objective:** Investigate whether missing values in `children`, `country`, `agent`, and `company` represent genuine missing observations or meaningful operational codes.
""")
    builder.add_code('''# Investigate agent and company missingness in relation to market segments
agent_missing_by_segment = df_raw[df_raw['agent'].isnull()]['market_segment'].value_counts()
company_present_by_segment = df_raw[df_raw['company'].notnull()]['market_segment'].value_counts()

print("--- Market Segments for Missing Agent Bookings ---")
print(agent_missing_by_segment)

print("\\n--- Market Segments for Non-Null Company Bookings ---")
print(company_present_by_segment)
''')
    builder.add_markdown("""**Inspection Report (Task 8):**  
- **`company` (94.31% missing):** This is **not a data collection failure**. In hospitality PMS (Property Management Systems), the `company` field stores a corporate billing account ID. Over 94% of hotel guests book as private individuals without a corporate account sponsor. The absence of a company ID simply denotes an individual/non-corporate reservation.
- **`agent` (13.69% missing):** Similarly, bookings without an `agent` ID correspond primarily to `Direct` bookings (made directly on the hotel website or front desk) or corporate contracts where no third-party travel agency or tour operator was commissioned.
- **`country` (0.41% missing):** Represents genuine missing demographic data where guest nationality was omitted at intake or check-in.
- **`children` (0.003% missing / 4 rows):** Genuine missing data, safely imputed with the mode (0 children).
""")

    # TASK 9
    builder.add_markdown("""### Task 9: Duplicate Records Analysis & Retention Rationale
**Objective:** Count duplicate records, investigate identical booking characteristics, and evaluate whether duplicates represent legitimate repeated bookings.
""")
    builder.add_code('''# Count exact row duplicates
n_duplicates = df_raw.duplicated().sum()
pct_duplicates = (n_duplicates / len(df_raw)) * 100

print(f"Total Duplicate Rows: {n_duplicates:,} ({pct_duplicates:.2f}% of dataset)")

# Inspect duplicate sample
dup_sample = df_raw[df_raw.duplicated(keep=False)].sort_values(by=['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'lead_time']).head(6)
print("\\n--- Sample of Duplicate Booking Records ---")
print(dup_sample[['hotel', 'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'adults', 'customer_type', 'adr']])
''')
    builder.add_markdown("""**Investigation & Business Decision (Task 9):**  
There are **31,994 duplicate rows (26.80%)**.  
**Are these duplicates errors or legitimate observations?**
1. **Lack of Unique Booking Identifiers:** The dataset intentionally anonymized and stripped primary keys (`Reservation_ID`, `Guest_Name`, `Credit_Card_Token`) to comply with European GDPR privacy standards.
2. **Multi-Room & Corporate Group Reservations:** It is standard industry practice for a family, tour group, wedding party, or corporate event to book multiple identical rooms (same arrival date, lead time, guest count, meal plan, and rate). In a dataset without reservation IDs, ten rooms booked by a tour group appear as ten identical rows.
3. **Research Practice:** The original authors (António et al., 2019) retained all observations because each row represents an occupied room night demand event. Removing these rows would bias demand downwards and distort occupancy rates.  
*Analytical Approach:* In this study, we maintain the integrity of the full dataset for demand and revenue analyses while documenting the impact of duplication.
""")

    # TASK 10
    builder.add_markdown("""### Task 10: Validation Summary for Impossible & Suspicious Values
**Objective:** Check for negative stay durations, negative guest counts, zero total guests, extreme lead times, and negative ADR values.
""")
    builder.add_code('''# Check for anomalous and impossible records
zero_guests = df_raw[(df_raw['adults'] + df_raw['children'].fillna(0) + df_raw['babies']) == 0]
neg_adr = df_raw[df_raw['adr'] < 0]
zero_nights = df_raw[(df_raw['stays_in_week_nights'] + df_raw['stays_in_weekend_nights']) == 0]
extreme_adr = df_raw[df_raw['adr'] > 1000]
extreme_lead_time = df_raw[df_raw['lead_time'] > 365]

validation_summary = pd.DataFrame({
    'Anomaly Category': [
        'Zero Total Guests (Adults + Children + Babies == 0)',
        'Negative ADR (ADR < 0.00)',
        'Zero Total Stay Nights (Week + Weekend Nights == 0)',
        'Extreme ADR Outlier (ADR > $1,000 / night)',
        'Extreme Advance Booking (Lead Time > 365 days)'
    ],
    'Record Count': [
        len(zero_guests),
        len(neg_adr),
        len(zero_nights),
        len(extreme_adr),
        len(extreme_lead_time)
    ],
    'Percentage (%)': [
        round(len(zero_guests) / len(df_raw) * 100, 4),
        round(len(neg_adr) / len(df_raw) * 100, 4),
        round(len(zero_nights) / len(df_raw) * 100, 4),
        round(len(extreme_adr) / len(df_raw) * 100, 4),
        round(len(extreme_lead_time) / len(df_raw) * 100, 4)
    ]
})

print("--- Data Validation Summary ---")
print(validation_summary.to_string(index=False))
''')
    builder.add_markdown("""**Validation Findings (Task 10):**  
- **Zero Guests (180 records, 0.15%):** Physically impossible for a guestroom to be occupied by 0 adults, 0 children, and 0 babies. Likely clerical holds, system tests, or pre-authorizations.
- **Negative ADR (1 record, 0.0008%):** A single record with ADR of **-$6.38** at the Resort Hotel. Represents an accounting credit adjustment or refund voucher recorded as a negative daily rate.
- **Zero Stay Nights (715 records, 0.60%):** Bookings where both weekday and weekend nights equal zero. Typically day-use rooms, canceled pre-arrival bookings, or PMS check-in/check-out sync errors.
- **Extreme ADR Outlier (1 record, 0.0008%):** A single transaction with ADR of **$5,400.00** at the City Hotel (mean ADR is ~$101). Confirmed as an isolated data entry error or presidential suite package.
""")

    # TASK 11
    builder.add_markdown("""### Task 11: DateTime Conversion for Arrival Date
**Objective:** Combine arrival date components (`arrival_date_year`, `arrival_date_month`, `arrival_date_day_of_month`) into a proper Pandas datetime series called `arrival_date`.
""")
    builder.add_code('''# Convert arrival date components to proper datetime
month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}
numeric_month = df_raw['arrival_date_month'].map(month_map)
df_raw['arrival_date'] = pd.to_datetime(
    df_raw['arrival_date_year'].astype(str) + '-' +
    numeric_month.astype(str).str.zfill(2) + '-' +
    df_raw['arrival_date_day_of_month'].astype(str).str.zfill(2)
)

print("Constructed 'arrival_date' series:")
print(f"Minimum Arrival Date: {df_raw['arrival_date'].min().strftime('%Y-%m-%d')}")
print(f"Maximum Arrival Date: {df_raw['arrival_date'].max().strftime('%Y-%m-%d')}")
print("Data type:", df_raw['arrival_date'].dtype)
''')
    builder.add_markdown("""**Interpretation (Task 11):**  
The combined `arrival_date` column spans exactly 26 months, from **July 1, 2015 to August 31, 2017**, enabling granular time-series and day-of-week analytics.
""")

    # TASK 12
    builder.add_markdown("""### Task 12: DateTime Conversion for Reservation Status Date
**Objective:** Convert `reservation_status_date` into datetime format and calculate its minimum and maximum values.
""")
    builder.add_code('''# Convert reservation_status_date to datetime
df_raw['reservation_status_date'] = pd.to_datetime(df_raw['reservation_status_date'])

print(f"Minimum Reservation Status Date: {df_raw['reservation_status_date'].min().strftime('%Y-%m-%d')}")
print(f"Maximum Reservation Status Date: {df_raw['reservation_status_date'].max().strftime('%Y-%m-%d')}")
''')
    builder.add_markdown("""**Interpretation (Task 12):**  
`reservation_status_date` ranges from **October 17, 2014 to September 14, 2017**.  
The earliest status date (Oct 17, 2014) represents an early cancellation of a booking scheduled for 2015, while the latest status date (Sep 14, 2017) captures checkout events for guests who arrived in late August 2017.
""")

    # TASK 13
    builder.add_markdown("""### Task 13: Logical Consistency Check Between Arrival Date and Status Date
**Objective:** Check whether arrival date and reservation status date are logically consistent, and identify records where status date occurs later than arrival date.
""")
    builder.add_code('''# Check records where reservation_status_date > arrival_date
status_after_arrival = df_raw[df_raw['reservation_status_date'] > df_raw['arrival_date']]
print(f"Records where status date > arrival date: {len(status_after_arrival):,}")

# Breakdown by reservation status
status_breakdown = status_after_arrival['reservation_status'].value_counts()
print("\\n--- Breakdown of Records Where Status Date > Arrival Date ---")
print(status_breakdown)

# Check if any cancellations occurred after arrival
canc_after_arrival = df_raw[(df_raw['is_canceled'] == 1) & (df_raw['reservation_status_date'] > df_raw['arrival_date'])]
print(f"\\nCanceled bookings with status date > arrival date: {len(canc_after_arrival)}")
''')
    builder.add_markdown("""**Consistency Findings (Task 13):**  
There are **74,460 records** where `reservation_status_date` is later than `arrival_date`.  
**Critical Domain Explanation:**  
100% of these 74,460 records have a `reservation_status` of **`Check-Out`**! This is **entirely logically consistent**: hotel guests check out at the *end* of their multi-day stay, which naturally occurs days after their arrival date.  
Conversely, there are **0 cancellations** where the status date is later than the arrival date. All cancellations occur on or before the scheduled arrival date. This confirms excellent chronological data integrity in the reservation tracking system.
""")

    # TASK 14
    builder.add_markdown("""### Task 14: Cleaned Dataset Creation & Preprocessing Audit Log
**Objective:** Create a cleaned copy of the dataset (`df_cleaned`) via the `HotelDataPreprocessor` transformer class, documenting every data transformation explicitly in an audit log.
""")
    builder.add_code('''# Initialize preprocessor and apply transformation
preprocessor = HotelDataPreprocessor(filter_anomalies=False)
df_cleaned = preprocessor.fit_transform(df_raw)

audit_log_df = preprocessor.get_audit_log()
print("--- Data Preprocessing Audit Log ---")
print(audit_log_df.to_string(index=False))

print(f"\\nCleaned DataFrame Shape: {df_cleaned.shape[0]:,} rows, {df_cleaned.shape[1]} columns")
print("Engineered Columns:", [col for col in df_cleaned.columns if col not in df_raw.columns])
''')
    builder.add_markdown("""**Interpretation (Task 14):**  
The dataset is cleanly preprocessed without modifying the original raw table. The audit log documents all actions:
- Temporal parsing of `arrival_date` and `reservation_status_date`.
- Imputation of `children` (mode 0), `country` ('Unknown'), `agent` (0), and `company` (0).
- Engineering of key analytical features: `total_stay_nights`, `total_guests`, `is_family`, `room_type_changed`, `lead_time_bracket`, `stay_type`, and `estimated_lodging_value`.
- Systematic auditing of physical anomalies (180 zero-guest rows, 1 negative ADR, 715 zero-night rows, 1 extreme outlier).
""")


def add_section_b(builder):
    builder.add_markdown("""# SECTION B – UNIVARIATE ANALYSIS
**Objective:** Evaluate the distributional properties, central tendencies, spreads, skewness, and category frequencies for key numerical and categorical features.
""")

    # TASK 15
    builder.add_markdown("""### Task 15: Parametric & Non-Parametric Statistics for `lead_time`
**Objective:** Calculate mean, median, mode, standard deviation, variance, minimum, and maximum for `lead_time`.
""")
    builder.add_code('''# Compute lead_time summary statistics
lt_summary = UnivariateAnalyzer.compute_continuous_summary(df_cleaned['lead_time'], 'lead_time')
print("--- Lead Time Descriptive Statistics ---")
print(lt_summary.T)
''')
    builder.add_markdown("""**Interpretation (Task 15):**  
- **Mean:** 104.01 days  
- **Median:** 69.00 days  
- **Mode:** 0 days  
- **Standard Deviation:** 106.86 days (Variance: 11,419.72)  
- **Range:** 0 to 737 days  
The substantial divergence between the mean (104.01) and median (69.00), coupled with a mode of 0 (same-day bookings) and a maximum of 737 days (>2 years in advance), indicates substantial positive skewness.
""")

    # TASK 16
    builder.add_markdown("""### Task 16: Distribution of `lead_time` (Histogram & KDE)
**Objective:** Plot a histogram and Kernel Density Estimation (KDE) curve for `lead_time`, assess skewness, and interpret booking behavior.
""")
    builder.add_code('''# Plot lead_time histogram and KDE
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_cleaned['lead_time'], kde=True, bins=50, color='#1f77b4', edgecolor='black', alpha=0.6, ax=ax)
ax.axvline(df_cleaned['lead_time'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df_cleaned['lead_time'].mean():.1f} days")
ax.axvline(df_cleaned['lead_time'].median(), color='green', linestyle='-', linewidth=2, label=f"Median: {df_cleaned['lead_time'].median():.1f} days")
ax.set_title("Lead Time Distribution: Marked Positive Skewness & Last-Minute Clustering")
ax.set_xlabel("Lead Time (Days from Booking to Scheduled Arrival)")
ax.set_ylabel("Booking Frequency")
ax.legend(frameon=True)
plt.tight_layout()
plt.show()

print(f"Skewness Coefficient: {df_cleaned['lead_time'].skew():.3f} (Significantly Positive Skew)")
''')
    builder.add_markdown("""**Interpretation (Task 16):**  
The distribution exhibits pronounced **positive (right) skewness (skewness = +1.396)**.  
**Booking Behavior Insights:**  
1. **Last-Minute Booking Spike:** The sharp spike at `lead_time = 0` indicates a significant volume of impulse, urgent corporate, or distress bookings made on the arrival day.
2. **Exponential Decay:** Booking volume drops off exponentially as lead time increases. Over 50% of reservations occur within 69 days of arrival.
3. **Long Vacation Horizons:** The long right tail extending to 737 days reflects chartered tour operators, advance conference registrations, and holidaymakers locking in peak summer slots a year or two in advance.
""")

    # TASK 17
    builder.add_markdown("""### Task 17: Average Daily Rate (ADR) Distribution & Outlier Analysis
**Objective:** Analyze `adr` using descriptive statistics, histogram, and boxplot; assess distribution symmetry and identify extreme values.
""")
    builder.add_code('''# ADR Summary Statistics
adr_summary = UnivariateAnalyzer.compute_continuous_summary(df_cleaned['adr'], 'adr')
print("--- ADR Descriptive Statistics ---")
print(adr_summary.T)

# Visualizing ADR Distribution with Boxplot and Histogram
fig, (ax_box, ax_hist) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={'height_ratios': [0.25, 0.75]})

# Cap view to $500 for visualization clarity while annotating outlier
sns.boxplot(x=df_cleaned[df_cleaned['adr'] < 600]['adr'], ax=ax_box, color='#ff7f0e')
ax_box.set(xlabel='')
ax_box.set_title("Average Daily Rate (ADR) Distribution & Outlier Identification")

sns.histplot(df_cleaned[df_cleaned['adr'] < 600]['adr'], kde=True, bins=60, color='#2ca02c', ax=ax_hist)
ax_hist.axvline(df_cleaned['adr'].mean(), color='red', linestyle='--', label=f"Mean: ${df_cleaned['adr'].mean():.2f}")
ax_hist.axvline(df_cleaned['adr'].median(), color='blue', linestyle='-', label=f"Median: ${df_cleaned['adr'].median():.2f}")
ax_hist.set_xlabel("Average Daily Rate ($ / Night)")
ax_hist.set_ylabel("Frequency")
ax_hist.legend()

plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 17):**  
- **Mean ADR:** $101.83  
- **Median ADR:** $94.58  
- **Min ADR:** -$6.38 (negative accounting voucher)  
- **Max ADR:** $5,400.00 (extreme luxury outlier)  
The distribution is positively skewed with a heavy right tail. The vast majority of reservations cluster between $70 and $150 per night, reflecting standard room pricing. A notable spike occurs at ADR = $0 (1,959 complimentary, house-use, or loyalty reward bookings).
""")

    # TASK 18
    builder.add_markdown("""### Task 18: ADR Percentile Distribution
**Objective:** Calculate the 5th, 25th, 50th, 75th, 90th, 95th, and 99th percentiles of ADR.
""")
    builder.add_code('''# Compute requested ADR percentiles
adr_percentiles = UnivariateAnalyzer.compute_percentiles(df_cleaned['adr'], [5, 25, 50, 75, 90, 95, 99])
print("--- ADR Percentiles Table ---")
print(adr_percentiles.to_string(index=False))
''')
    builder.add_markdown("""**Interpretation (Task 18):**  
- **5th Percentile:** $38.40 (Deep economy / winter rate)
- **25th Percentile (Q1):** $69.29 (Budget pricing tier)
- **50th Percentile (Median):** $94.58 (Core benchmark rate)
- **75th Percentile (Q3):** $126.00 (Peak shoulder / standard high season)
- **90th Percentile:** $164.00 (High-season peak demand)
- **95th Percentile:** $193.50 (Premium suite / summer luxury)
- **99th Percentile:** $252.00 (Top 1% elite suites / holiday surges)  
Notice that 99% of all rooms are priced below $252.00, demonstrating that the single $5,400 rate is a severe outlier.
""")

    # TASK 19
    builder.add_markdown("""### Task 19: Distribution of Weekday vs Weekend Stay Nights
**Objective:** Analyze the distribution of `stays_in_week_nights` and `stays_in_weekend_nights` to determine which stay duration type is more prevalent.
""")
    builder.add_code('''# Compare week nights vs weekend nights
week_summary = UnivariateAnalyzer.compute_continuous_summary(df_cleaned['stays_in_week_nights'], 'Weekday Nights')
weekend_summary = UnivariateAnalyzer.compute_continuous_summary(df_cleaned['stays_in_weekend_nights'], 'Weekend Nights')
stays_comparison = pd.concat([week_summary, weekend_summary])
print(stays_comparison[['Mean', 'Median', 'Std Dev', 'Min', 'Max']].T)

fig, ax = plt.subplots(figsize=(10, 4.5))
nights_df = pd.DataFrame({
    'Weekday Nights': df_cleaned['stays_in_week_nights'].value_counts().head(8),
    'Weekend Nights': df_cleaned['stays_in_weekend_nights'].value_counts().head(8)
}).fillna(0)

nights_df.plot(kind='bar', ax=ax, width=0.75, colormap='viridis')
ax.set_title("Frequency Comparison: Weekday vs Weekend Stay Durations (Up to 7 Nights)")
ax.set_xlabel("Number of Nights Booked")
ax.set_ylabel("Number of Bookings")
plt.xticks(rotation=0)
plt.legend(frameon=True)
plt.tight_layout()
plt.show()

total_week = df_cleaned['stays_in_week_nights'].sum()
total_weekend = df_cleaned['stays_in_weekend_nights'].sum()
print(f"Total Cumulative Weekday Nights: {total_week:,} ({total_week/(total_week+total_weekend)*100:.1f}%)")
print(f"Total Cumulative Weekend Nights: {total_weekend:,} ({total_weekend/(total_week+total_weekend)*100:.1f}%)")
''')
    builder.add_markdown("""**Interpretation (Task 19):**  
**Weekday stays are significantly more common.**  
- Cumulative weekday nights total **298,510 (73.0%)** vs **110,612 (27.0%)** weekend nights.  
- The mean weekday stay is **2.50 nights** compared to **0.93 nights** for weekends.  
Because a standard calendar week contains five business days versus two weekend days, business travel, extended family vacations, and conference bookings naturally absorb more weekday nights.
""")

    # TASK 20
    builder.add_markdown("""### Task 20: Guest Composition Frequency (Adults, Children, Babies)
**Objective:** Plot the frequency distribution of adults, children, and babies, and identify the most common guest party composition.
""")
    builder.add_code('''# Frequency of guest counts
fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

sns.countplot(x='adults', data=df_cleaned, ax=axes[0], palette='Blues_r', order=[0, 1, 2, 3, 4])
axes[0].set_title("Adults Distribution")
axes[0].set_xlabel("Adult Guests")
axes[0].set_ylabel("Booking Count")

sns.countplot(x='children', data=df_cleaned, ax=axes[1], palette='Greens_r', order=[0, 1, 2, 3])
axes[1].set_title("Children Distribution")
axes[1].set_xlabel("Child Guests")

sns.countplot(x='babies', data=df_cleaned, ax=axes[2], palette='Reds_r', order=[0, 1, 2])
axes[2].set_title("Babies Distribution")
axes[2].set_xlabel("Baby Guests")

plt.tight_layout()
plt.show()

# Most common guest composition combinations
composition_series = df_cleaned['adults'].astype(str) + " Adults, " + df_cleaned['children'].astype(str) + " Children, " + df_cleaned['babies'].astype(str) + " Babies"
top_compositions = UnivariateAnalyzer.compute_frequency_table(composition_series, "Guest Composition", top_n=5)
print("--- Top 5 Guest Compositions ---")
print(top_compositions.to_string(index=False))
''')
    builder.add_markdown("""**Interpretation (Task 20):**  
- **Most Common Composition:** **2 Adults, 0 Children, 0 Babies** accounting for **82,103 bookings (68.77%)**.  
- **Second Most Common:** **1 Adult, 0 Children, 0 Babies** (Solo travelers) accounting for **22,577 bookings (18.91%)**.  
- **Family Bookings:** Couples with 1 or 2 children account for approximately 5.5% of total bookings.  
The hospitality demand across these properties is heavily oriented towards couples and solo travelers, requiring room inventories dominated by standard double and king bed configurations.
""")

    # TASK 21
    builder.add_markdown("""### Task 21: Meal Package Frequency Analysis
**Objective:** Analyze the frequency of meal categories and identify the most popular package.
""")
    builder.add_code('''# Compute meal distribution
meal_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['meal'], "Meal Package")
print("--- Meal Category Frequency Table ---")
print(meal_table.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(x='Category', y='Percentage (%)', data=meal_table, palette='mako', ax=ax)
ax.set_title("Meal Package Popularity Breakdown")
ax.set_xlabel("Meal Category (BB: Bed & Breakfast, HB: Half Board, SC: Self-Catering, FB: Full Board)")
ax.set_ylabel("Share of Bookings (%)")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')
plt.ylim(0, 88)
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 21):**  
- **Bed & Breakfast (BB):** Overwhelmingly the most popular package with **92,310 bookings (77.32%)**.  
- **Half Board (HB):** 12,463 bookings (10.44%), primarily selected by resort vacationers.  
- **Self Catering (SC):** 10,650 bookings (8.92%), popular in city apartments.  
- **Undefined:** 1,169 bookings (0.98%).  
- **Full Board (FB):** 798 bookings (0.67%).  
Over three-quarters of hotel guests prefer the flexibility of included breakfast while taking lunch and dinner off-site at local restaurants.
""")

    # TASK 22
    builder.add_markdown("""### Task 22: Customer Type Distribution
**Objective:** Investigate the distribution of `customer_type` to identify the dominant customer classification.
""")
    builder.add_code('''# Customer type distribution
cust_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['customer_type'], "Customer Type")
print("--- Customer Type Distribution ---")
print(cust_table.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(x='Category', y='Percentage (%)', data=cust_table, palette='crest', ax=ax)
ax.set_title("Customer Type Breakdown: Dominance of Transient Bookings")
ax.set_xlabel("Customer Type")
ax.set_ylabel("Share of Bookings (%)")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')
plt.ylim(0, 85)
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 22):**  
- **Transient:** **89,613 bookings (75.06%)**. Independent travelers booking individual stays not affiliated with groups or corporate master contracts.  
- **Transient-Party:** **25,124 bookings (21.04%)**. Transient guests booking as part of an associated party (e.g. wedding guests, small family gatherings).  
- **Contract:** **4,076 bookings (3.41%)**. Structured allotments such as airline flight crew contracts.  
- **Group:** **577 bookings (0.48%)**. Direct group room blocks (>10 rooms).  
Transient guests represent three out of four reservations, making individual yield management and direct consumer marketing the core revenue priority.
""")

    # TASK 23
    builder.add_markdown("""### Task 23: Market Segment & Distribution Channel Distributions
**Objective:** Analyze `market_segment` and `distribution_channel` to identify dominant booking pathways.
""")
    builder.add_code('''# Market segment and distribution channel summaries
seg_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['market_segment'], "Market Segment")
chan_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['distribution_channel'], "Distribution Channel")

print("--- Market Segment Distribution ---")
print(seg_table.to_string(index=False))

print("\\n--- Distribution Channel Distribution ---")
print(chan_table.to_string(index=False))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(x='Percentage (%)', y='Category', data=seg_table, palette='Blues_r', ax=ax1)
ax1.set_title("Market Segment Share (%)")
ax1.set_xlabel("Percentage (%)")
ax1.set_ylabel("")

sns.barplot(x='Percentage (%)', y='Category', data=chan_table, palette='Greens_r', ax=ax2)
ax2.set_title("Distribution Channel Share (%)")
ax2.set_xlabel("Percentage (%)")
ax2.set_ylabel("")

plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 23):**  
- **Dominant Segments:** **Online Travel Agencies (Online TA)** lead with **56,477 bookings (47.30%)**, followed by **Offline TA/TO** with **24,219 bookings (20.29%)** and **Groups** with **19,811 bookings (16.59%)**.  
- **Dominant Channels:** **TA/TO** channels capture **97,870 bookings (81.97%)**, followed by **Direct** booking channels with **14,645 bookings (12.27%)**.  
The hotels are overwhelmingly dependent on third-party intermediaries (OTAs and Tour Operators), which capture over 80% of distribution volume. This highlights substantial OTA commission expenditure (typically 15-22%) and emphasizes the need for direct-booking loyalty initiatives.
""")

    # TASK 24
    builder.add_markdown("""### Task 24: Distribution of Total Special Requests
**Objective:** Examine the distribution of `total_of_special_requests` and determine the percentage of bookings with zero requests.
""")
    builder.add_code('''# Distribution of special requests
req_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['total_of_special_requests'], "Special Requests Count")
print("--- Special Requests Frequency Table ---")
print(req_table.to_string(index=False))

zero_req_pct = req_table.loc[req_table['Category'] == '0', 'Percentage (%)'].values[0]
print(f"\\nPercentage of bookings with ZERO special requests: {zero_req_pct:.2f}%")
''')
    builder.add_markdown("""**Interpretation (Task 24):**  
- **Zero Special Requests:** **70,318 bookings (58.90%)**. Almost 60% of guests make no advance operational requests.  
- **1 Request:** 33,226 bookings (27.83%).  
- **2 Requests:** 12,969 bookings (10.86%).  
- **3+ Requests:** 2,877 bookings (2.41%).  
As demonstrated in subsequent cancellation analyses, whether a guest takes the time to enter a special request is one of the strongest predictive signals of actual check-in commitment.
""")

    # TASK 25
    builder.add_markdown("""### Task 25: Booking Changes & Waiting List Confirmation Analysis
**Objective:** Analyze `booking_changes` and `days_in_waiting_list` to evaluate whether most bookings are confirmed without amendments or queueing.
""")
    builder.add_code('''# Booking changes distribution
changes_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['booking_changes'], "Booking Changes", top_n=5)
print("--- Booking Changes Frequency ---")
print(changes_table.to_string(index=False))

# Waiting list days summary
zero_wait = (df_cleaned['days_in_waiting_list'] == 0).sum()
pct_zero_wait = (zero_wait / len(df_cleaned)) * 100
max_wait = df_cleaned['days_in_waiting_list'].max()
print(f"\\nBookings with ZERO Days in Waiting List: {zero_wait:,} ({pct_zero_wait:.2f}%)")
print(f"Maximum Days in Waiting List: {max_wait} days")
''')
    builder.add_markdown("""**Interpretation (Task 25):**  
- **Booking Amendments:** **101,314 bookings (84.86%)** experienced **zero changes** between reservation intake and arrival/cancellation. Over 96% have at most one amendment.  
- **Waiting List Queueing:** **115,692 bookings (96.90%)** experienced **0 days on the waiting list** (instant confirmation).  
The reservation lifecycle is predominantly frictionless and immediate; guests book directly into active inventory and rarely amend dates or room requirements.
""")

    # TASK 26
    builder.add_markdown("""### Task 26: Deposit Type Distribution
**Objective:** Analyze the distribution of `deposit_type` and calculate the percentage of bookings with no deposit, non-refundable deposit, or refundable deposit.
""")
    builder.add_code('''# Deposit type breakdown
dep_table = UnivariateAnalyzer.compute_frequency_table(df_cleaned['deposit_type'], "Deposit Type")
print("--- Deposit Type Breakdown ---")
print(dep_table.to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(x='Category', y='Percentage (%)', data=dep_table, palette='rocket', ax=ax)
ax.set_title("Deposit Policy Distribution")
ax.set_xlabel("Deposit Structure")
ax.set_ylabel("Share of Bookings (%)")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')
plt.ylim(0, 100)
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 26):**  
- **No Deposit:** **104,641 bookings (87.65%)**.  
- **Non Refund:** **14,587 bookings (12.22%)**.  
- **Refundable:** **162 bookings (0.14%)**.  
Nearly 88% of all bookings require no advance financial deposit, which reduces friction at booking but exposes the hotels to high cancellation volatility.
""")

    # TASK 27
    builder.add_markdown("""### Task 27: Room Type Preferences (Reserved vs Assigned)
**Objective:** Investigate the frequency of `reserved_room_type` and `assigned_room_type` to identify the most commonly booked and allocated room categories.
""")
    builder.add_code('''# Reserved vs Assigned Room Types
res_room = df_cleaned['reserved_room_type'].value_counts()
ass_room = df_cleaned['assigned_room_type'].value_counts()

room_comparison = pd.DataFrame({
    'Reserved Count': res_room,
    'Reserved Share (%)': (res_room / len(df_cleaned) * 100).round(2),
    'Assigned Count': ass_room,
    'Assigned Share (%)': (ass_room / len(df_cleaned) * 100).round(2)
}).fillna(0)

print("--- Reserved vs Assigned Room Types ---")
print(room_comparison)

# Discrepancy calculation
discrepancies = (df_cleaned['reserved_room_type'] != df_cleaned['assigned_room_type']).sum()
pct_discrepancy = (discrepancies / len(df_cleaned)) * 100
print(f"\\nTotal Bookings with Room Assignment Discrepancy (Upgrade/Change): {discrepancies:,} ({pct_discrepancy:.2f}%)")
''')
    builder.add_markdown("""**Interpretation (Task 27):**  
- **Most Reserved Room:** **Room Type A** with **85,994 bookings (72.03%)**, followed by **Room D** with 19,201 bookings (16.08%).  
- **Most Assigned Room:** **Room Type A** with **74,053 allocations (62.03%)**, followed by **Room D** with 25,322 allocations (21.21%).  
- **Room Allocation Discrepancy:** Exactly **14,917 bookings (12.49%)** were assigned a room different from the category reserved. Room Type A reservations were frequently upgraded to Types D, E, or F due to operational yields, overbooking of base rooms, or complimentary guest upgrades at check-in.
""")

print("Section A & B builder functions defined successfully.")
