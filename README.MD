
# Voice Command Automation with Python

This repository contains a Python script that allows you to automate various tasks using voice commands. The script uses speech recognition to convert spoken commands into actions, enabling you to control your computer hands-free.

## Features

- Recognizes a customizable command prefix to trigger actions.
- Supports a variety of commands for tasks like opening websites, getting the current date and time, searching on Google, and more.
- Provides options to adjust audio chunk size and sample rate for optimal speech recognition.
- Easily customizable with the included `config.json` file.

## Getting Started

1. Clone this repository to your local machine.
2. Make sure you have Python installed.
3. Install the required Python packages using the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. Open the `config.json` file to customize your preferences, including the command prefix, language, audio chunk size, and sample rate.

## Usage

1. Run the script using the following command:

   ```bash
   python voice_command_automation.py
   ```

2. The script will prompt you to choose a microphone. Follow the instructions to select the desired microphone for speech input.
3. Start speaking commands after the listening prompt. Prefix your commands with the configured command prefix (default: 'tyas').

## Configuration

Edit the `config.json` file to configure the following settings:

- `language`: The language for speech recognition (e.g., 'en-US', 'en-GB', 'en-AU').
- `chunk_size`: Duration of each audio chunk in milliseconds (recommended: 4000 for optimal recognition).
- `rate`: Audio sample rate (recommended: 26000 for improved recognition).
- `prefix`: Command prefix for triggering voice commands.

## Examples

- Say 'tyas pause' to pause the program.
- Say 'tyas google AI technologies' to search for 'AI technologies' on Google.

## Contributing

Contributions are welcome! If you have suggestions, improvements, or additional features to add, feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License.

---

**Note:** Please be mindful of ethical considerations and respectful language while customizing commands.

**Disclaimer:** The provided content does not endorse or promote any offensive or inappropriate content. Please use the script responsibly and considerately.
```
