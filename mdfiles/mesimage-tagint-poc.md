# MES Image & Tag Integration POC

## Executive Summary

This Proof of Concept (POC) demonstrates a modern industrial integration architecture using Ignition SCADA, Kepware OPC, Microsoft SQL Server, REST APIs, and Web technologies.

The solution enables:

* Real-time OPC tag collection from machines
* Image upload and retrieval using REST APIs
* Centralized operational data storage
* Browser-based visualization
* Scalable MES/Industry 4.0 integration foundation

---

## Business Benefits

| Benefit                | Description                                   |
| ---------------------- | --------------------------------------------- |
| Centralized Visibility | Unified machine tags and image management     |
| Open Architecture      | REST API driven integrations                  |
| Reduced Manual Work    | Automated image and tag capture               |
| Future Ready           | Supports MES, AI and Analytics initiatives    |
| Fast Integration       | Rapid onboarding of machines and applications |

---

![MES SCADA Architecture](https://mermaid.ink/img/pako\:eNp1kM1qwzAQhF9F6NyL1yZJ2jS0U4q2hNIKTW1L6EJqI2kSx7YkW9K7d0hK7n4h0w7M7Dczs7sR2VhQm9oQq8oN4G4l4w0v6Q3a6q8Wq9PjQnM3eQfQYhQ7nZ0s1H9m5sB8Wk0t8Y0r6i7pM9lM2v1j3Jzq0f7n6m0m3G4n0G9Y0nVQv4z8Q6q5j3m9l0d0Q9W4wXj5x0m4x9fK6b7m4y6b7b4l3q5u8s0s1zq9m2f2a0f6V3k0n8A)

## High Level Architecture

![Industrial MES Integration](https://images.unsplash.com/photo-1563770660941-10a63607692e?q=80\&w=1200\&auto=format\&fit=crop)

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#4CAF50',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#1B5E20',
    'lineColor': '#0288D1',
    'secondaryColor': '#FF9800',
    'tertiaryColor': '#E3F2FD',
    'fontSize': '16px'
  },
  'flowchart': {
    'curve': 'basis'
  }
}}%%

flowchart LR

A[PLC / Machines]
:::machine
--> B[Kepware OPC Server]

B --> C[Ignition Gateway]

C --> D[(SQL Server)]

E[External Client]
:::client
-. POST Image API .-> C

F[HTML / Web Client]
:::web
-. GET Image API .-> C

C -->|Store Tags| D
C -->|Store Images| D
C -->|Retrieve Images| F

classDef machine fill:#1565C0,stroke:#0D47A1,color:#fff,stroke-width:3px;
classDef client fill:#EF6C00,stroke:#E65100,color:#fff,stroke-width:3px;
classDef web fill:#6A1B9A,stroke:#4A148C,color:#fff,stroke-width:3px;
```

---

![REST API Image Upload](https://images.unsplash.com/photo-1518770660439-4636190af475?q=80\&w=1200\&auto=format\&fit=crop)

# Image Upload Flow

```mermaid
%%{init: {
  'theme': 'forest',
  'themeVariables': {
    'actorBorder': '#1E88E5',
    'actorBkg': '#42A5F5',
    'actorTextColor': '#ffffff',
    'signalColor': '#43A047',
    'signalTextColor': '#000000'
  }
}}%%

sequenceDiagram

participant Client as External Client
participant Ignition as Ignition API
participant SQL as SQL Server

Client->>Ignition: POST Image + Metadata
Note over Client,Ignition: Base64 Encoded Image

Ignition->>Ignition: Decode Base64

Ignition->>SQL: Store Image Binary

SQL-->>Ignition: Success Response

Ignition-->>Client: JSON Success
```

---

![Image Retrieval Dashboard](https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80\&w=1200\&auto=format\&fit=crop)

# Image Retrieval Flow

```mermaid
%%{init: {
  'theme': 'neutral',
  'themeVariables': {
    'actorBorder': '#8E24AA',
    'actorBkg': '#AB47BC',
    'actorTextColor': '#ffffff',
    'signalColor': '#FB8C00'
  }
}}%%

sequenceDiagram

participant Browser
participant Ignition
participant SQL

Browser->>Ignition: GET Image API

Ignition->>SQL: Retrieve Latest Image

SQL-->>Ignition: Image Binary

Ignition-->>Browser: Stream Image Bytes

Browser->>Browser: Render Image
```

---

![Industrial OPC Connectivity](https://images.unsplash.com/photo-1581092921461-eab62e97a780?q=80\&w=1200\&auto=format\&fit=crop)

# OPC Tag Collection Flow

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'primaryColor': '#00BCD4',
    'primaryTextColor': '#ffffff',
    'lineColor': '#4DD0E1'
  }
}}%%

sequenceDiagram

participant PLC
participant Kepware
participant Ignition
participant SQL

PLC->>Kepware: OPC Tags

Kepware->>Ignition: Tag Values

Ignition->>Ignition: Timer Script Reads Tags

Ignition->>SQL: Insert MachineTags

SQL-->>Ignition: Success
```

---

# Animated Flow Diagram

```mermaid
%%{init: {
  'theme': 'base',
  'flowchart': {
    'curve': 'cardinal'
  }
}}%%

flowchart LR

A[Camera Client]
==> B[Ignition REST API]
==> C[(SQL Server)]
==> D[Web Client]

linkStyle 0 stroke:#FF5722,stroke-width:4px;
linkStyle 1 stroke:#4CAF50,stroke-width:4px;
linkStyle 2 stroke:#2196F3,stroke-width:4px;
```

---

# Notes

* Mermaid animations and colors work best in:

  * GitHub Markdown
  * GitLab
  * VS Code Mermaid Preview
  * Obsidian
  * MkDocs

* Some Markdown viewers may not support advanced Mermaid themes.

* For full animated arrows and interactive architecture diagrams, recommended tools:

  * Draw.io
  * Excalidraw
  * Lucidchart
  * Mermaid Live Editor
