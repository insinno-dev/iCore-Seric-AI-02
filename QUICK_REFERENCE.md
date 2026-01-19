# 🚀 Device Support Service - Quick Reference Guide

## 📍 Access Your Application

### Open the Web Interface
```
http://localhost:8501
```

**Status**: ✅ RUNNING NOW

---

## 💬 How to Use

### Step 1: Describe Your Issue
Type your device problem in the chat input:
```
"My laptop won't turn on"
"WiFi router keeps disconnecting"
"Printer is offline"
```

### Step 2: Answer Agent Questions
Follow the agent's diagnostic questions to narrow down the problem:
```
Agent: "When you try to power on, what happens?"
You: "Nothing - no lights or sounds"
```

### Step 3: Get Solutions
The system provides solutions from the knowledge base:
```
Agent: "Try these solutions:
1. Check power adapter connection
2. Test with different outlet
3. Force reset (hold power 30 seconds)
..."
```

### Step 4: Clear & Start Over
Click "Clear Conversation" button to start fresh

---

## 🧪 Run Tests (Optional)

### Validate Everything Works
```bash
python test_streamlit_app.py
```

**Expected Output**: ✓ All 8 tests passed

### Check Qdrant Connection
```bash
python diagnose_qdrant.py
```

**Expected Output**: ✓ Connected to Qdrant successfully

---

## 📁 Project Location
```
C:\Users\ChristianMichel\OneDrive - insinno GmbH\_insinno\Coding\Test-CrewAI
```

---

## 🎯 Key Features

- ✅ AI-powered device troubleshooting
- ✅ Real-time conversation
- ✅ Knowledge base integration
- ✅ Conversation history
- ✅ Clean, modern interface

---

## ⚠️ Troubleshooting

### Issue: App won't start
**Solution**: 
```bash
cd "C:\Users\ChristianMichel\OneDrive - insinno GmbH\_insinno\Coding\Test-CrewAI"
streamlit run app.py
```

### Issue: "Configuration Error" message
**Solution**: Check `.env` file has OPENAI_API_KEY

### Issue: "RAG Service Not Available"
**Solution**: Check internet connection to Qdrant Cloud

### Issue: Slow responses
**Solution**: This is normal (5-10 seconds). Agent is processing with GPT-4.

---

## 📞 Help

### Documentation Files
- `STREAMLIT_README.md` - Detailed web interface guide
- `README.md` - Full project documentation
- `QUICKSTART.md` - Getting started guide

### Run Diagnostics
```bash
python diagnose_qdrant.py
python test_streamlit_app.py
```

---

## 🔧 Configuration

### Environment Variables (in `.env`)
```
OPENAI_API_KEY=your-key-here
QDRANT_URL=https://...eu-central-1-0.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-key-here
QDRANT_COLLECTION_NAME=insinnoflux-seric
```

**Status**: ✅ Already configured

---

## 📊 System Information

| Component | Version | Status |
|-----------|---------|--------|
| CrewAI | 1.8.0 | ✅ |
| Streamlit | 1.53.0 | ✅ |
| Python | 3.13.7 | ✅ |
| Qdrant | Cloud | ✅ |
| OpenAI | GPT-4 | ✅ |

---

## ✨ Example Issues to Try

### Simple Issue
```
"My monitor has no picture"
```

### Medium Issue
```
"Keyboard keys are sticking and slow to respond"
```

### Complex Issue
```
"Computer randomly restarts when running heavy programs"
```

---

## 🎉 You're All Set!

Everything is ready to use. Just open **http://localhost:8501** and start chatting!

**Questions?** Check the documentation files or run tests.

**Issues?** See Troubleshooting section above.

---

**Last Updated**: January 2025
**Status**: ✅ Production Ready
