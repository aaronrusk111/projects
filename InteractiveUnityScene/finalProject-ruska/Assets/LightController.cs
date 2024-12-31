using UnityEngine;

public class LightController : MonoBehaviour
{
    public Transform lightSphere;          // sphere representing the light source
    public Material[] customMaterials;     // array of materials

    private static readonly int LightPositionID = Shader.PropertyToID("_LightPosition");

    [SerializeField] private bool lightOn = true;  
    [SerializeField] private float lightSpeed = 2.0f;  
    [SerializeField] private float radius = 5.0f;   
    [SerializeField] private float lightHeight = 3.0f;  

    private float time;  

    void Update()
    {
        time += Time.deltaTime * lightSpeed;
        float x = radius * Mathf.Cos(time);
        float z = radius * Mathf.Sin(time);

        float y = lightHeight;

        Vector3 lightPos = new Vector3(x, y, z);

        // Move the lightSphere
        if (lightSphere != null)
        {
            lightSphere.position = lightPos;
        }
        if (customMaterials != null)
        {
            foreach (Material material in customMaterials)
            {
                material.SetVector("_LightPosition", lightPos);

                material.SetFloat("_LightOn", lightOn ? 1.0f : 0.0f);
            }
        }
    }
}
