--1 create a table that focusses on  where cd_unnested.value = 'order_confirmation' 
--2 capture timestamp at start of session visitStartTime
--3 caputre time at first hit when session is on order_confirmation page
--4 subtract time stamps from eachother
    -- do not average out time to visualise


with ga as (
  select
 CONCAT(CAST(visitId AS STRING),'_',fullVisitorId) as sessionID,
   hit.time as hit_ts,
   visitStartTime,
   hit.type,
   hit.screenName,
   cd_unnested.value,
   cd_unnested
  from `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` 
  cross join  UNNEST(hit) as hit
  cross Join UNNEST(customDimensions) as cd_unnested
  where cd_unnested.value = 'order_confirmation' 
  
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
    TIMESTAMP_MILLIS(1000 * visitStartTime + min(hit_ts)) as order_confirmation_time,
  from ga
  group by sessionId, visitStartTime, hit_ts
),

-- Join it all together and calc differences
joined as (
  select
    --AVG(Timestamp_diff( order_confirmation_time, visitStartTime_ts , minute)) as ts_diff_minutes
    Timestamp_diff( order_confirmation_time, visitStartTime_ts , minute) as ts_diff_minutes
  from start
  inner join first_app_complete using(sessionID)
)
select * from joined

