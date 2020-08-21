--3 Average time taken to reach the order_confirmation screen per session (in minutes)?


with ga as (
  select
 CONCAT(CAST(visitId AS STRING),'_',fullVisitorId) as sessionID,
   hit.time as hit_ts,
   visitStartTime,
   hit.type,
   hit.screenName,
   cd.value,
  from `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` 
  cross join  UNNEST(hit) as hit
  cross Join UNNEST(customDimensions) as cd
  
),
-- Get start of app use
start as (
  select
    sessionId,
    TIMESTAMP_SECONDS(visitStartTime) as visitStartTime_ts,
  from ga
    group by ga.sessionID , visitStartTime
    
),
-- Get first instance of app-complete
first_app_complete as (
  select
    sessionId,
    TIMESTAMP_MILLIS(1000 * visitStartTime + hit_ts) as app_complete_ts,
  from ga
  
  /*where type = "TRANSACTION"
  VS
  where value = "order_confirmation" */
  
  --where type = "TRANSACTION"
  where value = "order_confirmation"
  group by sessionId, visitStartTime, hit_ts
),
-- Join it all together and calc differences
joined as (
  select
    sessionID,
    visitStartTime_ts,
    app_complete_ts,
    --AVG(Timestamp_diff( app_complete_ts, visitStartTime_ts , minute)) as ts_diff_minutes
    Timestamp_diff( app_complete_ts, visitStartTime_ts , minute) as ts_diff_minutes
  from start
  inner join first_app_complete using(sessionID)
)
select * from joined
-- select channelGrouping, count(sessionID) as session_count, avg(ts_diff_seconds) as average_seconds_to_complete from joined group by 1