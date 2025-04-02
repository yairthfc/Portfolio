//
// Created by yairt on 05/09/2023.
//
#include "Dense.h"

Dense::Dense(Matrix &weights, Matrix &bias, ActivationFunction func):_weights
(weights), _bias(bias), _func(func){}

Matrix Dense::get_weights()
{
    return _weights;
}

Matrix Dense::get_bias()
{
    return _bias;
}

ActivationFunction Dense::get_activation()
{
    return _func;
}

Matrix Dense::operator()(const Matrix &input) const
{
    Matrix new_mat = _weights * input + _bias;
    return _func(new_mat);
}

