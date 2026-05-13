# Ignition MES REST API Integration POC

## Overview

This project demonstrates a simple MES/SCADA integration using:

- Ignition Gateway
- Microsoft SQL Server
- Ignition Web Dev Module REST APIs
- OPC Tags from Kepware / Ignition Sample Tags
- Ignition Gateway Timer Scripts

The solution provides:

- Store OPC tag values into SQL Server
- REST GET API to retrieve tags
- Dynamic filtering using machineId and tagName
- Logging support
- SQL Server integration using Ignition Database Connections

---

# Architecture

```plaintext
Kepware OPC / Ignition Tags
            |
            v
Ignition Gateway Timer Script
            |
            v
Microsoft SQL Server
            |
            v
Ignition Web Dev REST APIs
            |
            v
External Clients / Browser / MES / Grafana
```

---

# Technologies Used

| Component | Purpose |
|---|---|
| Ignition Gateway | SCADA/MES Platform |
| Web Dev Module | REST API Hosting |
| Microsoft SQL Server | Database Storage |
| Jython | Ignition Scripting |
| OPC UA / Kepware | Tag Source |

---

# Database Setup

## Create Database

```sql
CREATE DATABASE MESDEV;
GO
```

---

## Create MachineTags Table

```sql
USE MESDEV;
GO

CREATE TABLE MachineTags
(
    id INT IDENTITY(1,1) PRIMARY KEY,

    machineId VARCHAR(100),

    tagName VARCHAR(255),

    tagValue VARCHAR(255),

    tagTimestamp DATETIME DEFAULT GETDATE()
);
GO
```

---

# Ignition Database Connection

Navigate:

```plaintext
Gateway → Config → Databases → Connections
```

Create Database Connection:

| Field | Value |
|---|---|
| Name | MESDEV |
| Type | Microsoft SQL Server |
| Host | localhost |
| Port | 1433 |
| Database | MESDEV |
| Username | sa |
| Password | yourpassword |

Ensure connection status is:

```plaintext
VALID
```

---

# OPC Tags Used

Example Tags:

```plaintext
[Sample_Tags]Realistic/Realistic0
[Sample_Tags]Realistic/Realistic1
```

These can later be replaced with:

- Kepware OPC Tags
- PLC Tags
- MQTT Engine Tags
- Modbus Tags

---

# Gateway Timer Script

## Purpose

Reads OPC tags periodically and stores values into SQL Server.

---

## Configure Timer Script

Navigate:

```plaintext
Designer → Project → Gateway Events → Timer Script
```

Settings:

| Property | Value |
|---|---|
| Delay Type | Fixed Delay |
| Delay | 5000 ms |

---

## Timer Script Code

```python
logger = system.util.getLogger("TagStore")


def storeTags():

    try:

        tags = [
            "[Sample_Tags]Realistic/Realistic0",
            "[Sample_Tags]Realistic/Realistic1"
        ]

        values = system.tag.readBlocking(tags)

        # Generate machineId based on current day
        currentDay = system.date.format(
            system.date.now(),
            "dd"
        )

        machineId = "M" + currentDay

        logger.info(
            "MachineId: " + machineId
        )

        for i, v in enumerate(values):

            if v.quality.isGood():

                tagName = str(tags[i])
                tagValue = str(v.value)

                query = """
                INSERT INTO MachineTags
                (
                    machineId,
                    tagName,
                    tagValue
                )
                VALUES
                (
                    ?, ?, ?
                )
                """

                system.db.runPrepUpdate(
                    query,
                    [
                        machineId,
                        tagName,
                        tagValue
                    ],
                    "MESDEV"
                )

                logger.info(
                    "Inserted : %s = %s" %
                    (tagName, tagValue)
                )

            else:

                logger.warn(
                    "Bad quality : %s" %
                    tags[i]
                )

    except Exception as e:

        logger.error(
            "SQL Error : " + str(e)
        )


storeTags()
```

---

# REST API Setup

## Enable Web Dev Module

Ensure Web Dev module is installed and enabled.

Navigate:

```plaintext
Gateway → Config → Modules
```

---

# Create Web Dev Resource

Navigate:

```plaintext
Designer → Web Dev
```

Create Resource:

```plaintext
MESIntegration/api/tags/getTags
```

---

# REST GET API Script

## Purpose

Provides:

- Get all tags
- Get by machineId
- Get by tagName
- Get by both machineId and tagName

---

## API Script

```python
def doGet(request, session):

    import system
    import traceback

    logger = system.util.getLogger("GETTAGS")

    try:

        logger.info("GET TAG API Called")

        params = request.get("params", {})

        machineId = str(
            params.get("machineId", "")
        ).strip()

        tagName = str(
            params.get("tagName", "")
        ).strip()

        logger.info(
            "machineId = %s , tagName = %s" %
            (machineId, tagName)
        )

        query = """
        SELECT TOP 100
            machineId,
            tagName,
            tagValue,
            tagTimestamp
        FROM MachineTags
        """

        conditions = []
        queryParams = []

        if machineId != "":

            conditions.append(
                "machineId = ?"
            )

            queryParams.append(
                machineId
            )

        if tagName != "":

            conditions.append(
                "tagName = ?"
            )

            queryParams.append(
                tagName
            )

        if len(conditions) > 0:

            query += " WHERE "
            query += " AND ".join(
                conditions
            )

        query += """
        ORDER BY tagTimestamp DESC
        """

        logger.info(
            "Final Query: " + query
        )

        rows = system.db.runPrepQuery(
            query,
            queryParams,
            "MESDEV"
        )

        data = []

        for row in rows:

            item = {

                "machineId":
                    str(row["machineId"]),

                "tagName":
                    str(row["tagName"]),

                "tagValue":
                    str(row["tagValue"]),

                "tagTimestamp":
                    str(row["tagTimestamp"])

            }

            data.append(item)

        response = {

            "status": "success",

            "count": len(data),

            "filters": {

                "machineId": machineId,

                "tagName": tagName

            },

            "data": data

        }

        return {

            "json": response

        }

    except Exception as e:

        logger.error(
            traceback.format_exc()
        )

        return {

            "json": {

                "status": "error",

                "message": str(e)

            }

        }
```

---

# API Usage

## Base URL

```plaintext
http://localhost:8088/system/webdev/samplequickstart/MESIntegration/api/tags/getTags
```

---

# Get All Tags

```plaintext
GET /system/webdev/samplequickstart/MESIntegration/api/tags/getTags
```

Example:

```plaintext
http://localhost:8088/system/webdev/samplequickstart/MESIntegration/api/tags/getTags
```

---

# Get By machineId

```plaintext
GET /system/webdev/samplequickstart/MESIntegration/api/tags/getTags?machineId=M14
```

Example:

```plaintext
http://localhost:8088/system/webdev/samplequickstart/MESIntegration/api/tags/getTags?machineId=M14
```

---

# Get By tagName

```plaintext
GET /system/webdev/samplequickstart/MESIntegration/api/tags/getTags?tagName=[Sample_Tags]Realistic/Realistic0
```

---

# Get By machineId and tagName

```plaintext
GET /system/webdev/samplequickstart/MESIntegration/api/tags/getTags?machineId=M14&tagName=[Sample_Tags]Realistic/Realistic0
```

---

# Example JSON Response

```json
{
  "status": "success",
  "count": 2,
  "filters": {
    "machineId": "M14",
    "tagName": "[Sample_Tags]Realistic/Realistic0"
  },
  "data": [
    {
      "machineId": "M14",
      "tagName": "[Sample_Tags]Realistic/Realistic0",
      "tagValue": "101.55",
      "tagTimestamp": "2026-05-14 10:55:00"
    }
  ]
}
```

---

# Logging

## Logger Names

| Logger | Purpose |
|---|---|
| TagStore | Timer Script Logs |
| GETTAGS | REST API Logs |

---

# View Logs

Navigate:

```plaintext
Gateway → Status → Logs
```

Filter:

```plaintext
TagStore
GETTAGS
```

---

# Common Troubleshooting

## HTTP 500 Error

Cause:

- Invalid JSON response
- Missing return statement
- Database connection failure
- SQL query issue

Solution:

- Ensure API returns:

```python
return {
    "json": response
}
```

---

## Database Connection Error

Verify:

```plaintext
Gateway → Config → Databases → Connections
```

Status must be:

```plaintext
VALID
```

---

## No Data Returned

Verify SQL Data:

```sql
SELECT TOP 10 *
FROM MachineTags
ORDER BY tagTimestamp DESC;
```

---

# Technical Notes

## Why runPrepQuery / runPrepUpdate

Prepared statements are used for:

- SQL Injection protection
- Better performance
- Parameterized queries
- Secure database access

---

## Why return {"json": response}

Ignition Web Dev requires explicit response type wrappers.

Correct:

```python
return {
    "json": response
}
```

Incorrect:

```python
return response
```

---

# Future Enhancements

Possible next upgrades:

- POST API for inserting external tags
- Store images into database
- API key authentication
- Swagger/OpenAPI documentation
- Pagination support
- Date range filtering
- MQTT integration
- Kafka integration
- Grafana dashboards
- Ignition Perspective visualization
- Tag aggregation APIs
- Real-time WebSocket streaming

---

# Conclusion

This POC demonstrates a lightweight MES/SCADA integration pattern using Ignition, SQL Server, and REST APIs.

The solutio