using System.Collections;
using System.Collections.Generic;
using System;

public class GraphEdge
{
    public Dictionary<string, string> parameters;
    public GraphNode destinationNode { get; protected set; }
    public GraphNode sourceNode { get; protected set; }

    public string id { get; protected set; }

    public GraphEdge(string id, GraphNode destinationNode)
    {
        parameters = new Dictionary<string, string>();
        this.id = id;
        this.destinationNode = destinationNode;
    }

    public void Delete()
    {
        // if an Edge is deleted, then affected ones are nodes that have that Edge as an outEdge which is only 1
        sourceNode.RemoveEdge(this);
    }

    public Action<GraphNode> GetOnNodeDeleted()
    {
        return OnNodeDeleted;
    }

    void OnNodeDeleted(GraphNode deletedNode)
    {
        if (deletedNode == destinationNode)
        {
            Delete();
        }
    }
}
