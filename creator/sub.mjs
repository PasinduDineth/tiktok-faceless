import { execSync } from "node:child_process";
import {
  existsSync,
  rmSync,
  writeFileSync,
  lstatSync,
  mkdirSync,
  readdirSync,
} from "node:fs";
import path from "path";
import {
  WHISPER_LANG,
  WHISPER_MODEL,
  WHISPER_PATH,
  WHISPER_VERSION,
} from "./whisper-config.mjs";
import {
  downloadWhisperModel,
  installWhisperCpp,
  transcribe,
  toCaptions,
} from "@remotion/install-whisper-cpp";

const extractToTempAudioFile = (fileToTranscribe, tempOutFile) => {
  // Converting audio file to 16khz wav file for Whisper
  try {
    // Try with regular ffmpeg first
    execSync(
      `ffmpeg -i "${fileToTranscribe}" -ar 16000 -ac 1 -c:a pcm_s16le "${tempOutFile}" -y`,
      { stdio: ["ignore", "inherit"] },
    );
  } catch (error) {
    console.log("Regular ffmpeg not found, trying remotion ffmpeg...");
    execSync(
      `npx remotion ffmpeg -i "${fileToTranscribe}" -ar 16000 -ac 1 -c:a pcm_s16le "${tempOutFile}" -y`,
      { stdio: ["ignore", "inherit"] },
    );
  }
};

const subFile = async (filePath, fileName, folder) => {
  const outPath = path.join(
    process.cwd(),
    "public",
    folder,
    fileName.replace(/\.(wav|mp3|m4a|flac|ogg)$/, ".json"),
  );

  const whisperCppOutput = await transcribe({
    inputPath: filePath,
    model: WHISPER_MODEL,
    tokenLevelTimestamps: true,
    whisperPath: WHISPER_PATH,
    whisperCppVersion: WHISPER_VERSION,
    printOutput: false,
    translateToEnglish: false,
    language: WHISPER_LANG,
    splitOnWord: true,
  });

  const { captions } = toCaptions({
    whisperCppOutput,
  });
  writeFileSync(
    outPath,
    JSON.stringify(captions, null, 2),
  );
};

const processAudio = async (fullPath, entry, directory) => {
  // Support common audio formats
  if (
    !fullPath.endsWith(".wav") &&
    !fullPath.endsWith(".mp3") &&
    !fullPath.endsWith(".m4a") &&
    !fullPath.endsWith(".flac") &&
    !fullPath.endsWith(".ogg")
  ) {
    return;
  }

  const isTranscribed = existsSync(
    fullPath
      .replace(/\.wav$/, ".json")
      .replace(/\.mp3$/, ".json")
      .replace(/\.m4a$/, ".json")
      .replace(/\.flac$/, ".json")
      .replace(/\.ogg$/, ".json")
  );
  if (isTranscribed) {
    console.log(`Skipping ${entry} - already transcribed`);
    return;
  }
  let shouldRemoveTempDirectory = false;
  if (!existsSync(path.join(process.cwd(), "temp"))) {
    mkdirSync(`temp`);
    shouldRemoveTempDirectory = true;
  }
  console.log("Processing audio file", entry);

  // Always convert audio to 16kHz WAV format for Whisper compatibility
  const tempWavFileName = entry.split(".")[0] + "_16khz.wav";
  const tempOutFilePath = path.join(process.cwd(), `temp/${tempWavFileName}`);
  
  console.log("Converting audio to 16kHz WAV format...");
  extractToTempAudioFile(fullPath, tempOutFilePath);

  await subFile(
    tempOutFilePath,
    entry,
    path.relative("public", directory),
  );
  if (shouldRemoveTempDirectory) {
    rmSync(path.join(process.cwd(), "temp"), { recursive: true });
  }
};

const processDirectory = async (directory) => {
  const entries = readdirSync(directory).filter((f) => f !== ".DS_Store");

  for (const entry of entries) {
    const fullPath = path.join(directory, entry);
    const stat = lstatSync(fullPath);

    if (stat.isDirectory()) {
      await processDirectory(fullPath); // Recurse into subdirectories
    } else {
      await processAudio(fullPath, entry, directory);
    }
  }
};

await installWhisperCpp({ to: WHISPER_PATH, version: WHISPER_VERSION });
await downloadWhisperModel({ folder: WHISPER_PATH, model: WHISPER_MODEL });

// Read arguments for filename if given else process all files in the directory
const hasArgs = process.argv.length > 2;

if (!hasArgs) {
  await processDirectory(path.join(process.cwd(), "public"));
  process.exit(0);
}

for (const arg of process.argv.slice(2)) {
  const fullPath = path.join(process.cwd(), arg);
  const stat = lstatSync(fullPath);

  if (stat.isDirectory()) {
    await processDirectory(fullPath);
    continue;
  }

  console.log(`Processing file ${fullPath}`);
  const directory = path.dirname(fullPath);
  const fileName = path.basename(fullPath);
  await processAudio(fullPath, fileName, directory);
}
