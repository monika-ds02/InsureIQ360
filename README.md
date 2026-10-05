\# InsureIQ 360



Insurance Claims \& Risk Analytics Platform



\## Overview



InsureIQ 360 is an end-to-end insurance analytics platform designed to manage claims, policies, risk analysis, fraud detection, data quality, workflow alerts, and real-time claim events.



The platform combines a FastAPI backend, React frontend, DuckDB analytics database, Apache Kafka event streaming, Apache Airflow orchestration, and ML-oriented risk analytics.



\## Key Features



\- JWT-based authentication

\- Insurance claim management

\- Policy management

\- Customer and policy claim analytics

\- Real-time Kafka claim events

\- Kafka event persistence

\- Risk analytics

\- Fraud detection

\- Data quality monitoring

\- Investigator workbench

\- SLA breach alerts

\- Investigator assignments

\- Reserve forecasting

\- Interactive dashboard

\- Airflow data pipeline orchestration

\- Docker-based infrastructure

\- Production deployment



\## Technology Stack



| Layer | Technology |

|---|---|

| Frontend | React + Vite |

| Backend | FastAPI + Python |

| Database | DuckDB |

| Streaming | Apache Kafka |

| Orchestration | Apache Airflow |

| Authentication | JWT |

| Password Security | pwdlib |

| API Documentation | Swagger / OpenAPI |

| Deployment | Docker + Vercel / Render |

| Testing | Pytest |



\## Architecture



```text

&#x20;                   ┌─────────────────────┐

&#x20;                   │     React UI        │

&#x20;                   │      Vite           │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │     FastAPI API     │

&#x20;                   │ Authentication/API  │

&#x20;                   └───────┬─────┬───────┘

&#x20;                           │       │

&#x20;                ┌──────────┘       └──────────┐

&#x20;                ▼                             ▼

&#x20;       ┌─────────────────┐           ┌─────────────────┐

&#x20;       │     DuckDB      │           │ Apache Kafka    │

&#x20;       │ Claims/Policies │           │ claims-events   │

&#x20;       └─────────────────┘           └────────┬────────┘

&#x20;                                              │

&#x20;                                              ▼

&#x20;                                     ┌─────────────────┐

&#x20;                                     │ Kafka Consumer  │

&#x20;                                     │ Event Persistence│

&#x20;                                     └─────────────────┘



&#x20;                   ┌─────────────────────┐

&#x20;                   │    Apache Airflow   │

&#x20;                   │ Data Quality / Risk │

&#x20;                   │ Fraud / Alerts      │

&#x20;                   └─────────────────────┘

