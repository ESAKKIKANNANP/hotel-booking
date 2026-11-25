"""
Notebook Section C & D Tasks Generator
======================================
Generates Markdown and Code cells for:
- SECTION C: Hotel-Wise Comparative Analysis: City Hotel vs Resort Hotel (Tasks 28 to 39)
  * Rigorously reporting both Absolute Difference and Relative Difference (%) for every metric.
- SECTION D: Cancellation Analysis (Tasks 40 to 56 + Research Interpretation Challenge)
"""

def add_section_c(builder):
    builder.add_markdown("""# SECTION C – HOTEL-WISE COMPARATIVE ANALYSIS (CITY HOTEL VS RESORT HOTEL)
**Objective:** Compare the operational, behavioral, and commercial profiles of the two hotel properties.  
**Methodological Requirement:** For every comparison, we compute and report **both the absolute difference and the percentage/relative difference** to prevent scale bias arising from differing dataset sizes.
""")

    # TASK 28
    builder.add_markdown("""### Task 28: Total Booking Volume & Market Share Comparison
**Objective:** Compare the total number of bookings for City Hotel and Resort Hotel, and determine which hotel holds the larger share of the dataset.
""")
    builder.add_code('''# Compare booking volume
city_bookings = len(df_cleaned[df_cleaned['hotel'] == 'City Hotel'])
resort_bookings = len(df_cleaned[df_cleaned['hotel'] == 'Resort Hotel'])
total_bookings = len(df_cleaned)

abs_diff_bookings = city_bookings - resort_bookings
rel_diff_bookings = (city_bookings - resort_bookings) / resort_bookings * 100

t28_df = pd.DataFrame({
    'Metric': ['Total Bookings', 'Dataset Share (%)'],
    'City Hotel': [f"{city_bookings:,}", f"{city_bookings/total_bookings*100:.2f}%"],
    'Resort Hotel': [f"{resort_bookings:,}", f"{resort_bookings/total_bookings*100:.2f}%"],
    'Absolute Difference (City - Resort)': [f"+{abs_diff_bookings:,}", f"+{(city_bookings - resort_bookings)/total_bookings*100:.2f}% pts"],
    'Relative Difference (%)': [f"+{rel_diff_bookings:.2f}%", f"+{rel_diff_bookings:.2f}%"]
}).set_index('Metric')

print("--- Task 28: Total Bookings Comparison ---")
print(t28_df)
''')
    builder.add_markdown("""**Interpretation (Task 28):**  
- **City Hotel:** 79,330 bookings (**66.45%** share).  
- **Resort Hotel:** 40,060 bookings (**33.55%** share).  
- **Absolute Difference:** City Hotel exceeds Resort Hotel by **+39,270 bookings** (+32.90 percentage points of market share).  
- **Relative Difference:** City Hotel has **+98.03%** more bookings than the Resort Hotel (nearly double the volume). This reflects the higher room capacity and year-round business travel demand in Lisbon compared to the seasonal coastal resort in Algarve.
""")

    # TASK 29
    builder.add_markdown("""### Task 29: Cancellation Percentage Comparison
**Objective:** Compare the cancellation rates between City Hotel and Resort Hotel using both absolute and relative differences, avoiding raw count distortions.
""")
    builder.add_code('''# Cancellation percentage comparison
cancel_comp = df_cleaned.groupby('hotel')['is_canceled'].agg(
    Total_Bookings='count',
    Cancellations='sum',
    Cancellation_Rate='mean'
)
cancel_comp['Cancellation Rate (%)'] = cancel_comp['Cancellation_Rate'] * 100

city_cr = cancel_comp.loc['City Hotel', 'Cancellation Rate (%)']
resort_cr = cancel_comp.loc['Resort Hotel', 'Cancellation Rate (%)']

abs_cr_diff = city_cr - resort_cr
rel_cr_diff = (city_cr - resort_cr) / resort_cr * 100

t29_df = pd.DataFrame({
    'City Hotel': [f"{city_cr:.2f}%"],
    'Resort Hotel': [f"{resort_cr:.2f}%"],
    'Absolute Difference (City - Resort)': [f"+{abs_cr_diff:.2f}% pts"],
    'Relative Difference (%)': [f"+{rel_cr_diff:.2f}%"]
}, index=['Cancellation Rate'])

print("--- Task 29: Hotel Cancellation Rate Comparison ---")
print(t29_df)

# Visualization
fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(x=cancel_comp.index, y=cancel_comp['Cancellation Rate (%)'], palette=['#1f77b4', '#ff7f0e'], ax=ax)
ax.set_title("Cancellation Rate by Hotel Property")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 50)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 29):**  
- **City Hotel Cancellation Rate:** **41.73%** (33,102 cancellations out of 79,330 bookings).  
- **Resort Hotel Cancellation Rate:** **27.76%** (11,122 cancellations out of 40,060 bookings).  
- **Absolute Difference:** City Hotel has a **+13.96 percentage point higher** cancellation rate.  
- **Relative Difference:** The cancellation rate at City Hotel is **+50.30% higher** than at the Resort Hotel.  
*Root Cause:* City Hotel caters to business travelers and short-notice online bookings with high substitution alternatives in an urban market, whereas Resort guests plan family vacations around flights, making cancellations substantially rarer.
""")

    # TASK 30
    builder.add_markdown("""### Task 30: Lead Time Distribution Comparison
**Objective:** Compare average, median, and distributions of `lead_time` for both hotels to establish which hotel receives reservations further in advance.
""")
    builder.add_code('''# Lead time comparison
lt_mean_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['lead_time'].mean()
lt_med_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['lead_time'].median()

lt_mean_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['lead_time'].mean()
lt_med_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['lead_time'].median()

t30_df = pd.DataFrame({
    'Metric': ['Mean Lead Time (Days)', 'Median Lead Time (Days)'],
    'City Hotel': [f"{lt_mean_city:.2f}", f"{lt_med_city:.1f}"],
    'Resort Hotel': [f"{lt_mean_resort:.2f}", f"{lt_med_resort:.1f}"],
    'Absolute Difference (City - Resort)': [f"+{lt_mean_city - lt_mean_resort:.2f}", f"+{lt_med_city - lt_med_resort:.1f}"],
    'Relative Difference (%)': [f"+{(lt_mean_city - lt_mean_resort)/lt_mean_resort*100:.2f}%", f"+{(lt_med_city - lt_med_resort)/lt_med_resort*100:.2f}%"]
}).set_index('Metric')

print("--- Task 30: Lead Time Comparison ---")
print(t30_df)

# KDE visualization
fig, ax = plt.subplots(figsize=(10, 4.5))
sns.kdeplot(data=df_cleaned, x='lead_time', hue='hotel', common_norm=False, fill=True, alpha=0.3, palette=['#ff7f0e', '#1f77b4'], ax=ax)
ax.set_title("Lead Time Density Distribution: City Hotel vs Resort Hotel")
ax.set_xlabel("Lead Time (Days)")
ax.set_ylabel("Density")
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 30):**  
- **City Hotel:** Mean = **109.74 days**, Median = **74.0 days**.  
- **Resort Hotel:** Mean = **92.68 days**, Median = **57.0 days**.  
- **Absolute Difference:** City Hotel bookings are made on average **+17.06 days further in advance** (Median is **+17.0 days higher**).  
- **Relative Difference:** City Hotel lead times are **+18.40% longer** on average (+29.82% higher median).  
*Key Insight:* Contrary to the intuition that vacations are planned earlier, City Hotel receives substantial advance bookings from international tour operators and conferences reserving large group room allotments months ahead.
""")

    # TASK 31
    builder.add_markdown("""### Task 31: Average Daily Rate (ADR) Comparison
**Objective:** Compare ADR distributions, mean, and median between City Hotel and Resort Hotel to determine which commands higher daily pricing.
""")
    builder.add_code('''# Filter out extreme outlier ($5400) for unbiased comparative metrics
df_adr_filtered = df_cleaned[df_cleaned['adr'] < 5000]

adr_mean_city = df_adr_filtered[df_adr_filtered['hotel'] == 'City Hotel']['adr'].mean()
adr_med_city = df_adr_filtered[df_adr_filtered['hotel'] == 'City Hotel']['adr'].median()

adr_mean_resort = df_adr_filtered[df_adr_filtered['hotel'] == 'Resort Hotel']['adr'].mean()
adr_med_resort = df_adr_filtered[df_adr_filtered['hotel'] == 'Resort Hotel']['adr'].median()

t31_df = pd.DataFrame({
    'Metric': ['Mean ADR ($)', 'Median ADR ($)'],
    'City Hotel': [f"${adr_mean_city:.2f}", f"${adr_med_city:.2f}"],
    'Resort Hotel': [f"${adr_mean_resort:.2f}", f"${adr_med_resort:.2f}"],
    'Absolute Difference (City - Resort)': [f"+${adr_mean_city - adr_mean_resort:.2f}", f"+${adr_med_city - adr_med_resort:.2f}"],
    'Relative Difference (%)': [f"+{(adr_mean_city - adr_mean_resort)/adr_mean_resort*100:.2f}%", f"+{(adr_med_city - adr_med_resort)/adr_med_resort*100:.2f}%"]
}).set_index('Metric')

print("--- Task 31: ADR Comparison ---")
print(t31_df)

fig, ax = plt.subplots(figsize=(9, 4.5))
sns.boxplot(x='hotel', y='adr', data=df_adr_filtered[df_adr_filtered['adr'] < 400], palette=['#ff7f0e', '#1f77b4'], ax=ax)
ax.set_title("ADR Distribution Comparison by Property Type (Rates < $400)")
ax.set_ylabel("ADR ($ / Night)")
ax.set_xlabel("Hotel")
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 31):**  
- **City Hotel:** Mean ADR = **$105.24**, Median ADR = **$99.90**.  
- **Resort Hotel:** Mean ADR = **$94.95**, Median ADR = **$75.00**.  
- **Absolute Difference:** City Hotel commands **+$10.29 higher mean ADR** and **+$24.90 higher median ADR**.  
- **Relative Difference:** City Hotel's median ADR is **+33.20% higher** than Resort Hotel (+10.84% higher mean).  
*Key Insight:* Resort Hotel exhibits extreme seasonal rate swings (very low rates in winter, very high in summer), pulling down its overall annual median. City Hotel maintains higher year-round pricing consistency driven by business travel.
""")

    # TASK 32
    builder.add_markdown("""### Task 32: Weekday vs Weekend Stay Pattern Comparison
**Objective:** Compare average weekday and weekend nights booked across properties to test whether Resort Hotel exhibits longer weekend stays.
""")
    builder.add_code('''# Compare stay patterns
week_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['stays_in_week_nights'].mean()
weekend_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['stays_in_weekend_nights'].mean()
total_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['total_stay_nights'].mean()

week_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['stays_in_week_nights'].mean()
weekend_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['stays_in_weekend_nights'].mean()
total_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['total_stay_nights'].mean()

t32_df = pd.DataFrame({
    'Stay Metric': ['Mean Weekday Nights', 'Mean Weekend Nights', 'Mean Total Stay Length'],
    'City Hotel': [f"{week_city:.2f}", f"{weekend_city:.2f}", f"{total_city:.2f}"],
    'Resort Hotel': [f"{week_resort:.2f}", f"{weekend_resort:.2f}", f"{total_resort:.2f}"],
    'Absolute Difference (City - Resort)': [f"{week_city - week_resort:.2f}", f"{weekend_city - weekend_resort:.2f}", f"{total_city - total_resort:.2f}"],
    'Relative Difference (%)': [f"{(week_city - week_resort)/week_resort*100:.2f}%", f"{(weekend_city - weekend_resort)/weekend_resort*100:.2f}%", f"{(total_city - total_resort)/total_resort*100:.2f}%"]
}).set_index('Stay Metric')

print("--- Task 32: Stay Duration Comparison ---")
print(t32_df)
''')
    builder.add_markdown("""**Interpretation (Task 32):**  
**Yes, the Resort Hotel exhibits a significantly longer weekend and total stay pattern:**  
- **Weekend Nights:** Resort Hotel averages **1.19 nights** vs City Hotel's **0.80 nights** (Resort is **+48.75% longer**).  
- **Weekday Nights:** Resort Hotel averages **3.13 nights** vs City Hotel's **2.18 nights** (Resort is **+43.58% longer**).  
- **Total Stay Length:** Resort guests stay on average **4.32 nights** vs **2.97 nights** at City Hotel (**+45.45% longer**).  
Resort guests book full vacation stays spanning full weeks or extended weekends, while City Hotel guests typically stay 2-3 nights for business trips or short city breaks.
""")

    # TASK 33
    builder.add_markdown("""### Task 33: Guest Composition & Family Orientation Comparison
**Objective:** Compare guest composition (adults, children, babies) to evaluate which hotel attracts more family-oriented bookings.
""")
    builder.add_code('''# Compare guest composition
adults_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['adults'].mean()
children_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['children'].mean()
babies_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['babies'].mean()
family_pct_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['is_family'].mean() * 100

adults_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['adults'].mean()
children_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['children'].mean()
babies_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['babies'].mean()
family_pct_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['is_family'].mean() * 100

t33_df = pd.DataFrame({
    'Composition Metric': ['Mean Adults', 'Mean Children', 'Mean Babies', 'Bookings with Children/Babies (%)'],
    'City Hotel': [f"{adults_city:.3f}", f"{children_city:.3f}", f"{babies_city:.3f}", f"{family_pct_city:.2f}%"],
    'Resort Hotel': [f"{adults_resort:.3f}", f"{children_resort:.3f}", f"{babies_resort:.3f}", f"{family_pct_resort:.2f}%"],
    'Absolute Difference (Resort - City)': [f"+{adults_resort - adults_city:.3f}", f"+{children_resort - children_city:.3f}", f"+{babies_resort - babies_city:.3f}", f"+{family_pct_resort - family_pct_city:.2f}% pts"],
    'Relative Difference (%)': [f"+{(adults_resort - adults_city)/adults_city*100:.2f}%", f"+{(children_resort - children_city)/children_city*100:.2f}%", f"+{(babies_resort - babies_city)/babies_city*100:.2f}%", f"+{(family_pct_resort - family_pct_city)/family_pct_city*100:.2f}%"]
}).set_index('Composition Metric')

print("--- Task 33: Guest Composition Comparison ---")
print(t33_df)
''')
    builder.add_markdown("""**Interpretation (Task 33):**  
**The Resort Hotel is substantially more family-oriented:**  
- **Family Booking Proportion:** **10.23%** of Resort Hotel bookings include children or babies, compared to only **7.08%** at City Hotel.  
- **Relative Difference:** Resort Hotel is **+44.49% more likely** to host families with children/infants.  
- Resort Hotel averages **0.129 children** and **0.014 babies** per booking, compared to 0.091 children and 0.005 babies at City Hotel (Resort averages nearly **triple** the rate of infant guests).
""")

    # TASK 34
    builder.add_markdown("""### Task 34: Meal Package Preference Comparison
**Objective:** Compare meal package preferences between City Hotel and Resort Hotel to identify distinctive guest dining habits.
""")
    builder.add_code('''# Compare meal package distributions
meal_comp = pd.crosstab(df_cleaned['hotel'], df_cleaned['meal'], normalize='index') * 100
print("--- Meal Preferences by Hotel Property (%) ---")
print(meal_comp.round(2))

fig, ax = plt.subplots(figsize=(9, 4.5))
meal_comp.T.plot(kind='bar', ax=ax, colormap='tab10', width=0.7)
ax.set_title("Meal Plan Selection by Hotel Property")
ax.set_ylabel("Share of Hotel Bookings (%)")
ax.set_xlabel("Meal Category")
plt.xticks(rotation=0)
plt.legend(title="Property")
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 34):**  
- **Bed & Breakfast (BB):** Most popular at both properties, but captures a higher share at City Hotel (**78.47%**) than Resort Hotel (**75.05%**).  
- **Half Board (HB):** Far more dominant at Resort Hotel (**20.00%**) vs City Hotel (**5.62%**). Absolute difference: **+14.38% points** (Relative difference: **+255.87%** higher at Resort Hotel).  
- **Self Catering (SC):** Exclusively captured at City Hotel (**13.34%**) vs Resort Hotel (0.00%).  
Resort guests stay on-site and book Half Board (breakfast + dinner), whereas City guests prefer bed & breakfast or room-only/self-catering so they can dine across the metropolitan area.
""")

    # TASK 35
    builder.add_markdown("""### Task 35: Bridge Analysis – Parking Space Demand & Distribution Channels
*Note on Task 35:* As noted in the project specifications ("No separate Task 35 description is visible in the supplied PDF"), we incorporate a vital comparative analysis of operational infrastructure: **Required Car Parking Spaces and Distribution Channels**.
""")
    builder.add_code('''# Comparative analysis of parking requirements and distribution channels
parking_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['required_car_parking_spaces'].mean()
parking_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['required_car_parking_spaces'].mean()

t35_parking = pd.DataFrame({
    'Metric': ['Mean Parking Spaces Requested / Booking', 'Pct Bookings Requesting Parking (%)'],
    'City Hotel': [f"{parking_city:.4f}", f"{(df_cleaned[df_cleaned['hotel']=='City Hotel']['required_car_parking_spaces'] > 0).mean()*100:.2f}%"],
    'Resort Hotel': [f"{parking_resort:.4f}", f"{(df_cleaned[df_cleaned['hotel']=='Resort Hotel']['required_car_parking_spaces'] > 0).mean()*100:.2f}%"],
    'Absolute Difference (Resort - City)': [f"+{parking_resort - parking_city:.4f}", f"+{((df_cleaned[df_cleaned['hotel']=='Resort Hotel']['required_car_parking_spaces'] > 0).mean() - (df_cleaned[df_cleaned['hotel']=='City Hotel']['required_car_parking_spaces'] > 0).mean())*100:.2f}% pts"],
    'Relative Difference (%)': [f"+{(parking_resort - parking_city)/parking_city*100:.2f}%", f"+{((df_cleaned[df_cleaned['hotel']=='Resort Hotel']['required_car_parking_spaces'] > 0).mean() - (df_cleaned[df_cleaned['hotel']=='City Hotel']['required_car_parking_spaces'] > 0).mean()) / (df_cleaned[df_cleaned['hotel']=='City Hotel']['required_car_parking_spaces'] > 0).mean()*100:.2f}%"]
}).set_index('Metric')

print("--- Task 35: Comparative Parking Demand Analysis ---")
print(t35_parking)
''')
    builder.add_markdown("""**Interpretation (Task 35):**  
- **Resort Parking Demand:** **13.57%** of Resort bookings require car parking spaces, compared to only **2.43%** of City Hotel bookings.  
- **Relative Difference:** Resort guests are **+458.44% more likely** to request parking.  
This reflects the geographic reality of coastal resorts requiring rental cars or driving, whereas urban hotels are accessed via public transit, taxis, and airport shuttles.
""")

    # TASK 36
    builder.add_markdown("""### Task 36: Customer Loyalty & Repeat Guest Proportion
**Objective:** Compare the percentage of repeat guests across hotel types to determine which property fosters greater customer retention.
""")
    builder.add_code('''# Compare repeat guests
repeat_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['is_repeated_guest'].mean() * 100
repeat_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['is_repeated_guest'].mean() * 100

abs_repeat_diff = repeat_resort - repeat_city
rel_repeat_diff = (repeat_resort - repeat_city) / repeat_city * 100

t36_df = pd.DataFrame({
    'City Hotel': [f"{repeat_city:.2f}%"],
    'Resort Hotel': [f"{repeat_resort:.2f}%"],
    'Absolute Difference (Resort - City)': [f"+{abs_repeat_diff:.2f}% pts"],
    'Relative Difference (%)': [f"+{rel_repeat_diff:.2f}%"]
}, index=['Repeat Guest Share'])

print("--- Task 36: Repeat Guest Percentage Comparison ---")
print(t36_df)
''')
    builder.add_markdown("""**Interpretation (Task 36):**  
- **Resort Hotel:** **4.43%** repeat guests.  
- **City Hotel:** **2.56%** repeat guests.  
- **Absolute Difference:** Resort Hotel has a **+1.87 percentage point higher** repeat guest share.  
- **Relative Difference:** Resort Hotel has a **+73.05% higher customer loyalty rate** than City Hotel.  
Leisure resort travelers develop emotional affinity and return for annual summer vacations, whereas urban business travelers frequently switch hotel chains based on corporate travel policies, price, and location.
""")

    # TASK 37
    builder.add_markdown("""### Task 37: Special Requests per Booking Comparison
**Objective:** Compare the average number of special requests per booking to evaluate operational service engagement across hotels.
""")
    builder.add_code('''# Compare special requests
req_mean_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['total_of_special_requests'].mean()
req_mean_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['total_of_special_requests'].mean()

t37_df = pd.DataFrame({
    'Metric': ['Mean Special Requests / Booking', 'Pct Bookings with >= 1 Request (%)'],
    'City Hotel': [f"{req_mean_city:.3f}", f"{(df_cleaned[df_cleaned['hotel']=='City Hotel']['total_of_special_requests'] > 0).mean()*100:.2f}%"],
    'Resort Hotel': [f"{req_mean_resort:.3f}", f"{(df_cleaned[df_cleaned['hotel']=='Resort Hotel']['total_of_special_requests'] > 0).mean()*100:.2f}%"],
    'Absolute Difference (Resort - City)': [f"+{req_mean_resort - req_mean_city:.3f}", f"+{((df_cleaned[df_cleaned['hotel']=='Resort Hotel']['total_of_special_requests'] > 0).mean() - (df_cleaned[df_cleaned['hotel']=='City Hotel']['total_of_special_requests'] > 0).mean())*100:.2f}% pts"],
    'Relative Difference (%)': [f"+{(req_mean_resort - req_mean_city)/req_mean_city*100:.2f}%", f"+{((df_cleaned[df_cleaned['hotel']=='Resort Hotel']['total_of_special_requests'] > 0).mean() - (df_cleaned[df_cleaned['hotel']=='City Hotel']['total_of_special_requests'] > 0).mean()) / (df_cleaned[df_cleaned['hotel']=='City Hotel']['total_of_special_requests'] > 0).mean()*100:.2f}%"]
}).set_index('Metric')

print("--- Task 37: Special Requests Comparison ---")
print(t37_df)
''')
    builder.add_markdown("""**Interpretation (Task 37):**  
- **Resort Hotel:** Averages **0.625 requests per booking** (43.20% of bookings make at least one request).  
- **City Hotel:** Averages **0.547 requests per booking** (40.04% of bookings make at least one request).  
- **Relative Difference:** Resort guests submit **+14.26% more special requests** per booking.  
Resort guests make more customized requests regarding room view (ocean view), floor level, bed configurations, and early check-in for leisure comfort.
""")

    # TASK 38
    builder.add_markdown("""### Task 38: Deposit Policy Distribution Comparison
**Objective:** Compare deposit-type distribution between hotels to examine whether non-refundable bookings are more prevalent at one property.
""")
    builder.add_code('''# Deposit type by hotel
dep_comp = pd.crosstab(df_cleaned['hotel'], df_cleaned['deposit_type'], normalize='index') * 100
print("--- Deposit Type Proportions by Hotel (%) ---")
print(dep_comp.round(2))

non_ref_city = dep_comp.loc['City Hotel', 'Non Refund']
non_ref_resort = dep_comp.loc['Resort Hotel', 'Non Refund']

t38_df = pd.DataFrame({
    'City Hotel': [f"{non_ref_city:.2f}%"],
    'Resort Hotel': [f"{non_ref_resort:.2f}%"],
    'Absolute Difference (City - Resort)': [f"+{non_ref_city - non_ref_resort:.2f}% pts"],
    'Relative Difference (%)': [f"+{(non_ref_city - non_ref_resort)/non_ref_resort*100:.2f}%"]
}, index=['Non-Refundable Deposit Share'])

print("\\n--- Task 38: Non-Refundable Deposit Comparison ---")
print(t38_df)
''')
    builder.add_markdown("""**Interpretation (Task 38):**  
**Non-refundable bookings are dramatically more common at the City Hotel:**  
- **City Hotel:** **16.22%** of all bookings are Non-Refundable (12,868 bookings).  
- **Resort Hotel:** Only **4.29%** of bookings are Non-Refundable (1,719 bookings).  
- **Absolute Difference:** City Hotel has a **+11.93% points higher** non-refundable share.  
- **Relative Difference:** Non-refundable bookings are **+278.09% more frequent** at City Hotel!  
*Context:* City Hotel aggressively leveraged non-refundable advance purchase rates through OTAs and tour group contracts to lock in high corporate volume, whereas Resort Hotel primarily used standard refundable or no-deposit reservation terms.
""")

    # TASK 39
    builder.add_markdown("""### Task 39: Room Allocation Discrepancy (Reserved vs Assigned Room)
**Objective:** Compare the rate of difference between reserved and assigned room types to determine where room reallocations and upgrades occur more frequently.
""")
    builder.add_code('''# Room type discrepancy comparison
disc_city = df_cleaned[df_cleaned['hotel'] == 'City Hotel']['room_type_changed'].mean() * 100
disc_resort = df_cleaned[df_cleaned['hotel'] == 'Resort Hotel']['room_type_changed'].mean() * 100

abs_disc_diff = disc_resort - disc_city
rel_disc_diff = (disc_resort - disc_city) / disc_city * 100

t39_df = pd.DataFrame({
    'City Hotel': [f"{disc_city:.2f}%"],
    'Resort Hotel': [f"{disc_resort:.2f}%"],
    'Absolute Difference (Resort - City)': [f"+{abs_disc_diff:.2f}% pts"],
    'Relative Difference (%)': [f"+{rel_disc_diff:.2f}%"]
}, index=['Room Discrepancy Rate (Reserved != Assigned)'])

print("--- Task 39: Room Discrepancy Comparison ---")
print(t39_df)
''')
    builder.add_markdown("""**Interpretation (Task 39):**  
- **Resort Hotel:** **19.26%** of bookings experience a room type discrepancy (7,716 bookings).  
- **City Hotel:** **9.08%** of bookings experience a room type discrepancy (7,201 bookings).  
- **Absolute Difference:** Resort Hotel reallocates rooms at a **+10.18% points higher rate**.  
- **Relative Difference:** Room discrepancies/upgrades are **+112.11% more frequent** at Resort Hotel!  
*Operational Reason:* Resort hotels operate with more diverse room categories (villas, suites, garden views, pool views) and actively use complimentary upgrades at check-in to delight guests or resolve seasonal overbooking in standard double rooms.
""")


def add_section_d(builder):
    builder.add_markdown("""# SECTION D – CANCELLATION ANALYSIS
**Objective:** Conduct an exhaustive, multidimensional investigation into the behavioral, operational, and commercial drivers of hotel booking cancellations.
""")

    # TASK 40
    builder.add_markdown("""### Task 40: Total Cancellations & Overall Cancellation Rate
**Objective:** Calculate the total number of cancelled and non-cancelled bookings, and the overall dataset cancellation rate.
""")
    builder.add_code('''# Overall cancellation totals
canc_counts = df_cleaned['is_canceled'].value_counts()
canc_rate = df_cleaned['is_canceled'].mean() * 100

t40_df = pd.DataFrame({
    'Booking Status': ['Confirmed / Checked Out (0)', 'Cancelled / No-Show (1)', 'Total Reservations'],
    'Count': [canc_counts[0], canc_counts[1], len(df_cleaned)],
    'Percentage (%)': [f"{canc_counts[0]/len(df_cleaned)*100:.2f}%", f"{canc_counts[1]/len(df_cleaned)*100:.2f}%", "100.00%"]
}).set_index('Booking Status')

print("--- Task 40: Overall Cancellation Summary ---")
print(t40_df)
print(f"\\nOverall Dataset Cancellation Rate: {canc_rate:.2f}%")
''')
    builder.add_markdown("""**Interpretation (Task 40):**  
- **Non-Cancelled Bookings:** **75,166 reservations (62.96%)**.  
- **Cancelled Bookings:** **44,224 reservations (37.04%)**.  
- **Overall Cancellation Rate:** **37.04%**.  
More than one out of every three hotel bookings is cancelled prior to arrival, representing severe operational disruption and potential revenue loss.
""")

    # TASK 41
    builder.add_markdown("""### Task 41: Target Variable Balance & Visual Profiling
**Objective:** Plot a count plot and percentage bar chart of cancellation status, and assess target class balance.
""")
    builder.add_code('''# Visualizing target class balance
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# Countplot
sns.countplot(x='is_canceled', data=df_cleaned, palette=['#2ca02c', '#d62728'], ax=ax1)
ax1.set_title("Reservation Status: Raw Counts")
ax1.set_xlabel("Cancellation Status (0 = Not Canceled, 1 = Canceled)")
ax1.set_ylabel("Number of Bookings")
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():,}", (p.get_x() + p.get_width() / 2., p.get_height() / 2), ha='center', color='white', fontweight='bold')

# Percentage Bar Chart
pct_data = df_cleaned['is_canceled'].value_counts(normalize=True) * 100
sns.barplot(x=pct_data.index, y=pct_data.values, palette=['#2ca02c', '#d62728'], ax=ax2)
ax2.set_title("Reservation Status: Percentage Share (%)")
ax2.set_xlabel("Cancellation Status (0 = Not Canceled, 1 = Canceled)")
ax2.set_ylabel("Share (%)")
ax2.set_ylim(0, 75)
for p in ax2.patches:
    ax2.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 41):**  
**Target Class Balance Evaluation:**  
The dataset exhibits a **63% to 37% distribution**. This represents a **mild, healthy class imbalance** that does not suffer from extreme rarity (unlike fraud detection at 0.1%). Predictive models trained on this target will not require extreme oversampling (SMOTE) to achieve solid recall, though stratified sampling and PR-AUC/ROC-AUC evaluation are recommended.
""")

    # TASK 42
    builder.add_markdown("""### Task 42: Cancellation Rate Separately by Hotel Property
**Objective:** Calculate and contrast the cancellation rate separately for City Hotel and Resort Hotel.
""")
    builder.add_code('''# Hotel cancellation rates
t42_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'hotel')
print("--- Task 42: Cancellation Rate by Hotel Property ---")
print(t42_df)
''')
    builder.add_markdown("""**Interpretation (Task 42):**  
- **City Hotel:** **41.73% cancellation rate** (33,102 cancellations across 79,330 bookings).  
- **Resort Hotel:** **27.76% cancellation rate** (11,122 cancellations across 40,060 bookings).  
City Hotel accounts for 74.85% of all cancellations in the entire dataset. The urban commercial property faces acute revenue volatility compared to the leisure resort.
""")

    # TASK 43
    builder.add_markdown("""### Task 43: Cancellation Rate by Lead Time Intervals
**Objective:** Analyze cancellation rates across defined lead time intervals: 0-7 days, 8-30 days, 31-90 days, 91-180 days, 181-365 days, and >365 days.
""")
    builder.add_code('''# Group by defined lead time bins
t43_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'lead_time_bracket')
print("--- Task 43: Cancellation Rate by Lead Time Interval ---")
print(t43_df)

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.barplot(x=t43_df.index, y=t43_df['Cancellation Rate (%)'], palette='Reds', ax=ax)
ax.set_title("Cancellation Rate by Lead Time Interval: Strict Monotonic Escalation")
ax.set_xlabel("Lead Time Bracket")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 80)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 43):**  
**Cancellation probability exhibits a strict, unbroken monotonic escalation as lead time increases:**  
- **0–7 days:** **9.63% cancellation rate** (Near certainty of arrival).  
- **8–30 days:** **27.86% cancellation rate**.  
- **31–90 days:** **37.70% cancellation rate**.  
- **91–180 days:** **44.71% cancellation rate**.  
- **181–365 days:** **55.45% cancellation rate** (More likely to cancel than arrive!).  
- **>365 days:** **67.66% cancellation rate** (Over two-thirds cancelled!).  
*Managerial Takeaway:* As the planning horizon widens, the probability of schedule disruption, price comparison shopping, or speculative reservation abandonment multiplies. Overbooking models must apply exponential discounting to bookings made over 90 days out.
""")

    # TASK 44
    builder.add_markdown("""### Task 44: ADR Comparison Between Cancelled and Non-Cancelled Bookings
**Objective:** Compare recorded ADR values between cancelled and non-cancelled reservations.
""")
    builder.add_code('''# Filter extreme outlier for unbiased comparison
df_adr_clean = df_cleaned[df_cleaned['adr'] < 5000]

adr_by_cancel = df_adr_clean.groupby('is_canceled')['adr'].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
adr_by_cancel.index = ['Confirmed (0)', 'Cancelled (1)']
print("--- Task 44: ADR by Cancellation Status ---")
print(adr_by_cancel.round(2))

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.boxplot(x='is_canceled', y='adr', data=df_adr_clean[df_adr_clean['adr'] < 350], palette=['#2ca02c', '#d62728'], ax=ax)
ax.set_title("ADR Comparison: Confirmed vs Cancelled Bookings (Rates < $350)")
ax.set_xticklabels(['Confirmed (0)', 'Cancelled (1)'])
ax.set_ylabel("Average Daily Rate ($ / Night)")
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 44):**  
- **Confirmed Bookings (0):** Mean ADR = **$99.99**, Median ADR = **$93.60**.  
- **Cancelled Bookings (1):** Mean ADR = **$104.96**, Median ADR = **$99.00**.  
- **Difference:** Cancelled bookings have a **+$4.97 higher mean ADR** (+5.0% higher).  
*Key Insight:* Higher daily room rates correlate with higher cancellation propensity. Guests booking at premium rates are more sensitive to price shopping on competitor OTA listings and rebook at lower rates if last-minute promotional deals emerge.
""")

    # TASK 45
    builder.add_markdown("""### Task 45: Cancellation Rates Across Market Segments
**Objective:** Compare cancellation rates across market segments to identify high-risk commercial channels.
""")
    builder.add_code('''# Market segment cancellation rates
t45_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'market_segment')
print("--- Task 45: Cancellation Rate by Market Segment ---")
print(t45_df)

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.barplot(x=t45_df.index, y=t45_df['Cancellation Rate (%)'], palette='magma', ax=ax)
ax.set_title("Cancellation Rate by Market Segment")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 75)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 45):**  
- **Groups:** Highest cancellation rate at **61.06%** (12,097 cancellations across 19,811 bookings). Group blocks are notoriously speculative and frequently dumped back into inventory.  
- **Online TA:** **36.72% cancellation rate** (captures the largest absolute cancellation volume: 20,739 cancellations).  
- **Offline TA/TO:** **34.32% cancellation rate**.  
- **Corporate:** **18.73% cancellation rate**.  
- **Direct:** **15.35% cancellation rate** (Lowest cancellation among commercial segments).  
- **Complementary:** **13.06% cancellation rate**.  
*Takeaway:* Direct bookings cancel at **less than half the rate of Online TA bookings** and one-fourth the rate of Group blocks!
""")

    # TASK 46
    builder.add_markdown("""### Task 46: Cancellation Rates Across Distribution Channels
**Objective:** Compare cancellation rates across distribution channels (TA/TO, Direct, Corporate, GDS).
""")
    builder.add_code('''# Distribution channel cancellation rates
t46_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'distribution_channel')
print("--- Task 46: Cancellation Rate by Distribution Channel ---")
print(t46_df)
''')
    builder.add_markdown("""**Interpretation (Task 46):**  
- **TA/TO Channel:** **41.06% cancellation rate** (captures 40,177 cancellations — **90.85% of all cancellations** in the entire dataset!).  
- **GDS (Global Distribution Systems):** **19.37% cancellation rate** (Corporate travel management systems like Sabre/Amadeus).  
- **Direct Channel:** **17.46% cancellation rate** (Lowest cancellation rate).  
- **Corporate Channel:** **17.28% cancellation rate**.  
Third-party intermediaries drive nine out of ten cancellations due to easy one-click cancellation policies on platforms like Booking.com and Expedia.
""")

    # TASK 47
    builder.add_markdown("""### Task 47: The Non-Refundable Deposit Paradox
**Objective:** Analyze cancellation rates by deposit type and resolve the statistical and commercial paradox of non-refundable bookings.
""")
    builder.add_code('''# Cancellation by deposit type
t47_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'deposit_type')
print("--- Task 47: Cancellation Rate by Deposit Type ---")
print(t47_df)

fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(x=t47_df.index, y=t47_df['Cancellation Rate (%)'], palette=['#2ca02c', '#d62728', '#1f77b4'], ax=ax)
ax.set_title("The Non-Refundable Deposit Paradox: 99.36% Cancellation Rate")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 115)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 2), ha='center', fontweight='bold', color='black')
plt.tight_layout()
plt.show()

# Crosstab deposit type by market segment to resolve the paradox
paradox_crosstab = pd.crosstab(df_cleaned['deposit_type'], df_cleaned['market_segment'])
print("\\n--- Deposit Type by Market Segment (Resolving the Paradox) ---")
print(paradox_crosstab)
''')
    builder.add_markdown("""**Interpretation & Resolution of the Paradox (Task 47):**  
- **No Deposit:** **28.38% cancellation rate** (104,641 bookings).  
- **Refundable:** **22.22% cancellation rate** (162 bookings).  
- **Non Refund:** **99.36% cancellation rate** (14,494 cancellations across 14,587 bookings!).  

**Why do Non-Refundable bookings cancel at 99.36%?**  
This is the famous **"Non-Refund Paradox"** in hotel revenue management literature:
1. **Confounding with Group Contracts:** As proven in the crosstab above, **88.4% of all Non-Refund bookings (12,894 out of 14,587)** belong to the **Groups market segment**!
2. **Bulk Block Cut-off Policies:** Tour operators and conference organizers reserved bulk room blocks under strict non-refundable payment schedules. When group travel failed to materialize, the entire block was officially cancelled in the PMS prior to the cut-off date.
3. **Revenue Retention:** While recorded as `is_canceled = 1` in the PMS reservation ledger, the hotel retained the non-refundable forfeiture fees. Thus, from an accounting perspective, cancellation did not equal 100% loss of revenue.
""")

    # TASK 48
    builder.add_markdown("""### Task 48: Cancellation Rates Across Customer Types
**Objective:** Compare cancellation rates across customer types (Transient vs Contract vs Group vs Transient-Party).
""")
    builder.add_code('''# Customer type cancellation rates
t48_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'customer_type')
print("--- Task 48: Cancellation Rate by Customer Type ---")
print(t48_df)
''')
    builder.add_markdown("""**Interpretation (Task 48):**  
- **Transient:** Highest cancellation rate at **40.75%** (36,514 cancellations).  
- **Contract:** **30.96% cancellation rate**.  
- **Transient-Party:** **25.43% cancellation rate**.  
- **Group:** **10.23% cancellation rate** (Lowest cancellation rate).  
Individual transient bookings carry the highest cancellation risk because they lack collective social obligations or contractual commitments.
""")

    # TASK 49
    builder.add_markdown("""### Task 49: Cancellation Rates Relative to Special Requests
**Objective:** Analyze cancellation rates relative to the total number of special requests to test whether requests indicate arrival commitment.
""")
    builder.add_code('''# Cancellation rate by special requests count
t49_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'total_of_special_requests')
print("--- Task 49: Cancellation Rate by Special Requests ---")
print(t49_df)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.lineplot(x=t49_df.index.astype(int), y=t49_df['Cancellation Rate (%)'], marker='o', linewidth=3, markersize=8, color='#d62728', ax=ax)
ax.set_title("Cancellation Rate Drops Monotonically with Special Requests")
ax.set_xlabel("Number of Special Requests Submitted")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 55)
for x, y in zip(t49_df.index.astype(int), t49_df['Cancellation Rate (%)']):
    ax.annotate(f"{y:.1f}%", (x, y + 2), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 49):**  
**Yes, special requests are a powerful indicator of actual guest arrival:**  
- **0 Requests:** **47.72% cancellation rate**.  
- **1 Request:** **22.02% cancellation rate** (More than halved!).  
- **2 Requests:** **22.10% cancellation rate**.  
- **3 Requests:** **17.86% cancellation rate**.  
- **4 Requests:** **10.59% cancellation rate**.  
- **5 Requests:** **5.00% cancellation rate** (95% arrival rate!).  
*Behavioral Mechanism:* Submitting a special request (twin beds, quiet room, baby crib) signals that the customer is actively visualizing their stay, making operational travel plans, and psychologically invested in the trip.
""")

    # TASK 50
    builder.add_markdown("""### Task 50: Cancellation Rates for Repeat vs Non-Repeat Guests
**Objective:** Compare cancellation rates between repeat guests and first-time visitors.
""")
    builder.add_code('''# Cancellation by repeat guest status
t50_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'is_repeated_guest')
t50_df.index = ['First-Time Guest (0)', 'Repeat Guest (1)']
print("--- Task 50: Cancellation Rate by Guest Loyalty ---")
print(t50_df)

abs_rep_canc_diff = t50_df.loc['First-Time Guest (0)', 'Cancellation Rate (%)'] - t50_df.loc['Repeat Guest (1)', 'Cancellation Rate (%)']
rel_rep_canc_diff = abs_rep_canc_diff / t50_df.loc['Repeat Guest (1)', 'Cancellation Rate (%)'] * 100
print(f"\\nAbsolute Difference: First-time guests cancel {abs_rep_canc_diff:.2f}% points more often.")
print(f"Relative Difference: First-time guests are {rel_rep_canc_diff:.2f}% more likely to cancel than repeat guests.")
''')
    builder.add_markdown("""**Interpretation (Task 50):**  
- **First-Time Guests:** **37.79% cancellation rate** (43,672 cancellations).  
- **Repeat Guests:** **14.49% cancellation rate** (552 cancellations).  
- **Absolute Difference:** First-time guests cancel **+23.30 percentage points more often**.  
- **Relative Difference:** Repeat guests are **2.6 times less likely to cancel** (-61.66% lower cancellation rate). Customer retention directly insulates the hotel from cancellation shocks.
""")

    # TASK 51
    builder.add_markdown("""### Task 51: Impact of Previous Cancellation History
**Objective:** Investigate whether customers with a historical record of prior cancellations exhibit elevated cancellation rates on current bookings.
""")
    builder.add_code('''# Cancellation by prior cancellation history
df_cleaned['has_prior_cancellations'] = (df_cleaned['previous_cancellations'] > 0).astype(int)

t51_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'has_prior_cancellations')
t51_df.index = ['No Prior Cancellations (0)', 'Has Prior Cancellation History (1)']
print("--- Task 51: Cancellation Rate by Prior Cancellation History ---")
print(t51_df)
''')
    builder.add_markdown("""**Interpretation (Task 51):**  
- **No Prior Cancellations:** **33.91% cancellation rate**.  
- **Has Prior Cancellations:** **91.64% cancellation rate** (5,942 cancellations across 6,484 bookings!).  
*Critical Finding:* A customer history of previous cancellations is the **single strongest individual behavioral predictor of future cancellation** in the entire dataset. Customers who cancelled in the past repeat that behavior over 91% of the time.
""")

    # TASK 52
    builder.add_markdown("""### Task 52: Cancellation Rates Across Reserved Room Types
**Objective:** Compare cancellation rates across reserved room categories.
""")
    builder.add_code('''# Cancellation by reserved room type
t52_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'reserved_room_type')
print("--- Task 52: Cancellation Rate by Reserved Room Type ---")
print(t52_df)
''')
    builder.add_markdown("""**Interpretation (Task 52):**  
- **Room Type A (Standard):** **39.11% cancellation rate** (captures 33,630 cancellations — 76.0% of all cancellations).  
- **Room Type D (Superior):** **31.78% cancellation rate**.  
- **Room Type E (Deluxe):** **27.24% cancellation rate**.  
- **Room Type P (Presidential/Hold):** **100.00% cancellation rate** (12 bookings, all cancelled).  
Standard baseline rooms (Type A) exhibit significantly higher cancellation rates than premium family suites and deluxe rooms (Types D, E, F, G), which are booked by committed vacationers.
""")

    # TASK 53
    builder.add_markdown("""### Task 53: Cancellation Rates for Room Allocation Mismatches
**Objective:** Analyze cancellation rates for bookings where the reserved room type differs from the assigned room type.
""")
    builder.add_code('''# Cancellation by room assignment discrepancy
t53_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'room_type_changed')
t53_df.index = ['Assigned as Reserved (0)', 'Room Discrepancy / Upgrade (1)']
print("--- Task 53: Cancellation Rate by Room Type Mismatch ---")
print(t53_df)

fig, ax = plt.subplots(figsize=(7, 4.5))
sns.barplot(x=t53_df.index, y=t53_df['Cancellation Rate (%)'], palette=['#d62728', '#2ca02c'], ax=ax)
ax.set_title("Cancellation Rate: Room Matches vs Room Upgrade/Discrepancy")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 50)
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 53):**  
- **Room Matches Reserved:** **41.56% cancellation rate** (43,422 cancellations across 104,473 bookings).  
- **Room Discrepancy / Upgrade:** **5.38% cancellation rate** (802 cancellations across 14,917 bookings).  
- **Absolute Difference:** Bookings with room discrepancies cancel **36.18 percentage points less often**!  
*Operational Mechanism:* Room reassignments and complimentary upgrades occur **at the front desk during check-in** or during room blocking on the morning of arrival. Canceled bookings almost never reach this operational milestone, explaining why room discrepancies are strongly associated with confirmed check-ins.
""")

    # TASK 54
    builder.add_markdown("""### Task 54: Cancellation Rates Relative to Booking Changes
**Objective:** Investigate cancellation rates relative to the number of booking modifications and amendments made.
""")
    builder.add_code('''# Categorize booking changes
df_cleaned['changes_bracket'] = np.where(df_cleaned['booking_changes'] == 0, '0 Changes',
                               np.where(df_cleaned['booking_changes'] <= 2, '1-2 Changes', '3+ Changes'))

t54_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'changes_bracket')
print("--- Task 54: Cancellation Rate by Booking Changes ---")
print(t54_df)
''')
    builder.add_markdown("""**Interpretation (Task 54):**  
- **0 Booking Changes:** **40.85% cancellation rate** (41,391 cancellations).  
- **1–2 Booking Changes:** **15.59% cancellation rate** (2,573 cancellations).  
- **3+ Booking Changes:** **16.56% cancellation rate** (260 cancellations).  
*Key Insight:* Guests who actively modify their reservations (updating dates, adding guests, changing meal plans) exhibit **less than half the cancellation rate** of static bookings. Proactive engagement indicates real travel execution.
""")

    # TASK 55
    builder.add_markdown("""### Task 55: Geographic Cancellation Rates Across Top 15 Origin Countries
**Objective:** Compare cancellation rates across the top 15 origin countries by booking volume.
""")
    builder.add_code('''# Top 15 origin countries cancellation rates
top15_countries = df_cleaned['country'].value_counts().head(15).index
df_top15_geo = df_cleaned[df_cleaned['country'].isin(top15_countries)]

t55_df = df_top15_geo.groupby('country').agg(
    Total_Bookings=('is_canceled', 'count'),
    Cancellations=('is_canceled', 'sum'),
    Cancellation_Rate=('is_canceled', 'mean')
).sort_values(by='Total_Bookings', ascending=False)

t55_df['Cancellation Rate (%)'] = (t55_df['Cancellation_Rate'] * 100).round(2)
print("--- Task 55: Cancellation Rates Across Top 15 Countries ---")
print(t55_df[['Total_Bookings', 'Cancellations', 'Cancellation Rate (%)']])

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x=t55_df.index, y=t55_df['Cancellation Rate (%)'], palette='coolwarm', ax=ax)
ax.axhline(df_cleaned['is_canceled'].mean()*100, color='black', linestyle='--', label=f"Global Avg: {df_cleaned['is_canceled'].mean()*100:.1f}%")
ax.set_title("Cancellation Rates by Country of Origin (Top 15 Volume Markets)")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_xlabel("Country Code (ISO 3166-1)")
ax.set_ylim(0, 65)
ax.legend()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1), ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()
''')
    builder.add_markdown("""**Interpretation (Task 55):**  
- **Portugal (PRT - Domestic Market):** By far the largest booking source (48,590 bookings) and carries the highest cancellation rate at **56.64%**!  
- **International European Travelers:**  
  - Germany (DEU): **16.71%**  
  - France (FRA): **18.57%**  
  - United Kingdom (GBR): **20.22%**  
  - Austria (AUT): **18.21%**  
  - Netherlands (NLD): **18.39%**  
*Strategic Insight:* Domestic Portuguese travelers face low travel friction (driving distance, no non-refundable flights) and exhibit high cancellation rates. Conversely, foreign tourists booking flights to Portugal rarely cancel once travel itineraries are booked.
""")

    # TASK 56
    builder.add_markdown("""### Task 56: Cancellation Rates by Stay Duration Type (Weekday vs Weekend Heavy)
**Objective:** Compare cancellation rates between weekday-heavy and weekend-heavy stays.
""")
    builder.add_code('''# Cancellation rate by stay structure
t56_df = CancellationAnalyzer.cancellation_by_dimension(df_cleaned, 'stay_type')
print("--- Task 56: Cancellation Rate by Stay Type Structure ---")
print(t56_df)
''')
    builder.add_markdown("""**Interpretation (Task 56):**  
- **Weekday-Heavy Stays:** **37.47% cancellation rate** (captures 34,152 cancellations).  
- **Weekend-Heavy Stays:** **34.09% cancellation rate** (captures 4,590 cancellations).  
- **Balanced/Zero Stays:** **37.07% cancellation rate**.  
Weekday-heavy stays (often corporate or long group allocations) experience a slightly higher cancellation rate (+3.38% points) than weekend-heavy leisure getaways.
""")

    # RESEARCH CHALLENGE
    builder.add_markdown("""### Research Interpretation Challenge: Synthesis of Cancellation Drivers
**Core Question:** *Which variables are most strongly associated with cancellations? Are they independent effects or interconnected?*

1. **Hierarchy of Cancellation Predictors:**
   - **Prior Cancellation History (`previous_cancellations`):** 91.6% cancellation rate (Relative Risk: 2.7x vs baseline).
   - **Lead Time (`lead_time`):** Scales monotonically from 9.6% (0-7 days) to 67.7% (>365 days).
   - **Special Requests (`total_of_special_requests`):** Drops from 47.7% (0 requests) down to 5.0% (5 requests).
   - **Origin Country (`country`):** Domestic (PRT: 56.6%) vs International (<20%).
   - **Deposit Type (`deposit_type`):** Non-Refund (99.4%) vs No Deposit (28.4%).
   - **Market Segment (`market_segment`):** Groups (61.1%) vs Direct (15.4%).

2. **Interconnected & Confounded Dynamics:**
   - **The Group-Deposit Confounding:** Non-refundable deposits do not cause cancellations; rather, group tour operators reserving large allotments were required to accept non-refundable terms, and speculative group blocks were subsequently cancelled wholesale.
   - **Lead Time & Geography Interaction:** Long lead times interact with domestic vs international channels; domestic travelers booking far in advance frequently abandon tentative weekend reservations, whereas international travelers lock in flights.
   - **Operational Artifacts:** Room discrepancy (`room_type_changed`) and booking amendments are operational indicators of surviving to check-in, rather than pre-booking causal barriers.
""")

print("Section C & D builder functions defined successfully.")
