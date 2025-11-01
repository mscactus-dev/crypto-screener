# 🔴 Bitcoin Astrology - LIVE Version Instructions

This version calculates **real-time planetary positions** from your CSV data every time you open it!

## 🚀 Quick Start (3 Easy Steps)

### Step 1: Open Terminal/Command Prompt

**On Mac/Linux:**
- Press `Command + Space`, type `terminal`, press Enter
- Navigate to this folder: `cd /path/to/crypto-screener`

**On Windows:**
- Press `Windows Key + R`, type `cmd`, press Enter
- Navigate to this folder: `cd C:\path\to\crypto-screener`

### Step 2: Start the Server

**Mac/Linux:**
```bash
python3 server.py
```

**Windows:**
```bash
python server.py
```

**OR just double-click:**
- `START_SERVER.sh` (Mac/Linux)
- `START_SERVER.bat` (Windows)

### Step 3: Open in Browser

Once you see:
```
Server running at: http://localhost:8000/
```

**Open this link in your browser:**
```
http://localhost:8000/bitcoin-astrology-live.html
```

---

## ✨ Features

### 🔄 Auto-Updating Data
- **Clock:** Updates every second
- **Planetary Positions:** Calculates fresh data from CSV on page load
- **Auto-Refresh:** Data refreshes every 5 minutes automatically
- **Last Updated:** Shows exact timestamp of calculation

### 📊 What Updates Live
- ✅ Malefic Aspects count
- ✅ Benefic Aspects count
- ✅ Mercury Status (Direct/Retrograde)
- ✅ Mars-Uranus hard aspect detection
- ✅ Current planetary positions
- ✅ All aspects to Bitcoin natal chart
- ✅ Timestamp

---

## 🛑 How to Stop the Server

Press `Ctrl + C` in the terminal/command prompt where the server is running.

---

## 🆚 Standalone vs Live Version

### Standalone Version (`bitcoin-astrology-standalone.html`)
- ✅ Works offline (no server needed)
- ✅ Just double-click to open
- ❌ Planetary data is "frozen" from when file was created
- 📅 Best for: Quick checks, offline use

### Live Version (`bitcoin-astrology-live.html`)
- ✅ Always calculates fresh positions from CSV
- ✅ Auto-refreshes every 5 minutes
- ❌ Requires Python server running
- ❌ Need internet for fonts/icons
- 📅 Best for: Monitoring, accurate real-time data

---

## ❓ Troubleshooting

### "Connection refused" or "Cannot GET /run-astro-calc"
**Solution:** Make sure the Python server is running! See Step 2 above.

### "No module named..." or Python errors
**Solution:** This project uses only Python standard library. Make sure you have Python 3.7+ installed:
```bash
python3 --version
```

### Port 8000 already in use
**Solution:** Either:
1. Stop whatever is using port 8000, OR
2. Edit `server.py` and change `PORT = 8000` to `PORT = 8001` (or any free port)

### Data shows as "0 0 None"
**Solution:** Check browser console (F12 → Console tab) for errors. The server might not be running.

---

## 🎯 Pro Tips

1. **Keep Server Running:** Leave the terminal open in the background while using the app
2. **Bookmark It:** Bookmark `http://localhost:8000/bitcoin-astrology-live.html` for quick access
3. **Check Console:** Press F12 in browser to see live data loading messages
4. **Manual Refresh:** Just reload the page (F5) to get instant fresh calculations

---

## 📁 Files You Need

Make sure these files are in the same folder:
- ✅ `server.py` - Web server
- ✅ `astro_calc.py` - Calculation engine
- ✅ `bitcoin-astrology-live.html` - Web interface
- ✅ `CLAUDE Planetary Positions 2025-2035.csv` - Your ephemeris data

---

**Enjoy your live Bitcoin astrology tracker!** 🌟🪐📈
