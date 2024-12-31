using UnityEngine;

public class TerrainController : MonoBehaviour
{
    public Material terrainMaterial;  
    public Color terrainColor = Color.green;

    void Start()
    {

        if (terrainMaterial != null)
        {
            
            terrainMaterial.SetColor("_ObjectColor", terrainColor); 
        }
        else
        {
            Debug.LogWarning("Terrain material not assigned.");
        }
    }
    public void SetTerrainColor(Color newColor)
    {
        terrainColor = newColor;
        if (terrainMaterial != null)
        {
            terrainMaterial.SetColor("_ObjectColor", terrainColor); 
        }
    }
}
