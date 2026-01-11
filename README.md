# Varinaut

**An Agentic AI Prediction Machine**

Varinaut is an AI-powered forecasting system inspired by [Superforecasting](https://en.wikipedia.org/wiki/Superforecasting) and platforms like [FateBook](https://fatebook.io/public). It autonomously researches prediction questions, synthesizes information from multiple sources, and produces calibrated probability estimates—with a human in the loop to review, challenge, and refine the reasoning.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Evaluation & Calibration](#evaluation--calibration)
- [Scope & Limitations](#scope--limitations)
- [References](#references)

---

## Overview

Give Varinaut a prediction question like:

> "John Smith wins the 2028 US presidential election"

The system will:

1. **Search** multiple sources (X.com, Polymarket, Google)
2. **Analyze** and synthesize the gathered information
3. **Produce** a likelihood percentage (e.g., "5%") with detailed reasoning
4. **Pause** for human review—you can inspect sources, challenge the reasoning, or provide additional context
5. **Store** the prediction with full history of updates

Over time, as predictions resolve, Varinaut calculates and displays a [**Brier score**](https://en.wikipedia.org/wiki/Brier_score) to track forecasting accuracy.

---

## How It Works

<pre>
┌───────────────────────────────────────────────────────────────────────┐
│                           VARINAUT FLOW                               │
└───────────────────────────────────────────────────────────────────────┘

  User: "Will X happen?"
           │
           ▼
  ┌─────────────────┐
  │  CREATE         │  User submits a prediction question
  │  PREDICTION     │  with optional resolution date
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  SEARCH         │  Agent searches:
  │  SOURCES        │  • X.com (sentiment, expert opinions)
  │                 │  • Polymarket (market prices)
  │                 │  • Google (news, analysis)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  CHUNK &        │  Process results:
  │  EMBED          │  • Extract relevant text
  │                 │  • Generate embeddings
  │                 │  • Store in Chroma
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  RAG            │  Retrieve most relevant
  │  RETRIEVE       │  context for synthesis
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  SYNTHESIZE     │  LLM produces:
  │                 │  • Likelihood percentage
  │                 │  • Reasoning chain
  │                 │  • Source citations
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  HUMAN          │  User reviews:
  │  CHECKPOINT     │  • Inspect reasoning
  │                 │  • Challenge analysis
  │                 │  • Provide additional info
  │                 │  • Adjust likelihood
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  STORE          │  Save prediction with:
  │  PREDICTION     │  • Final likelihood
  │                 │  • Reasoning & sources
  │                 │  • Timestamp
  └─────────────────┘
           │
           │  (Daily or scheduled)
           ▼
  ┌─────────────────┐
  │  UPDATE         │  Re-run search & synthesis
  │  CYCLE          │  to update likelihood
  └─────────────────┘
           │
           │  (When outcome known)
           ▼
  ┌─────────────────┐
  │  EVALUATE       │  Mark as TRUE/FALSE
  │  OUTCOME        │  Update Brier score
  └─────────────────┘
</pre>

---

## Key Features

### 🔮 Prediction Management
- Create prediction questions with optional resolution dates
- Track multiple predictions simultaneously
- View full history of likelihood updates for each prediction

### 🔍 Multi-Source Research
- **X.com**: Public sentiment, expert opinions, breaking news
- **Polymarket**: Prediction market prices as probability signals
- **Google**: News articles, analysis, historical context

### 🧠 AI-Powered Analysis
- LangGraph-based agent for structured reasoning
- RAG pipeline for context-aware synthesis
- Transparent reasoning chains with source citations

### 👤 Human-in-the-Loop
- Review agent's reasoning before accepting predictions
- Challenge analysis or provide additional context
- Adjust likelihood percentages based on your judgment
- Request revisions with specific feedback

### 📊 Calibration Tracking
- Evaluate predictions as TRUE/FALSE when outcomes become known
- Automatic Brier score calculation
- Historical accuracy visualization
- Track forecasting improvement over time

### ⏰ Scheduled Updates
- Trigger daily (or custom interval) updates to existing predictions
- See how predictions evolve as new information emerges
- Full audit trail of all changes

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| **LangGraph** | Core agent orchestration: Search → Analyze → Synthesize → Checkpoint |
| **LangChain** | Document loaders, text splitters, summarization chains |
| **Chroma** | Vector database for storing and retrieving research corpus |
| **RAG** | Retrieve relevant context from past research and sources |
| **DeepEval** | LLM evaluation metrics: faithfulness, coherence, hallucination detection |
| **FastAPI** | Async API with WebSocket support for real-time updates |
| **AsyncIO** | Asynchronous prediction jobs and background tasks |
| **Python 3.12** | Modern Python with latest features |
| **uv** | Fast Python package management |
| **React** | Interactive prediction dashboard |
| **TypeScript** | Type-safe frontend development |
| **Vite** | Fast frontend build tooling |
| **Bun** | Fast frontend runtime & package management |
| **Tailwind** | UI styling and components |
| **SQLite** | Lightweight persistent storage |
| **Makefile** | Development commands and automation |

---

## Architecture

### System Components

<pre>
┌─────────────────────────────────────────────────────────────────────────────┐
│                                FRONTEND                                     │
│                         (React + Vite + TypeScript)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Dashboard  │  │ Prediction  │  │  Approval   │  │   Brier Score       │ │
│  │    View     │  │   Detail    │  │   Panel     │  │      Chart          │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ HTTP / WebSocket
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 BACKEND                                     │
│                         (FastAPI + AsyncIO + Python)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ /predictions│  │  /approve   │  │  /evaluate  │  │      /evals         │ │
│  │    CRUD     │  │  endpoint   │  │  outcomes   │  │    LLM metrics      │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         SERVICES                                    │    │
│  │  prediction_service.py  │  brier_service.py  │  eval_service.py     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  AGENT                                      │
│                              (LangGraph)                                    │
│                                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │ Search   │───▶│ Search   │───▶│ Search   │───▶│  Embed   │              │
│   │  X.com   │    │Polymarket│    │  Google  │    │ & Store  │              │
│   └──────────┘    └──────────┘    └──────────┘    └────┬─────┘              │
│                                                        │                    │
│                                                        ▼                    │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │  Output  │◀───│  Human   │◀───│Synthestic│◀───│   RAG    │              │
│   │          │    │Checkpoint│    │          │    │ Retrieve │              │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌──────────┐     ┌──────────┐     ┌──────────┐
       │  Chroma  │     │  SQLite  │     │ DeepEval │
       │ (Vectors)│     │  (Data)  │     │ (Evals)  │
       └──────────┘     └──────────┘     └──────────┘
</pre>

### User Flow Sequence

<pre>
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  USER  │     │ FRONTEND │     │ BACKEND  │     │  AGENT   │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                │
    │ Enter question│                │                │
    │──────────────▶│                │                │
    │               │                │                │
    │               │ POST /predictions               │
    │               │───────────────▶│                │
    │               │                │                │
    │               │   prediction_id│                │
    │               │◀───────────────│ Start agent    │
    │               │                │───────────────▶│
    │               │                │                │
    │               │ Connect WebSocket               │
    │               │───────────────▶│                │
    │               │                │                │
    │               │                │    Progress    │
    │ See progress  │ WS: progress   │◀───────────────│
    │◀──────────────│◀───────────────│                │
    │               │                │                │
    │               │                │ Human checkpoint
    │ Review reasoning WS: need_approval              │
    │◀──────────────│◀───────────────│◀───────────────│
    │               │                │                │
    │ Challenge/    │                │                │
    │ Approve       │                │                │
    │──────────────▶│                │                │
    │               │ POST /approve  │                │
    │               │───────────────▶│    Resume      │
    │               │                │───────────────▶│
    │               │                │                │
    │               │                │   Complete     │
    │ View prediction WS: complete   │◀───────────────│
    │◀──────────────│◀───────────────│                │
    │               │                │                │
    │ (Later: evaluate outcome)      │                │
    │──────────────▶│ POST /evaluate │                │
    │               │───────────────▶│                │
    │               │                │                │
    │ View Brier    │ GET /brier     │                │
    │ score         │◀───────────────│                │
    │◀──────────────│                │                │
</pre>

---

## Project Structure

<pre>
varinaut/
├── apps/
│   ├── api/                           # FastAPI Backend
│   │   ├── src/
│   │   │   ├── main.py                # Application entrypoint
│   │   │   ├── config.py              # Environment configuration
│   │   │   ├── sqldb.py               # SQLite with SQLAlchemy
│   │   │   ├── routers/
│   │   │   │   ├── predictions.py     # CRUD for predictions
│   │   │   │   ├── approve.py         # Human approval endpoint
│   │   │   │   ├── evaluate.py        # Mark outcomes TRUE/FALSE
│   │   │   │   └── evals.py           # LLM eval results
│   │   │   └── services/
│   │   │       ├── prediction_service.py
│   │   │       ├── brier_service.py   # Brier score calculation
│   │   │       └── eval_service.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── varinautsqlite.db          # SQLite file (gitignored)
│   │
│   └── web/                           # React Frontend
│       ├── src/
│       │   ├── main.tsx
│       │   ├── App.tsx
│       │   ├── components/
│       │   │   ├── PredictionCard.tsx
│       │   │   ├── PredictionHistory.tsx
│       │   │   ├── ReasoningViewer.tsx
│       │   │   ├── ApprovalPanel.tsx
│       │   │   └── BrierScoreChart.tsx
│       │   ├── hooks/
│       │   └── pages/
│       │       ├── Dashboard.tsx      # List predictions + Brier score
│       │       └── PredictionDetail.tsx
│       ├── package.json
│       ├── vite.config.ts
│       └── tailwind.config.js
│
├── packages/
│   ├── agent/                         # LangGraph Agent (THE CORE)
│   │   ├── src/
│   │   │   ├── graph.py               # Agent state machine
│   │   │   ├── state.py               # State definitions
│   │   │   └── nodes/
│   │   │       ├── search_x.py        # X.com search
│   │   │       ├── search_polymarket.py
│   │   │       ├── search_google.py
│   │   │       ├── synthesize.py      # LLM reasoning
│   │   │       └── checkpoint.py      # Human-in-the-loop
│   │   └── pyproject.toml
│   │
│   ├── evals/                         # LLM Evals (THE DIFFERENTIATOR)
│   │   ├── src/
│   │   │   ├── runner.py
│   │   │   └── metrics/
│   │   └── pyproject.toml
│   │
│   └── vectordb/                      # Chroma Utilities
│       ├── src/
│       │   ├── client.py
│       │   └── embeddings.py
│       └── pyproject.toml
│
├── .env.example
├── .gitignore
├── Makefile
├── pyproject.toml
└── README.md
</pre>

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Installation

TODO

### Environment Variables

```bash
# .env.example
AI_MODEL_NAME=your-ai-model-name
AI_MODEL_API_URL=your-ai-model-api-url
AI_MODEL_API_KEY=your-ai-model-api-key
X_API_KEY=your-x-api-key
X_API_SECRET=your-x-api-secret
POLYMARKET_API_KEY=your-polymarket-key
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CSE_ID=your-custom-search-engine-id
```

---

## Usage

### Creating a Prediction

1. Navigate to the dashboard at `http://localhost:5173`
2. Click "New Prediction"
3. Enter your prediction question (e.g., "John Smith wins the 2028 US presidential election")
4. Set a known date
5. Click "Create"

### Reviewing & Approving

When the agent completes its research:

1. Review the proposed likelihood percentage
2. Inspect the reasoning chain and source citations
3. Either:
   - **Accept**: Confirm the prediction as-is
   - **Challenge**: Provide feedback and request a revision
   - **Reject**: Terminate the research process

### Updating Predictions

TODO

### Evaluating Outcomes

When a prediction's outcome becomes known:

1. Navigate to the prediction detail page
2. Click "Evaluate Outcome"
3. Select TRUE or FALSE
4. The Brier score will automatically update

---

## Evaluation & Calibration

### Brier Score

The [Brier score](https://en.wikipedia.org/wiki/Brier_score) measures prediction accuracy:

```
Brier Score = (1/N) × Σ(forecast - outcome)²
```

- **range**: 0 (perfect) to 1 (worst)
- **forecast**: Your probability estimate (0 to 1)
- **outcome**: Actual result (0 = FALSE, 1 = TRUE)

### LLM Evaluation Metrics

DeepEval assesses the quality of agent reasoning:

| Metric | Description |
|--------|-------------|
| **Source Quality** | Did the agent find credible, relevant sources? |
| **Faithfulness** | Does reasoning accurately reflect source information? |
| **Hallucination** | Are there claims not backed by sources? |
| **Coherence** | Is the reasoning well-structured and logical? |
| **Calibration** | Are probability estimates well-justified? |

---

## Scope & Limitations

This is a **demo project** for learning and showcasing agentic AI capabilities. The following aspects have been deliberately omitted (maybe I'll add them later and deploy this to the cloud):

- ❌ Authentication & Authorization
- ❌ Rate-Limiting
- ❌ Multi-user support
- ❌ Production database
- ❌ Containerization
- ❌ CI/CD Pipelines

---

## References

- 📚 [Superforecasting: The Art and Science of Prediction](https://en.wikipedia.org/wiki/Superforecasting) by Philip E. Tetlock
- 🔮 [PredictionBook](https://predictionbook.com) - Inspiration for prediction tracking (now defunct and replaced by FateBook)
- 📈 [Polymarket](https://polymarket.com) - Prediction markets
- 🦜 [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- ✅ [DeepEval Documentation](https://docs.confident-ai.com)
- 📊 [Brier Score](https://en.wikipedia.org/wiki/Brier_score) - Calibration metric

---

## License

MIT

---

<p align="center">
  <i>Built to explore agentic AI, human-in-the-loop patterns, and rigorous evaluation.</i>
</p>
