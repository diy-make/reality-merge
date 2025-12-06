# reality-merge

## Project: Reality Merge

**Reality Merge** is a "SensAI hack" inspired by the **Peace Arch Portal System (PAPS)** idea space, which is outlined in the [Portal Panel Proposal](https://github.com/diy-make/portal/blob/main/event/2025/oct/portal_panel_proposal.md).

### What is Reality Merge?

**Reality Merge** is the core AI-powered engine of this project. It leverages Large Language Models, specifically Google's Gemini family, to create a "merged reality" from diverse sources of information.

The central concept is the merging of "Shades"—distinct pieces of information, ideas, or project contexts. The system is designed to:
- **Analyze and Understand:** Programmatically fetch and parse information from sources like GitHub README files to understand the "shade" of a given project.
- **Synthesize and Merge:** Use AI to find similarities and create new, synthesized concepts from multiple "shades".
- **Bridge Worlds:** The ultimate goal is to apply this "merged reality" to bridge the gap between different communities and environments, from digital "sim" environments to real-world makerspaces, as envisioned in the Peace Arch Portal System (PAPS) concept.

This AI-driven synthesis is the "SensAI hack" that will power the connection between the makerspaces.

![The Reality Merge Concept](png/reality-merge-project-concept.png)

Our goal is to develop a system to connect physical makerspaces, starting with a proof-of-concept and then expanding to a wider network.

### Proof-of-Concept: Frontier Tower

The initial proof-of-concept will be implemented at [Frontier Tower](https://frontiertower.io/) in San Francisco, connecting the 7th-floor makerspace with the 12th floor.

### Stretch Goals

Once the PoC is successful, our stretch goals are to connect with other makerspaces, including:
- [DUNA Residences](https://www.dunaresidences.com/about) (Honduras)
- A makerspace in Brazil.
- [Founder Haus](https://founderhaus.club/)

### DUNA Makerspace & The YesTheory Feature

The DUNA makerspace, a key inspiration for this project, has gained significant attention from a [YesTheory video](https://youtu.be/pdmVDO0a8dc?si=CVHNPpoDpFWw9GBB&t=904) with nearly 3 million views. The video's tour of the makerspace highlights its potential as a hub for innovation.

![YesTheory DUNA Makerspace Tour 1](png/yes-theory-duna-makerspace-tour-1.png)
*A glimpse into the DUNA makerspace from the YesTheory video.*

![YesTheory DUNA Makerspace Tour 2](png/yes-theory-duna-makerspace-tour-2.png)
*Another view of the popular makerspace tour.*

This is the Notion: https://sensaihack.notion.site/SensAI-Hack-in-San-Francisco-27dd7964cb7c80eebd4af085a55b7832

The Devpost link is here: https://devpost.com/software/reality-merge

## Discord Links

- **Group Outside Channel:** https://discord.gg/pJJtrpJ3Q
- **Channel:** https://discord.gg/p4RXZ3S8
- **Group Inside Channel:** https://discord.com/channels/1239895395715256330/1446608810809626816

## Our Stack

Our stack includes our Make.DIY dotfiles configuration of a https://github.com/google-gemini/gemini-cli environment.

![Gemini CLI Stack](png/gemini-cli-stack.png)

### Workflow Example

![Gemini CLI Workflow Example](png/gemini-cli-workflow-example.png)

## Hackathon Information

This project was created for the SensAI Hack in San Francisco, which took place from December 5-7, 2025.

### Submission Guidelines

- **Platform:** Devpost
- **Project Naming:** Must be prefixed with a room number and location code (e.g., "207-SF11 HackFace").
- **Deliverables:** APK and demo video.

### Judging Criteria

Projects are judged on a 20-point scale across four categories:

1.  **VR Idea & Gameplay (5 pts):** Must be innovative, fun, and engaging.
2.  **Standalone App Potential (5 pts):** Should have the potential to attract, engage, and retain users on the Meta Quest platform. Existing projects can be submitted if they have significant upgrades.
3.  **Execution & Polish (5 pts):** The app should be well-executed with a polished user experience and perform reliably on Meta Quest.
4.  **Category Specific Capabilities (5 pts):** Based on criteria detailed in a separate presentation.

## Development Setup

Before running the application, you need to set up the Python virtual environment and install the required dependencies.

1.  **Run the setup script:**
    ```bash
    sh sh/setup_env.sh
    ```
    This will create a `.venv` directory and install the packages listed in `requirements.txt`.

2.  **Activate the virtual environment:**
    To activate the environment for your current shell session, run:
    ```bash
    source .venv/bin/activate
    ```

## Google Drive Integration

Setting up OAuth 2.0 is a powerful one-time step. It allows this command-line tool to securely access your Google Drive files on your behalf. This unlocks the ability to automate tasks like listing files, downloading assets, and potentially uploading new content directly from your terminal, bridging the gap between your cloud storage and your local development workflow.

This project can be configured to interact with a Google Drive folder to manage assets.

### Setup

To use this feature, you will need to enable the Google Drive API and get your `client_secret.json` file.

1.  **Enable the Google Drive API:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project or select an existing one.
    *   In the API Library, search for "Google Drive API" and enable it.

2.  **Download `client_secret.json`:**
    *   In the "Credentials" section of the APIs & Services dashboard, click "Create Credentials" and select "OAuth client ID".
    *   Choose "Desktop app" as the application type.
    *   Download the JSON file and save it as `client_secret.json` in the root of this project.

3.  **Run the Authentication Script:**
    *   Execute the following command in your terminal:
        ```bash
        sh sh/authenticate_gdrive.sh
        ```
    *   This will open a browser window for you to authorize access to your Google Drive. After you approve, a `token.json` file will be created.

### Usage

Once the setup is complete, you can use the following commands:

*   `reality-merge drive list`: List the files in the configured Google Drive folder.
*   `reality-merge drive download <file_name>`: Download a file from the folder.

*(Note: These commands are not yet implemented.)*

### Setup in Action

1.  **OAuth Consent Screen:** The authentication script will prompt you to authorize the application in your browser.
    ![OAuth Consent Screen](png/gdrive-oauth-consent-screen.png)

2.  **Authentication Script Execution:** The script will provide a URL and confirm success in the terminal.
    ![Authentication Script Execution](png/gdrive-auth-script-execution.png)

3.  **CLI Command Test:** A successful test of the `drive list` command confirms the integration is working.
    ![CLI List Command Test](png/gdrive-cli-list-command-test.png)



