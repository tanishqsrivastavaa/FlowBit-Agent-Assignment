# FlowBit-Agent-Assignment
## Multi-Agent AI Document Processing System

## 🧠 Objective

A modular multi-agent AI system designed to process and classify inputs from diverse formats (PDF, JSON, Email) and route them intelligently based on detected **format** and **intent**. It enables seamless orchestration and shared memory across agents for traceability and context retention.

---

## 🧩 System Architecture

### 1. 🧭 Classifier Agent
**Input**: Raw file (PDF), JSON, or Email content  
**Responsibilities**:
- Detects input format: `PDF`, `JSON`, `Email`
- Classifies intent: `Invoice`, `RFQ`, `Complaint`, `Regulation`, etc.
- Routes to the correct agent (`JSON Agent`, `Email Agent`, etc.)
- Logs format and intent in shared memory

---

### 2. 📦 JSON Agent
**Input**: Structured JSON payload  
**Responsibilities**:
- Parses and reformats JSON to a target schema
- Validates schema and flags missing or anomalous fields
- Sends parsed data to memory module for logging

---

### 3. 📧 Email Agent
**Input**: Email content (text or HTML)  
**Responsibilities**:
- Extracts metadata: sender, subject, timestamp
- Detects intent and urgency
- Formats data for CRM-style consumption
- Stores parsed output in memory

---

### 🗂 Shared Memory Module
**Purpose**: Central lightweight context store  
**Can use**: `Redis`, `SQLite`, or in-memory store (###ONLY USED in-memory)
**Tracks**:
- Input metadata (source, type, timestamp)
- Extracted fields (sender, topic, urgency, etc.)
- Thread/conversation ID
- Last known state per input

---

## 🔄 Example Flow

1. **User sends email**
2. **Classifier Agent** detects:
   - Format: `Email`
   - Intent: `RFQ`
3. **Routes** to `Email Agent`
4. **Email Agent** extracts:
   - Sender: john@example.com
   - Intent: RFQ
   - Urgency: High
5. Shared **Memory Module** logs:
   - Format: Email
   - Intent: RFQ
   - Sender: john@example.com
   - Timestamp
   - Thread ID

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Install required libraries:

```bash
pip install -r requirements.txt
