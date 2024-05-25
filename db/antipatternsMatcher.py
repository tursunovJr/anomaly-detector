from dsl.helper import *
from enum import Enum

class AntipatternsMatcher:

  bottleneck_service_query = """
    with t1 as(SELECT t1.*, row_number() OVER (PARTITION by InvID, OperationName ORDER by ID) as rnRQ  from TracingEvents t1 WHERE EventType = "RQ")
    , t2 as(SELECT t2.*, row_number() OVER (PARTITION by InvID, OperationName ORDER by ID) as rnRSAndSE  from TracingEvents t2 WHERE EventType in  ("RS", "SE"))
    , stat as (SELECT t1.InvID, t1.OperationName, t1.EventType, t1.EventTimestamp, t1.rnRQ, t2.EventType, t2.EventTimestamp, t2.rnRSAndSE, (t2.EventTimestamp - t1.EventTimestamp) as diffTime
    FROM t1 LEFT JOIN t2 on t1.InvID = t2.InvID AND t1.OperationName = t2.OperationName AND t1.rnRQ = t2.rnRSAndSE
    WHERE t2.EventType = "RS" AND diffTime >= 0
    ORDER by t1.InvID, t1.OperationName, t1.rnRQ
    )
    SELECT stat.OperationName, round(avg(diffTime)/1000) as avgDiffTime
    FROM stat
    GROUP by OperationName
    HAVING avgDiffTime > 5
    ORDER by avgDiffTime DESC
  """

  chatty_service_query = """
    with t1 as(SELECT t1.*, row_number() OVER (PARTITION by InvID, OperationName ORDER by ID) as rnRQ  from TracingEvents t1 WHERE EventType = "RQ")
    , t2 as(SELECT t2.*, row_number() OVER (PARTITION by InvID, OperationName ORDER by ID) as rnRSAndSE  from TracingEvents t2 WHERE EventType in  ("RS", "SE"))
    , stat as (SELECT t1.InvID, t1.OperationName, t1.EventType, t1.EventTimestamp, t1.rnRQ, t2.EventType, t2.EventTimestamp, t2.rnRSAndSE, t2.PayloadSize, (t2.EventTimestamp - t1.EventTimestamp) as diffTime
    FROM t1 LEFT JOIN t2 on t1.InvID = t2.InvID AND t1.OperationName = t2.OperationName AND t1.rnRQ = t2.rnRSAndSE
    WHERE t2.EventType = "RS" AND diffTime >= 0
    ORDER by t1.InvID, t1.OperationName, t1.rnRQ
    )
    SELECT stat.OperationName, round(avg(PayloadSize)) as avgPayloadSize, round(avg(diffTime)) as avgDiffTime
    FROM stat
    GROUP by OperationName
    HAVING avgPayloadSize < 1000 AND avgDiffTime < 7000
    ORDER by avgDiffTime DESC, avgPayloadSize DESC
  """

  duplicated_service_query = """
    SELECT OperationName, EventType, min(PayloadSize) as min1, max(PayloadSize) as max1, max(PayloadSize) - min(PayloadSize) as diff1, count(*) as cnt1
    from EventsBy3ActivitiesPerCase1
    GROUP by OperationName, EventType
    HAVING cnt1 > 50 AND diff1 = 0
    ORDER by diff1, OperationName, EventType
  """

  nobody_home_query = """
    SELECT OperationName,  EventType, count(*) as cnt, min(PayloadSize) as min1, max(PayloadSize) as max1, avg(PayloadSize) as avg1 
    from FullData3
    WHERE EventType == "RS"
    Group by OperationName,  EventType
    HAVING cnt <= 5 AND avg1 > 5000
    ORDER by cnt, avg1 DESC
  """

  service_chain_query = """
    SELECT DISTINCT OperationName, count(DISTINCT InvNodeName) as UniqueInvNodeName
    from FullData3
    GROUP by OperationName
    HAVING UniqueInvNodeName > 15
  """

  lost_data_query = """
    with t1 as(SELECT * from TracingEvents WHERE EventType = "RQ")
    , t2 as(SELECT * from TracingEvents WHERE EventType in  ("RS", "SE"))
    , stat1 as( SELECT InvID, OperationName, count(*) as cnt FROM t1 GROUP by InvID, OperationName)
    , stat2 as( SELECT InvID, OperationName, count(*) as cnt FROM t2 GROUP by InvID, OperationName)
    SELECT stat1.InvID, stat1.OperationName, stat1.cnt as cntRQ, stat2.cnt as cntRSAndSE
    FROM stat1 LEFT JOIN stat2 on stat1.InvID = stat2.InvID AND stat1.OperationName = stat2.OperationName
    WHERE cntRQ != cntRSAndSE
  """

  sql_queries = {
    'BottleneckService': bottleneck_service_query,
    'ChattyService': chatty_service_query,
    'DuplicatedService': duplicated_service_query,
    'LostDataService': lost_data_query,
    'NobodyHome': nobody_home_query,
    'ServiceChain': service_chain_query
  }