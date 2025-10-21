import path from "node:path";

// Where to install Whisper.cpp to
export const WHISPER_PATH = path.join(process.cwd(), "whisper.cpp");

// The version of Whisper.cpp to install
export const WHISPER_VERSION = "1.6.0";

// Which model to use.
// | Model            | Disk   | Mem      |
// |------------------|--------|----------|
// | tiny             | 75 MB  | ~390 MB  |
// | tiny.en          | 75 MB  | ~390 MB  |
// | base             | 142 MB | ~500 MB  |
// | base.en          | 142 MB | ~500 MB  |
// | small            | 466 MB | ~1.0 GB  |
// | small.en         | 466 MB | ~1.0 GB  |
// | medium           | 1.5 GB | ~2.6 GB  |
// | medium.en        | 1.5 GB | ~2.6 GB  |
// | large-v1         | 2.9 GB | ~4.7 GB  |
// | large-v2         | 2.9 GB | ~4.7 GB  |
// | large-v3         | 2.9 GB | ~4.7 GB  |
// | large-v3-turbo   | 1.5 GB | ~4.7 GB  | // Only supported from Whisper.cpp 1.7.2 and higher
// | large            | 2.9 GB | ~4.7 GB  |

/**
 * @type {import('@remotion/install-whisper-cpp').WhisperModel}
 */
export const WHISPER_MODEL = "base"; // Multilingual model (use "base.en" for English-only, faster)

// Language to transcribe
// Set to "auto" for automatic language detection, or specify a language code
// IMPORTANT: If you use a language other than English, use a multilingual model (remove .en from model name)
// Common language codes:
// en = English, es = Spanish, fr = French, de = German, it = Italian, pt = Portuguese
// nl = Dutch, pl = Polish, ru = Russian, ja = Japanese, ko = Korean, zh = Chinese
// ar = Arabic, hi = Hindi, tr = Turkish, sv = Swedish, da = Danish, no = Norwegian
// fi = Finnish, uk = Ukrainian, cs = Czech, ro = Romanian, el = Greek, th = Thai
// vi = Vietnamese, id = Indonesian, he = Hebrew, fa = Persian
// Full list: https://github.com/openai/whisper/blob/main/whisper/tokenizer.py
/**
 * @type {import('@remotion/install-whisper-cpp').Language | "auto"}
 */
export const WHISPER_LANG = "auto"; // Auto-detect language (or set specific code like "en", "es", etc.)