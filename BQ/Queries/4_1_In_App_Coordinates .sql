--1 select session data from shoplist where cd_unnested.value = 'shop_list' 
    --1.1 get latitude values
    --1.2 get longitude values
    --1.3 find most frequent latitude values per session_id as there are multiple
    --1.4 find most frequent Longitude values per session_id as there are multiple
    --1.5 Amalgamste session id, longitude, latitude as well as a new combined geo point column

--2 select session data from  order_confirmation where cd_unnested.value = 'order_confirmation' 
  --2,1 - 2.5, repeat above steps but for order_confirmation
  
--3 Combine data to register if location has changed and the distance to which it has
 


--Create data set that grabs lat & long at shop_list
with listing_start as ( 
  select
  date,
  hit_unnested.time as hit_time,
  hit_unnested.customDimensions as CustomDimensions,
  CONCAT(CAST(visitId AS STRING),'_',fullVisitorId) as session_id,
  from `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` 
  join UNNEST(hit) as hit_unnested
  Join UNNEST(customDimensions) as cd_unnested
  where cd_unnested.value = 'shop_list' 
  order by session_id
  ),

--there will be multiple locations at shop_list. Grab the location with the greatest frequency

lat_freq_shop_start as(
select -- could throw in a distinct here
   session_id, 
   --CustomDimensions,
   cd_unnested.value as lat_start,
 from listing_start
 Join UNNEST(customDimensions) as cd_unnested
 where cd_unnested.index = 19 ),


long_freq_shop_start as(
select  (session_id) -- could throw in a distinct here
   session_id,
   --CustomDimensions,
   cd_unnested.value as long_start,
 from listing_start
 Join UNNEST(customDimensions) as cd_unnested
 where cd_unnested.index = 18 ),
 
 ---------------------
 --Queries that select most frequent lat & long on shoplist page
 ---------------------

  
   long_shop  as (
    Select
      long_freq_shop_start.session_id,
      long_freq_shop_start.long_start AS long_shop_mf, 
    FROM long_freq_shop_start 
    where long_freq_shop_start.long_start != 'NA'
    group by long_freq_shop_start.session_id ,  long_freq_shop_start.long_start
    order by long_freq_shop_start.session_id, count(*)  DESC
   
   ),
   
   lat_shop as (
    SELECT 
      lat_freq_shop_start.session_id,
      lat_freq_shop_start.lat_start AS lat_shop_mf , 
    FROM lat_freq_shop_start
    where lat_freq_shop_start.lat_start != 'NA'
    group by lat_freq_shop_start.session_id ,  lat_freq_shop_start.lat_start
    order by lat_freq_shop_start.session_id, count(*)  DESc
   ),
 
 --------------------------------------------------------------------------------------------
 --SHOP COORDINATES DONE
 shop_location as (
 select
    lat_shop.session_id as ID,
    lat_shop.lat_shop_mf,                   --should be a sql query
    long_shop.long_shop_mf,                 --should be a sql query
    --ST_GEOGPOINT(longitude, latitude)
    ST_GEOGPOINT(   cast(long_shop.long_shop_mf as float64), cast(lat_shop.lat_shop_mf as float64)) as shoplist_coord 
 from lat_shop join long_shop 
    on lat_shop.session_id = long_shop.session_id
  ),
   


 --------------------------------------------------------------------------------------------

  --Create data set that grabs lat & long at shop_list
order_confirmation_end as ( 
  select
  date,
  hit_unnested.time as hit_time,
  hit_unnested.customDimensions as CustomDimensions,
  CONCAT(CAST(visitId AS STRING),'_',fullVisitorId) as session_id,
  from `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` 
  join UNNEST(hit) as hit_unnested
  Join UNNEST(customDimensions) as cd_unnested
  where cd_unnested.value = 'order_confirmation' 
  order by session_id
  ),

--there will be multiple locations at shop_list. Grab the location with the greatest frequency

lat_freq_OC_end as(
select -- could throw in a distinct here
   session_id, 
   --CustomDimensions,
   cd_unnested.value as lat_end,
 from order_confirmation_end
 Join UNNEST(customDimensions) as cd_unnested
 where cd_unnested.index = 19 ),


long_freq_OC_end as(
select  (session_id) -- could throw in a distinct here
   session_id,
   --CustomDimensions,
   cd_unnested.value as long_end,
 from order_confirmation_end
 Join UNNEST(customDimensions) as cd_unnested
 where cd_unnested.index = 18 ),
 
 ---------------------
 --Queries that select most frequent lat & long on shoplist page
 ---------------------

  
   long_OC  as (
    Select
      long_freq_OC_end.session_id,
      long_freq_OC_end.long_end AS long_OC_mf, 
    FROM long_freq_OC_end
    where  long_freq_OC_end.long_end != 'NA'
    group by long_freq_OC_end.session_id ,  long_freq_OC_end.long_end
    order by long_freq_OC_end.session_id, count(*)  DESC
   ),
   
   lat_OC as (
    SELECT 
      lat_freq_OC_end.session_id,
      lat_freq_OC_end.lat_end AS lat_OC_mf , 
    FROM lat_freq_OC_end
    where lat_freq_OC_end.lat_end != 'NA'
    group by lat_freq_OC_end.session_id ,  lat_freq_OC_end.lat_end
    order by lat_freq_OC_end.session_id, count(*)  DESc
   ),
 

 ------------------------------------
 OC_location as (
  select
    lat_OC.session_id as ID,
    lat_OC.lat_OC_mf,                   --should be a sql query
    long_OC.long_OC_mf,                 --should be a sql query
    --ST_GEOGPOINT(longitude, latitude)
    ST_GEOGPOINT(   cast(long_OC.long_OC_mf as float64), cast(lat_OC.lat_OC_mf as float64)) as OC_coord 
 from lat_OC join long_OC 
    on lat_OC.session_id = long_OC.session_id 
 ),

------------------------------------
 -- Clean and amalgamate location data


coordinate_table as (
select 
OC_location.ID,
   shop_location.lat_shop_mf,
   shop_location.long_shop_mf,
   OC_location.lat_OC_mf,
   OC_location.long_OC_mf,
   ST_GEOGPOINT(   cast(OC_location.long_OC_mf as float64), cast(OC_location.lat_OC_mf as float64)) as OC_coord, 
   ST_GEOGPOINT(   safe_cast(shop_location.long_shop_mf as float64), safe_cast(shop_location.lat_shop_mf as float64)) as shop_coord  -- Requires safe_cast
from  OC_location inner join shop_location 
  on OC_location.ID = shop_location.ID)

------------------------------------------------------------------------------------------
-- determine if a change in location has occured and to what extent

select 
  ID,
  OC_coord as Order_Confirmation_Point,
  shop_coord Shop_List_Point,
  ST_EQUALS(OC_coord,shop_coord) as Location_Changed,
  ST_distance(OC_coord, shop_coord)/1000 as Distance_Changed_KM
  
from coordinate_table
  
  
  
  
  


 
