# Maya Callbacks

## `OpenMaya.MDGMessage`
This class is usued to register callbacks for **Dependency Graph** related messages.

1. `addNodeAddedCallback`, this method registers a callback that is called
whenever a new node is added to the dependency graph.

2. `addNodeRemovedCallback`, this method registers a callback that is
called whenever a new node is removed from the dependency graph.

## `OpenMaya.MModelMessage`
 This class is used to register callbacks for **model** related message.

 1. `addCallback`, this method adds a new callback for the specified
 model message.

 2. `addAfterDuplicateCallback`.

 3. `addBeforeDuplicateCallback`.

4. `addNodeAddedToModelCallback`, this method is used to register a
 callback that is called when a **dag node** is about to be added to the
 Maya model.

5. `addNodeRemovedFromModelCallback`, this method registers a callback
callback that is called when the specified **dag node** is being
removed from the Maya model.

## `OpenMaya.MSceneMessage`
This class is used to register callbacks for scene related message.

1. `addCallback`, adds a new callback for the specified scene message. if a
'before' message is sent, the corresponding 'after' message will be as well.

## `OpenMaya.MMessage`
This is the base class for message callbacks.

1. `removeCallback`, removes the specified callback from Maya. This method
must be called for all callbacks registered by a plug-in before that plug-in
 is unloaded.
