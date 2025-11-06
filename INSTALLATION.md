# 🎮 Installation Guide - Let's Get Started!

Welcome, future game developer! This guide will help you set up everything you need to create and share your Pygame projects online. Don't worry - we'll go step by step! 🚀

---

## 📋 What We're Installing

Before we start coding, we need some tools:
- **Python** - The programming language we'll use
- **pip** - A tool that downloads Python packages for us
- **virtualenv** - Creates a special folder for our project's tools
- **Streamlit** - Makes beautiful websites easily
- **Pygame** - Helps us create games!

---

## 🍎 For Mac Users (Using Terminal)

### Step 1: Install Homebrew (if you don't have it)
Homebrew is like an app store for programming tools!

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python 3
```bash
brew install python3
```

Check if it worked:
```bash
python3 --version
```
You should see something like "Python 3.11.x" or higher! ✅

### Step 3: Install pip (it comes with Python, but let's make sure)
```bash
python3 -m ensurepip --upgrade
```

### Step 4: Create a Virtual Environment
Think of this as a special "box" just for this project's tools!

```bash
# Navigate to your project folder
cd ~/Desktop/Python/streamlit-pygame-tutorial

# Create the virtual environment
python3 -m venv venv

# Turn it on! (You'll need to do this every time you work on the project)
source venv/bin/activate
```

When it's active, you'll see `(venv)` at the start of your terminal line! 🎉

### Step 5: Install All Python Packages
Now let's install all the tools we need:

```bash
pip install streamlit pygame pillow watchdog
```

Or use our requirements file:
```bash
pip install -r requirements.txt
```

---

## 🪟 For Windows Users

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation!

### Step 2: Open Command Prompt
Press `Windows Key + R`, type `cmd`, and press Enter

### Step 3: Create Virtual Environment
```bash
# Navigate to your project folder
cd Desktop\Python\streamlit-pygame-tutorial

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### Step 4: Install Packages
```bash
pip install streamlit pygame pillow watchdog
```

---

## 🧪 Test Your Installation

Let's make sure everything works! Run this in your terminal:

```bash
python3 -c "import streamlit, pygame; print('✅ All good! Ready to code!')"
```

If you see "✅ All good! Ready to code!" - you're ready! 🎉

---

## 🚀 Running Your App

Once everything is installed:

```bash
# Make sure you're in the project folder
cd ~/Desktop/Python/streamlit-pygame-tutorial

# Activate virtual environment (if not already active)
source venv/bin/activate  # Mac
# OR
venv\Scripts\activate     # Windows

# Run the app!
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501` and you'll see your game hosting website! 🎮

---

## 🆘 Troubleshooting

### "Command not found: python3"
- Try using `python` instead of `python3`
- Make sure Python is installed correctly

### "Permission denied"
- On Mac, you might need to add `sudo` before the command
- Example: `sudo brew install python3`

### "pip install not working"
- Make sure your virtual environment is activated (you should see `(venv)` in your terminal)
- Try `python3 -m pip install` instead of just `pip install`

### App won't start
- Make sure you're in the correct folder: `cd ~/Desktop/Python/streamlit-pygame-tutorial`
- Check that your virtual environment is active
- Try running: `streamlit --version` to verify Streamlit is installed

---

## 📚 Next Steps

Once installation is complete:
1. Read the `README.md` file to understand the project structure
2. Open `app.py` and read through the comments - it's like a tutorial!
3. Try running the example games
4. Create your own game and add it to the `/games` folder
5. Deploy your site to Streamlit Cloud (instructions in `DEPLOYMENT.md`)

Happy coding! 🎉👨‍💻👩‍💻
