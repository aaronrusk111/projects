using UnityEngine;

public class CameraController : MonoBehaviour
{
    public enum CameraMode { FirstPerson, AutoOrbit }
    [SerializeField] private CameraMode currentMode = CameraMode.FirstPerson;

    [Header("First Person Controls")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float lookSpeed = 2f;
    private float yaw = 0f, pitch = 0f;

    [Header("Auto Orbit")]
    [SerializeField] private Transform target; 
    [SerializeField] private float orbitDistance = 10f;
    [SerializeField] private float autoOrbitSpeed = 10f;
    private float orbitYaw = 0f;

    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;

        yaw = transform.eulerAngles.y;
        pitch = transform.eulerAngles.x;
    }

    void Update()
    {
        switch (currentMode)
        {
            case CameraMode.FirstPerson:
                HandleFirstPersonControls();
                break;

            case CameraMode.AutoOrbit:
                HandleAutoOrbit();
                break;
        }

        if (Input.GetKeyDown(KeyCode.Alpha1))
            currentMode = CameraMode.FirstPerson;
        if (Input.GetKeyDown(KeyCode.Alpha2))
            currentMode = CameraMode.AutoOrbit;
    }
    private void HandleFirstPersonControls()
    {
        pitch -= lookSpeed*Input.GetAxis("Mouse Y");
        yaw += lookSpeed*Input.GetAxis("Mouse X");
        pitch = Mathf.Clamp(pitch, -90f, 90f);
        transform.eulerAngles = new Vector3(pitch, yaw, 0f);

        Vector3 forward = transform.forward*Input.GetAxis("Vertical");
        Vector3 right = transform.right*Input.GetAxis("Horizontal");
        transform.position += (forward+right) * moveSpeed*Time.deltaTime;
    }
    private void HandleAutoOrbit()
    {
        if (target == null)
        return;

        orbitYaw +=autoOrbitSpeed*Time.deltaTime;

        Quaternion rotation = Quaternion.Euler(30f,orbitYaw,0f);
        Vector3 offset = rotation*new Vector3(0,0,-orbitDistance);

        transform.position = target.position + offset;
        transform.LookAt(target);
    }
}
