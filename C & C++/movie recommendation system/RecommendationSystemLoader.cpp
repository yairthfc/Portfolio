//
// Created by yairt on 11/09/2023.
//
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
using std::string;
#include "RecommendationSystemLoader.h"
#define TEN 10



std::unique_ptr<RecommendationSystem>
RecommendationSystemLoader::create_rs_from_movies(
        const string &movies_file_path) noexcept(false)
{
    std::ifstream myfile (movies_file_path);
    string my_line;
    std::unique_ptr<RecommendationSystem> new_sys =
            std::make_unique<RecommendationSystem>();
    if (myfile.is_open()){
        while (std::getline(myfile, my_line)){
            std::vector<double> features;
            std::stringstream ss(my_line);
            string word;
            string name = word;
            int year;
            int i = 0;
            while (getline(ss, word, ' ')){
                if (i == 0){
                    int j =0;
                    string temp = word;
                    std::stringstream tempss(temp);
                    string tempo;
                    while(getline(tempss, tempo, '-')){
                        if (j == 0){name = tempo;}
                        if (j == 1){year = std::stoi(tempo);}
                        j++;
                    }
                }
                else{
                    if (std::stoi(word) > TEN || std::stoi(word) < 1){
                        throw std::runtime_error("invalid");
                    }
                    features.push_back(std::stoi(word));
                }
                i++;
            }
            new_sys->add_movie(name, year, features);
        }
    } else{throw std::runtime_error("file path invalid.");}
    return new_sys;
}