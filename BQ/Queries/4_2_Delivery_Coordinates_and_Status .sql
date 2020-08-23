--frontendOrderId : An order Id that is exposed in clients and shown to the customers, matches transactionID

--1 combine transaction_id from hits & 4_coordinate_change_table to work with BackendDataSample
--2 combine above table with BackendDataSample and calculate  if order status as well as delivery location change  



-- create table that tracks transaction_id & session_id
with transaction_table as (
  select
  CONCAT(CAST(visitId AS STRING),'_',fullVisitorId) as session_id,
  hit_unnested.transactionId,
  location_changed,
  from `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export`
  join UNNEST(hit) as hit_unnested
  inner join `ben-trollope-final-answers.Final_Answers.4_coordinate_change_table` on CONCAT(CAST(visitId AS STRING),'_',fullVisitorId) = ID
  where hit_unnested.transactionId is not NULL )


-- if geo points are null than customer did not place an order
-- if not order was placed successfully 
SELECT  
transaction_table.session_id,
transaction_table.location_changed,

geopointCustomer,
geopointDropoff,
orderDate,
ST_DISTANCE(geopointCustomer,geopointDropoff) as dropOffDistanceChanged,
       (CASE -- used distance as st_empty was throwing errors
            WHEN ST_DISTANCE(geopointCustomer,geopointDropoff) > -1 THEN 'SUCCESSFUL_DELIVERY'
            ELSE 'ORDER_NOT_PLACED'
         END) AS OrderStatus,
         
          (CASE -- used distance as st_empty was not working
            WHEN ST_EQUALS(geopointCustomer,geopointDropoff) is NULL THEN null
            WHEN ST_EQUALS(geopointCustomer,geopointDropoff) = TRUE THEN TRUE
            ELSE FALSE
         END) AS DeliveryLocationChange,
         
FROM `dhh-analytics-hiringspace.BackendDataSample.transactionalData` 
inner join transaction_table on  transaction_table.transactionId = frontendOrderId



