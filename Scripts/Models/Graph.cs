using System.Collections;
using System.Collections.Generic;
using System;

public class Graph
{
    public string name;
    public List<GraphNode> nodes { get; protected set; }

    public Graph(string name)
    {
        nodes = new List<GraphNode>();
    }

    public GraphNode CreateNode(string id)
    {
        GraphNode _node = new GraphNode(id);
        nodes.Add(_node);
        return _node;
    }

    public List<GraphEdge> GetGraphEdges()
    {
        List<GraphEdge> edges = new List<GraphEdge>();
        foreach (GraphNode node in nodes)
        {
            edges.AddRange(node.outEdges);
        }
        return edges;
    }
}
