# reality-merge

## Project Goal: The Peace Arch Portal System (PAPS)

This repository is a "SensAI hack" of the idea space outlined in the [Portal Panel Proposal](https://github.com/diy-make/portal/blob/main/event/2025/oct/portal_panel_proposal.md).

Our goal is to develop the **Peace Arch Portal System (PAPS)**, a network to connect physical makerspaces, starting with the founding nodes at:
- [Founder Haus](https://founderhaus.club/)
- [DUNA Residences](https://www.dunaresidences.com/about) (Roatán)
- [Frontier Tower](https://frontiertower.io/) (San Francisco)

### DUNA Makerspace & The YesTheory Feature

The DUNA makerspace has gained significant attention, highlighted in a [YesTheory video](https://youtu.be/pdmVDO0a8dc?si=CVHNPpoDpFWw9GBB&t=904) that has amassed nearly 3 million views. The most popular segment of the video features a tour of the makerspace, showcasing its potential as a hub for innovation and creation.

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

## Google Drive Integration

This project can be configured to interact with a Google Drive folder to manage assets.

### Setup

To use this feature, you will need to enable the Google Drive API and get OAuth 2.0 credentials for your Google account.

1.  **Enable the Google Drive API:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project or select an existing one.
    *   In the API Library, search for "Google Drive API" and enable it.

2.  **Create OAuth 2.0 Credentials:**
    *   In the "Credentials" section of the APIs & Services dashboard, click "Create Credentials" and select "OAuth client ID".
    *   Choose "Desktop app" as the application type.
    *   Download the JSON file and save it as `client_secret.json` in the root of this project.

### Usage

Once the setup is complete, you can use the following commands:

*   `reality-merge drive list`: List the files in the configured Google Drive folder.
*   `reality-merge drive download <file_name>`: Download a file from the folder.

*(Note: These commands are not yet implemented.)*



