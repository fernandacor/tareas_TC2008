/*
Functions to work with transformation matrices in 3D

Gilberto Echeverria
2022-11-03
*/

// ESTE ARCHIVO LO TENEMOS QUE TENER EN EL PROYECTO


using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Enumeration to define the axis
public enum AXIS {X, Y, Z};
// Values:        0  1  2

public class HW_Transforms : MonoBehaviour
{
    public static Matrix4x4 TranslationMat(float tx, float ty, float tz)
    {
        // Matrices de transformación
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 3] = tx;
        matrix[1, 3] = ty;
        matrix[2, 3] = tz;
        return matrix;
    }

    public static Matrix4x4 ScaleMat(float sx, float sy, float sz)
    {
        // Matriz de escala, en la diagonal se sustituyen los valores de la escala
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 0] = sx;
        matrix[1, 1] = sy;
        matrix[2, 2] = sz;
        return matrix;
    }

    public static Matrix4x4 RotateMat(float angle, AXIS axis)
    {
        // Matriz de rotación
        float rads = angle * Mathf.Deg2Rad;
        Mathf.Sin(rads);

        Matrix4x4 matrix = Matrix4x4.identity;
        if (axis == AXIS.X) {

        } else if (axis == AXIS.Y) {

        } else if (axis == AXIS.Z) {

        }
        return matrix;
    }
}
