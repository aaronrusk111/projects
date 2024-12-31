using UnityEngine;
using UnityEngine.UI; 

public class HelpScreen : MonoBehaviour
{
    public GameObject helpText; 
    private bool helpVisible = false; 

    void Start()
    {
        // Hide at start
        if (helpText != null)
            helpText.SetActive(false);
    }

    void Update()
    {
        // Toggle on h input
        if (Input.GetKeyDown(KeyCode.H))
        {
            helpVisible = !helpVisible;
            helpText.SetActive(helpVisible);
        }
    }
}
