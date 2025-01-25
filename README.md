# HashBuster

HashBuster is an advanced password cracking tool designed for security professionals, penetration testers, and ethical hackers. It provides a powerful and flexible solution for cracking hashed passwords using dictionary and brute force attacks. With support for multiple hash algorithms and parallel processing, HashBuster is built to handle real-world password recovery scenarios efficiently.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

HashBuster is a command-line tool that helps security professionals recover lost or forgotten passwords by cracking their hashed representations. It supports popular hash algorithms like MD5, SHA1, SHA256, SHA512, and bcrypt. Whether you're performing a security audit, testing password strength, or recovering a lost password, HashBuster provides a robust and efficient solution.

---

## Features

- **Multi-Algorithm Support**: Crack hashes using MD5, SHA1, SHA256, SHA512, and bcrypt.
- **Dictionary Attack**: Use a wordlist to crack passwords with optional mutations (leet speak, case variations, and numeric suffixes).
- **Brute Force Attack**: Generate password candidates from a customizable character set.
- **Parallel Processing**: Leverage multiple CPU cores for faster cracking.
- **Bcrypt Support**: Optimized for cracking bcrypt hashes with dictionary attacks.
- **Customizable**: Adjust parameters like password length, character set, and number of processes.
- **Validation**: Automatically validates hash formats before cracking.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- `pip` for package management

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/tanm-sys/HashBuster.git
   cd HashBuster
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install `bcrypt` for bcrypt hash support:
   ```bash
   pip install bcrypt
   ```

4. Run HashBuster:
   ```bash
   python hashbuster.py
   ```

---

## Usage

### Basic Commands

1. **Dictionary Attack**:
   ```bash
   python hashbuster.py <hash> <hash_type> dict -w wordlist.txt -m -p 8
   ```
   - `<hash>`: The target hash to crack.
   - `<hash_type>`: The hash algorithm (e.g., md5, sha256, bcrypt).
   - `-w`: Path to the wordlist file.
   - `-m`: Enable mutations (leet speak, case variations, etc.).
   - `-p`: Number of parallel processes.

2. **Brute Force Attack**:
   ```bash
   python hashbuster.py <hash> <hash_type> brute -l 6 -c "abcdef123" -p 4
   ```
   - `-l`: Maximum password length.
   - `-c`: Custom character set.
   - `-p`: Number of parallel processes.

### Examples

- Crack an MD5 hash using a dictionary attack:
  ```bash
  python hashbuster.py 5f4dcc3b5aa765d61d8327deb882cf99 md5 dict -w wordlist.txt
  ```

- Crack a bcrypt hash with mutations:
  ```bash
  python hashbuster.py $2a$12$3e8Z7r1K9f4tY7hB6v8XeO bcrypt dict -w wordlist.txt -m
  ```

- Crack a SHA256 hash using brute force:
  ```bash
  python hashbuster.py e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 sha256 brute -l 5
  ```

---

## Contributing

We welcome contributions from the community! If you'd like to contribute to HashBuster, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request and describe your changes.

Please ensure your code follows the project's style guidelines and includes appropriate tests.

---

## License

HashBuster is released under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments

- Inspired by the need for efficient and ethical password recovery tools.
- Built with ❤️ by [tanm-sys](https://github.com/tanm-sys).

---

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/tanm-sys/HashBuster/issues).

---

**Disclaimer**: HashBuster is intended for legal and ethical use only. Always ensure you have proper authorization before using this tool on any system. The developers are not responsible for any misuse or damage caused by this software.
