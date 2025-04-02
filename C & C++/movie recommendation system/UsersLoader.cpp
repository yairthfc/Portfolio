//
// Created by yairt on 12/09/2023.
//
#include "Movie.h"
#include "RecommendationSystem.h"
#include "UsersLoader.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

std::vector<User> UsersLoader::create_users(const std::string
&users_file_path,
                        std::unique_ptr<RecommendationSystem> rs1) noexcept
                        (false){
    std::shared_ptr<RecommendationSystem> rs = std::move(rs1);
    int counter = 0;
    std::vector<User> users;
    std::vector<sp_movie> movies;
    string my_line;
    std::ifstream myfile (users_file_path);
    if (myfile.is_open()){
        while (myfile){
            std::getline(myfile, my_line);
            std::stringstream ss(my_line);
            string word;
            if (counter == 0){
                while (getline(ss, word, ' ')){
                    int j =0;
                    string temp = word;
                    std::stringstream tempss(temp);
                    string tempo, majo;
                    while(getline(tempss, tempo, '-')){
                        if (j == 0){majo = tempo;}
                        if (j == 1){auto* is = rs.get();
                            auto it = *is;
                            movies.push_back(it.get_movie(majo, std::stoi
                            (tempo)));}
                        j++;}
                }}
            else{
                rank_map* rr = new rank_map(0, sp_movie_hash, sp_movie_equal);
                int j =0;
                string tempo, majo;
                auto it1 = movies.begin();
                while(getline(ss, tempo, ' ')){
                    if (j == 0){majo = tempo;}
                    else{if ((tempo[0] < '1' || tempo[0] > '9' )&& tempo[0] !=
                                                                   'N'){throw
                                       std::runtime_error("invalidooooo");}
                    if (tempo == "NA" || tempo == "NA\r"){tempo = "0";}
                        (*rr)[*it1] = std::stoi(tempo);
                    ++it1;}
                    j++;}
                User user(majo, rr, rs);
                users.push_back(user);
            }
            counter++;
        }
    }
    else{throw std::runtime_error("file path invalid.");}
    return users;
}