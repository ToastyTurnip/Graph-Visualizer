using System.Collections;
using System.Collections.Generic;
using System;

public class GraphNode
{
    public Dictionary<string, string> parameters;
    public List<GraphEdge> outEdges;
    public string id { get; protected set; }
    public GraphNode(string id)
    {
        parameters = new Dictionary<string, string>();
        this.id = id;
        outEdges = new List<GraphEdge>();
    }

    public void AddParameter(string parameter, string value)
    {
        parameters[parameter] = value;
    }

    public void AddEdge(GraphEdge edge)
    {
        outEdges.Add(edge);
    }

    public void RemoveEdge(GraphEdge edge)
    {
        if (outEdges.Contains(edge))
            outEdges.Remove(edge);
    }

    // NODE DELETION SECTION:
    // These functions and callbacks let other objects listen for events where a node is up for deletion
    // deleteNodeCallback should be called BEFORE a node gets deleted so that instances that uses it can handle
    // the cleanup process.
    // if a Node is deleted then the affected ones are edges that have that Node as a destination Node
    Action<GraphNode> deleteNodeCallback;
    public void ListenForNodeDeletionEvent(Action<GraphNode> callback)
    {
        deleteNodeCallback += callback;
    }

    public void UnListenForNodeDeletionEvent(Action<GraphNode> callback)
    {
        deleteNodeCallback -= callback;
    }

    public void Delete()
    {
        deleteNodeCallback?.Invoke(this);
    }
}
