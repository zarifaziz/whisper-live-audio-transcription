# Whisper Audio Live Transcription 

Welcome to the Whisper Audio Live Transcription tool. This application utilizes the power of the Whisper library to provide real-time transcription of audio captured from your microphone. It's designed to be easy to set up and use, whether you're a developer looking to integrate transcription capabilities into your projects or just someone interested in experimenting with speech recognition technology.

This tool not only writes the live transcription to a file at the path set in `settings.transcript_file` but also prints it to the terminal.

## Prerequisites

This application has been tested with Python 3.10.3. It is recommended to use 
the same Python version for compatibility purposes.

### System Dependencies

The following system dependencies are required: `portaudio`, `ffmpeg`, and `llvm`.

To install these on macOS:
```
brew install portaudio ffmpeg
arch -arm64 brew install llvm@14
echo 'export LLVM_CONFIG="/opt/homebrew/Cellar/llvm@14/14.0.6/bin/llvm-config"' >> ~/.zshrc
source ~/.zshrc
```

To install these on Ubuntu:
```
sudo apt-get install portaudio19-dev ffmpeg libllvm-14-llvm-config
```

To install these on Windows (using Chocolatey):
```
choco install portaudio ffmpeg llvm
```

### Python Dependencies

Dependencies can be installed using Poetry as follows:
```
poetry install --no-root
```

### Running the Application
Execute the following command to run the app:
```
python -m src.transcribe.main
```

### Code Linting and Formatting
To lint and format the codebase, use the following commands:
```
ruff format . && ruff check .
```

## Contributing

We welcome contributions from the community! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write your code and add tests if applicable.
4. Ensure your code adheres to the style guidelines by running the linting commands.
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

* Thanks to the open-source community for the continuous support and inspiration.
* Special thanks to the contributors of the `whisper` library for making audio transcription more accessible.
