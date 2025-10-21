# Video Generator GUI - Workflow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO GENERATOR GUI                       │
│                    (video_generator_gui.py)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ User Interaction
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Browse Audio │     │Browse Images │     │Browse Caption│
│              │     │              │     │              │
│  .mp3 .wav   │     │  .jpg .png   │     │    .json     │
│  .m4a .aac   │     │    .webp     │     │  (optional)  │
└──────────────┘     └──────────────┘     └──────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Render Button   │
                    │   (Click to      │
                    │   start render)  │
                    └──────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         FILE PREPARATION PHASE           │
        │                                          │
        │  1. Clear old assets folders             │
        │  2. Copy audio to assets/audio/          │
        │  3. Copy images to assets/images/        │
        │     (renamed as image_1, image_2, etc.)  │
        │  4. Copy caption to assets/audio/        │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         RENDERING PHASE                  │
        │                                          │
        │  1. Run: npm run render                  │
        │  2. Node.js executes render.js           │
        │  3. Remotion bundles project             │
        │  4. Video rendered to out/video.mp4      │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         SAVE PHASE                       │
        │                                          │
        │  1. User selects save location           │
        │  2. Video copied to chosen location      │
        │  3. Success message displayed            │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         CLEANUP PHASE                    │
        │                                          │
        │  1. Clear assets/audio/ folder           │
        │  2. Clear assets/images/ folder          │
        │  3. Remove remotion_entry_*.jsx files    │
        │  4. Remove out/video.mp4                 │
        │  5. Reset GUI selections                 │
        └─────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Ready for      │
                    │   Next Video!    │
                    └──────────────────┘
```

## Data Flow

```
User Files (Original Location)
        │
        ├─ audio_file.mp3 ──────────┐
        ├─ image_1.jpg ──────────────┤
        ├─ image_2.jpg ──────────────┼──► Copy to Assets
        ├─ image_3.jpg ──────────────┤
        └─ captions.json ────────────┘
                                      │
                                      ▼
                        ┌─────────────────────┐
                        │  public/assets/     │
                        │                     │
                        │  ├─ audio/          │
                        │  │  ├─ audio.mp3    │
                        │  │  └─ audio.json   │
                        │  │                  │
                        │  └─ images/         │
                        │     ├─ image_1.jpg  │
                        │     ├─ image_2.jpg  │
                        │     └─ image_3.jpg  │
                        └─────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────┐
                        │   render.js         │
                        │   (Node.js)         │
                        │                     │
                        │ - Reads assets      │
                        │ - Bundles React     │
                        │ - Renders video     │
                        └─────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────┐
                        │    out/video.mp4    │
                        │  (Temporary file)   │
                        └─────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────┐
                        │  User's Chosen      │
                        │  Location           │
                        │  (Final video)      │
                        └─────────────────────┘
```

## GUI State Machine

```
┌─────────────┐
│   READY     │◄──────────────────────────────────┐
│             │                                   │
│ • All       │                                   │
│   buttons   │                                   │
│   enabled   │                                   │
└─────────────┘                                   │
      │                                           │
      │ User clicks "Render"                      │
      │                                           │
      ▼                                           │
┌─────────────┐                                   │
│  RENDERING  │                                   │
│             │                                   │
│ • Render    │                                   │
│   button    │                                   │
│   disabled  │                                   │
│ • Progress  │                                   │
│   bar       │                                   │
│   running   │                                   │
└─────────────┘                                   │
      │                                           │
      │ Render completes                          │
      │                                           │
      ▼                                           │
┌─────────────┐                                   │
│   SAVING    │                                   │
│             │                                   │
│ • Save      │                                   │
│   dialog    │                                   │
│   shown     │                                   │
└─────────────┘                                   │
      │                                           │
      │ User saves file                           │
      │                                           │
      ▼                                           │
┌─────────────┐                                   │
│  CLEANUP    │                                   │
│             │                                   │
│ • Removing  │                                   │
│   temp      │                                   │
│   files     │                                   │
│ • Clearing  │                                   │
│   UI        │                                   │
└─────────────┘                                   │
      │                                           │
      │ Cleanup complete                          │
      │                                           │
      └───────────────────────────────────────────┘
```

## Thread Model

```
┌──────────────────────────────────────────────┐
│           MAIN THREAD (GUI)                  │
│                                              │
│  • Handles all UI interactions               │
│  • Updates UI elements                       │
│  • Shows dialogs                             │
└──────────────────────────────────────────────┘
                    │
                    │ Creates
                    ▼
┌──────────────────────────────────────────────┐
│         RENDERING THREAD                     │
│                                              │
│  1. Clear assets folders                     │
│  2. Copy files                               │
│  3. Run npm render (subprocess)              │
│  4. Signal main thread when done             │
└──────────────────────────────────────────────┘
                    │
                    │ Calls back to
                    ▼
┌──────────────────────────────────────────────┐
│           MAIN THREAD (GUI)                  │
│                                              │
│  • Shows save dialog                         │
│  • Performs cleanup                          │
│  • Resets UI                                 │
└──────────────────────────────────────────────┘
```

## File Structure

```
creator/
│
├── GUI/                              ← New GUI folder
│   ├── video_generator_gui.py        ← Main application
│   ├── config.py                     ← Configuration
│   ├── start_gui.bat                 ← Windows launcher
│   ├── test_setup.py                 ← Setup checker
│   ├── requirements.txt              ← Python deps info
│   ├── README.md                     ← Basic docs
│   ├── QUICKSTART.md                 ← Quick guide
│   ├── USER_GUIDE.md                 ← Complete guide
│   └── WORKFLOW.md                   ← This file
│
├── public/
│   └── assets/
│       ├── audio/                    ← Audio files go here
│       └── images/                   ← Images go here
│
├── out/
│   └── video.mp4                     ← Rendered video (temp)
│
├── src/
│   ├── Video.jsx                     ← Main video component
│   ├── CaptionDisplay.jsx            ← Caption component
│   └── ...
│
├── render.js                         ← Rendering script
├── package.json                      ← Node.js config
└── ...
```

## Error Handling Flow

```
┌─────────────┐
│ User Action │
└─────────────┘
      │
      ▼
┌─────────────┐      Error?      ┌──────────────┐
│  Operation  │────────YES───────►│ Log to       │
│             │                   │ Status Log   │
└─────────────┘                   └──────────────┘
      │                                  │
      NO                                 │
      │                                  ▼
      ▼                           ┌──────────────┐
┌─────────────┐                   │ Show Error   │
│  Continue   │                   │ Dialog       │
│  to Next    │                   └──────────────┘
│  Step       │                          │
└─────────────┘                          │
                                         ▼
                                  ┌──────────────┐
                                  │ Reset UI     │
                                  │ to Ready     │
                                  └──────────────┘
```

## Key Features

### Automated Workflow
- ✓ Automatic file preparation
- ✓ Background rendering
- ✓ Automatic cleanup

### User-Friendly
- ✓ Clear visual feedback
- ✓ Detailed logging
- ✓ Error messages

### Robust
- ✓ Thread-safe operations
- ✓ Error handling
- ✓ State management

### Flexible
- ✓ Configurable settings
- ✓ Optional captions
- ✓ Multiple file formats
