//
// Created by yairt on 11/ZERO9/2ZERO23.
//
#include "RecommendationSystem.h"
#include <cmath>
#include <algorithm>
#define POW_NUM 2
#define ZERO 0


double RecommendationSystem::get_degree (const
std::vector<double> &v1, const std::vector<double> &v2)
{
    return scalar_prod (v1, v2) / (vec_size (v1) * vec_size (v2));

}

double RecommendationSystem::vec_size (const std::vector<double> &vec)
{
    double sum = ZERO;
    for (double i : vec)
    {
        sum += pow (i, POW_NUM);
    }
    return sqrt (sum);
}


double RecommendationSystem::scalar_prod (const std::vector<double> &v1,
                                          const std::vector<double> &v2)
{
    double sum = ZERO;
    for (unsigned int i = ZERO; i < v1.size(); ++i)
    {
        sum += v1[i] * v2[i];
    }
    return sum;
}


sp_movie RecommendationSystem::add_movie(const std::string &name, int year,
                                         const std::vector<double> &features)
{
    Movie movie(name, year);
    sp_movie sp = std::make_shared<Movie>(movie);
    (*_ranks_map)[sp] = features;
    return sp;
}

sp_movie RecommendationSystem::get_movie(const std::string &name, int year)
const
{
    Movie movie(name, year);
    sp_movie sp = std::make_shared<Movie>(movie);
    auto it = _ranks_map->find(sp);
    if (it != _ranks_map->end()){
        return it->first;
    }
    else{return nullptr;}
}


sp_movie RecommendationSystem::recommend_by_content(const User &user)
{
    double sum = ZERO;
    std::map<sp_movie, double> has;
    std::map<sp_movie, double> has_not;
    auto it = user.get_ranks()->begin();
    while (it != user.get_ranks()->end()){
        if (it->second != ZERO) {
            sum += it->second;
            has[it->first] = it->second;
        }
        else{has_not[it->first] = it->second;}
        ++it;}
    sum = sum/ has.size();
    auto it1 = has.begin();
    while (it1 != has.end()){
        it1->second = it1->second - sum;
        ++it1;}
    std::vector<double> ranker;
    auto it2 = has.begin();
    for (unsigned int i = ZERO; i < _ranks_map->begin()->second.size(); i++){
        float mid_sum = ZERO;
        while (it2 != has.end()){
            auto temp = _ranks_map->find(it2->first);
            mid_sum += temp->second[i] * it2->second;
            ++it2;}
        ranker.push_back(mid_sum);
        it2 = has.begin();
    }
    auto it3 = has_not.begin();
    auto it5 = has_not.begin();
    while(it3 != has_not.end()){
        float  summit1,summit2,summit3,summit = ZERO;
        for (unsigned int k = ZERO; k < ranker.size(); k++){
            auto temp1 = _ranks_map->find(it3->first);
            summit1 += ranker[k] * temp1->second[k];}
        for (unsigned int k = ZERO; k < ranker.size(); k++){
            auto temp1 = _ranks_map->find(it3->first);
            summit2 += temp1->second[k] * temp1->second[k];}
        summit2 = std::sqrt(summit2);
        for (unsigned int k = ZERO; k < ranker.size(); k++){
            summit3 += ranker[k] * ranker[k];}
        summit3 = std::sqrt(summit3);
        summit = summit1/ (summit2* summit3);
        it3->second = summit;
        if (it3->second > it5->second){it5 = it3;}
        summit1 = ZERO;summit2 = ZERO;summit3 = ZERO;summit = ZERO;
        ++it3;
    }return it5->first;}

bool sortbyval(const std::pair<sp_movie , double> &a,
               const std::pair<sp_movie , double> &b)
{
    return (a.second > b.second);
}

sp_movie RecommendationSystem::recommend_by_cf(const User &user, int k)
{
    std::vector<std::pair<sp_movie, double>> temp_map;
    std::map<sp_movie, double> has;
    std::map<sp_movie, double> has_not;
    auto it = user.get_ranks()->begin();
    while (it != user.get_ranks()->end()){
        if (it->second != ZERO) {has[it->first] = it->second;}
        else{has_not[it->first] = it->second;}
        ++it;
    }
    auto it1 = has_not.begin();
    auto it5 = has_not.begin();
    while(it1 != has_not.end()){
        auto a = predict_movie_score(user, it1->first, k);
        has_not.find(it1->first)->second = a;
        if (it1->second > it5->second){it5 = it1;}
        ++it1;
    }
    return it5->first;
}




double RecommendationSystem::predict_movie_score(const User &user,
                                         const sp_movie &movie, int k)
{
    std::vector<std::pair<sp_movie, double>> temp_map;
    std::map<sp_movie, double> has;
    std::map<sp_movie, double> has_not;
    auto it = user.get_ranks()->begin();
    while (it != user.get_ranks()->end()){
        if (it->second != ZERO) {has[it->first] = it->second;}
        else{has_not[it->first] = it->second;}
        ++it;
    }
//    auto it1 = has_not.find({movie, ZERO});
    double sum1, sum2, sum3, sum = ZERO;
    auto it2 = has.begin();
    while(it2 != has.end()){
        sum1 = scalar_prod(_ranks_map->find(it2->first)->second,
                           _ranks_map->find(movie)->second);
        sum2 = scalar_prod(_ranks_map->find(movie)->second,
                           _ranks_map->find(movie)->second);
        sum3 = scalar_prod(_ranks_map->find(it2->first)->second,
                           _ranks_map->find(it2->first)->second);
        sum = sum1 / (std::sqrt(sum2) * std::sqrt(sum3));
        temp_map.push_back(std::make_pair(it2->first, sum));
        sum1 = ZERO;sum2 = ZERO;sum3 = ZERO;sum = ZERO;
        ++it2;
    }
    std::sort(temp_map.begin(), temp_map.end(), sortbyval);
    double summ1,summ2, summ = ZERO;
    auto it3 = temp_map.begin();
    for (int i = ZERO; i < k; i++){
        summ1 += it3->second * user.get_ranks()->find(it3->first)->second;
        summ2 += it3->second;
        ++it3;
    }
    summ = summ1 / summ2;
    return summ;
}


std::ostream& operator<<(std::ostream& os, const RecommendationSystem& rs){
    auto it = rs._ranks_map->begin();
    while(it != rs._ranks_map->end()){
        auto* its = it->first.get();
        os << *its ;
        ++it;
    }
    return os;
}