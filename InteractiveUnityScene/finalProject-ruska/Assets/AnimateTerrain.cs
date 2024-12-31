using System.Collections;
using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshCollider))]
public class AnimatedTerrain : MonoBehaviour
{
    public float amplitude = 1f;      
    public float frequency = 0.5f;   
    public float speed = 1f;          
    private Vector3[] originalVertices;  
    private Mesh mesh;               
    private float time = 0f;          

    void Start()
    {
        mesh = GetComponent<MeshFilter>().mesh;

        // Instantiate to avoid modifying shared mesh
        mesh = Instantiate(mesh);
        GetComponent<MeshFilter>().mesh = mesh;

        originalVertices = mesh.vertices;
    }

    void Update()
    {
        AnimateTerrain();
    }

    void AnimateTerrain()
    {
        Vector3[] vertices = new Vector3[originalVertices.Length];
        time += Time.deltaTime * speed;  

        // Loop through each vertex to modify its height
        for (int i = 0; i < originalVertices.Length; i++)
        {
            Vector3 vertex = originalVertices[i];

            // Calculate sine wave based on position and time
            float wave = Mathf.Sin((vertex.x + vertex.z + time) * frequency) * amplitude;

            // Modify the y (height) value of the vertex
            vertex.y = wave;

            vertices[i] = vertex;
        }

        // Apply the modified vertices
        mesh.vertices = vertices;

        // Recalculate normals for proper lighting/shading
        mesh.RecalculateNormals();

        // Update the MeshCollider to match the animated mesh
        MeshCollider meshCollider = GetComponent<MeshCollider>();
        if (meshCollider != null)
        {
            meshCollider.sharedMesh = null;  // Clear the existing collider
            meshCollider.sharedMesh = mesh;  // Assign the updated mesh
        }
    }
}
