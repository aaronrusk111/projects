using UnityEngine;

public class RollingBallInteraction : MonoBehaviour
{
    private Vector3 lastMousePosition;
    private bool isClickingOnArch = false;  // check if click is on the arch

    public GameObject arch; 

    void Update()
    {
        if (Input.GetMouseButtonDown(0)) 
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                if (hit.transform.gameObject == arch)
                {
                    isClickingOnArch = true;
                }
                else
                {
                    isClickingOnArch = false;
                }
            }
        }
        if (isClickingOnArch && Input.GetMouseButton(0)) 
        {
            Vector3 delta = Input.mousePosition - lastMousePosition;
            float rotationSpeed = 0.25f;

            arch.transform.Rotate(Vector3.up, -delta.x * rotationSpeed, Space.World);
            arch.transform.Rotate(Vector3.right, delta.y * rotationSpeed, Space.World);
        }
        
        lastMousePosition = Input.mousePosition;

        // stop draggin when user releases mouse
        if (Input.GetMouseButtonUp(0))
        {
            isClickingOnArch = false;
        }
    }
}
