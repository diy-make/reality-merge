# Reality Merge: Hackathon Game Plan

This document outlines a 12-hour game plan for a 4-person team to build the "Reality Merge" proof-of-concept.

**Team Roles:**
-   **Person A (Unity/MR Lead):** Focuses on the core Unity scene, MRUK, and Spatial Anchors.
-   **Person B (Networking Lead):** Focuses on Photon Fusion setup and networking logic.
-   **Person C (Content & Interaction):** Focuses on loading the 3D models with glTFast and implementing grab interactions.
-   **Person D (Backend & AI Services):** Focuses on the supporting backend, including the "Shades" AI concept and the web server to host models.

---

### **Evening 1 (8 PM - 12 AM: 4 Hours)**

**Objective:** Establish the shared space and get a primitive object synced between two users.

-   **All (30 mins):**
    -   Project setup: All team members clone the repo, open the Unity project, and ensure it builds to the headset.
    -   Review architecture doc (`This_is_the_System_Architecture_&_Data_Flow_.md`).

-   **Person A (Unity/MR Lead) (3.5 hours):**
    -   **Task:** Implement **Phase 1: The Anchor (Part 1)**.
    -   Integrate the MR Utility Kit (MRUK) into the main scene.
    -   Write the script to detect the best table surface (`GetCurrentRoom().GetBestKeyWallOrTable()`).
    -   Create a simple visualization (e.g., a cube) to show where the anchor point is being created locally.
    -   Write the code to create an `OVRSpatialAnchor` at that point.

-   **Person B (Networking Lead) (3.5 hours):**
    -   **Task:** Set up Photon Fusion.
    -   Create a Photon App ID on the Photon dashboard.
    -   Install the Fusion SDK into the Unity project.
    -   Create a basic "Network Runner" prefab.
    -   Implement a simple "connect/disconnect" UI and logic so two players can join the same session.

-   **Person C (Content & Interaction) (3.5 hours):**
    -   **Task:** Prepare content and basic interaction.
    -   Find or create a few simple `.glb` 3D models (e.g., cube, sphere, engine).
    -   Install `glTFast` into the project.
    -   Create a simple test script that can load a `.glb` from a local file path and display it.

-   **Person D (Backend & AI) (3.5 hours):**
    -   **Task:** Set up the supportive stack.
    -   Familiarize with the Python CLI we've built (`reality_merge.py`).
    -   Set up a simple Python Flask or FastAPI web server.
    -   Create an endpoint that can serve the `.glb` models Person C has prepared.
    -   Begin prototyping the "Shades" AI logic: write a Python script that can take two strings and use the Gemini API to generate a "merged" concept.

---

### **Day 2 (9 AM - 5 PM: 8 Hours)**

**Objective:** Complete all three phases and have a demonstrable proof-of-concept.

-   **All (15 mins):**
    -   Morning stand-up: Review evening progress and confirm today's plan.

-   **Person A & B (Unity/MR + Networking) (4 hours):**
    -   **Task:** Implement **Phase 1: The Anchor (Part 2)** and the `AnchorNetworkBridge`.
    -   **Person B:** Write the RPC to share the anchor's UUID (`RPC_ShareAnchorID`).
    -   **Person A:** Write the logic to receive the UUID and load the anchor (`LoadUnboundAnchors`).
    -   **Together:** Implement the `AnchorNetworkBridge.cs` script to connect the loaded `OVRSpatialAnchor` to a new `NetworkObject` (the `CAD_Container`). This is the most critical integration step.
    -   **Test:** The goal is to have an empty `CAD_Container` GameObject appear in the exact same real-world location for both users.

-   **Person C & D (Content + Backend) (4 hours):**
    -   **Task:** Implement **Phase 2: The Content**.
    -   **Person D:** Finalize the web server. Ensure all `.glb` models are hosted and have stable URLs.
    -   **Person C:**
        -   Create the `CAD_Container` prefab with a `Networked` string property for the model URL.
        -   Write the `OnUrlChanged` callback function.
        -   Integrate the `glTFast` logic to download and instantiate the model from the synced URL.
        -   Create a simple UI (e.g., a floating button) that, when pressed, sets the `ModelUrl` property on the `CAD_Container`.
    -   **Test:** The goal is to have User A press a button, and the corresponding 3D model appears on the table for both User A and User B.

-   **All (1 hour):**
    -   Lunch break & progress check.

-   **Person A, B, C (3 hours):**
    -   **Task:** Implement **Phase 3: The Interaction**.
    -   **Person C:** Add the `Grabbable` component from the Meta Interaction SDK to the loaded models.
    -   **Person B:** Add the `NetworkTransform` component to the `CAD_Container` prefab.
    -   **Person A:** Write the code that calls `RequestStateAuthority()` when a user grabs the object.
    -   **Test:** The goal is for one user to be able to grab, move, and rotate the model, and have the other user see the movements in real-time.

-   **Person D (3 hours):**
    -   **Task:** Refine and document the AI backend.
    -   Create a simple web UI for the "Shades" prototype.
    -   Prepare a short video or a series of screenshots demonstrating the AI's capability to "merge" concepts. This will be part of the final submission video.

-   **All (Final Hour):**
    -   Final integration testing.
    -   Record the final demo video, showing the full workflow.
    -   Prepare the Devpost submission page.
