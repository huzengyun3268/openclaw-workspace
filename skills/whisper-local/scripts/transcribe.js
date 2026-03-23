#!/usr/bin/env node
/**
 * Local Whisper transcription script
 * Usage: node transcribe.js <audio_file> [language]
 * Output: JSON { text: "...", language: "...", duration: ... }
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PYTHON = '"C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"';
const MODEL_DIR = 'C:/tools/whisper_models';
const OUTPUT_DIR = 'C:/tools/whisper_output';

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function transcribe(audioFile, language = 'zh') {
  ensureDir(OUTPUT_DIR);
  
  // Build the Python command
  const outputName = 'transcript_' + Date.now();
  const outputPath = path.join(OUTPUT_DIR, outputName);
  
  const args = [
    PYTHON,
    '-X', 'utf8',
    '-m', 'whisper',
    path.resolve(audioFile),
    '--model_dir', MODEL_DIR,
    '--model', 'base',
    '--language', language,
    '--output_dir', OUTPUT_DIR,
    '--output_format', 'json',
    '--task', 'transcribe',
    '--device', 'cpu'
  ];
  
  try {
    const result = execSync(args.join(' '), {
      encoding: 'utf8',
      timeout: 300000,
      maxBuffer: 50 * 1024 * 1024
    });
    
    // Read the output JSON
    const jsonPath = path.join(OUTPUT_DIR, outputName + '.json');
    if (fs.existsSync(jsonPath)) {
      const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      // Clean up
      try { fs.unlinkSync(jsonPath); } catch(e) {}
      try { fs.unlinkSync(path.join(OUTPUT_DIR, outputName + '.txt')); } catch(e) {}
      try { fs.unlinkSync(path.join(OUTPUT_DIR, outputName + '.vtt')); } catch(e) {}
      try { fs.unlinkSync(path.join(OUTPUT_DIR, outputName + '.srt')); } catch(e) {}
      try { fs.unlinkSync(path.join(OUTPUT_DIR, outputName + '.tsv')); } catch(e) {}
      return {
        text: data.text || '',
        language: data.language || language,
        duration: data.duration || 0
      };
    }
    
    // Fallback: try to parse from the output
    return { text: result.trim(), language, duration: 0 };
  } catch (err) {
    throw new Error('Transcription failed: ' + err.message);
  }
}

// CLI entry point
if (require.main === module) {
  const audioFile = process.argv[2];
  const language = process.argv[3] || 'zh';
  
  if (!audioFile) {
    console.error('Usage: node transcribe.js <audio_file> [language]');
    process.exit(1);
  }
  
  if (!fs.existsSync(audioFile)) {
    console.error('Error: Audio file not found: ' + audioFile);
    process.exit(1);
  }
  
  try {
    const result = transcribe(audioFile, language);
    console.log(JSON.stringify(result));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { transcribe };
