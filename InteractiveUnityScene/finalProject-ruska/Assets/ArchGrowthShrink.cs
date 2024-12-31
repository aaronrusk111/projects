using UnityEngine;

public class AnimatedArch : MonoBehaviour
{
    public float maxScaleFactor = 2.0f; 

    private Vector3 initialScale;       
    private bool growing = true; 

    void Start()
    {
        initialScale = transform.localScale; 
    }

    void Update()
    {
        AnimateArch();
    }

    void AnimateArch()
    {
        float deltaScale = 0.25f * Time.deltaTime;

        if (growing)
        {
            // Grow arch
            transform.localScale += Vector3.one * deltaScale;

            // Stop at max
            if (transform.localScale.x >= initialScale.x * maxScaleFactor)
            {
                transform.localScale = Vector3.one * (initialScale.x * maxScaleFactor);
                // Begin shrink
                growing = false; 
            }
        }
        else
        {
            // Shrink arch
            transform.localScale -= Vector3.one * deltaScale;

            if (DetectTerrainCollision())
            {
                growing = true; 
            }

            transform.localScale = Vector3.Max(transform.localScale, initialScale * 0.1f);
        }
    }

    bool DetectTerrainCollision()
    {
        RaycastHit hit;

        Vector3 leftRayOrigin = transform.position-transform.right*transform.localScale.x*0.5f;
        Vector3 rightRayOrigin = transform.position+transform.right*transform.localScale.x*0.5f;

        float rayLength = transform.localScale.y * 0.6f; 
        bool leftHit = Physics.Raycast(leftRayOrigin, Vector3.down, out hit, rayLength) && hit.collider.CompareTag("Terrain");
        bool rightHit = Physics.Raycast(rightRayOrigin, Vector3.down, out hit, rayLength) && hit.collider.CompareTag("Terrain");
        // Return true if either side hits the terrain
        return leftHit || rightHit; 
    }
}
