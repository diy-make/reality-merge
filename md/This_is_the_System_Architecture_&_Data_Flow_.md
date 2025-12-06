# This is the System Architecture & Data Flow 

This is the **System Architecture & Data Flow** for your project.

You are effectively building a **"relay race"** where data is handed off from one SDK to the next. If you break this chain, the app crashes.

Here is exactly how the 4 components (MRUK, Shared Anchors, Photon, glTFast) mesh together technically.

### **The "Life of a Packet" (Step-by-Step Architecture)**

**Phase 1: The Stage (Establishing the Shared Coordinate System)**

*Goal: Everyone agrees that "0,0,0" is the center of the physical table.*

* **Detection (Local):**
* **User A** looks at a table.
* **MR Utility Kit (MRUK)** fires MRUK.Instance.GetCurrentRoom().GetBestKeyWallOrTable().
* *Result:* User A gets a local Vector3 (e.g., 2.5, 0.8, 1.0) representing the table center.
* **Anchoring (Local -> Cloud):**
* **User A's Code** instantiates an empty GameObject ("AnchorPoint") at that Vector3.
* **Meta SDK** creates an OVRSpatialAnchor on it.
* **User A** calls SaveAnchorAsync() then ShareAnchorAsync().
* *Result:* Meta's Cloud stores this anchor and returns a **UUID** (e.g., 88a-22b-33c).
* **Synchronization (Cloud -> Network):**
* **Photon Fusion** takes that UUID.
* **User A** sends an RPC: RPC_ShareAnchorID("88a-22b-33c").
* **User B** receives the UUID.
* **Alignment (Network -> Local):**
* **User B's Code** calls OVRSpatialAnchor.LoadUnboundAnchors("88a-22b-33c").
* **Meta SDK** recognizes the room features and "snaps" that UUID to **User B's physical table**.
* *Result:* Both users now have an invisible "AnchorPoint" GameObject that is perfectly aligned in the real world.

### **Phase 2: The Object (Spawning the Content)**

*Goal: User A selects a file, and it appears for User B.*

* **Selection (UI):**
* **User A** touches the "Load Engine" button.
* **Code** maps "Engine" to a URL: https://myserver.com/engine.glb.
* **State Change (Network):**
* **Photon Fusion** has a NetworkObject called CAD_Container sitting as a child of the "AnchorPoint".
* This object has a property: [Networked(OnChanged = nameof(OnUrlChanged))] string ModelUrl.
* **User A** sets ModelUrl = "https://myserver.com/engine.glb".
* **Reaction (Network -> Local):**
* **Photon** syncs this string to User B immediately.
* **User B's** OnUrlChanged function fires automatically.
* **Loading (Local):**
* **glTFast** (on both headsets) reads the URL.
* It downloads the .glb file.
* It instantiates the mesh as a child of CAD_Container.
* *Result:* Because CAD_Container is attached to the "AnchorPoint" (Phase 1), the engine appears on the table for everyone.

### **Phase 3: The Interaction (Manipulation)**

*Goal: User A spins the object, User B sees it spin.*

* **The Grab:**
* **User A** reaches out with **Meta Interaction SDK** hands.
* Their hand touches the Grabbable component on the engine.
* **The Authority Handover:**
* **Code** detects the grab event.
* It calls NetworkObject.RequestStateAuthority().
* **Photon** transfers ownership of the object from "Host" to "User A".
* **The Sync Loop:**
* While User A holds it, their local physics engine moves the object.
* **Photon ****NetworkTransform** component observes this movement.
* It broadcasts the new Rotation/Scale to User B every tick.
* **The Release:**
* User A lets go.
* The object stays in its new rotation.
* Authority remains with User A until User B grabs it.

### **Summary Architecture Diagram**

Code snippet

graph TD

    subgraph "Phase 1: The Anchor"

    A[MRUK Detects Table] -->|Vector3| B[Create OVRSpatialAnchor]

    B -->|Save to Meta Cloud| C[Get Anchor UUID]

    C -->|Photon RPC| D[User B Receives UUID]

    D -->|LoadUnboundAnchors| E[User B Snaps Anchor to Real Table]

    end


    subgraph "Phase 2: The Content"

    F[User A Selects 'Engine'] -->|Set Networked Var| G[Photon Syncs URL String]

    G -->|OnUrlChanged Event| H[glTFast Downloads GLB]

    H -->|Instantiate| I[Model Appears on Anchor]

    end


    subgraph "Phase 3: The Sync"

    J[User A Grabs Model] -->|RequestStateAuthority| K[Ownership Transfer]

    K -->|User A Moves Hand| L[NetworkTransform Syncs XYZ]

    L -->|Update Transform| M[User B Sees Motion]

    end


### **The "Glue" Code (What connects them)**

You need **one specific script** to bridge the gap between Meta's Anchor and Photon's Network Object.

**Script Name:** AnchorNetworkBridge.cs

* **Attached to:** The Photon Network Runner.
**Logic:**C#// Pseudo-code logic

public void OnAnchorLoaded(OVRSpatialAnchor anchor) {

    // 1. We found the shared anchor in the real world

    // 2. Now, spawn the Photon "Content Container" attached to it

    if (Runner.IsServer) {

        var networkObj = Runner.Spawn(CadContainerPrefab);

        networkObj.transform.setParent(anchor.transform, false);

    }

}


**This is the only tricky part.** You must ensure the NetworkObject is physically parented to the OVRSpatialAnchor GameObject. Once that hierarchy is set, Unity handles the rest.


