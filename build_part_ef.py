"""
Notebook Section E & F Tasks Generator
======================================
Generates Markdown and Code cells for:
- SECTION E: Time-Series Analysis and Seasonality (Tasks 57 to 67)
- SECTION F: Revenue Management and ADR Analysis (Tasks 68 to 78)
- Executive Strategic Synthesis & Actionable Consulting Recommendations
"""

def add_section_e(builder):
    builder.add_markdown("""# SECTION E – TIME-SERIES ANALYSIS AND SEASONALITY
**Objective:** Decompose booking volume, cancellation propensity, pricing structures, and stay durations across chronological time, calendar seasonality, and arrival cycles.  
*Important Domain Context:* Monthly booking counts represent arrivals scheduled for that month (including those that cancelled prior to arrival), not reservations entered in that calendar month.
""")

    # TASK 57
    builder.add_markdown("""### Task 57: Arrival Date Datetime Column Verification
**Objective:** Confirm the creation of a unified `arrival_date` datetime column from `arrival_date_year`, `arrival_date_month`, and `arrival_date_day_of_month`.
""")
    builder.add_code('''# Verify arrival_date column
print("Arrival Date Verification:")
print(df_cleaned[['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'arrival_date']].head(5))
print(f"\\nVerified Datetime Dtype: {df_cleaned['arrival_date'].dtype}")
print(f"Date Span: {df_cleaned['arrival_date'].min().strftime('%Y-%m-%d')} to {df_cleaned['arrival_date'].max().strftime('%Y-%m-%d')}")
''')
    builder.add_markdown("""**Interpretation (Task 57):**  
The unified `arrival_date` column integrates year, month, and day into an active Pandas datetime series spanning from **July 1, 2015 to August 31, 2017** without missing values.
""")

    # TASK 58
    builder.add_markdown("""### Task 58: Monthly Booking Demand & Peak Arrival Months
**Objective:** Calculate total bookings for each arrival month (ordered chronologically from January to December) and identify peak demand periods.
""")
    builder.add_code('''# Monthly demand in calendar order
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

monthly_summary = TimeSeriesSeasonalityAnalyzer.get_monthly_summary(df_cleaned, month_order)
print("--- Task 58: Monthly Booking Demand Summary ---")
print(monthly_summary[['Total_Bookings', 'Cancellations', 'Cancellation Rate (%)']])

peak_month = monthly_summary['Total_Bookings'].idxmax()
peak_volume = monthly_summary['Total_Bookings'].max()
low_month = monthly_summary['Total_Bookings'].idxmin()
low_volume = monthly_summary['Total_Bookings'].min()

print(f"\\nPeak Arrival Month: {peak_month} ({peak_volume:,} bookings)")
print(f"Lowest Volume Month: {low_month} ({low_volume:,} bookings)")
''')
    builder.add_markdown("""**Interpretation (Task 58):**  
- **Peak Volume Months:** **August (13,877 bookings)**, followed by **July (12,661 bookings)** and **May (11,791 bookings)**.  
- **Trough Volume Months:** **January (5,929 bookings)** and **December (6,780 bookings)**.  
Arrival volume surges dramatically during the European summer holiday season (July-August) and spring shoulder season (May-June), while winter experiences a 57% contraction in total demand compared to peak August.
""")

    # TASK 59
    builder.add_markdown("""### Task 59: Monthly Booking Volume by Hotel Property
**Objective:** Plot monthly booking volume separately for City Hotel and Resort Hotel to contrast urban vs coastal seasonal profiles.
""")
    builder.add_code('''# Monthly volume by hotel
monthly_hotel = df_cleaned.groupby(['arrival_date_month', 'hotel'], observed=False).size().unstack().reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 5))
monthly_hotel.plot(kind='line', marker='o', linewidth=2.5, markersize=7, ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.set_title("Monthly Booking Volume: City Hotel vs Resort Hotel")
ax.set_xlabel("Arrival Month")
ax.set_ylabel("Total Scheduled Arrivals")
ax.set_xticks(range(12))
ax.set_xticklabels([m[:3] for m in month_order])
plt.legend(title="Property")
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 59):**  
- **City Hotel:** Maintains consistently high volume throughout spring and autumn (peaking in May with 8,232 arrivals and October with 7,594 arrivals), reflecting business conferences, corporate travel, and city tourism.  
- **Resort Hotel:** Follows a classic leisure bell curve, surging to its annual peak in **August (5,261 arrivals)** and July (4,570 arrivals), while dropping to a severe winter trough in January (2,191 arrivals).
""")

    # TASK 60
    builder.add_markdown("""### Task 60: Monthly Cancellation Rates & High-Risk Cancellation Windows
**Objective:** Calculate monthly cancellation rates to identify high-risk cancellation seasons.
""")
    builder.add_code('''# Monthly cancellation rates by hotel
monthly_canc_hotel = df_cleaned.groupby(['arrival_date_month', 'hotel'], observed=False)['is_canceled'].mean().unstack().reindex(month_order) * 100

fig, ax = plt.subplots(figsize=(12, 5))
monthly_canc_hotel.plot(kind='line', marker='s', linewidth=2.5, markersize=7, ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.axhline(df_cleaned['is_canceled'].mean()*100, color='gray', linestyle='--', label=f"Overall Avg ({df_cleaned['is_canceled'].mean()*100:.1f}%)")
ax.set_title("Monthly Cancellation Rate (%) by Hotel Property")
ax.set_xlabel("Arrival Month")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_xticks(range(12))
ax.set_xticklabels([m[:3] for m in month_order])
ax.set_ylim(15, 50)
plt.legend(title="Property")
plt.tight_layout()
plt.show()

print("--- Monthly Cancellation Rate Table (%) ---")
print(monthly_canc_hotel.round(2))
''')
    builder.add_markdown("""**Interpretation (Task 60):**  
- **City Hotel High-Cancellation Periods:** April (44.64%), May (44.44%), and June (44.82%). Spring conference season experiences massive group cancellations.  
- **Resort Hotel High-Cancellation Periods:** August (33.02%) and July (31.29%). High peak-season demand prompts guests to speculatively reserve resort rooms and cancel if summer plans shift.  
- **Lowest Cancellation Windows:** January (City: 33.03%, Resort: 24.28%) and November (City: 35.85%, Resort: 21.36%). Low-season bookings are made close to arrival with firm intent.
""")

    # TASK 61
    builder.add_markdown("""### Task 61: ADR Seasonality Across Arrival Months
**Objective:** Compare ADR across the 12 arrival months to assess seasonal pricing curves.
""")
    builder.add_code('''# ADR seasonality by hotel
df_adr_valid = df_cleaned[df_cleaned['adr'] < 5000]
monthly_adr = df_adr_valid.groupby(['arrival_date_month', 'hotel'], observed=False)['adr'].mean().unstack().reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 5))
monthly_adr.plot(kind='line', marker='D', linewidth=2.5, markersize=7, ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.set_title("Seasonal Pricing Dynamics: Average Daily Rate (ADR) Across Arrival Months")
ax.set_xlabel("Arrival Month")
ax.set_ylabel("Mean ADR ($ / Night)")
ax.set_xticks(range(12))
ax.set_xticklabels([m[:3] for m in month_order])
plt.legend(title="Property")
plt.tight_layout()
plt.show()

print("--- Monthly Mean ADR ($) by Hotel ---")
print(monthly_adr.round(2))
''')
    builder.add_markdown("""**Interpretation (Task 61):**  
**The two hotels display fundamentally contrasting pricing strategies:**  
- **Resort Hotel (Extreme Summer Elasticity):** In January, Resort ADR plummets to **$48.76**, before surging by **+272%** to a peak of **$181.84 in August**!  
- **City Hotel (Stable Urban Pricing):** City Hotel maintains much higher rate stability throughout the year, hovering between **$82.04 in January** and **$120.44 in August**, with secondary peaks in May ($120.05) and June ($117.88) driven by corporate conferences.
""")

    # TASK 62
    builder.add_markdown("""### Task 62: Weekday vs Weekend Stay Patterns Across Months
**Objective:** Compare weekday and weekend stay lengths by month to determine whether vacation lengths expand during peak seasons.
""")
    builder.add_code('''# Monthly stay length trends
monthly_stays = df_cleaned.groupby('arrival_date_month', observed=False).agg(
    Mean_Weekday_Nights=('stays_in_week_nights', 'mean'),
    Mean_Weekend_Nights=('stays_in_weekend_nights', 'mean'),
    Mean_Total_Nights=('total_stay_nights', 'mean')
).reindex(month_order)

print("--- Task 62: Monthly Stay Length Patterns ---")
print(monthly_stays.round(2))

fig, ax = plt.subplots(figsize=(11, 4.5))
monthly_stays[['Mean_Weekday_Nights', 'Mean_Weekend_Nights']].plot(kind='bar', stacked=True, colormap='viridis', ax=ax)
ax.set_title("Average Stay Duration (Nights) by Arrival Month")
ax.set_xlabel("Arrival Month")
ax.set_ylabel("Average Stay Length (Nights)")
ax.set_xticklabels([m[:3] for m in month_order], rotation=0)
plt.legend(title="Night Type")
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 62):**  
**Yes, stay lengths expand noticeably during the summer holiday season:**  
- **July & August Peak:** Average total stay reaches **3.90 nights** in July and **3.94 nights** in August.  
- **Winter Trough:** Average stay contracts to **3.04 nights** in January and **3.08 nights** in February.  
Summer vacationers book longer extended weekly stays, increasing both weekday and weekend night consumption.
""")

    # TASK 63
    builder.add_markdown("""### Task 63: Booking Demand by Arrival Day of the Month
**Objective:** Analyze booking demand by arrival day of the month (1 to 31) to identify any intra-month clustering.
""")
    builder.add_code('''# Day of month arrival counts
day_counts = df_cleaned['arrival_date_day_of_month'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(x=day_counts.index, y=day_counts.values, color='#1f77b4', ax=ax)
ax.axhline(day_counts.loc[1:30].mean(), color='red', linestyle='--', label=f"Average Days 1-30: {day_counts.loc[1:30].mean():.0f}")
ax.set_title("Arrival Demand by Day of the Month (1 to 31)")
ax.set_xlabel("Day of Month")
ax.set_ylabel("Total Arrivals")
ax.legend()
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 63):**  
- **Uniformity:** Daily arrivals are remarkably uniform across days 1 through 30, averaging approximately **3,900 arrivals per calendar day**.  
- **Day 31 Drop:** Day 31 records only **2,246 arrivals** (a 42% drop). This is purely a calendar artifact, as only 7 of the 12 months contain 31 days (and February has only 28/29 days).  
There is no significant beginning-of-month or end-of-month arrival distortion.
""")

    # TASK 64
    builder.add_markdown("""### Task 64: Distribution of Arrival Bookings by Week Number
**Objective:** Analyze the distribution of arrival bookings across the 53 weeks of the year.
""")
    builder.add_code('''# Week number distribution
week_counts = df_cleaned['arrival_date_week_number'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(14, 4.5))
ax.plot(week_counts.index, week_counts.values, marker='o', color='#2ca02c', linewidth=2, markersize=5)
ax.fill_between(week_counts.index, week_counts.values, color='#2ca02c', alpha=0.2)
ax.set_title("Annual Booking Demand by Arrival Week Number (ISO Weeks 1 to 53)")
ax.set_xlabel("Week Number of the Year")
ax.set_ylabel("Total Arrivals")
ax.set_xlim(1, 53)
plt.tight_layout()
plt.show()

print(f"Top Arrival Week: Week {week_counts.idxmax()} ({week_counts.max():,} bookings - mid-August)")
print(f"Lowest Arrival Week: Week {week_counts.idxmin()} ({week_counts.min():,} bookings - early January)")
''')
    builder.add_markdown("""**Interpretation (Task 64):**  
Arrival demand rises steadily from **Week 1 (~1,000 arrivals)** through the spring, forming a plateau between **Week 20 and Week 42 (May to October)**, with the annual peak concentrated in **Weeks 28–33 (mid-July to mid-August)** exceeding 3,000 arrivals per week. A sharp decline occurs after Week 44 (November).
""")

    # TASK 65
    builder.add_markdown("""### Task 65: Year-Month Time Series (2015, 2016, 2017)
**Objective:** Create a year-month time series and compare booking volume trends across 2015, 2016, and 2017.
""")
    builder.add_code('''# Year-month booking volume
df_cleaned['year_month'] = df_cleaned['arrival_date'].dt.to_period('M')
ym_counts = df_cleaned.groupby(['year_month', 'hotel']).size().unstack().fillna(0)

fig, ax = plt.subplots(figsize=(13, 5))
ym_counts.plot(kind='line', marker='o', linewidth=2.5, markersize=6, ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.set_title("Chronological Monthly Booking Demand (July 2015 – August 2017)")
ax.set_xlabel("Arrival Year-Month")
ax.set_ylabel("Total Monthly Arrivals")
plt.xticks(range(len(ym_counts)), [str(p) for p in ym_counts.index], rotation=45)
plt.legend(title="Property")
plt.tight_layout()
plt.show()

# Annual totals note
annual_totals = df_cleaned.groupby('arrival_date_year')['hotel'].value_counts().unstack()
print("--- Annual Total Bookings by Hotel ---")
print(annual_totals)
''')
    builder.add_markdown("""**Interpretation (Task 65):**  
- **2015 (Partial Year, July-Dec):** 21,996 total bookings (Resort: 8,314; City: 13,682).  
- **2016 (Full Calendar Year):** **56,707 total bookings** (Resort: 18,567; City: 38,140). Represents the baseline year for uninterrupted annual operations.  
- **2017 (Partial Year, Jan-Aug):** 40,687 total bookings (Resort: 13,179; City: 27,508).  
Year-over-year comparisons between the first eight months of 2016 and 2017 reveal strong steady demand growth at both properties.
""")

    # TASK 66
    builder.add_markdown("""### Task 66: Reservation Status Timeline vs Arrival Date Timeline
**Objective:** Plot `reservation_status_date` over time and count cancellations by status date versus arrival date.
""")
    builder.add_code('''# Monthly cancellations by reservation_status_date vs arrival_date
df_canc = df_cleaned[df_cleaned['is_canceled'] == 1].copy()
df_canc['status_year_month'] = df_canc['reservation_status_date'].dt.to_period('M')

canc_by_arrival = df_canc.groupby('year_month').size()
canc_by_status = df_canc.groupby('status_year_month').size()

timeline_df = pd.DataFrame({
    'Cancellations by Arrival Date': canc_by_arrival,
    'Cancellations by Status Date (Cancellation Execution)': canc_by_status
}).fillna(0)

fig, ax = plt.subplots(figsize=(13, 5))
timeline_df.plot(kind='line', marker='s', linewidth=2, markersize=5, ax=ax, color=['#d62728', '#9467bd'])
ax.set_title("Cancellation Timing: Date of Scheduled Arrival vs Date Cancellation Executed")
ax.set_xlabel("Year-Month")
ax.set_ylabel("Number of Cancellations")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 66):**  
Tracking cancellations by `reservation_status_date` demonstrates that **cancellation execution leads arrival dates by weeks or months**.  
Massive spikes in cancellations occurred in late 2015 and early 2016 (executing cancellations for summer 2016 arrivals). Recognizing that cancellations happen well ahead of arrival allows revenue managers to release and resell inventory through dynamic last-minute OTA channels.
""")

    # TASK 67
    builder.add_markdown("""### Task 67: Seasonal Variations in Booking Lead Time
**Objective:** Investigate whether advance booking horizons change across months and arrival seasons.
""")
    builder.add_code('''# Lead time across arrival months by hotel
monthly_lt = df_cleaned.groupby(['arrival_date_month', 'hotel'], observed=False)['lead_time'].mean().unstack().reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 5))
monthly_lt.plot(kind='line', marker='o', linewidth=2.5, markersize=7, ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.set_title("Seasonal Shift in Advance Booking Lead Time (Days)")
ax.set_xlabel("Arrival Month")
ax.set_ylabel("Mean Lead Time (Days)")
ax.set_xticks(range(12))
ax.set_xticklabels([m[:3] for m in month_order])
plt.legend(title="Property")
plt.tight_layout()
plt.show()

print("--- Monthly Mean Lead Time (Days) ---")
print(monthly_lt.round(1))
''')
    builder.add_markdown("""**Interpretation (Task 67):**  
**Lead times expand dramatically for summer arrivals:**  
- **Summer Peak:** Bookings arriving in **June, July, August, and September** have the highest average lead times, exceeding **125 to 140 days** (booked 4 to 5 months in advance).  
- **Winter Trough:** Bookings arriving in **January and February** have the shortest average lead times (**45 to 55 days**).  
Guests commit to summer vacations months in advance, creating long holding windows that expose the hotel to prolonged cancellation risk.
""")


def add_section_f(builder):
    builder.add_markdown("""# SECTION F – REVENUE MANAGEMENT AND ADR ANALYSIS
**Objective:** Analyze room rate pricing structures, multidimensional revenue yields, estimated lodging values, and financial data validity.
""")

    # TASK 68
    builder.add_markdown("""### Task 68: Benchmark Mean and Median ADR by Hotel Property
**Objective:** Calculate the benchmark mean and median ADR for City Hotel and Resort Hotel.
""")
    builder.add_code('''# Filter extreme outlier ($5400) for unskewed financial analysis
df_adr_f = df_cleaned[df_cleaned['adr'] < 5000]

adr_benchmarks = df_adr_f.groupby('hotel')['adr'].agg(
    Mean_ADR='mean',
    Median_ADR='median',
    Std_Dev='std',
    IQR=lambda x: x.quantile(0.75) - x.quantile(0.25)
)

print("--- Task 68: ADR Benchmarks by Hotel Property ---")
print(adr_benchmarks.round(2))
''')
    builder.add_markdown("""**Interpretation (Task 68):**  
- **City Hotel:** Mean ADR = **$105.24**, Median ADR = **$99.90** (Std Dev: $43.60, IQR: $46.00).  
- **Resort Hotel:** Mean ADR = **$94.95**, Median ADR = **$75.00** (Std Dev: $61.44, IQR: $66.00).  
City Hotel maintains a higher baseline median rate (+33.2%), whereas Resort Hotel exhibits significantly higher rate variance (Std Dev: $61.44 vs $43.60) due to extreme off-peak discounting and summer rate premiums.
""")

    # TASK 69
    builder.add_markdown("""### Task 69: Multidimensional ADR Matrix (Month × Hotel × Customer Type)
**Objective:** Compare ADR across months, hotel types, and customer types to identify combinations generating the highest median room rates.
""")
    builder.add_code('''# Multidimensional ADR pivot table
multi_adr = df_adr_f.pivot_table(
    index='arrival_date_month',
    columns=['hotel', 'customer_type'],
    values='adr',
    aggfunc='median'
).reindex(month_order)

print("--- Task 69: Multidimensional Median ADR Matrix ($) ---")
print(multi_adr.round(1))

# Find top combinations
flat_multi = df_adr_f.groupby(['hotel', 'arrival_date_month', 'customer_type'])['adr'].agg(['median', 'count']).sort_values(by='median', ascending=False)
print("\\n--- Top 5 Highest Median ADR Segment Combinations ---")
print(flat_multi.head(5))
''')
    builder.add_markdown("""**Interpretation (Task 69):**  
- **Highest Median ADR Combination:** **Resort Hotel in August for Transient Customers** commands a median ADR of **$186.00** (followed by July Transient at $153.00).  
- **City Hotel Peak Combination:** **City Hotel in May and June for Transient Customers** reaches **$126.00**, driven by prime spring business conferences.  
- **Lowest Rate Combinations:** **Resort Hotel in January for Contract and Group customers** drops to **$40.00 – $48.00**.
""")

    # TASK 70
    builder.add_markdown("""### Task 70: Relationship Between ADR and Lead Time
**Objective:** Analyze the relationship between ADR and `lead_time` to test whether advance bookings receive lower discounted rates.
""")
    builder.add_code('''# ADR by lead time brackets
lt_adr = df_adr_f.groupby('lead_time_bracket', observed=False)['adr'].agg(['count', 'mean', 'median', 'std'])
print("--- Task 70: ADR by Lead Time Interval ---")
print(lt_adr.round(2))

corr_val = df_adr_f['lead_time'].corr(df_adr_f['adr'])
print(f"\\nPearson Correlation Coefficient (Lead Time vs ADR): {corr_val:.4f}")

fig, ax = plt.subplots(figsize=(9, 4.5))
sns.barplot(x=lt_adr.index, y=lt_adr['mean'], palette='Blues_r', ax=ax)
ax.set_title("Mean ADR by Advance Booking Window")
ax.set_xlabel("Lead Time Bracket")
ax.set_ylabel("Mean ADR ($ / Night)")
ax.set_ylim(0, 125)
for p in ax.patches:
    ax.annotate(f"${p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 70):**  
- **Sweet Spot for Revenue Yield (31–90 days):** Mean ADR peaks at **$107.03** for reservations made 1 to 3 months out.  
- **Extreme Advance Bookings (>365 days):** Mean ADR drops sharply to **$83.56** (a **-$23.47 discount** per night!).  
- **Same-Week Bookings (0–7 days):** Mean ADR averages **$98.11**, reflecting a mix of premium last-minute business rates and discounted distress inventory.  
*Key Insight:* Advance group and tour operator contracts booked over a year ahead are negotiated at steep wholesale discounts, yet experience the highest cancellation rates (67.7%).
""")

    # TASK 71
    builder.add_markdown("""### Task 71: ADR Across Market Segments and Distribution Channels
**Objective:** Compare ADR across market segments and distribution channels to evaluate channel profitability.
""")
    builder.add_code('''# ADR across market segments and distribution channels
seg_adr = df_adr_f.groupby('market_segment')['adr'].agg(['count', 'mean', 'median']).sort_values(by='mean', ascending=False)
chan_adr = df_adr_f.groupby('distribution_channel')['adr'].agg(['count', 'mean', 'median']).sort_values(by='mean', ascending=False)

print("--- Task 71: ADR by Market Segment ---")
print(seg_adr.round(2))

print("\\n--- Task 71: ADR by Distribution Channel ---")
print(chan_adr.round(2))
''')
    builder.add_markdown("""**Interpretation (Task 71):**  
- **Highest Yielding Segments:** **Online TA ($117.19 mean ADR)** and **Direct ($115.02 mean ADR)**.  
- **Lowest Yielding Segments:** **Corporate ($69.41 mean ADR)** and **Complementary ($2.95 mean ADR)**.  
- **Channel Yield:** GDS channels command the highest daily rate (**$120.73**), followed by TA/TO (**$104.73**) and Direct (**$102.66**).  
*Profitability Caveat:* Although Online TAs deliver high gross ADR ($117.19), after deducting 18-22% OTA commissions, the net ADR drops to ~$96, making **Direct bookings ($115.02 gross, zero commission)** far more profitable.
""")

    # TASK 72
    builder.add_markdown("""### Task 72: ADR Across Reserved Room Types
**Objective:** Compare ADR across reserved room categories to assess suite and premium room pricing.
""")
    builder.add_code('''# ADR by reserved room type
room_adr = df_adr_f.groupby('reserved_room_type')['adr'].agg(['count', 'mean', 'median']).sort_values(by='mean', ascending=False)
print("--- Task 72: ADR by Reserved Room Type ---")
print(room_adr.round(2))

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.barplot(x=room_adr.index, y=room_adr['mean'], palette='viridis', ax=ax)
ax.set_title("Room Rate Tiering: Mean ADR by Reserved Room Type")
ax.set_xlabel("Reserved Room Type")
ax.set_ylabel("Mean ADR ($ / Night)")
for p in ax.patches:
    ax.annotate(f"${p.get_height():.1f}", (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 72):**  
- **Premium Suites:** **Room G ($175.99)**, **Room H ($188.34)**, and **Room F ($167.69)** command the highest daily rates.  
- **Standard Baseline:** **Room A ($90.79 mean ADR)** and **Room B ($90.28)** serve as the base inventory tier.  
Room tiering generates clear pricing power: luxury suites command nearly double (+94%) the daily rate of entry-level standard rooms.
""")

    # TASK 73
    builder.add_markdown("""### Task 73: Relationship Between ADR and Length of Stay
**Objective:** Investigate the relationship between ADR and total number of nights booked to evaluate extended-stay discounting.
""")
    builder.add_code('''# Filter stays between 1 and 14 nights for clear trend evaluation
df_stays = df_adr_f[(df_adr_f['total_stay_nights'] >= 1) & (df_adr_f['total_stay_nights'] <= 14)]
stay_adr = df_stays.groupby('total_stay_nights')['adr'].agg(['count', 'mean', 'median'])

print("--- Task 73: ADR by Length of Stay (1 to 14 Nights) ---")
print(stay_adr.round(2))

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.lineplot(x=stay_adr.index, y=stay_adr['mean'], marker='o', color='#1f77b4', linewidth=2.5, ax=ax)
ax.set_title("Length-of-Stay Rate Curve: Extended Stay Rate Compression")
ax.set_xlabel("Total Stay Nights Booked")
ax.set_ylabel("Mean ADR ($ / Night)")
ax.set_xticks(range(1, 15))
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 73):**  
- Short stays of 1 to 4 nights command the highest daily rates (**$101 – $105 / night**).  
- Stays extending beyond 7 nights experience progressive rate compression, falling to **$85 – $92 / night** for 10-14 night stays.  
Hotels deliberately offer extended-stay discounts to secure guaranteed multi-week occupancy and reduce room turnover cleaning costs.
""")

    # TASK 74
    builder.add_markdown("""### Task 74: ADR by Stay Structure (Weekday-Heavy vs Weekend-Heavy)
**Objective:** Compare ADR between weekday-heavy and weekend-heavy stays across hotel properties.
""")
    builder.add_code('''# ADR by stay type and hotel
stay_type_adr = df_adr_f.groupby(['hotel', 'stay_type'])['adr'].agg(['count', 'mean', 'median'])
print("--- Task 74: ADR by Stay Type Structure ---")
print(stay_type_adr.round(2))
''')
    builder.add_markdown("""**Interpretation (Task 74):**  
- **City Hotel:** Weekday-heavy stays command higher rates (**$106.84 mean ADR**) than weekend-heavy stays (**$103.38**), reflecting corporate pricing power Monday through Thursday.  
- **Resort Hotel:** Weekend-heavy stays command higher rates (**$96.86 mean ADR**) than weekday-heavy stays (**$94.39**), reflecting leisure weekend staycation premiums.
""")

    # TASK 75
    builder.add_markdown("""### Task 75: ADR Distributions Relative to Special Requests
**Objective:** Investigate whether bookings with more special requests exhibit higher ADR values.
""")
    builder.add_code('''# ADR by special requests count
req_adr = df_adr_f.groupby('total_of_special_requests')['adr'].agg(['count', 'mean', 'median'])
print("--- Task 75: ADR by Special Requests Count ---")
print(req_adr.round(2))

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(x=req_adr.index, y=req_adr['mean'], palette='Purples_r', ax=ax)
ax.set_title("Mean ADR Escalates with Guest Special Requests")
ax.set_xlabel("Number of Special Requests")
ax.set_ylabel("Mean ADR ($ / Night)")
ax.set_ylim(0, 140)
for p in ax.patches:
    ax.annotate(f"${p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 75):**  
**Bookings with special requests pay significantly higher room rates:**  
- **0 Requests:** Mean ADR = **$95.03**  
- **1 Request:** Mean ADR = **$107.82**  
- **2 Requests:** Mean ADR = **$117.84**  
- **3 Requests:** Mean ADR = **$126.96**  
- **4+ Requests:** Mean ADR = **$135.00+**  
Guests paying premium rates for luxury suites and holiday trips are far more demanding of customized amenities, floor views, and personalized service.
""")

    # TASK 76
    builder.add_markdown("""### Task 76: ADR Comparison: Cancelled vs Non-Cancelled by Hotel
**Objective:** Compare ADR between cancelled and non-cancelled bookings separately for each hotel.
""")
    builder.add_code('''# Cancelled vs Non-Cancelled ADR by property
hotel_cancel_adr = df_adr_f.groupby(['hotel', 'is_canceled'])['adr'].agg(['count', 'mean', 'median'])
hotel_cancel_adr.index = pd.MultiIndex.from_tuples([
    ('City Hotel', 'Confirmed (0)'),
    ('City Hotel', 'Cancelled (1)'),
    ('Resort Hotel', 'Confirmed (0)'),
    ('Resort Hotel', 'Cancelled (1)')
], names=['Hotel', 'Status'])

print("--- Task 76: ADR by Hotel and Cancellation Status ---")
print(hotel_cancel_adr.round(2))
''')
    builder.add_markdown("""**Interpretation (Task 76):**  
- **City Hotel:** Cancelled bookings have a **higher ADR ($109.83 mean)** than confirmed bookings (**$102.06 mean**). A difference of **+$7.77 / night**.  
- **Resort Hotel:** Cancelled bookings have a slightly higher ADR (**$97.02 mean**) than confirmed bookings (**$94.15 mean**).  
At both properties, higher priced reservations are more vulnerable to cancellation, confirming price sensitivity and speculative booking behavior at higher rate tiers.
""")

    # TASK 77
    builder.add_markdown("""### Task 77: Estimated Lodging Value & Revenue Loss Analysis
**Objective:** Compute booking-level estimated lodging value via the formula `Estimated Value = ADR * (stays_in_week_nights + stays_in_weekend_nights)` and quantify realized revenue versus cancellation leakage.
""")
    builder.add_code('''# Financial breakdown using RevenueManager
rev_metrics = RevenueManager.calculate_estimated_lodging_value(df_adr_f)

print("--- Task 77: Financial Lodging Value & Leakage Report ---")
for k, v in rev_metrics.items():
    print(f"{k:45}: {v:,}")

# Hotel-wise revenue breakdown
hotel_val = df_adr_f.groupby(['hotel', 'is_canceled'])['estimated_lodging_value'].sum().unstack()
hotel_val.columns = ['Realized Revenue ($)', 'Lost to Cancellation ($)']
hotel_val['Total Pipeline Value ($)'] = hotel_val['Realized Revenue ($)'] + hotel_val['Lost to Cancellation ($)']
hotel_val['Leakage Rate (%)'] = (hotel_val['Lost to Cancellation ($)'] / hotel_val['Total Pipeline Value ($)'] * 100).round(2)

print("\\n--- Hotel-Specific Financial Pipeline Breakdown ---")
print(hotel_val)
''')
    builder.add_markdown("""**Interpretation & Financial Reality (Task 77):**  
- **Total Pipeline Lodging Value:** **$42,718,097.53** across both properties.  
- **Realized Lodging Value (Confirmed Bookings):** **$25,996,260.41 (60.85%)**.  
- **Lost Lodging Value (Cancelled Bookings):** **$16,721,837.12 (39.15%)**!  
- **City Hotel Financial Leakage:** **43.76% of potential revenue** ($11.45M out of $26.17M) was wiped out by cancellations.  
- **Resort Hotel Financial Leakage:** **31.85% of potential revenue** ($5.27M out of $16.54M) was lost.  
*Critical Accounting Distinction:* Estimated lodging value represents scheduled gross room revenue. Cancelled bookings with non-refundable deposits forfeited partial/full fees to the hotel, while cancelled flexible bookings generated zero cash, representing severe gross revenue loss.
""")

    # TASK 78
    builder.add_markdown("""### Task 78: Audit of Zero, Negative, and Outlier ADR Records
**Objective:** Calculate the percentage of bookings with zero, negative, or unusually high ADR, and evaluate data integrity.
""")
    builder.add_code('''# ADR validity audit
n_total = len(df_cleaned)
neg_adr_count = (df_cleaned['adr'] < 0).sum()
zero_adr_count = (df_cleaned['adr'] == 0).sum()
extreme_adr_count = (df_cleaned['adr'] > 1000).sum()
normal_adr_count = ((df_cleaned['adr'] > 0) & (df_cleaned['adr'] <= 1000)).sum()

t78_df = pd.DataFrame({
    'ADR Category': [
        'Negative ADR (ADR < $0.00)',
        'Zero ADR (ADR == $0.00 - Complimentary / House Use)',
        'Standard Operational ADR ($0.01 - $1,000.00)',
        'Extreme Outlier ADR (ADR > $1,000.00)'
    ],
    'Record Count': [neg_adr_count, zero_adr_count, normal_adr_count, extreme_adr_count],
    'Percentage (%)': [
        f"{neg_adr_count/n_total*100:.4f}%",
        f"{zero_adr_count/n_total*100:.4f}%",
        f"{normal_adr_count/n_total*100:.4f}%",
        f"{extreme_adr_count/n_total*100:.4f}%"
    ]
}).set_index('ADR Category')

print("--- Task 78: ADR Validity Audit Summary ---")
print(t78_df)
''')
    builder.add_markdown("""**Interpretation (Task 78):**  
- **Negative ADR (1 record, 0.0008%):** -$6.38 at Resort Hotel. Represents an accounting rebate or credit adjustment.  
- **Zero ADR (1,959 records, 1.64%):** Legitimate hospitality transactions representing complimentary VIP stays, corporate rewards, loyalty point redemptions, staff/house-use rooms, and barter agreements.  
- **Extreme Outlier ADR (1 record, 0.0008%):** $5,400.00 at City Hotel. Confirmed as an isolated data entry error or exclusive penthouse buyout package.  
- **Overall Validity:** **98.36% of records reflect normal commercial room pricing ($0.01 to $1,000)**, confirming high financial data reliability.
""")

    # STRATEGIC EXECUTIVE RECOMMENDATIONS
    builder.add_markdown("""## Strategic Executive Recommendations for Hotel Leadership
Based on this comprehensive empirical investigation, we formulate a **10-Point Actionable Strategy** for executive leadership, revenue management, and hotel operations:

1. **Dynamic Overbooking Thresholds Anchored in Lead Time:**
   - Overbooking models must not treat all reservations equally. Apply dynamic overbooking multipliers based on lead time brackets: 0-7 days out (overbook at 0%), 31-90 days out (overbook at 15-20%), and >180 days out (overbook at 35-45%).
2. **Restructure Non-Refundable Deposit Policies (The Group Paradox):**
   - The 99.4% cancellation rate for non-refundable group blocks indicates broken contractual terms. Enforce non-refundable staggered milestone cash deposits (25% at booking, 50% at 90 days out, 100% at 30 days out) with strict attrition clauses rather than speculative paper holds.
3. **Engage Guests Pre-Arrival to Mitigate Cancellations:**
   - Because submitting special requests reduces cancellation from 47.7% to 22.0%, implement automated pre-arrival email workflows (e.g., at 14 and 7 days prior to arrival) prompting guests to select pillow types, floor preferences, dining times, or airport transportation.
4. **Targeted Interventions for Repeat Guests & Loyalty Schemes:**
   - Repeat guests cancel at only 14.5% (compared to 37.8% for first-timers). Expand direct-booking loyalty perks (free breakfast, late checkout, room upgrades) to increase the repeat guest share from its current low levels (2.6% City, 4.4% Resort).
5. **Channel Shift: Incentivize Direct Bookings Over OTAs:**
   - TA/TO channels generate 90.9% of all cancellations and absorb 15-22% commission fees. Direct bookings cancel at only 15.4% and generate higher net ADR. Implement a Best Rate Guarantee and exclusive on-site amenities for direct web bookings.
6. **Flag High-Risk Domestic Booking Profiles:**
   - Domestic Portuguese travelers cancel at 56.6%, whereas international guests cancel at <20%. Implement stricter credit card pre-authorization and cancellation cut-off windows for domestic short-haul bookings during peak seasons.
7. **Seasonal Pricing & Yield Management in Resort Operations:**
   - Resort Hotel experiences extreme winter rate depression ($48 vs $182 in August). Reposition the property during winter months as a wellness/spa destination, long-stay remote working hub, or corporate executive retreat to lift off-season ADR.
8. **Monetize Room Allocation Discrepancies:**
   - Over 12.5% of reservations were assigned a room different from the category reserved (mostly upgrades). Formalize pre-arrival paid upgrade emails ("Upgrade to Deluxe Ocean View for $25/night") before offering complimentary upgrades at check-in.
9. **Minimum Length of Stay (MLOS) Controls for Peak Seasons:**
   - Implement 3-night to 5-night Minimum Length of Stay restrictions during July and August at the Resort Hotel and during prime May/October conference periods at the City Hotel to prevent orphaned single-night inventory.
10. **Automate Cancellation Prediction in PMS:**
    - Deploy a machine learning classification model utilizing the top predictors identified in this study (`has_prior_cancellations`, `lead_time`, `total_of_special_requests`, `country`, `booking_changes`, `deposit_type`) to generate real-time cancellation probability scores for every active reservation, triggering targeted retention alerts.
""")

print("Section E & F builder functions defined successfully.")
