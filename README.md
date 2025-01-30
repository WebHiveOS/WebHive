<img src="./assets/webhive-logo-new.png" alt="Web Hive" width="full"/>

<br/>

<a href="https://twitter.com/WebHiveOS" target="_blank">
  <img src="https://img.shields.io/twitter/follow/WebHiveOS?style=social" alt="Follow @WebHiveOS on Twitter" />
</a> <br><br>




**Web Hive:** Designed with an intuitive interface leveraging state-of-the-art frameworks, this platform simplifies interactions with AI agents, delivering a smooth and efficient user experience.

**Comprehensive LLM Integration:** Our platform supports a variety of leading-edge Large Language Models (LLMs), such as Gemini, OpenAI, Azure AI, Anthropic, DeepSeek, and Ollama, with plans to continuously expand and include additional models in the future.

**Seamless Browser Connectivity:** Integrate your preferred browser effortlessly, eliminating repetitive login hurdles and simplifying authentication processes. High-quality screen recording is also included for enhanced functionality.

**Uninterrupted Sessions:** Keep your browser environment active between tasks, enabling seamless access to your interaction history and maintaining the operational context of AI activities.

## Setup Options

### Method 1: Install Locally

Refer to the [Quickstart Guide](https://docs.browser-use.com/quickstart#prepare-the-environment) or proceed with the steps outlined below to begin.

> Requires Python 3.11 or later.

To begin, we suggest using [uv](https://docs.astral.sh/uv/) to set up the Python environment.

```bash
uv venv --python 3.11
```

and activate it using:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
uv pip install -r requirements.txt
```

Next, install Playwright:

```bash
playwright install
```

### Method 2: Docker Setup

1. **Requirements:**
   - Ensure Docker and Docker Compose are installed on your system
   - Git is needed to clone the repository

2. **Setup:**
   ```bash
   # Clone the repository
   git clone https://github.com/browser-use/web-ui.git
   cd web-ui

   # Copy and configure environment variables
   cp .env.example .env
   # Edit .env with your preferred text editor and add your API keys
   ```

3. **Launch Using Docker:**
   ```bash
   # Build and start the container with default settings (browser closes after AI tasks)
   docker compose up --build

   # Or run with persistent browser (browser stays open between AI tasks)
   CHROME_PERSISTENT_SESSION=true docker compose up --build
   ```

4. **Open the Application:**
   - Web Hive: `http://localhost:7788`
   - Use VNC Viewer (to observe browser interactions): `http://localhost:6080/vnc.html`
   
  The default VNC password is set to "vncpassword." You can modify it by updating the `VNC_PASSWORD` environment variable in your `.env` file.


## Usage

### Local Setup
1. Copy the `.env.example` file to `.env` and configure your environment variables, such as API keys for the LLM:  
   `cp .env.example .env`  
2. **Start the Application:**  
    ```bash
    python webhive.py --ip 127.0.0.1 --port 7788
    ```
4. Web Hive options:
- `--ip`: Specifies the IP address Web Hive binds to. Default: `127.0.0.1`.  
- `--port`: Specifies the port Web Hive binds to. Default: `7788`.  
- `--theme`: Defines the user interface theme. Default: `Ocean`.  
  - **Default**: A balanced, standard design.  
  - **Soft**: Muted colors for a relaxed aesthetic.  
  - **Monochrome**: Grayscale for simplicity and focus.  
  - **Glass**: A modern, semi-transparent look.  
  - **Origin**: A retro-inspired, classic appearance.  
  - **Citrus**: Bright and fresh colors with a vibrant feel.  
  - **Ocean** (default): A calming, blue ocean-inspired design.  
- `--dark-mode`: Activates dark mode for the interface.  
3.  **Access Web Hive:** Launch your web browser and go to `http://127.0.0.1:7788`.
4. **Using Your Own Browser (Optional):**  
   - Configure the following environment variables:  
     - `CHROME_PATH`: Set this to the path of your browser's executable.  
     - `CHROME_USER_DATA`: Set this to your browser's user data directory.  

     - Windows 
        ```env
         CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
         CHROME_USER_DATA="C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"
        ```
        > Note: On Windows systems, replace `YourUsername` with your actual Windows username in the paths.
      - Mac
        ```env
         CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
         CHROME_USER_DATA="~/Library/Application Support/Google/Chrome/Profile 1"
        ```
    - Close all Chrome windows.  
    - Open Web Hive in a non-chrome browser, such as Firefox or Edge. This step is crucial as the persistent browser context will utilize Chrome's data when running the agent.  
    - In the Browser Settings, enable the "Use Own Browser" option.  
5. **Keep Browser Open (Optional):**  
   - Add `CHROME_PERSISTENT_SESSION=true` to your `.env` file.  

### Docker Setup  
1. **Environment Variables:**  
   - All configurations are managed via the `.env` file.  
   - Key environment variables include:  
     ```
     # LLM API Keys
     OPENAI_API_KEY=your_api_key_here
     ANTHROPIC_API_KEY=your_api_key_here
     GOOGLE_API_KEY=your_api_key_here

     # Browser Settings
     CHROME_PERSISTENT_SESSION=true   # Enable to keep the browser open between AI tasks
     RESOLUTION=1920x1080x24         # Specify resolution in the format: WIDTHxHEIGHTxDEPTH
     RESOLUTION_WIDTH=1920           # Set the screen width in pixels
     RESOLUTION_HEIGHT=1080           # Set the screen height in pixels

     # VNC Settings
     VNC_PASSWORD=your_vnc_password  # Optional, defaults to "vncpassword"
     ```

2. **Browser Persistence Modes:**  
   - **Default Mode (`CHROME_PERSISTENT_SESSION=false`):**  
     - The browser starts and shuts down with each AI task.  
     - Ensures a clean slate for every interaction.  
     - Optimized for lower resource consumption.  

  - **Persistent Mode (`CHROME_PERSISTENT_SESSION=true`):**  
  - Keeps the browser open between AI tasks.  
  - Retains history and session state.  
  - Enables viewing of previous AI interactions.  
  - Can be configured in the `.env` file or set as an environment variable when starting the container.  

3. **Viewing Browser Interactions:**  
   - Open the noVNC viewer by navigating to `http://localhost:6080/vnc.html`.  
   - Enter the VNC password (default: "vncpassword" or the value set in the `VNC_PASSWORD` environment variable).  
   - You can now observe all browser interactions in real time.  

4. **Managing the Container:**  
   ```bash
   # Launch with persistent browser session
   CHROME_PERSISTENT_SESSION=true docker compose up -d  

   # Launch in default mode (browser resets after each task)
   docker compose up -d  

   # Monitor real-time logs
   docker compose logs -f  

   # Shut down and remove the container
   docker compose down  
  
   ```

## Changelog
- [x] **2025/01/26:** Thanks to @vvincent1234. Now Web Hive can combine with DeepSeek-r1 for enhanced AI capabilities!
