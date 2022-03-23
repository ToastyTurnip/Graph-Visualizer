using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GraphManager : MonoBehaviour
{
    public static GraphManager Instance;

    public Dictionary<GraphNode, GameObject> nodeGameObjectMap;
    // Start is called before the first frame update
    void Awake()
    {
        if (Instance == null)
            Instance = this;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
