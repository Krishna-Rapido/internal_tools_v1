import pandas as pd
# import fastparquet
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
pd.set_option('display.max_columns', None)
from pyhive import presto


def get_presto_connection(username: str):
    """Create a Presto connection with the given username"""
    return presto.connect(
        host='presto-gateway.processing.data.production.internal',
        port='80',
        username=username
    )


def get_captain_id(mobile_number_df: pd.DataFrame, username: str):
    """
    Fetch captain_id for given mobile numbers from Presto
    
    Args:
        mobile_number_df: DataFrame with 'mobile_number' column
        username: Presto username for connection
    
    Returns:
        DataFrame with mobile_number and captain_id columns
    """
    presto_connection = get_presto_connection(username)
    
    query = f"""
    select captain_id, mobile_number from 
    datasets.captain_supply_journey_summary
    where date_format(date_parse(registration_date, '%Y-%m-%d'), '%Y%m%d') > '20200101'
    and mobile_number in {tuple(list(map(str, (mobile_number_df.mobile_number.unique()))))}
    
    """
    df = pd.read_sql(query, presto_connection)
    # Ensure the 'mobile_number' column is of the same dtype before merging
    mobile_number_df['mobile_number'] = mobile_number_df['mobile_number'].astype(str)
    df['mobile_number'] = df['mobile_number'].astype(str)
    return mobile_number_df.merge(df, on='mobile_number', how='left')



def get_ao_funnel(captain_id_df: pd.DataFrame, username: str, start_date: str = '20250801', 
                  end_date: str = '20251031', time_level: str = 'daily', tod_level: str = 'daily'):
    """
    Fetch AO funnel metrics for given captain IDs from Presto
    
    Args:
        captain_id_df: DataFrame with 'captain_id' column
        username: Presto username for connection
        start_date: Start date in YYYYMMDD format (default: '20250801')
        end_date: End date in YYYYMMDD format (default: '20251031')
        time_level: Time aggregation level - 'daily', 'weekly', or 'monthly' (default: 'daily')
        tod_level: Time of day level - 'daily', 'afternoon', 'evening', 'morning', 'night', or 'all' (default: 'daily')
    
    Returns:
        DataFrame with funnel metrics
    """
    presto_connection = get_presto_connection(username)
    
    query = f"""


        with service_mapping as (
                    select captain_id,  geo_city geo_city, substr(replace(time_value,'-',''),1,8) as run_date,
                        case 
                            when count_net_days_last_28_days >= 15 then 'daily'
                            when count_net_days_last_28_days<= 14 and count_net_days_last_28_days >= 1 and count_net_weeks_last_28_days>=3 then 'weekly'
                            when count_net_days_last_28_days<= 14 and count_net_days_last_28_days >= 1 and count_net_weeks_last_28_days<3 then 'monthly'
                            when count_net_days_last_28_days =0 and captain_net_days_last_83_days > 0 then 'quarterly'
                        else 'rest' end as consistency_segment, 
                        case 
                            when count_net_days_last_28_days>0 and count_total_rides_last_28_days/cast(count_net_days_last_28_days as double) > 15 then 'UHP'
                            when count_net_days_last_28_days>0 and count_total_rides_last_28_days/cast(count_net_days_last_28_days as double) > 10 then 'HP'
                            when count_net_days_last_28_days>0 and count_total_rides_last_28_days/cast(count_net_days_last_28_days as double) > 5 then 'MP'
                            when count_net_days_last_28_days>0 and count_total_rides_last_28_days/cast(count_net_days_last_28_days as double) > 0 then 'LP'
                        else 'ZP' end as performance_segment
                    from mne.ms_1842554619_2584218394
                    where time_level = 'daily'
                    and replace(substr(time_value,1,10),'-','') between '{start_date}'  and '{end_date}'
                    and lower(geo_city) in ('hyderabad','bangalore','delhi','ahmedabad','chennai','jaipur','lucknow','mumbai','kolkata','pune')
    ),
    base as (
        
        select lower(a.city) as city,
        a.captain_id,
        b.consistency_segment,
        b.performance_segment,
        case 
            when lower('{time_level}')='weekly' then concat(cast(year(date_parse(a.yyyymmdd, '%Y%m%d')) as varchar),'_',cast(week(date_parse(a.yyyymmdd, '%Y%m%d')) as varchar))
            when lower('{time_level}')='monthly' then concat(cast(year(date_parse(a.yyyymmdd,'%Y%m%d')) as varchar),'_',cast(month(date_parse(a.yyyymmdd,'%Y%m%d')) as varchar))
            when lower('{time_level}')='daily' then yyyymmdd
        end as time,
        sum(
        case
            when lower('{tod_level}') = 'daily' then coalesce(count_captain_num_online_daily_city, 0)
            when lower('{tod_level}') = 'afternoon' then coalesce(count_num_online_afternoon_daily_city, 0)
            when lower('{tod_level}') = 'evening' then coalesce(count_num_online_evening_peak_daily_city, 0)
            when lower('{tod_level}') = 'morning' then coalesce(count_num_online_morning_peak_daily_city, 0)
            when lower('{tod_level}') = 'night' then coalesce(count_num_online_rest_midnight_daily_city, 0)
            when lower('{tod_level}') = 'all' then coalesce(count_captain_num_online_daily_city, 0)
        end
    ) as online_events,
    count(distinct case when coalesce(count_captain_num_online_daily_city, 0) > 0 then yyyymmdd end) as online_days,
    count(distinct case when (coalesce(count_captain_net_rides_taxi_all_day_city, 0) + coalesce(count_captain_c2c_orders_all_day_city, 0) + coalesce(count_captain_delivery_orders_all_day_city, 0)) > 0 then yyyymmdd end) as net_days,
    sum(
        case
            when lower('{tod_level}') = 'daily' then coalesce(count_captain_net_rides_taxi_all_day_city, 0)
            when lower('{tod_level}') = 'afternoon' then coalesce(count_captain_net_rides_delivery_afternoon_city, 0)
            when lower('{tod_level}') = 'evening' then coalesce(count_captain_net_rides_taxi_evening_peak_city, 0)
            when lower('{tod_level}') = 'morning' then coalesce(count_captain_net_rides_taxi_morning_peak_city, 0)
            when lower('{tod_level}') = 'night' then coalesce(count_captain_net_rides_taxi_rest_midnight_city, 0)
            when lower('{tod_level}') = 'all' then coalesce(count_captain_net_rides_taxi_all_day_city, 0)
        end
    ) as net_rides_taxi,
    sum(
        case
            when lower('{tod_level}') = 'daily' then coalesce(count_captain_c2c_orders_all_day_city, 0)
            when lower('{tod_level}') = 'afternoon' then coalesce(count_captain_net_rides_c2c_afternoon_city, 0)
            when lower('{tod_level}') = 'evening' then coalesce(count_captain_net_rides_c2c_evening_peak_city, 0)
            when lower('{tod_level}') = 'morning' then coalesce(count_captain_net_rides_c2c_morning_peak_city, 0)
            when lower('{tod_level}') = 'night' then coalesce(count_captain_c2c_orders_all_day_city, 0)
            when lower('{tod_level}') = 'all' then coalesce(count_captain_c2c_orders_all_day_city, 0)
        end
    ) as net_rides_c2c,
    sum(
        case
            when lower('{tod_level}') = 'daily' then coalesce(count_captain_delivery_orders_all_day_city, 0)
            when lower('{tod_level}') = 'afternoon' then coalesce(count_captain_net_rides_delivery_afternoon_city, 0)
            when lower('{tod_level}') = 'evening' then coalesce(count_captain_net_rides_delivery_evening_peak_city, 0)
            when lower('{tod_level}') = 'morning' then coalesce(count_captain_net_rides_delivery_morning_peak_city, 0)
            when lower('{tod_level}') = 'night' then coalesce(count_captain_net_rides_taxi_all_day_city, 0)
            when lower('{tod_level}') = 'all' then coalesce(count_captain_net_rides_taxi_all_day_city, 0)
        end
    ) as net_rides_delivery,
    count(distinct case when (coalesce(count_captain_accepted_pings_taxi_all_day_city, 0) + coalesce(count_captain_accepted_pings_delivery_all_day_city, 0)) > 0 then yyyymmdd end) as accepted_days,
    avg(
        case
            when lower('{tod_level}') = 'daily' then (coalesce(count_captain_accepted_orders_all_day_taxi, 0) + coalesce(count_captain_accepted_orders_all_day_c2c, 0) + coalesce(count_captain_accepted_orders_all_day_delivery, 0))
            when lower('{tod_level}') = 'afternoon' then (coalesce(count_captain_accepted_orders_afternoon_taxi, 0))
            when lower('{tod_level}') = 'evening' then (coalesce(count_captain_accepted_orders_evening_peak_c2c, 0) + coalesce(count_captain_accepted_orders_evening_peak_delivery, 0) + coalesce(count_captain_accepted_orders_evening_peak_taxi, 0))
            when lower('{tod_level}') = 'morning' then (coalesce(count_captain_accepted_pings_morning_peak_delivery, 0) + coalesce(count_captain_accepted_pings_morning_peak_c2c, 0) + coalesce(count_captain_accepted_orders_morning_peak_taxi, 0))
            when lower('{tod_level}') = 'night' then coalesce(count_num_online_rest_midnight_daily_city, 0)
            when lower('{tod_level}') = 'all' then (coalesce(count_captain_accepted_orders_all_day_taxi, 0) + coalesce(count_captain_accepted_orders_all_day_c2c, 0) + coalesce(count_captain_accepted_orders_all_day_delivery, 0))
        end
    ) as accepted_orders,
    sum(coalesce(count_captain_accepted_orders_all_day_taxi, 0)) as accepted_orders_sum, -- Renamed to avoid duplicate alias
    count(distinct case when (coalesce(count_captain_gross_pings_taxi_all_day_city, 0) + coalesce(count_captain_gross_pings_delivery_all_day_city, 0)) > 0 then yyyymmdd end) as gross_days,
    count(distinct case when coalesce(count_captain_number_app_open_captains_daily_all_day_city, 0) > 0 then yyyymmdd end) as ao_days,
    avg(case when coalesce(count_captain_num_online_daily_city, 0) > 0 and (coalesce(count_captain_accepted_pings_taxi_all_day_city, 0) + coalesce(count_captain_accepted_pings_delivery_all_day_city, 0)) = 0 then coalesce(sum_captain_total_lh_daily_city, 0) end) as total_lh_nonO2a,
    sum(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_total_lh_daily_city, 0) else 0 end) as total_lh_sum,
    avg(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_total_lh_daily_city, 0) end) as total_lh,
    max(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_total_lh_daily_city, 0) end) as max_lh_per_day,
    avg(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_total_lh_morning_peak_daily_city, 0) end) as total_lh_morning_peak,
    avg(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_total_lh_afternoon_daily_city, 0) end) as total_lh_afternoon,
    avg(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_total_lh_evening_peak_daily_city, 0) end) as total_lh_evening_peak,
    avg(case when coalesce(count_captain_num_online_daily_city, 0) > 0 then coalesce(sum_captain_idle_lh_daily_city, 0) end) as idle_lh,
    sum(coalesce(count_captain_gross_pings_link_all_day_city, 0)) as total_pings_link,
    avg(case when (coalesce(count_captain_accepted_pings_taxi_all_day_city, 0) + coalesce(count_captain_accepted_pings_delivery_all_day_city, 0)) > 0 then (coalesce(count_captain_gross_pings_taxi_all_day_city, 0) + coalesce(count_captain_gross_pings_delivery_all_day_city, 0)) end) as gross_pings,
    avg(case when (coalesce(count_captain_accepted_pings_taxi_all_day_city, 0) + coalesce(count_captain_accepted_pings_delivery_all_day_city, 0)) > 0 then (coalesce(count_captain_accepted_pings_taxi_all_day_city, 0) + coalesce(count_captain_accepted_pings_delivery_all_day_city, 0)) end) as accepted_pings,
    sum(coalesce(count_captain_net_rides_taxi_all_day_city, 0) + coalesce(count_captain_c2c_orders_all_day_city, 0) + coalesce(count_captain_delivery_orders_all_day_city, 0)) / nullif(cast(sum(coalesce(count_captain_accepted_pings_taxi_all_day_city, 0) + coalesce(count_captain_accepted_pings_delivery_all_day_city, 0)) as double), 0) as dapr
    from metrics.captain_base_metrics_enriched a
    left join service_mapping b on a.captain_id = b.captain_id and a.yyyymmdd = b.run_date
    where 
    yyyymmdd >= '{start_date}'
    and yyyymmdd <= '{end_date}'
    and a.captain_id in {tuple(list(captain_id_df.captain_id.dropna().unique()))}
    
    group by 1,2,3,4,5
    )

    select * from base


    """.format(tod_level=tod_level, time_level=time_level, start_date=start_date, end_date=end_date)
    df = pd.read_sql_query(query, presto_connection)
    captain_id_df['captain_id'] = captain_id_df['captain_id'].astype(str)
    df['captain_id'] = df['captain_id'].astype(str)
    return captain_id_df.merge(df, on='captain_id', how='inner')


def dapr_bucket(username: str, start_date: str, end_date: str, city: str, service_category: str, low_dapr: float, high_dapr: float):
    """
    Fetch DAPR bucket distribution data from Presto
    
    Args:
        username: Presto username for connection
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        city: City name (e.g., 'delhi', 'bangalore')
        service_category: Service category
        low_dapr: Low DAPR threshold
        high_dapr: High DAPR threshold
    
    Returns:
        DataFrame with DAPR bucket distribution
    """
    presto_connection = get_presto_connection(username)
    query = f"""
    with mapping as (SELECT 
       service_category,
       service_level
FROM datasets.service_level_mapping_qc   
where service_category = '{service_category}'
group by 1,2) , 

city as (SELECT 
       city_display_name  
FROM datasets.service_level_mapping_qc   
where lower(city_display_name) = lower('{city}')
group by 1) , 


dapr as ( 
SELECT 
    yyyymmdd, 
    captain_id, 
    city_name, 
    CASE 
        WHEN accepted_pings < 20 THEN 'less_than_20_pings'
        WHEN dapr <= {low_dapr} AND accepted_pings >= 20 THEN 'BAD'
        WHEN dapr >= {high_dapr} AND accepted_pings >= 20 THEN 'GOOD' 
        WHEN dapr > {low_dapr} AND dapr < {high_dapr} AND accepted_pings >= 20 THEN 'AVG' 
    END AS Dapr_bucket
FROM reports_internal.marketplace_dapr_twenty_pings_combined_v7_v8
WHERE yyyymmdd >= '{start_date}'
and yyyymmdd <= '{end_date}'
AND service_category IN (SELECT service_category FROM mapping)
AND city_name IN (SELECT city_display_name FROM city)),
    

    
active as (select *
from
(select captainid ,a.yyyymmdd , Dapr_bucket ,
sum(net_orders) as dropped_rides_day, sum(accepted_pings) as accp_pings_day,
sum(accepted_pings + riderrejected_pings + riderbusy_pings) as pings_rec_day,
sum(accepted_pings)-sum(net_orders) as cancelled_day
from datasets.captain_svo_daily_kpi a
left join dapr b on a.captainid=b.captain_id and a.city=b.city_name and a.yyyymmdd=b.yyyymmdd

where a.yyyymmdd >= '{start_date}'
and a.yyyymmdd <= '{end_date}'

    and service_name in (select  service_level from mapping )
    and city in (select city_display_name  from city )
    and Dapr_bucket is not null
group by 1,2,3
having  sum(accepted_pings + riderrejected_pings + riderbusy_pings)>0))

select yyyymmdd  ,Dapr_bucket , active_caps , dropped , total_pings ,  cancelled , 
active_caps/cast(active_caps_total as real ) as per_caps ,
total_pings/cast(pings_total as real ) as per_total_pings ,
accepted/cast(accepted_total as real ) as per_accp ,
dropped/cast(dropped_total as real ) as per_dropped ,
cancelled/cast(cancelled_total as real ) as per_cancel,
100*dropped/cast(accepted as real ) as avg_dapr
from
(select a.yyyymmdd  ,case when Dapr_bucket is null then 'less_than_20_pings' else Dapr_bucket end as Dapr_bucket, 
active_caps_total,dropped_total , accepted_total , pings_total , cancelled_total , 
count(captainid) as active_caps , 
sum(dropped_rides_day) as dropped,
sum(accp_pings_day) as accepted,
sum(pings_rec_day) as total_pings , 
sum(cancelled_day) as cancelled
from active a
inner join (select yyyymmdd , 
count(captainid) active_caps_total, 
sum(dropped_rides_day) as dropped_total,
sum(accp_pings_day) as accepted_total,
sum(pings_rec_day) as pings_total , 
sum(cancelled_day) as cancelled_total
from active
where Dapr_bucket is not null
group by 1
) b on a.yyyymmdd = b.yyyymmdd
group by 1,2,3,4,5,6,7
)
order by  yyyymmdd , Dapr_bucket

    """
    df = pd.read_sql_query(query, presto_connection)
    return df


def fe2net(username: str, start_date: str, end_date: str, city: str, service_category: str, geo_level: str, time_level: str):
    """
    Fetch FE2Net funnel data from Presto
    
    Args:
        username: Presto username for connection
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        city: City name (e.g., 'delhi', 'bangalore')
        service_category: Service category
        geo_level: Geographic level (e.g., 'city', 'zone')
        time_level: Time aggregation level (e.g., 'daily', 'weekly')
    
    Returns:
        DataFrame with FE2Net funnel metrics
    """
    presto_connection = get_presto_connection(username)
    
    query = f"""
    select
    city as "City", 
    time_level as "Time Level", 
    time_value as "Time Value",
    geo_level as "Geo Level",
    geo_value as "Geo Value",
    service as Service,
    login_hours,
    fe_sessions,
    gross_session,
    fe2rr,
    fe2net,
    gsr2net,
    gross_orders,
    mapped_orders,
    net_orders,
    g2n_req_percent,
    g2n_mapped_percent,
    stress_gsr_login_hours,
    accepted_orders_out_of_mapped as AOR,
    accepted_orders_out_of_gross_percent,
    total_pings,
    net_order_per_login_hour,
    unmapped_orders_percent,
    stockout_percent,
    cobrm_percent,
    expiry_mapped_percent,
    cobra_percent,
    ocara_percent,
    avg_mr as avg_mapped_riders_count,
    median_mr as median_mapped_riders_count,
    online_captains,
    gross_captains,
    net_captains,
    idle_hours,
    time_spent_earning_percent,
    login_hours_per_online_captain,
    rph,
    rides_per_net_rider,
    apr,
    rider_busy_percent,
    rider_reject_percent,
    dpr,
    dapr,
    matching_efficiency_pings_per_net_order,
    avg_fm_accepted_orders_kms,
    median_fm_accepted_orders_kms,
    avg_fm_dropped_orders_kms,
    median_fm_dropped_orders_kms,
    avg_fm_ocara_orders_kms,
    median_fm_ocara_orders_kms,
    avg_shown_eta,
    avg_actual_eta,
    avg_tta_secs
from experiments.fe2net_dashboard_lite
where
 substr(replace(time_value,'-',''),1,10) >= '{start_date}' 
and substr(replace(time_value,'-',''),1,10) <= '{end_date}'
    and service = '{service_category}'
    and geo_level = '{geo_level}'
    and lower(city) = lower('{city}')
    and time_level = '{time_level}'
    -- [[and {{geo_value}}]]
    and geo_value != ''
order by 3 asc
    """
    df = pd.read_sql_query(query, presto_connection)
    return df