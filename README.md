# IntraMind – Internal Knowledge Intelligence

An enterprise-grade **Retrieval-Augmented Generation (RAG)** backend that provides
accurate, explainable, and secure answers grounded in internal organizational documents.

This project follows real-world enterprise GenAI backend practices:
- Offline ingestion
- Online query serving
- JWT-based authentication
- Retrieval-grounded confidence scoring
- Modular, scalable backend architecture

---

## Problem Statement
Employees struggle to search internal policies, SOPs, and wikis efficiently.
Traditional search lacks context, traceability, and reliability.

This system solves that using RAG with source-backed answers and confidence scoring.

---

## Tech Stack
- FastAPI
- LangChain
- FAISS
- HuggingFace MiniLM Embeddings
- Groq LLM
- JWT Authentication
- Streamlit (UI)

---

## How to Run

### Build Vector Store
```bash
python -m scripts.build_vectorstore
```

### Run Backend
```bash
uvicorn app.main:app --reload
```

---

### Run UI Page
```bash
streamlit run streamlit_app.py
```

---

## Conversational & RAG Testing Scenarios

This section documents **how IntraMind is validated**, focusing on **retrieval grounding,
conversational memory, and failure handling**.

These tests ensure the system behaves like a **ChatGPT-style enterprise knowledge assistant**.

---

### 1. Baseline Retrieval Test (Single-Turn)

**Test Question**
```
Is manager approval required for travel reimbursement?
```

**Expected**
- Clear answer grounded in policy documents
- Source files listed
- Confidence score between 0.0 and 1.0

---

### 2. Conversational Memory Test (Follow-Up)

**Conversation**
```
User: Is manager approval required for travel reimbursement?
User: What about international travel?
```

**Expected**
- Follow-up interpreted in context
- No clarification questions
- No hallucinated information

---

### 3. Ellipsis / Implicit Context Test

**Conversation**
```
User: What documents are needed for expense claims?
User: And for meals?
```

**Expected**
- “Meals” understood as meal expense claims
- Uses the same document context
- No redundant explanations

---

### 4. Topic Switching Test

**Conversation**
```
User: Explain travel reimbursement policy.
User: Now explain leave policy.
```

**Expected**
- Second answer ignores travel context
- Fresh retrieval based on leave-related documents

---

### 5. Bounded Memory Test

**Test**
```
(After multiple travel-related questions)
User: What is the office attendance policy?
```

**Expected**
- Older travel context is ignored
- Answer based only on attendance documents

---

### 6. Hallucination Guard Test (Out-of-Scope)

**Test Question**
```
What is the Friday dress code?
```

**Expected**
- Response indicates information is not available

---

## Disclaimer
AI-generated answers should be reviewed before compliance-critical use.
