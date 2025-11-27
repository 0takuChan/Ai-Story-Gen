# AI Story Game

เกมสร้างเรื่องราวแบบ Interactive โดยใช้ AI ในการสร้างเนื้อเรื่องและตัวเลือก แต่ละตัวเลือกนำไปสู่จุดจบที่ต่างกัน

## เทคโนโลยีที่ใช้

### Backend
- **Python 3.8+**
- **FastAPI** - Web framework
- **LangChain** - สำหรับจัดการ LLM chains
- **ChatGroq** - AI model (Mixtral-8x7b)
- **RAG (Retrieval-Augmented Generation)** - ใช้ FAISS vector store
- **HuggingFace Embeddings** - สำหรับ semantic search

### Frontend
- **React 18**
- **Vite** - Build tool
- **Axios** - HTTP client

## การติดตั้งและรันโปรเจค

### 1. ตั้งค่า Backend

```powershell
# เข้าไปยัง backend directory
cd backend

# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน virtual environment
.\venv\Scripts\Activate.ps1

# ติดตั้ง dependencies
pip install -r requirements.txt

# สร้างไฟล์ .env และใส่ API key
# คัดลอกจาก .env.example
cp .env.example .env

# แก้ไขไฟล์ .env และใส่ GROQ_API_KEY ของคุณ
# ดาวน์โหลด API key ได้ที่: https://console.groq.com/keys
```

### 2. ตั้งค่า Frontend

```powershell
# เปิด terminal ใหม่
# เข้าไปยัง frontend directory
cd frontend

# ติดตั้ง dependencies
npm install
```

### 3. รันโปรเจค

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
# Backend จะรันที่ http://localhost:8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
# Frontend จะรันที่ http://localhost:3000
```

### 4. เปิดเบราว์เซอร์

เปิดไปที่ `http://localhost:3000` เพื่อเล่นเกม

## วิธีการใช้งาน

1. **เลือกธีม** - เลือกธีมเรื่องที่ต้องการ (ผจญภัย, ลึกลับ, ไซไฟ, สยองขวัญ, โรแมนติก)
2. **อ่านเนื้อเรื่อง** - AI จะสร้างเนื้อเรื่องเริ่มต้นให้
3. **เลือกตัวเลือก** - เลือก 1 จาก 3 ตัวเลือกที่ AI เสนอ
4. **เนื้อเรื่องดำเนินต่อ** - AI จะสร้างเนื้อเรื่องต่อตามที่คุณเลือก
5. **จบเรื่อง** - หลังจาก 4-5 ครั้งเรื่องจะจบลง แต่ละครั้งที่เล่นจะได้จุดจบที่ต่างกัน

## หลักการทำงานของ RAG

โปรเจคนี้ใช้ RAG (Retrieval-Augmented Generation) ดังนี้:

1. **Vector Store** - เก็บ story templates ในรูปแบบ embeddings ด้วย FAISS
2. **Semantic Search** - เมื่อเริ่มเรื่อง AI จะค้นหาเรื่องที่คล้ายกันจาก vector store
3. **Context Enhancement** - ใช้เรื่องที่ค้นพบเป็นบริบทเสริมให้ LLM สร้างเรื่องที่สอดคล้องกับธีม
4. **Dynamic Generation** - LLM สร้างเนื้อเรื่องใหม่โดยอ้างอิงจาก templates และ user choices

## โครงสร้างโปรเจค

```
Project_AI/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── story_generator.py   # LangChain + RAG logic
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # ตัวอย่าง environment variables
│   └── .env                # API keys (ต้องสร้างเอง)
│
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── services/       # API calls
    │   ├── App.jsx        # Main app
    │   └── main.jsx       # Entry point
    ├── package.json
    └── vite.config.js
```

## API Endpoints

- `GET /` - Health check
- `GET /api/game/themes` - ดึงรายการธีมที่มี
- `POST /api/game/start` - เริ่มเกมใหม่
- `POST /api/game/choice` - ส่งตัวเลือกและรับเนื้อเรื่องต่อ

## ตัวอย่างการใช้ API

```javascript
// เริ่มเกม
POST /api/game/start
{
  "theme": "adventure"
}

// เลือกตัวเลือก
POST /api/game/choice
{
  "story_id": "uuid-here",
  "choice_index": 0,
  "context": "คุณเดินเข้าไปในถ้ำ"
}
```

## ข้อควรรู้

- เรื่องจะจบภายใน 4-5 ตา (turns)
- แต่ละครั้งที่เล่นจะได้เรื่องและจุดจบที่ต่างกัน
- AI ใช้ RAG เพื่อให้เรื่องสอดคล้องกับธีมที่เลือก
- รองรับภาษาไทย

## License

MIT License

## Contributors

Created for CE392 Project - AI Story Game with RAG
