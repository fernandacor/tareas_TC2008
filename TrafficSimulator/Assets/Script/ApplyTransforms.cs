using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    [SerializeField] Object[] wheels;
    [SerializeField] Vector3 displacement;
    [SerializeField] float rotationSpeed;
    [SerializeField] AXIS rotationAxis;

    Mesh[] meshs;
    Vector3[][] baseVertices;
    Vector3[][] newVertices;


    // Start is called before the first frame update
    void Start()
    {
        meshs = new Mesh[5];
        baseVertices = new Vector3[5][];
        newVertices = new Vector3[5][];

        meshs[0] = GetComponentInChildren<MeshFilter>().mesh;
        for (int i = 1; i < 5; i++)
        {
            meshs[i] = wheels[i - 1].GetComponentInChildren<MeshFilter>().mesh;
        }

        for (int i = 0; i < meshs.Length; i++)
        {

            baseVertices[i] = meshs[i].vertices;

            newVertices[i] = new Vector3[baseVertices[i].Length];
            for (int j = 0; j < baseVertices.Length; j++)
            {
                newVertices[i][j] = baseVertices[i][j];
            }
        }

    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        for (int i = 0; i < meshs.Length; i++)
        {
            Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time,
                                                            displacement.y * Time.time,
                                                            displacement.z * Time.time);

            Matrix4x4 moveOrigin = HW_Transforms.TranslationMat(-displacement.x,
                                                                -displacement.y,
                                                                -displacement.z);

            Matrix4x4 moveObject = HW_Transforms.TranslationMat(displacement.x,
                                                                displacement.y,
                                                                displacement.z);

            Matrix4x4 rotate = HW_Transforms.RotateMat(rotationSpeed * Time.time, rotationAxis);

            Matrix4x4 composite = move;
            if (i > 0)
                composite *= rotate;

            for (int j = 0; j < newVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(baseVertices[i][j].x,
                                            baseVertices[i][j].y,
                                            baseVertices[i][j].z,
                                            1);

                newVertices[i][j] = composite * temp;

            }
            meshs[i].vertices = newVertices[i];
            meshs[i].RecalculateNormals();
        }
    }
}

