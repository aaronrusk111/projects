using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArchController : MonoBehaviour
{
    public Material archMaterial; 
    public Color archColor = Color.red; 

    void Start()
    {
        if (archMaterial != null)
        {
            archMaterial.SetColor("_ObjectColor", archColor);
        }
        else
        {
            Debug.LogWarning("Arch material not assigned.");
        }
    }
    public void SetArchColor(Color newColor)
    {
        archColor = newColor;
        if (archMaterial != null)
        {
            archMaterial.SetColor("_ObjectColor", archColor);
        }
    }
}

