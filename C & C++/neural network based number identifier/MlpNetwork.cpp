//
// Created by yairt on 05/09/2023.
//
#include "MlpNetwork.h"
#define NUM_OF_DIGITS 10
#include "iostream"

MlpNetwork ::MlpNetwork(Matrix wheights_arr[MLP_SIZE], Matrix biases_arr[MLP_SIZE])
{
    if (wheights_arr[0].get_cols() != weights_dims[0].cols ||
    wheights_arr[0].get_rows() !=
    weights_dims[0].rows
    || wheights_arr[1].get_cols() != weights_dims[1].cols || wheights_arr[1]
    .get_rows()
    != weights_dims[1].rows
    || wheights_arr[2].get_cols() != weights_dims[2].cols || wheights_arr[2]
    .get_rows()
    != weights_dims[2].rows
    || wheights_arr[3].get_cols() != weights_dims[3].cols || wheights_arr[3]
    .get_rows() !=
    weights_dims[3].rows){
        throw std::length_error("length does not match");
    }
    if (biases_arr[0].get_cols() != bias_dims[0].cols || biases_arr[0].get_rows() !=
    bias_dims[0].rows
        || biases_arr[1].get_cols() != bias_dims[1].cols || biases_arr[1]
        .get_rows() !=
        bias_dims[1].rows
        || biases_arr[2].get_cols() != bias_dims[2].cols || biases_arr[2]
        .get_rows() !=
        bias_dims[2].rows
        || biases_arr[3].get_cols() != bias_dims[3].cols || biases_arr[3]
        .get_rows() != bias_dims[3].rows){
        throw std::length_error("length does not match");
    }
    _dense_arr = new Dense[MLP_SIZE]{
            Dense(wheights_arr[0], biases_arr[0], activation::relu),
            Dense(wheights_arr[1], biases_arr[1], activation::relu),
            Dense(wheights_arr[2], biases_arr[2], activation::relu),
            Dense(wheights_arr[3], biases_arr[3], activation::softmax)
    };

}

digit MlpNetwork::operator()(Matrix &input) const
{
    input.vectorize();
    Matrix layer1 = _dense_arr[0](input);
    Matrix layer2 = _dense_arr[1](layer1);
    Matrix layer3 = _dense_arr[2](layer2);
    Matrix layer4 = _dense_arr[3](layer3);
    digit dig;
    int str_ind = 0;
    float str_int_prb = 0;
    for (int i = 0; i< NUM_OF_DIGITS; i++){
        if(layer4[i] < str_int_prb){ continue;}
        else{str_ind = i; str_int_prb = layer4[i];}
    }
    dig.value = str_ind;
    dig.probability = str_int_prb;
    return dig;
}