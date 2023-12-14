# Whisper Audio Live transcription 

## Getting started

This app was tested on Python 3.10.3 so using the same version is recommended.

### Installing external dependencies
`portaudio`, `ffmpeg`, and `llvm` are needed.

Installing them on Mac
```
brew install portaudio ffmpeg

arch -arm64 brew install llvm@14
export LLVM_CONFIG="/opt/homebrew/Cellar/llvm@14/14.0.6/bin/llvm-config" 
```

### Installing python dependencies

Using poetry
```
poetry install --no-root
```

Using pip
```
poetry export -f requirements.txt --output requirements.txt --without-hashes

pip install -r requirements.txt
```

### Run the app
```
python main.py
```

### Linting and formatting
```
ruff format . && ruff check .
```
