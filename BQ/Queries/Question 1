--1. How many sessions are there?

SELECT 

COUNT(DISTINCT fullvisitorid) AS UniqueUsers,
COUNT(DISTINCT visitid) AS UniqueVisits,
COUNT(DISTINCT CONCAT(CAST(fullvisitorid AS string),CAST(visitid AS string))) AS TotalNumberOfSessions,


FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` 