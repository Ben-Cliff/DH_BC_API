--2. How many sessions does each visitor create?


SELECT
fullvisitorid AS distinct_fullvisitorid,
visitid AS distinct_visitid,
COUNT(*) over (partition by fullvisitorid) as occurrences,
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export`
GROUP BY
distinct_fullvisitorid,
distinct_visitid
HAVING 
    COUNT(*) > 1;
    
    
    
    
    