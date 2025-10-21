# Caption Troubleshooting Guide

## ✅ Caption Format Requirements

Your caption JSON file **MUST** follow this exact format:

```json
[
  {
    "text": "Your word or phrase",
    "startMs": 0,
    "endMs": 500,
    "timestampMs": 0,
    "confidence": 0.95
  },
  {
    "text": "Next word",
    "startMs": 500,
    "endMs": 1000,
    "timestampMs": 500,
    "confidence": 0.98
  }
]
```

## 🔍 Common Issues and Solutions

### Issue 1: Captions Don't Appear in Video

**Possible Causes:**
1. ❌ Wrong JSON format
2. ❌ File not named correctly
3. ❌ Invalid JSON syntax
4. ❌ Wrong field names

**Solutions:**
- ✅ Verify your JSON is an **array** (starts with `[` not `{`)
- ✅ Use `startMs` and `endMs` (NOT `start` and `end`)
- ✅ File will be saved as `Untitled.json` automatically
- ✅ Validate JSON at https://jsonlint.com/

### Issue 2: JSON Validation Error

**Symptoms:**
- GUI shows "Invalid JSON file" error
- Caption file won't load

**Solutions:**
1. Check for:
   - Missing commas between objects
   - Extra commas after last object
   - Unclosed brackets or braces
   - Unescaped quotes in text
2. Use a JSON validator
3. Copy the example format exactly

### Issue 3: Timing Issues

**Symptoms:**
- Captions appear at wrong time
- Captions too fast/slow
- Captions don't sync with audio

**Solutions:**
- Ensure times are in **milliseconds** (not seconds)
- 1 second = 1000 milliseconds
- `startMs` should be less than `endMs`
- No overlapping times between words
- `timestampMs` should match `startMs`

## 📋 Field Descriptions

### Required Fields:

**`text`** (string)
- The word or phrase to display
- Can include spaces for phrases
- Use quotes for apostrophes: `"don't"` → `"don\\'t"`

**`startMs`** (number)
- When caption starts (milliseconds)
- Must be >= 0
- Must be < endMs

**`endMs`** (number)
- When caption ends (milliseconds)
- Must be > startMs
- Should not exceed audio duration

**`timestampMs`** (number)
- Reference timestamp (milliseconds)
- Usually same as startMs
- Used for synchronization

### Optional Fields:

**`confidence`** (number)
- Confidence score from speech recognition
- Range: 0.0 to 1.0
- Higher = more confident
- Can be omitted or set to 1.0

## ✏️ Creating Caption Files

### Method 1: Manual Creation

1. Create a text file
2. Save as `.json`
3. Follow the format above
4. Validate at jsonlint.com
5. Import in GUI

### Method 2: Conversion from Other Formats

If you have captions in a different format, convert them:

**From SRT format:**
```
1
00:00:00,000 --> 00:00:00,500
Hello

2
00:00:00,500 --> 00:00:01,000
World
```

**To JSON:**
```json
[
  {
    "text": "Hello",
    "startMs": 0,
    "endMs": 500,
    "timestampMs": 0,
    "confidence": 1.0
  },
  {
    "text": "World",
    "startMs": 500,
    "endMs": 1000,
    "timestampMs": 500,
    "confidence": 1.0
  }
]
```

### Method 3: Auto-Generation (Future)

The project may support auto-generation with:
```bash
npm run create-subtitles "path/to/audio.mp3"
```

This will create a JSON file automatically.

## 🧪 Testing Your Caption File

### Quick Test:

1. Open your JSON in a text editor
2. Copy the content
3. Paste into: https://jsonlint.com/
4. Click "Validate JSON"
5. Should say "Valid JSON"

### Structure Test:

Your JSON should:
- Start with `[` (opening bracket)
- Contain objects with `{}`
- Separate objects with commas
- End with `]` (closing bracket)

### Example Test File:

Use the included `example_captions.json` as a reference.

## 📐 Time Calculation Tips

### Converting Seconds to Milliseconds:
- 0.5 seconds = 500 ms
- 1 second = 1000 ms
- 1.5 seconds = 1500 ms
- 2 seconds = 2000 ms

### Calculating Duration:
- If a word lasts 0.5 seconds starting at 1 second:
  - startMs: 1000
  - endMs: 1500
  - duration: 500 ms

### Typical Word Durations:
- Short word (1-3 letters): 200-400 ms
- Medium word (4-6 letters): 400-600 ms
- Long word (7+ letters): 600-1000 ms
- Pause between words: 100-200 ms

## ⚠️ Common Mistakes

### ❌ WRONG - Using "start" instead of "startMs":
```json
[
  {
    "text": "Hello",
    "start": 0,        ← WRONG
    "end": 500         ← WRONG
  }
]
```

### ✅ CORRECT:
```json
[
  {
    "text": "Hello",
    "startMs": 0,      ← CORRECT
    "endMs": 500       ← CORRECT
  }
]
```

### ❌ WRONG - Wrapping in "words" object:
```json
{
  "words": [           ← WRONG - Extra wrapper
    {
      "text": "Hello",
      "startMs": 0,
      "endMs": 500
    }
  ]
}
```

### ✅ CORRECT:
```json
[                      ← CORRECT - Direct array
  {
    "text": "Hello",
    "startMs": 0,
    "endMs": 500
  }
]
```

### ❌ WRONG - Using seconds instead of milliseconds:
```json
[
  {
    "text": "Hello",
    "startMs": 0.5,    ← WRONG - Should be 500
    "endMs": 1.0       ← WRONG - Should be 1000
  }
]
```

### ✅ CORRECT:
```json
[
  {
    "text": "Hello",
    "startMs": 500,    ← CORRECT
    "endMs": 1000      ← CORRECT
  }
]
```

## 🔧 Advanced: Minimal Format

Minimum required fields (though confidence is recommended):

```json
[
  {
    "text": "Hello",
    "startMs": 0,
    "endMs": 500,
    "timestampMs": 0
  }
]
```

## 📞 Still Having Issues?

1. **Validate your JSON** at jsonlint.com
2. **Compare** with `example_captions.json`
3. **Check** the Status Log in the GUI for errors
4. **Verify** the file loads without error
5. **Test** with a simple 2-word caption first

## 📝 Example Workflow

1. Create `my_captions.json`
2. Add this content:
```json
[
  {
    "text": "Test",
    "startMs": 0,
    "endMs": 1000,
    "timestampMs": 0,
    "confidence": 1.0
  }
]
```
3. Validate at jsonlint.com
4. Import in GUI
5. Render video
6. Verify caption appears

If it works, expand with more words!

## 🎯 Best Practices

- ✅ Start simple with 2-3 words
- ✅ Validate before importing
- ✅ Use consistent timing
- ✅ Leave gaps between words
- ✅ Match audio duration
- ✅ Keep backup copies
- ✅ Test incrementally

## 📚 Resources

- JSON Validator: https://jsonlint.com/
- Example file: `example_captions.json`
- User Guide: `USER_GUIDE.md`
- Format documentation: `README.md`

---

**Remember:** The caption file must be:
1. Valid JSON (check with validator)
2. An array (not object)
3. Using milliseconds (not seconds)
4. Using correct field names (startMs, endMs, not start, end)
5. Will be saved as `Untitled.json` automatically
