<!--
  =============================================================================
  Phuchello / GitHub Profile README Template
  AUTO-GENERATED via scripts/render_profile.py from data/*.yml
  DO NOT EDIT README.md DIRECTLY. Edit data/projects.yml, data/stack.yml,
  or data/profile.yml, then run: python scripts/render_profile.py
  =============================================================================
-->

<div align="center">
  <img src="assets/network-banner.svg" alt="Phuchello Network Intelligence Banner" width="100%">
</div>

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ NOC CONSOLE :: PHUCHELLO.NET                               SYS_STATE: ONLINE│
├─────────────────────────────────────────────────────────────────────────────┤
│ IDENTITY   : Võ Trọng Phúc (Phuchello)                                      │
│ ROLE       : Network Engineering · AIoT · Research Systems                  │
│ AFFILIATION: University of Information Technology — VNU-HCM (UIT)           │
│ LOCATION   : Ho Chi Minh City, Vietnam                                      │
│ MISSION    : Building intelligent systems where networks, edge, & AI meet.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## // 01. ENGINEERING & RESEARCH FOCUS

Undergraduate systems student and researcher at **UIT (VNU-HCM)**. Working at the intersection of network engineering, edge devices (AIoT), and research intelligence infrastructure. Focused on deterministic, provenance-aware architectures from transport protocols to cloud databases.

* **Network Engineering & Observability** — Socket programming (TCP/UDP), application-layer protocols (HTTP/REST, SMTP, FTP), RAW socket sniffing, and deep packet analysis via Wireshark.
* **Edge Systems & AIoT** — Microcontroller interfacing (ESP32), sensor telemetry streams, and lightweight MQTT pub/sub messaging architectures.
* **Research Intelligence Infrastructure** — Provenance-first data modeling, asynchronous academic ingestion pipelines (arXiv, Crossref, OpenAlex, Semantic Scholar), and PostgreSQL `pgvector` vector storage.

---

## // 02. SYSTEM ARCHITECTURE & RESEARCH TRAJECTORY

A conceptual map of technical directions spanning physical sensing, network transport, data engineering, and personal research memory.

<div align="center">
  <img src="assets/topology.svg" alt="Edge-to-Cloud System Architecture & Research Trajectory" width="100%">
</div>

---

## // 03. TECHNICAL CAPABILITIES BY SYSTEM LAYER

### `// LAYER :: NETWORKING`
> *Transport layer protocols, socket programming, and packet analysis*

| Capability | Focus / Engineering Details |
|---|---|
| **TCP/IP & UDP** | Stream framing, datagram boundaries, 3-way handshake mechanics |
| **Socket Programming** | Client-server architecture, non-blocking I/O, multi-client concurrency |
| **Application Protocols** | HTTP/1.1, RESTful APIs, SMTP, POP3, IMAP, FTP |
| **Packet Observability** | Wireshark dissection, display filters, RAW socket packet capture |
| **Network Security** | AES-256 payload encryption, SHA-256 integrity hashing, basic TLS/SSL concepts |

### `// LAYER :: EDGE & AIoT`
> *Physical sensing, microcontroller interfacing, and distributed telemetry*

| Capability | Focus / Engineering Details |
|---|---|
| **ESP32 & Microcontrollers** | Hardware GPIO control, sensor polling, serial communication |
| **MQTT Protocol** | Lightweight pub/sub messaging, QoS levels, edge telemetry broker |
| **Sensors & Peripherals** | Analog/digital data acquisition, environment telemetry |
| **Edge Computing (Exploring)** | Local signal filtering, lightweight edge inference, gateway routing |

### `// LAYER :: SYSTEMS & DATA CORE`
> *Operating system primitives, data engines, and foundational tooling*

| Capability | Focus / Engineering Details |
|---|---|
| **Linux / POSIX** | Shell scripting, process management, file I/O streams |
| **PostgreSQL 16** | Relational modeling, async drivers (asyncpg), ACID transactions, Alembic migrations |
| **Docker & Compose** | Multi-container services, reproducible local dev environments |
| **C / C++** | Manual memory allocation, pointer mechanics, algorithmic optimization |
| **Git & Version Control** | Deterministic branch workflows, modular repo management |

### `// LAYER :: CLOUD & INFRASTRUCTURE`
> *Deployment environments, CI/CD automation, and service orchestration*

| Capability | Focus / Engineering Details |
|---|---|
| **Container Orchestration** | Docker Compose service meshes, volume management, health checks |
| **CI/CD Automation** | GitHub Actions workflows, automated testing, migration checks |
| **Async Service Design** | Asynchronous task execution, retry/backoff policies, rate limiting |

### `// LAYER :: INTELLIGENCE & RESEARCH`
> *Scientific data ingestion, vector search, and provenance engineering*

| Capability | Focus / Engineering Details |
|---|---|
| **Python 3.12 Ecosystem** | FastAPI async, Pydantic v2 validation, SQLAlchemy 2.0 async ORM |
| **Vector Search (pgvector)** | HNSW / IVFFlat indexing, similarity search, hybrid retrieval |
| **Scientific Ingestion** | Metadata pipelines for arXiv, Crossref, OpenAlex, Semantic Scholar |
| **Provenance Architecture** | Durable evidence-to-claim lineage, idempotent deduplication |

---

## // 04. FEATURED SYSTEMS & REPOSITORIES

### [Intel OS (NCKH)](https://github.com/Phuchello/NCKH)
**Category:** `Research Intelligence & Systems` &nbsp;|&nbsp; **Status:** `Active (G2 Ingestion Review)` &nbsp;|&nbsp; **Stack:** `Python 3.12` · `FastAPI (Async)` · `PostgreSQL 16 + pgvector` · `SQLAlchemy 2.x / asyncpg` · `Alembic Migrations` · `Docker Compose`

> **A personal scientific intelligence platform turning massive literature into provenance-aware research memory**

A research-engineering platform built around an Intelligence Lake, Personal Research Memory, and Research Opportunity Memory. Engineered with a modular monolith architecture, async HTTP ingestion pipelines for academic sources (arXiv, Crossref, OpenAlex, Semantic Scholar), conservative multi-provider reconciliation, and PostgreSQL pgvector embeddings.

🔗 **Links:** [Repository](https://github.com/Phuchello/NCKH) · [Docs](https://github.com/Phuchello/NCKH/blob/main/docs/PUBLIC_PROGRESS.md)

---

### [NT106 Network Programming Handbook](https://github.com/Phuchello/NT106_UIT_HANDBOOK)
**Category:** `Network Engineering & Observability` &nbsp;|&nbsp; **Status:** `Completed / Reference` &nbsp;|&nbsp; **Stack:** `TCP / UDP Sockets` · `RAW Sockets (Promiscuous)` · `Wireshark Analysis` · `HTTP / REST APIs` · `Multithreaded I/O` · `AES-256 / SHA-256`

> **Comprehensive systems engineering handbook covering socket programming, application protocols, and packet sniffing**

An in-depth 18-chapter practical and theoretical reference for Network Programming (NT106) at UIT. Implements end-to-end socket architectures (TCP stream framing, UDP datagrams, multi-client servers), application layer protocols (HTTP REST, SMTP/POP3/IMAP, FTP), promiscuous RAW socket packet sniffers, and Wireshark filter dissection.

🔗 **Links:** [Repository](https://github.com/Phuchello/NT106_UIT_HANDBOOK) · [Web View](https://github.com/Phuchello/NT106_UIT_HANDBOOK/blob/main/NT106_CamNang_LapTrinhMang_UIT_VoTrongPhuc_PRECODEX.pdf)

---

### [DSA Comprehensive Handbook](https://github.com/Phuchello/DSA_UIT_HANDBOOK)
**Category:** `Algorithms & Systems Foundations` &nbsp;|&nbsp; **Status:** `Completed / Reference` &nbsp;|&nbsp; **Stack:** `C++ / STL` · `Tree Algorithms (AVL, B-Tree)` · `Graph Algorithms (Dijkstra, BFS/DFS)` · `Asymptotic Proofs` · `Dry-Run Tracing` · `KaTeX Math`

> **Pedagogical data structures and algorithms reference with dry-run tables and asymptotic proofs**

A rigorous 16-chapter engineering handbook covering algorithmic complexity (Big-O, Omega, Theta), 10 sorting algorithms with memory/stability analysis, pointer-based data structures (BST, AVL trees, B-Trees, Min/Max Heaps), collision-resolved hash tables, and graph traversal/shortest path algorithms.

🔗 **Links:** [Repository](https://github.com/Phuchello/DSA_UIT_HANDBOOK) · [Web View](https://phuchello.github.io/DSA_UIT_HANDBOOK/)

---

## // 05. CURRENT RESEARCH & LEARNING TRAJECTORY

* **Intel OS (NCKH) G2 Ingestion Closure** — Completing adversarial review for multi-provider academic metadata reconciliation, idempotent database upserts, and resilient async HTTP rate-limiting.
* **Network Observability & Protocols** — Deepening packet inspection techniques, custom frame dissection, and socket concurrency models.
* **Edge Telemetry Pipelines** — Experimenting with ESP32 sensor nodes transmitting structured telemetry via MQTT to containerized ingestion gateways.

---

## // 06. CONNECT & TELEMETRY

<div align="center">

```text
[phuchello@noc-uit-01 ~]$ ping -c 1 vntrphuc.network
64 bytes from uit-node-01: icmp_seq=1 ttl=64 time=0.038 ms
--- status: 0% packet loss | systems operational | open to research collaboration ---
```

[![GitHub](https://img.shields.io/badge/GitHub-Phuchello-00E5FF?style=flat-square&logo=github&logoColor=070B14)](https://github.com/Phuchello)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-phucvopro-38BDF8?style=flat-square&logo=linkedin&logoColor=070B14)](https://www.linkedin.com/in/phucvopro/)

</div>
