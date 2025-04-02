//
// Created by yairt on 04/09/2023.
//
#include "Activation.h"

Matrix activation::relu (const Matrix &mat)
{
    Matrix new_mat(mat.get_rows(), mat.get_cols());
    for (int i = 0 ; i<mat.get_rows(); i++ ){
        int row_start = i*mat.get_cols();
        for (int j = 0; j< mat.get_cols(); j++){
            if( mat[row_start +j] < 0)
            {
                new_mat[row_start +j] = 0;
            }
            else {
                new_mat[row_start + j] = mat[row_start + j];
            }
        }
    }
    return new_mat;
}



Matrix activation::softmax(const Matrix &mat)
{
    float sum = 0;
    Matrix new_mat(mat.get_rows(), mat.get_cols());
    for (int i = 0 ; i<mat.get_rows(); i++ ){
        int row_start = i*mat.get_cols();
        for (int j = 0; j< mat.get_cols(); j++){
            sum += std::exp(mat[row_start + j]);
        }
    }
    if (sum !=0){
        for (int i = 0 ; i<mat.get_rows(); i++ ){
            int row_start = i*mat.get_cols();
            for (int j = 0; j< mat.get_cols(); j++){
                new_mat[row_start + j] =std::exp(mat[row_start + j]) / sum;
            }
        }
        return new_mat;
    }
    return mat;;
}
