"""
OOP Analytical Architecture for Hotel Booking Demand Analysis
============================================================
This module encapsulates all data loading, preprocessing, univariate,
comparative, cancellation, time-series, and revenue management logic
into clean, reusable Python classes adhering to PEP 8 and PEP 257 standards.
"""

from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class HotelDataLoader:
    """Encapsulates raw data ingestion, H1/H2 file partition handling,
    and initial schema inspection routines.
    """

    def __init__(self, file_path: str = 'hotel_bookings.csv') -> None:
        """Initialize loader with file path.

        Parameters
        ----------
        file_path : str
            Relative or absolute path to the hotel bookings CSV dataset.
        """
        self.file_path = file_path

    def load_raw_data(self) -> pd.DataFrame:
        """Load raw CSV dataset into a Pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            Unmodified raw hotel booking demand dataset.
        """
        return pd.read_csv(self.file_path)

    def get_h1_h2_split(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Simulate loading separate H1 (Resort Hotel) and H2 (City Hotel) datasets.

        Parameters
        ----------
        df : pd.DataFrame
            Combined raw hotel booking dataset.

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            H1 (Resort Hotel subset) and H2 (City Hotel subset).
        """
        h1 = df[df['hotel'] == 'Resort Hotel'].copy()
        h2 = df[df['hotel'] == 'City Hotel'].copy()
        return h1, h2

    def generate_data_dictionary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate a structured metadata data dictionary for all columns.

        Parameters
        ----------
        df : pd.DataFrame
            The hotel bookings DataFrame.

        Returns
        -------
        pd.DataFrame
            Data dictionary containing variable names, data types,
            analytical categories, and functional descriptions.
        """
        descriptions = {
            'hotel': 'Type of hotel property (Resort Hotel or City Hotel)',
            'is_canceled': 'Binary flag indicating whether booking was canceled (1) or not (0)',
            'lead_time': 'Number of days elapsed between entering date of booking and arrival date',
            'arrival_date_year': 'Year of arrival date (2015, 2016, 2017)',
            'arrival_date_month': 'Month of arrival date with 12 months categories',
            'arrival_date_week_number': 'Week number of arrival date as defined in ISO 8601',
            'arrival_date_day_of_month': 'Day of the month of the arrival date (1-31)',
            'stays_in_weekend_nights': 'Number of weekend nights (Saturday or Sunday) stayed or booked',
            'stays_in_week_nights': 'Number of weekday nights (Monday to Friday) stayed or booked',
            'adults': 'Number of adult guests included in the reservation',
            'children': 'Number of child guests (aged 2 to 12)',
            'babies': 'Number of baby/infant guests (under age 2)',
            'meal': 'Type of meal booked (BB: Bed & Breakfast, HB: Half Board, FB: Full Board, SC: Self Catering, Undefined)',
            'country': 'Country of origin of primary guest in ISO 3166-1 alpha-3 code',
            'market_segment': 'Market segment designation (Direct, Corporate, Online TA, Offline TA/TO, Groups, Complementary, Aviation)',
            'distribution_channel': 'Booking distribution channel (TA/TO, Direct, Corporate, GDS, Undefined)',
            'is_repeated_guest': 'Binary flag indicating if guest booking name is a repeat guest (1) or new (0)',
            'previous_cancellations': 'Number of previous bookings that were canceled by the customer prior to current booking',
            'previous_bookings_not_canceled': 'Number of previous bookings not canceled by customer prior to current booking',
            'reserved_room_type': 'Code of room type reserved by customer (A-L)',
            'assigned_room_type': 'Code of room type actually assigned to booking (may differ due to operational allocation/upgrade)',
            'booking_changes': 'Number of changes/amendments made to the booking until check-in or cancellation',
            'deposit_type': 'Indication if customer made a deposit (No Deposit, Non Refund, Refundable)',
            'agent': 'ID of the travel agency that made the booking (numeric code)',
            'company': 'ID of the corporate company/entity that made the booking or pays fees (numeric code)',
            'days_in_waiting_list': 'Number of days booking was on waiting list before confirmed to customer',
            'customer_type': 'Type of booking customer (Transient, Transient-Party, Contract, Group)',
            'adr': 'Average Daily Rate defined by dividing the sum of all lodging transactions by total staying nights',
            'required_car_parking_spaces': 'Number of car parking spaces requested by the customer',
            'total_of_special_requests': 'Number of special requests made by customer (e.g. high floor, twin bed)',
            'reservation_status': 'Final reservation status (Check-Out, Canceled, No-Show)',
            'reservation_status_date': 'Date at which the last status was set (YYYY-MM-DD)'
        }
        
        categories = {
            'hotel': 'Categorical (Nominal)',
            'is_canceled': 'Binary (Target)',
            'lead_time': 'Numerical (Discrete/Interval)',
            'arrival_date_year': 'Temporal (Year)',
            'arrival_date_month': 'Temporal (Month)',
            'arrival_date_week_number': 'Temporal (Week Number)',
            'arrival_date_day_of_month': 'Temporal (Day)',
            'stays_in_weekend_nights': 'Numerical (Discrete)',
            'stays_in_week_nights': 'Numerical (Discrete)',
            'adults': 'Numerical (Discrete)',
            'children': 'Numerical (Discrete)',
            'babies': 'Numerical (Discrete)',
            'meal': 'Categorical (Nominal)',
            'country': 'Categorical (Geographic)',
            'market_segment': 'Categorical (Nominal)',
            'distribution_channel': 'Categorical (Nominal)',
            'is_repeated_guest': 'Binary Flag',
            'previous_cancellations': 'Numerical (Discrete Count)',
            'previous_bookings_not_canceled': 'Numerical (Discrete Count)',
            'reserved_room_type': 'Categorical (Nominal/Ordinal)',
            'assigned_room_type': 'Categorical (Nominal/Ordinal)',
            'booking_changes': 'Numerical (Discrete Count)',
            'deposit_type': 'Categorical (Nominal)',
            'agent': 'Categorical (Identifier)',
            'company': 'Categorical (Identifier)',
            'days_in_waiting_list': 'Numerical (Discrete/Interval)',
            'customer_type': 'Categorical (Nominal)',
            'adr': 'Numerical (Continuous Financial)',
            'required_car_parking_spaces': 'Numerical (Discrete Count)',
            'total_of_special_requests': 'Numerical (Discrete Count)',
            'reservation_status': 'Categorical (Nominal/Status)',
            'reservation_status_date': 'Temporal (Date)'
        }

        dict_df = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': [str(df[col].dtype) for col in df.columns],
            'Analytical Category': [categories.get(col, 'Unknown') for col in df.columns],
            'Description': [descriptions.get(col, 'N/A') for col in df.columns]
        })
        return dict_df


class HotelDataPreprocessor:
    """Custom transformer class for rigorous data cleaning, missing value handling,
    anomaly filtering, and feature engineering with complete audit logging.
    """

    def __init__(self, filter_anomalies: bool = False) -> None:
        """Initialize preprocessor.

        Parameters
        ----------
        filter_anomalies : bool, default=False
            Whether to strictly remove impossible/anomalous rows or retain
            them for comparative transparency.
        """
        self.filter_anomalies = filter_anomalies
        self.audit_log: List[Dict[str, Any]] = []

    def log_action(self, step: str, action: str, impact: str) -> None:
        """Record an explicit data modification event into the audit trail.

        Parameters
        ----------
        step : str
            Pipeline processing phase.
        action : str
            Specific technical transformation applied.
        impact : str
            Data volume, schema, or distribution consequence.
        """
        self.audit_log.append({
            'Pipeline Step': step,
            'Transformation Action': action,
            'Impact / Records Affected': impact
        })

    def fit(self, df: pd.DataFrame) -> 'HotelDataPreprocessor':
        """Fit preprocessor parameters on dataset.

        Parameters
        ----------
        df : pd.DataFrame
            Input hotel bookings DataFrame.

        Returns
        -------
        HotelDataPreprocessor
            Fitted preprocessor instance.
        """
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Execute full cleaning, conversion, and feature engineering pipeline.

        Parameters
        ----------
        df : pd.DataFrame
            Raw input hotel bookings DataFrame.

        Returns
        -------
        pd.DataFrame
            Fully preprocessed and enriched DataFrame.
        """
        cleaned = df.copy()

        # Step 1: Datetime conversions
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        numeric_month = cleaned['arrival_date_month'].map(month_map)
        cleaned['arrival_date'] = pd.to_datetime(
            cleaned['arrival_date_year'].astype(str) + '-' +
            numeric_month.astype(str).str.zfill(2) + '-' +
            cleaned['arrival_date_day_of_month'].astype(str).str.zfill(2)
        )
        cleaned['reservation_status_date'] = pd.to_datetime(cleaned['reservation_status_date'])
        self.log_action(
            'Temporal Parsing',
            'Constructed arrival_date from year, month, and day; converted reservation_status_date to datetime',
            f'Parsed 2 datetime fields across {len(cleaned):,} records'
        )

        # Step 2: Handle missing values
        # children: 4 missing -> fill with mode 0
        children_missing = cleaned['children'].isnull().sum()
        cleaned['children'] = cleaned['children'].fillna(0.0).astype(int)
        self.log_action(
            'Missing Value Imputation',
            'Imputed missing children counts with 0 (mode)',
            f'{children_missing} records imputed'
        )

        # country: 488 missing -> fill with 'Unknown'
        country_missing = cleaned['country'].isnull().sum()
        cleaned['country'] = cleaned['country'].fillna('Unknown')
        self.log_action(
            'Missing Value Imputation',
            'Imputed missing country codes with "Unknown"',
            f'{country_missing} records imputed'
        )

        # agent & company: NULL means direct booking without intermediary
        agent_null = cleaned['agent'].isnull().sum()
        company_null = cleaned['company'].isnull().sum()
        cleaned['agent'] = cleaned['agent'].fillna(0)
        cleaned['company'] = cleaned['company'].fillna(0)
        cleaned['has_agent'] = (cleaned['agent'] != 0).astype(int)
        cleaned['has_company'] = (cleaned['company'] != 0).astype(int)
        self.log_action(
            'Intermediary Identification',
            'Replaced missing agent and company IDs with 0; engineered has_agent and has_company flags',
            f'{agent_null:,} agent and {company_null:,} company records encoded'
        )

        # Step 3: Feature Engineering
        cleaned['total_stay_nights'] = cleaned['stays_in_week_nights'] + cleaned['stays_in_weekend_nights']
        cleaned['total_guests'] = cleaned['adults'] + cleaned['children'] + cleaned['babies']
        cleaned['is_family'] = ((cleaned['children'] > 0) | (cleaned['babies'] > 0)).astype(int)
        cleaned['room_type_changed'] = (cleaned['reserved_room_type'] != cleaned['assigned_room_type']).astype(int)
        
        # Lead time bins
        cleaned['lead_time_bracket'] = pd.cut(
            cleaned['lead_time'],
            bins=[-1, 7, 30, 90, 180, 365, np.inf],
            labels=['0-7 days', '8-30 days', '31-90 days', '91-180 days', '181-365 days', '>365 days']
        )

        # Stay pattern type
        cleaned['stay_type'] = np.where(
            cleaned['stays_in_week_nights'] > cleaned['stays_in_weekend_nights'], 'Weekday-heavy',
            np.where(cleaned['stays_in_weekend_nights'] > cleaned['stays_in_week_nights'], 'Weekend-heavy', 'Balanced/Zero')
        )

        # Estimated lodging value
        cleaned['estimated_lodging_value'] = cleaned['adr'] * cleaned['total_stay_nights']

        self.log_action(
            'Feature Engineering',
            'Engineered total_stay_nights, total_guests, is_family, room_type_changed, lead_time_bracket, stay_type, estimated_lodging_value',
            'Enriched dataset with 7 new analytical attributes'
        )

        # Step 4: Outlier and anomaly documentation
        zero_guests_count = (cleaned['total_guests'] == 0).sum()
        neg_adr_count = (cleaned['adr'] < 0).sum()
        zero_nights_count = (cleaned['total_stay_nights'] == 0).sum()
        extreme_adr_count = (cleaned['adr'] > 1000).sum()

        if self.filter_anomalies:
            cleaned = cleaned[
                (cleaned['total_guests'] > 0) &
                (cleaned['adr'] >= 0) &
                (cleaned['total_stay_nights'] > 0) &
                (cleaned['adr'] < 5000)
            ].copy()
            self.log_action(
                'Anomaly Filtering',
                'Removed zero guests, negative ADR, zero nights, and extreme ADR outliers',
                f'Filtered {df.shape[0] - cleaned.shape[0]:,} anomalous records'
            )
        else:
            self.log_action(
                'Anomaly Auditing',
                'Flagged zero guests (180), negative ADR (1), zero stay nights (715), and extreme ADR (1) for selective handling',
                f'{zero_guests_count + neg_adr_count + zero_nights_count + extreme_adr_count:,} anomalies audited'
            )

        return cleaned

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fit preprocessor and transform dataset.

        Parameters
        ----------
        df : pd.DataFrame
            Raw hotel bookings DataFrame.

        Returns
        -------
        pd.DataFrame
            Cleaned and transformed DataFrame.
        """
        return self.fit(df).transform(df)

    def get_audit_log(self) -> pd.DataFrame:
        """Return the complete data transformation log as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Transformation log of all preprocessing steps and their impacts.
        """
        return pd.DataFrame(self.audit_log)


class UnivariateAnalyzer:
    """Encapsulates statistical summary calculations and visualizations
    for individual numerical and categorical features.
    """

    @staticmethod
    def compute_continuous_summary(series: pd.Series, variable_name: str) -> pd.DataFrame:
        """Compute parametric and non-parametric summary statistics.

        Parameters
        ----------
        series : pd.Series
            Target numeric series.
        variable_name : str
            Descriptive label for the variable.

        Returns
        -------
        pd.DataFrame
            Table containing mean, median, mode, standard deviation,
            variance, minimum, and maximum.
        """
        mode_val = series.mode()[0] if not series.mode().empty else np.nan
        summary = {
            'Variable': variable_name,
            'Count': len(series),
            'Mean': series.mean(),
            'Median': series.median(),
            'Mode': mode_val,
            'Std Dev': series.std(),
            'Variance': series.var(),
            'Min': series.min(),
            'Max': series.max(),
            'Skewness': series.skew(),
            'Kurtosis': series.kurt()
        }
        return pd.DataFrame([summary]).set_index('Variable')

    @staticmethod
    def compute_percentiles(series: pd.Series, percentiles: List[float] = [5, 25, 50, 75, 90, 95, 99]) -> pd.DataFrame:
        """Compute specific percentile values for a continuous variable.

        Parameters
        ----------
        series : pd.Series
            Target continuous series.
        percentiles : List[float]
            List of percentile ranks to compute.

        Returns
        -------
        pd.DataFrame
            Percentile distribution table.
        """
        pct_values = np.percentile(series.dropna(), percentiles)
        return pd.DataFrame({
            'Percentile': [f"{p}th" for p in percentiles],
            'Value': pct_values
        })

    @staticmethod
    def compute_frequency_table(series: pd.Series, variable_name: str, top_n: Optional[int] = None) -> pd.DataFrame:
        """Compute count and percentage distributions for categorical variables.

        Parameters
        ----------
        series : pd.Series
            Target categorical series.
        variable_name : str
            Descriptive label for variable.
        top_n : int, optional
            Limit table to top N frequent categories.

        Returns
        -------
        pd.DataFrame
            Frequency table with counts and percentages.
        """
        counts = series.value_counts(dropna=False)
        if top_n is not None:
            counts = counts.head(top_n)
        pcts = (counts / len(series)) * 100
        cum_pcts = pcts.cumsum()
        return pd.DataFrame({
            'Category': counts.index.astype(str),
            'Count': counts.values,
            'Percentage (%)': pcts.values.round(2),
            'Cumulative (%)': cum_pcts.values.round(2)
        })


class ComparativeHotelAnalyzer:
    """Encapsulates hotel-wise comparative analysis (City Hotel vs Resort Hotel)
    computing both absolute and relative differences for all metrics.
    """

    @staticmethod
    def compare_metric(
        df: pd.DataFrame,
        metric: str,
        group_col: str = 'hotel',
        agg_func: str = 'mean'
    ) -> pd.DataFrame:
        """Compare a metric between City Hotel and Resort Hotel, reporting
        both absolute and relative percentage differences.

        Parameters
        ----------
        df : pd.DataFrame
            Cleaned hotel bookings DataFrame.
        metric : str
            Numeric column name to compare.
        group_col : str, default='hotel'
            Grouping column (hotel).
        agg_func : str, default='mean'
            Aggregation method ('mean', 'median', 'sum', 'count').

        Returns
        -------
        pd.DataFrame
            Comparative table showing City Hotel, Resort Hotel, Absolute Difference,
            and Relative Difference (%).
        """
        agg_series = df.groupby(group_col)[metric].agg(agg_func)
        city_val = agg_series.get('City Hotel', np.nan)
        resort_val = agg_series.get('Resort Hotel', np.nan)
        abs_diff = city_val - resort_val
        rel_diff = ((city_val - resort_val) / resort_val * 100) if resort_val != 0 else np.nan

        return pd.DataFrame({
            'City Hotel': [city_val],
            'Resort Hotel': [resort_val],
            'Absolute Difference (City - Resort)': [abs_diff],
            'Relative Difference (%)': [rel_diff]
        }, index=[f"{metric} ({agg_func})"])


class CancellationAnalyzer:
    """Encapsulates multidimensional cancellation analytics, risk segmentation,
    and investigation of the Non-Refund deposit paradox.
    """

    @staticmethod
    def cancellation_by_dimension(
        df: pd.DataFrame,
        dim_col: str,
        target_col: str = 'is_canceled',
        top_n: Optional[int] = None
    ) -> pd.DataFrame:
        """Calculate total bookings, cancellations, and cancellation rates
        across categories of a given dimension.

        Parameters
        ----------
        df : pd.DataFrame
            Cleaned hotel bookings DataFrame.
        dim_col : str
            Dimension column to segment by.
        target_col : str, default='is_canceled'
            Binary cancellation flag.
        top_n : int, optional
            Limit to top N categories by booking count.

        Returns
        -------
        pd.DataFrame
            Segmentation table with Total Bookings, Cancellations,
            Cancellation Rate (%), and Segment Share (%).
        """
        grouped = df.groupby(dim_col, observed=False)[target_col].agg(
            Total_Bookings='count',
            Cancellations='sum',
            Cancellation_Rate='mean'
        )
        if top_n is not None:
            grouped = grouped.sort_values(by='Total_Bookings', ascending=False).head(top_n)
        
        grouped['Cancellation Rate (%)'] = (grouped['Cancellation_Rate'] * 100).round(2)
        grouped['Segment Share (%)'] = ((grouped['Total_Bookings'] / len(df)) * 100).round(2)
        return grouped[['Total_Bookings', 'Cancellations', 'Cancellation Rate (%)', 'Segment Share (%)']]


class TimeSeriesSeasonalityAnalyzer:
    """Encapsulates temporal demand dynamics, calendar seasonality,
    and lead-time shifts over the reservation timeline.
    """

    @staticmethod
    def get_monthly_summary(
        df: pd.DataFrame,
        month_order: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Generate monthly booking demand, cancellations, and ADR trends.

        Parameters
        ----------
        df : pd.DataFrame
            Cleaned hotel bookings DataFrame.
        month_order : List[str], optional
            Chronological calendar ordering for months.

        Returns
        -------
        pd.DataFrame
            Chronologically sorted monthly summary table.
        """
        if month_order is None:
            month_order = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]

        monthly = df.groupby('arrival_date_month', observed=False).agg(
            Total_Bookings=('is_canceled', 'count'),
            Cancellations=('is_canceled', 'sum'),
            Cancellation_Rate=('is_canceled', 'mean'),
            Mean_ADR=('adr', 'mean'),
            Median_ADR=('adr', 'median'),
            Mean_Lead_Time=('lead_time', 'mean')
        ).reindex(month_order)

        monthly['Cancellation Rate (%)'] = (monthly['Cancellation_Rate'] * 100).round(2)
        return monthly


class RevenueManager:
    """Encapsulates revenue management analytics, ADR profiling,
    lodging value calculations, and data validity checks.
    """

    @staticmethod
    def calculate_estimated_lodging_value(df: pd.DataFrame) -> Dict[str, Any]:
        """Compute estimated lodging value and analyze revenue loss to cancellations.

        Formula:
            Estimated Value = ADR * (stays_in_week_nights + stays_in_weekend_nights)

        Parameters
        ----------
        df : pd.DataFrame
            Cleaned hotel bookings DataFrame.

        Returns
        -------
        Dict[str, Any]
            Comprehensive financial breakdown of potential value,
            realized value, and canceled revenue leakage.
        """
        total_value = df['estimated_lodging_value'].sum()
        realized_value = df[df['is_canceled'] == 0]['estimated_lodging_value'].sum()
        lost_value = df[df['is_canceled'] == 1]['estimated_lodging_value'].sum()
        
        return {
            'Total Estimated Lodging Value ($)': round(total_value, 2),
            'Realized Lodging Value (Non-Canceled) ($)': round(realized_value, 2),
            'Lost Lodging Value (Canceled) ($)': round(lost_value, 2),
            'Revenue Leakage Rate (%)': round((lost_value / total_value) * 100, 2),
            'Mean Booking Value ($)': round(df['estimated_lodging_value'].mean(), 2),
            'Median Booking Value ($)': round(df['estimated_lodging_value'].median(), 2),
            'Mean Value (Canceled) ($)': round(df[df['is_canceled'] == 1]['estimated_lodging_value'].mean(), 2),
            'Mean Value (Non-Canceled) ($)': round(df[df['is_canceled'] == 0]['estimated_lodging_value'].mean(), 2)
        }

print("OOP analytical architecture module compiled successfully.")
