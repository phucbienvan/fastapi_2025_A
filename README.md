# FastAPI Project

## Prerequisites

- Python 3.9.6
- Conda (optional)

## Setup Instructions

### 1. Install Python Environment

If using Conda:
```bash
# Install conda
# Install Python 3.9.6
conda create -n py396 python=3.9.6
conda activate py396
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
touch .env
```

Add your environment variables to the `.env` file.

### 5. Run the Application

```bash
fastapi dev main.py
```

