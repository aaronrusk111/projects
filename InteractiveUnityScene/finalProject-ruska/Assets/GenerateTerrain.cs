using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshCollider))]
public class ProceduralAnimatedTerrain : MonoBehaviour
{
    public int width = 10;           
    public int length = 10;          
    public float terrainWidth = 10f;
    public float terrainLength = 10f;
    public float amplitude = 1f;   
    public float frequency = 0.5f;  
    public float speed = 1f;         
    private Mesh mesh;
    private Vector3[] originalVertices;
    private float time = 0f;
    void Start()
    {
        GenerateTerrain();
        originalVertices = mesh.vertices; 
        MeshCollider meshCollider = GetComponent<MeshCollider>();
        if (meshCollider == null)
        {
            meshCollider = gameObject.AddComponent<MeshCollider>();
        }
        meshCollider.sharedMesh = mesh;
    }
    void Update()
    {
        AnimateTerrain();
    }

    void GenerateTerrain()
    {
        mesh = new Mesh();
        GetComponent<MeshFilter>().mesh = mesh;

        int numVertices = (width + 1) * (length + 1);
        Vector3[] vertices = new Vector3[numVertices];
        Vector2[] uv = new Vector2[numVertices];
        int[] triangles = new int[width * length * 6];

        int vertIndex = 0;
        for (int z = 0; z <= length; z++)
        {
            for (int x = 0; x <= width; x++)
            {
                float posX = x * terrainWidth / width;
                float posZ = z * terrainLength / length;
                vertices[vertIndex] = new Vector3(posX, 0f, posZ); 
                uv[vertIndex] = new Vector2((float)x / width, (float)z / length);
                vertIndex++;
            }
        }

        int triIndex = 0;
        for (int z = 0; z < length; z++)
        {
            for (int x = 0; x < width; x++)
            {
                int topLeft = z * (width + 1) + x;
                int topRight = topLeft + 1;
                int bottomLeft = (z + 1) * (width + 1) + x;
                int bottomRight = bottomLeft + 1;

                triangles[triIndex++] = topLeft;
                triangles[triIndex++] = bottomLeft;
                triangles[triIndex++] = topRight;

                triangles[triIndex++] = topRight;
                triangles[triIndex++] = bottomLeft;
                triangles[triIndex++] = bottomRight;
            }
        }

        mesh.vertices = vertices;
        mesh.uv = uv;
        mesh.triangles = triangles;
        mesh.RecalculateNormals();
    }

    void AnimateTerrain()
    {
        Vector3[] vertices = mesh.vertices;
        time += Time.deltaTime * speed;

        for (int i = 0; i < vertices.Length; i++)
        {
            Vector3 vertex = vertices[i];
            float wave = Mathf.Sin((vertex.x + vertex.z + time) * frequency) * amplitude;
            vertex.y = wave; 
            vertices[i] = vertex;
        }

        mesh.vertices = vertices; 
        mesh.RecalculateNormals(); 

        MeshCollider meshCollider = GetComponent<MeshCollider>();
        if (meshCollider != null)
        {
            meshCollider.sharedMesh = mesh; 
        }
    }
}
