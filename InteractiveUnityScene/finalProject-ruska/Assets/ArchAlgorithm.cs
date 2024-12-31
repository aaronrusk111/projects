using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer), typeof(MeshCollider))]
public class ArchGenerator : MonoBehaviour
{
    [Header("Arch Parameters")]
    public int segments = 32;  
    public float innerRadius = 2f;  
    public float thickness = 0.5f;  
    public float height = 3f;       

    void Start()
    {
        GenerateArch();
    }
    void GenerateArch()
{
    Mesh mesh = new Mesh();
    mesh.name = "Arch";

    List<Vector3> vertices = new List<Vector3>();
    List<int> triangles = new List<int>();
    List<Vector3> normals = new List<Vector3>();
    List<Vector2> uvs = new List<Vector2>();  // Add a list for UV coordinates

    float angleStep = Mathf.PI / segments;  // step angle in π radians

    // Loop to create vertices
    for (int i = 0; i <= segments; i++)
    {
        float angle = i * angleStep;
        float cos = Mathf.Cos(angle);
        float sin = Mathf.Sin(angle);

        // Outer points
        vertices.Add(new Vector3(cos * innerRadius, sin * innerRadius + height, thickness / 2));
        vertices.Add(new Vector3(cos * innerRadius, sin * innerRadius + height, -thickness / 2));

        // Inner points
        vertices.Add(new Vector3(cos * (innerRadius - thickness), sin * (innerRadius - thickness) + height, thickness / 2));
        vertices.Add(new Vector3(cos * (innerRadius - thickness), sin * (innerRadius - thickness) + height, -thickness / 2));

        // Generate UVs (make sure to match the number of vertices)
        float u = (float)i / segments;
        uvs.Add(new Vector2(u, 0));  // For outer side, bottom
        uvs.Add(new Vector2(u, 1));  // For outer side, top
        uvs.Add(new Vector2(u, 0));  // For inner side, bottom
        uvs.Add(new Vector2(u, 1));  // For inner side, top
    }

    // Generate triangles
    for (int i = 0; i < segments; i++)
    {
        int offset = i * 4;

        // Front side
        triangles.Add(offset);
        triangles.Add(offset + 2);
        triangles.Add(offset + 4);

        triangles.Add(offset + 4);
        triangles.Add(offset + 2);
        triangles.Add(offset + 6);

        // Back side
        triangles.Add(offset + 1);
        triangles.Add(offset + 5);
        triangles.Add(offset + 3);

        triangles.Add(offset + 3);
        triangles.Add(offset + 5);
        triangles.Add(offset + 7);

        // Side faces
        for (int j = 0; j < 2; j++)
        {
            int baseIndex = offset + j * 2;
            triangles.Add(baseIndex);
            triangles.Add(baseIndex + 1);
            triangles.Add(baseIndex + 2);

            triangles.Add(baseIndex + 2);
            triangles.Add(baseIndex + 1);
            triangles.Add(baseIndex + 3);
        }
    }

    // Get normals pointing out
    for (int i = 0; i < vertices.Count; i++)
    {
        normals.Add(Vector3.forward);  // Default normals
    }

    mesh.vertices = vertices.ToArray();
    mesh.triangles = triangles.ToArray();
    mesh.normals = normals.ToArray();
    mesh.uv = uvs.ToArray();  // Set the UVs

    // Recalculate normals to ensure they're correct for the mesh geometry
    mesh.RecalculateNormals();

    // Assign the mesh to the MeshFilter
    MeshFilter meshFilter = GetComponent<MeshFilter>();
    meshFilter.mesh = mesh;

    // Assign the mesh to the MeshCollider
    MeshCollider meshCollider = GetComponent<MeshCollider>();
    meshCollider.sharedMesh = mesh;
}

    

}
