import pandas as pd
import numpy as np

import random
import pickle
from math import *

from sklearn.metrics.pairwise import cosine_similarity
from lightfm import LightFM
from lightfm.data import Dataset

class DataLoad():
    def __init__(self, ingredient_df_path=None, product_df_path=None, dummy_survey_df_path=None, review_df_path=None, user_features_list_path=None, item_features_path=None, dataset_path=None, model_path=None):
        self.ingredient_df_path = ingredient_df_path
        self.product_df_path = product_df_path
        self.review_df_path = review_df_path
        self.dummy_survey_df_path = dummy_survey_df_path
        self.user_features_list_path = user_features_list_path
        self.item_features_path = item_features_path
        self.dataset_path = dataset_path
        self.model_path = model_path

    def dataload(self):
        loaded_data = []

        if self.ingredient_df_path:
            with open(self.ingredient_df_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
                
        if self.product_df_path:
            with open(self.product_df_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
            
        if self.dummy_survey_df_path:
            with open(self.dummy_survey_df_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
                
        if self.review_df_path:
            with open(self.review_df_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
            
        if self.user_features_list_path:     
            with open(self.user_features_list_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
            
        if self.item_features_path:
            with open(self.item_features_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
            
        if self.dataset_path:
            with open(self.dataset_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
            
        if self.model_path:
            with open(self.model_path, 'rb') as f:
                loaded_data.append(pickle.load(f))
            
        return tuple(loaded_data)



class DefinedVariable:
    function_list = ['HF01', 'HF02', 'HF03', 'HF04', 'HF05', 'HF06', 'HF07', 'HF08', 'HF09', 'HF10', 'HF11',
        'HF12', 'HF13', 'HF14', 'HF15', 'HF16', 'HF17', 'HF18', 'HF19', 'HF20', 'HF21', 'HF22', 'HF23', 'HF24', 'HF25']

    allergy_disease_list = ['AL01', 'AL02', 'AL03', 'AL04', 'AL05', 'AL06', 'AL07', 'AL08', 'AL09', 'AL10', 'AL11', 'AL12', 'AL13',
        'AL14', 'AL15', 'AL16', 'AL17', 'AL18', 'AL19', 'AL20',
            'DI01', 'DI02', 'DI03', 'DI04', 'DI05', 'DI06', 'DI07', 'DI08', 'DI09', 'DI10', 'DI11',
        'DI12', 'DI13', 'DI14', 'DI15', 'DI16', 'DI17']

    survey_list = ['survey_pregnancy', 'surve_operation', 'survey_alchol', 'survey_smoking',
                    'AL01', 'AL02', 'AL03', 'AL04', 'AL05', 'AL06', 'AL07', 'AL08', 'AL09', 'AL10', 
                    'AL11', 'AL12', 'AL13', 'AL14', 'AL15', 'AL16', 'AL17', 'AL18', 'AL19', 'AL20', 
                    'DI01', 'DI02', 'DI03', 'DI04', 'DI05', 'DI06', 'DI07', 'DI08', 'DI09', 'DI10', 
                    'DI11', 'DI12', 'DI13', 'DI14', 'DI15', 'DI16', 'DI17']


    ingredient_caution_dict = {'비타민 A' : 18,
                            '베타카로틴' : 136,
                            '요오드' : 429
                            }

    all_smoker_drop_ingredient_ids = [18, 13, 66, 74, 79, 90, 195, 289] # 흡연자에게 추천되면 안되는 ingredient_id 리스트

    weights = {
        'visited_at': 0.1, # 5번 조회할 때 +1
        'like_created_at': 1,
        'review_rating': 1,
        'sim_grp' : 5, # max=5
        'product_function_sim' : 5, # max=5
        'product_ingredient_sim' : 5
    }
    
    
class DataPreprocessor(DefinedVariable):
    
    def __init__(self, survey_df, dummy_survey_df):
        super().__init__()
        self.survey_df = survey_df
        self.dummy_survey_df = dummy_survey_df
        self.function_list = DefinedVariable.function_list 
        
    @staticmethod
    def create_code_list_col(survey_df, code_list, col_name):
        survey_df[col_name] = survey_df.apply(lambda row: [code for code in code_list if row[code] == 1], axis=1)
        survey_df[col_name] = survey_df[col_name].apply(lambda x: x if len(x) > 0 else ['HF00'])
        return survey_df
    
    @staticmethod
    def create_str_col(survey_df, list_col_name, new_str_col_name):
        survey_df[new_str_col_name] = survey_df[list_col_name].apply(lambda x: ', '.join(x) if isinstance(x, list) else 'HF00')
        return survey_df
    
    def preprocess_data(self):
        # 컬럼 값 수정 및 추가
        # if self.survey_df['HF00'] == 1:
        #     survey_row = self.survey_df
        #     survey_df = self.dummy_survey_df
        #     survey_row['HF00'] = 0
        #     sim_profile_grp_function_list = RecommendModel.find_sim_grp_function_rank(self, survey_df, survey_row, top_n=5)
        #     for function in sim_profile_grp_function_list:
        #         survey_row[function] = 1
        # self.survey_df = survey_row
        new_survey_df = DataPreprocessor.create_code_list_col(self.survey_df, self.function_list, 'function_code')
        new_survey_df = DataPreprocessor.create_str_col(new_survey_df, 'function_code', 'function_code_str')
        new_survey_df['HF_sum'] = new_survey_df[self.function_list].sum(axis=1)
        profile_id = int(new_survey_df['profile_id'])
        self.dummy_survey_df = self.dummy_survey_df[['survey_id', 'user_id', 'profile_id', 'survey_age_group', 'survey_sex',
                                        'survey_pregnancy', 'survey_operation', 'survey_alcohol',
                                        'survey_smoking', 'HF00', 'HF01', 'HF02', 'HF03', 'HF04', 'HF05',
                                        'HF06', 'HF07', 'HF08', 'HF09', 'HF10', 'HF11', 'HF12', 'HF13', 'HF14',
                                        'HF15', 'HF16', 'HF17', 'HF18', 'HF19', 'HF20', 'HF21', 'HF22', 'HF23',
                                        'HF24', 'HF25', 'HF_sum', 'AL01', 'AL02', 'AL03', 'AL04', 'AL05',
                                        'AL06', 'AL07', 'AL08', 'AL09', 'AL10', 'AL11', 'AL12', 'AL13', 'AL14',
                                        'AL15', 'AL16', 'AL17', 'AL18', 'AL19', 'AL20', 'DI01', 'DI02', 'DI03',
                                        'DI04', 'DI05', 'DI06', 'DI07', 'DI08', 'DI09', 'DI10', 'DI11', 'DI12',
                                        'DI13', 'DI14', 'DI15', 'DI16', 'DI17', 'function_code',
                                        'function_code_str', 'recom_ingredients_fin']]
        self.dummy_survey_df.rename(columns={'recom_ingredients_fin':'ingredient_id'}, inplace=True)
    
        new_survey_df['ingredient_id'] = 0
        
        # dummy_survey_df에 추천받는 사용자와 같은 survey_id, profile_id가 있을 경우 drop
        if new_survey_df['survey_id'].astype(int).isin(self.dummy_survey_df['survey_id']).any():
            drop_idxs = self.dummy_survey_df[self.dummy_survey_df['survey_id'].isin(new_survey_df['survey_id'].astype(int))].index.tolist()
            self.dummy_survey_df.drop(index=drop_idxs, inplace=True)
        elif new_survey_df['profile_id'].astype(int).isin(self.dummy_survey_df['profile_id']).any():
            drop_idxs = self.dummy_survey_df[self.dummy_survey_df['profile_id'].isin(new_survey_df['profile_id'].astype(int))].index.tolist()
            self.dummy_survey_df.drop(index=drop_idxs, inplace=True)

        fin_survey_df = pd.concat([new_survey_df, self.dummy_survey_df], axis=0, ignore_index=True)
       
        # if (new_survey_df['survey_sex'] == 0):
        #     if (new_survey_df['AL05'] == 0):
        #         new_survey_df['AL05'] = 1
        #     elif (new_survey_df['AL06'] == 0):
        #         new_survey_df['AL06'] = 1
        # else:
        #     if (new_survey_df['DI15'] == 1) & (new_survey_df['AL05'] == 0):
        #         new_survey_df['AL05'] = 1
        #     elif (new_survey_df['DI15'] == 1) & (new_survey_df['AL06'] == 0):
        #         new_survey_df['AL06'] = 1
        fin_survey_df.loc[fin_survey_df['survey_sex'] == 0, 'AL05'] = 1
        fin_survey_df.loc[fin_survey_df['survey_sex'] == 0, 'AL06'] = 1
        fin_survey_df.loc[(fin_survey_df['survey_sex'] == 1) & (fin_survey_df['DI15'] == 1), 'AL05'] = 1
        fin_survey_df.loc[(fin_survey_df['survey_sex'] == 1) & (fin_survey_df['DI15'] == 1), 'AL06'] = 1
        
        return profile_id, fin_survey_df # self.survey_df # new_survey_df


class RecommendModel(DefinedVariable):
    def __init__(self, survey_df, product_df, ingredient_df, profile_id, review_df, user_features_list, item_features, dataset, model):
    # def __init__(self, survey_df, product_df, ingredient_df, profile_id):
        super().__init__()
        self.survey_df = survey_df
        self.ingredient_df = ingredient_df
        self.product_df = product_df
        self.review_df = review_df
        self.profile_id = profile_id
        self.user_features_list = user_features_list
        self.item_features = item_features
        self.dataset = dataset
        self.model = model
        
        self.function_list = DefinedVariable.function_list 
        self.allergy_disease_list = DefinedVariable.allergy_disease_list
        self.survey_list = DefinedVariable.survey_list
        self.ingredient_caution_dict = DefinedVariable.ingredient_caution_dict
        self.all_smoker_drop_ingredient_ids = DefinedVariable.all_smoker_drop_ingredient_ids
        self.weights = DefinedVariable.weights
    
    @staticmethod
    def find_profile_id_row(survey_df, profile_id):
#         survey_idx = survey_df.loc[survey_df['profile_id'] == profile_id].index[0]
#         survey_row = survey_df.loc[survey_idx]
#         return survey_idx, survey_row
        survey_idx = survey_df[survey_df['profile_id'] == profile_id].index
        if len(survey_idx) > 0:
            survey_row = survey_df.loc[survey_idx[0]] 
            return survey_idx[0], survey_row
        else:
            # 특정 profile_id를 찾을 수 없는 경우에 대한 처리
            print('[Error] : 추천받고 싶은 사용자의 profile_id를 찾을 수 없습니다.')

    @staticmethod
    def find_sim_grp_function_rank(self, survey_df, survey_row, top_n=5):
        # Flask에서는 삭제될 코드
        sim_survey_grp = survey_df[(survey_df['survey_sex'] == survey_row['survey_sex']) & (survey_df['survey_age_group'] == survey_row['survey_age_group'])]

        function_freq = {function_code: sim_survey_grp[function_code].sum() for function_code in self.function_list}

        function_ranking = sorted(function_freq.items(), key=lambda x: x[1], reverse=True)
        
        total_frequency = sum(freq for _, freq in function_ranking)

        # function_ratios = [(function_code, round(freq / total_frequency, 3)) for function_code, freq in function_ranking][:top_n]
        function_ratios = [function_code for function_code, freq in function_ranking][:top_n]

        return function_ratios
    
    @staticmethod
    def create_check_name_dict(ingredient_df, num=5):
        check_name_dict = {}
        for name in ingredient_df['ingredient_name']:
            prefix = name[:num]
            if prefix != '비타민 B':
                check_name_dict.setdefault(prefix, []).append(name) 
        
        check_name_dict = {key: value for key, value in check_name_dict.items() if len(value) > 1}
        
        return check_name_dict 
    
    @staticmethod
    def recommend_ingredients(self, survey_df, ingredient_df, profile_id, top_n=10):
        survey_idx, survey_row = RecommendModel.find_profile_id_row(survey_df, profile_id)
        
        drop_caution_idx_list = []
        for allergy_disease in self.allergy_disease_list:
            if survey_row[allergy_disease] == 1:
                drop_caution_idxs = ingredient_df[ingredient_df[allergy_disease] == 1].index.tolist()
                drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_pregnancy'] == 1:
            drop_caution_idxs = ingredient_df[(ingredient_df['P3'] == 1) | (ingredient_df['P2'] == 1) | (ingredient_df['P1'] == 1)].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_operation'] == 1:
            drop_caution_idxs = ingredient_df[ingredient_df['OPERATION'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_smoking'] == 1:
            drop_caution_idxs = ingredient_df[(ingredient_df['SMOKE'] == 1) | (ingredient_df['ingredient_id'].isin([18, 13, 66, 74, 79, 90, 195, 289]))].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
            if survey_row['survey_sex'] == 1:
                drop_caution_idxs = ingredient_df[(ingredient_df['ingredient_id'] == 424) | (ingredient_df['ingredient_id'] == 143)].index.tolist()
                drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_age_group'] == 0:
            drop_caution_idxs = ingredient_df[(ingredient_df['KIDS'] == 1) & (ingredient_df['ADULT'] == 1)].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs) 
        if survey_row['survey_age_group'] == 10:
            drop_caution_idxs = ingredient_df[(ingredient_df['TEENAGER'] == 1) & (ingredient_df['ADULT'] == 1)].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_sex'] == 1:
            drop_caution_idxs = ingredient_df[ingredient_df['MALE'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs) 
        if survey_row['survey_age_group'] == 60:
            drop_caution_idxs = ingredient_df[ingredient_df['OLD'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        
        recom_ingredient_df = ingredient_df.drop(index=list(set(drop_caution_idx_list)))

        
        selected_functions = survey_row['function_code'] 
        i_s_hfs = []
        for hf_list in recom_ingredient_df['function_code']:
            i_selected_functions = [hf for hf in hf_list if hf in selected_functions]
            i_s_hfs.append(i_selected_functions)
        recom_ingredient_df['selected_function_code'] = i_s_hfs
        
        recom_ingredient_df['selected_function_code_cnt'] = 0
        recom_ingredient_df['selected_function_code_cnt'] =recom_ingredient_df.loc[(recom_ingredient_df['selected_function_code'].notnull()), 'selected_function_code'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        
        recom_rating = (recom_ingredient_df['selected_function_code_cnt'] * 3) + (recom_ingredient_df['ingredient_type'] * 0.3) + (recom_ingredient_df['function_code_cnt'] * 0.1 ) # + ( add_rating * 0.2 ) 
        
        # 건강기능 선택하지 않았을 경우 - 협업 필터링으로 가산점
        if survey_row['HF00'] == 1:
            sim_profile_grp_function_rank = RecommendModel.find_sim_grp_function_rank(self, survey_df, survey_row, top_n=5)
            sim_profile_grp_function_names = [x[0] for x in sim_profile_grp_function_rank]
            sim_profile_grp_function_freqs = [x[1] for x in sim_profile_grp_function_rank]
            add_cnt = 0
            for selected_function in selected_functions:
                for idx, grp_function in enumerate(sim_profile_grp_function_names):
                    if selected_function == grp_function:
                        # add_rating += sim_profile_grp_function_freqs[idx]
                        add_cnt += 1
                        
            recom_rating += ( add_cnt * 3 ) 
                
        recom_ingredient_df['rating'] = round(recom_rating, 2)
        
        if survey_row['survey_pregnancy'] == 1:
            pregnancy_mask = (recom_ingredient_df['ingredient_name'] == '엽산') | (recom_ingredient_df['ingredient_name'] == '철')
            recom_ingredient_df.loc[pregnancy_mask, 'rating'] += 10
            
        if survey_row['survey_smoking'] == 1:
            smoking_mask = (recom_ingredient_df['ingredient_name'] == '비타민 C')
            recom_ingredient_df.loc[smoking_mask, 'rating'] += 10
        
        recom_ingredient_df['rank'] = recom_ingredient_df['rating'].rank(method='dense', ascending=False).astype(np.int32)
        recom_ingredient_df = recom_ingredient_df.sort_values(by=['rank'], ascending=True)[:top_n * 10] # 넉넉하게 100개에서 다시 필터링
        recom_ingredient_df.reset_index(drop=True, inplace=True)
        
        check_name_dict = RecommendModel.create_check_name_dict(recom_ingredient_df, 5) 
        check_prefix = set()
        
        for idx, survey_row in recom_ingredient_df.iterrows():
            name_value = survey_row['ingredient_name']
            prefix = name_value[:5]
            
            if prefix in check_prefix:
                continue
            check_prefix.add(prefix)
            
            if prefix in check_name_dict:
                values = check_name_dict[prefix]
                selected_value = random.choice(values)
                drop_value = recom_ingredient_df[(recom_ingredient_df['ingredient_name'].str.startswith(prefix)) & (recom_ingredient_df['ingredient_name'] != selected_value)].index
                recom_ingredient_df.drop(drop_value, inplace=True)
                recom_ingredient_df.reset_index(drop=True, inplace=True)
        
        check_hfs = []
        head_idx = []
        tail_idx = []
        for idx, survey_row in recom_ingredient_df.iterrows():
            selected_functions = survey_row['selected_function_code']
            for selected_function in selected_functions:
                if selected_function not in check_hfs:
                    check_hfs.append(selected_function)
                    if idx not in head_idx:
                        head_idx.append(idx)
                else : 
                    if (idx not in head_idx) and (idx not in tail_idx):
                        tail_idx.append(idx)
                
        recom_ingredient_df.loc[head_idx, 'rating'] += 15
        
        # 특정 영양성분 주의사항에 해당하는 영양성분 행 제거 - 코드 수정필요 - 일단 제외
#         for idx in range(len(recom_ingredient_df)):
#             for key, value in self.ingredient_caution_dict.items():
#                 try:
#                     if recom_ingredient_df.loc[idx, key] == 1:
#                         stay_rows = ingredient_df.loc[ingredient_df['ingredient_id'] != value]
#                         recom_ingredient_df = recom_ingredient_df[recom_ingredient_df['ingredient_id'].isin(stay_rows['ingredient_id'])] 
#                 except KeyError: # 해당하는 행이 없을 경우 
#                     continue
                    
        recom_ingredient_df.reset_index(drop=True, inplace=True)
        
        recom_ingredient_df['rank'] = recom_ingredient_df['rating'].rank(method='dense', ascending=False).astype(np.int32)
        recom_ingredient_df = recom_ingredient_df.sort_values(by=['rank'], ascending=True)[:top_n] # top_n 추출
        recom_ingredient_df.reset_index(drop=True, inplace=True)
        
        return recom_ingredient_df        
    
    @staticmethod
    def recommend_top5_ingredients(recom_ingredient_df, n=5):
        ranks = {i: recom_ingredient_df[recom_ingredient_df['rank'] == i].index.tolist() for i in range(1, 6)}
        recom_top5_ingredient_index = []
        for i in range(1, 6):
            if len(ranks[i]) >= n - len(recom_top5_ingredient_index):
                recom_top5_ingredient_index.extend(np.random.choice(ranks[i], n - len(recom_top5_ingredient_index), replace=False))
            else:
                recom_top5_ingredient_index.extend(ranks[i])
                
        recom_top5_ingredient_df = recom_ingredient_df.iloc[recom_top5_ingredient_index].reset_index(drop=True)
        
        return recom_top5_ingredient_df
    
    def run_recommend_ingredients_function(self):
        survey_idx, survey_row = RecommendModel.find_profile_id_row(self.survey_df, self.profile_id)
        recom_ingredient_df = RecommendModel.recommend_ingredients(self, self.survey_df, self.ingredient_df, self.profile_id, top_n=10)
        recom_top5_ingredient_df = RecommendModel.recommend_top5_ingredients(recom_ingredient_df, n=5)
        recom_ingredient_id_list = recom_top5_ingredient_df['ingredient_id'].tolist()
        survey_row['ingredient_id'] = recom_ingredient_id_list
        # self.survey_df.loc[survey_idx, 'ingredient_id'] = list(map(int, self.survey_df.loc[survey_idx, 'ingredient_id'].split(', ')))
        return recom_ingredient_id_list, recom_top5_ingredient_df, survey_row
    
    # def add_recom_ingredeint(self):
        
    #     self.survey_row['ingredient_id'] = 
    
    # 영양제 추천 --------------------------------------------------------
    @staticmethod
    def function_similarity(target_function, comparison_function):
        intersection = set(target_function).intersection(set(comparison_function))
        union = set(target_function).union(set(comparison_function))
        if len(intersection) == len(set(target_function)):
            function_sim = float(1)
        else:
            function_sim = float(len(intersection)/len(union))
        return function_sim
    
    @staticmethod
    def find_selected_code(target, comparison):
        intersection = list(set(target).intersection(set(comparison)))
        if len(intersection) == 0:
            intersection = np.nan 
        return intersection

    @staticmethod
    def find_sim_grp(survey_df, profile_id, check_cols, top_n_percentage=0.4):
        
        survey_idx, survey_row = RecommendModel.find_profile_id_row(survey_df, profile_id) 
        
        # 유사 사용자그룹 
        # sim_sex_age_grp = df[df['profile_id'] != profile_id] # Flask용 코드
        sim_sex_age_grp = survey_df[(survey_df['survey_sex'] == survey_row['survey_sex']) & (survey_df['survey_age_group'] == survey_row['survey_age_group'])]
        
        if survey_row['function_code'] != ['HF00']:
            sim_sex_age_grp['sim_grp'] = sim_sex_age_grp['function_code'].apply(lambda x: RecommendModel.function_similarity(survey_row['function_code'], x))
            
            top_n = int(round(len(sim_sex_age_grp) * top_n_percentage, 0))
            sim_df = sim_sex_age_grp.sort_values(by=['sim_grp'], ascending=False)[:top_n]

            sim_df.drop(index=survey_idx, inplace=True) 
            sim_df.reset_index(drop=True, inplace=True)
            
        else:
            sim_sex_age_grp_surveys = np.array(sim_sex_age_grp[check_cols])
            check_cols_sim = cosine_similarity(sim_sex_age_grp_surveys, sim_sex_age_grp_surveys)
            check_cols_sim_sorted_ind = check_cols_sim.argsort()[:, ::-1]

            top_n = int(round(len(sim_sex_age_grp) * top_n_percentage, 0))
            sim_idxs = check_cols_sim_sorted_ind[survey_idx, :top_n].reshape(-1)
            sim_idxs = sim_idxs[sim_idxs != survey_idx]
            
            sim_df = sim_sex_age_grp.iloc[sim_idxs]
            sim_df.reset_index(drop=True, inplace=True)
            
            sim_df['sim_grp'] = sim_df.index
        
        return sim_df
    
    def filter_product(self, survey_row): #, min_rating_avg=0, min_rating_cnt=0):
            
        # survey_idx, survey_row = RecommendModel.find_profile_id_row(survey_df, profile_id)

        drop_caution_idx_list = []
        for allergy_disease in self.allergy_disease_list:
            if survey_row[allergy_disease] == 1:
                drop_caution_idxs = self.product_df[self.product_df[allergy_disease] == 1].index.tolist()
                drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_pregnancy'] == 1:
            drop_caution_idxs = self.product_df[(self.product_df['P3'] == 1) | (self.product_df['P2'] == 1) | (self.product_df['P1'] == 1)].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_operation'] == 1:
            drop_caution_idxs = self.product_df[self.product_df['OPERATION'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_smoking'] == 1:
            drop_caution_idxs = self.product_df[self.product_df['SMOKE'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
            for idx, ingredients in self.product_df.loc[self.product_df['ingredient_id'].notna(), 'ingredient_id'].items():
                if any(ingredient in self.all_smoker_drop_ingredient_ids for ingredient in ingredients):
                    drop_caution_idx_list.append(idx)
            if survey_row['survey_sex'] == 1:
                drop_caution_idxs = self.product_df[(self.product_df['ingredient_id'] == 424) | (self.product_df['ingredient_id'] == 143)].index.tolist()
                drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_age_group'] == 0:
            drop_caution_idxs = self.product_df[(self.product_df['KIDS'] == 1) & (self.product_df['ADULT'] == 1)].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs) 
        if survey_row['survey_age_group'] == 10:
            drop_caution_idxs = self.product_df[(self.product_df['TEENAGER'] == 1) & (self.product_df['ADULT'] == 1)].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
        if survey_row['survey_sex'] == 1:
            drop_caution_idxs = self.product_df[self.product_df['MALE'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs) 
        if survey_row['survey_age_group'] == 60:
            drop_caution_idxs = self.product_df[self.product_df['OLD'] == 1].index.tolist()
            drop_caution_idx_list.extend(drop_caution_idxs)
             
        filter_product_df = self.product_df.drop(index=list(set(drop_caution_idx_list)))
        
        # print(f'1 : {len(filter_product_df)}')
        
        # recom_ingredient_id_list = recom_top5_ingredient_df['ingredient_id'].tolist()
        recom_ingredient_id_list = survey_row['ingredient_id']
        filter_product_df['product_ingredient_sim'] = filter_product_df['ingredient_id'].apply(lambda x: RecommendModel.function_similarity(recom_ingredient_id_list, x) if isinstance(x, list) else x)
        
        filter_product_df['selected_ingredient'] = filter_product_df['ingredient_id'].apply(lambda x: RecommendModel.find_selected_code(recom_ingredient_id_list, x) if isinstance(x, list) else x)
        filter_product_df['selected_ingredient_cnt'] = 0
        filter_product_df['selected_ingredient_cnt'] = filter_product_df[filter_product_df['selected_ingredient'].notna()]['selected_ingredient'].apply(lambda x: len(x) if isinstance(x, list) else 0)                                 
        filter_product_df.loc[filter_product_df['selected_ingredient_cnt'].notna(), 'selected_ingredient_cnt'].astype(int)
        
        selected_functions = survey_row['function_code'] 
        filter_product_df['product_function_sim'] = filter_product_df['function_code'].apply(lambda x: RecommendModel.function_similarity(survey_row['function_code'], x) if isinstance(survey_row['function_code'], list) else 0)
        
        # # 건강기능 선택했을 경우에만 0인 값 drop
        # if (selected_functions != 'HF00') and (isinstance(selected_functions, list)):    
        #     drop_zero_sim_idxs = filter_product_df[filter_product_df['product_function_sim'] == 0].index.tolist()
        #     filter_product_df.drop(index=drop_zero_sim_idxs, inplace=True)
        #     print(f'2 : {len(filter_product_df)}')
        
        filter_product_df['selected_function_code'] = 0
        filter_product_df['selected_function_code_cnt'] = 0
          
        # # 결측치 제외
        # if (isinstance(selected_functions, list)):
        filter_product_df['selected_function_code'] = filter_product_df['function_code'].apply(lambda x: RecommendModel.find_selected_code(selected_functions, x))
        filter_product_df['selected_function_code_cnt'] = filter_product_df['selected_function_code'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        
        # print(f'3 : {len(filter_product_df)}')
            
        filter_product_df = filter_product_df.sort_values(by=['product_function_sim', 'product_ingredient_sim'], ascending=False)
        filter_product_df.reset_index(drop=True, inplace=True)
        
            
        # 6. 평균 평점이 min_rating_avg점 이상고, 평점이 min_rating_cnt개 이상인 영양제만 추출 - 아직 값이 없음
        # filter_product_df = filter_product_df[(filter_product_df['product_rating_avg'] >= min_rating_avg) & (filter_product_df['product_rating_cnt'] >= min_rating_cnt)]

        filter_product_id_list = filter_product_df['product_id'].tolist()
        
        return filter_product_df


    def calculate_weighted_rating(self, sim_grp_review_df):
        weighted_view = self.weights['visited_at'] * sim_grp_review_df['visited_at']
        weighted_like = self.weights['like_created_at'] * sim_grp_review_df['like_created_at']
        weighted_review_rating = self.weights['review_rating'] * sim_grp_review_df['review_rating']
        weighted_sim_grp = self.weights['sim_grp'] * sim_grp_review_df['sim_grp']
        # weighted_product_function_sim = self.weights['product_function_sim'] * sim_grp_review_df['product_function_sim']
        # weighted_product_ingredient_sim = self.weights['product_ingredient_sim'] * sim_grp_review_df['product_ingredient_sim']
    
        sim_grp_review_df['new_rating'] = weighted_view + weighted_like + weighted_review_rating + weighted_sim_grp # + weighted_product_function_sim + weighted_product_ingredient_sim
        return sim_grp_review_df
    
    def run_recommend_products_function(self, survey_row, recom_min_rating=1):
        recom_top5_ingredient_df = RecommendModel.run_recommend_ingredients_function(self)
        sim_sex_age_grp = RecommendModel.find_sim_grp(self.survey_df, self.profile_id, self.function_list, top_n_percentage=0.4)
        
        filter_product_df = RecommendModel.filter_product(self, survey_row) #, min_rating_avg=0, min_rating_cnt=0)
        
        sim_grp_review_df = pd.merge(sim_sex_age_grp[['profile_id', 'sim_grp']], self.review_df, how='inner', on='profile_id')
        sim_grp_review_df = pd.merge(sim_grp_review_df , filter_product_df[['product_id', 'selected_ingredient', 'selected_ingredient_cnt', 'selected_function_code', 'selected_function_code_cnt', 'product_function_sim', 'product_ingredient_sim']], how='inner', on='product_id')
        # sim_grp_review_df = pd.merge(sim_grp_review_df , filter_product_df['product_id'], how='inner', on='product_id')
        
        sim_grp_review_df = sim_grp_review_df[sim_grp_review_df['review_rating'] >= recom_min_rating]
        
        sim_grp_review_df = RecommendModel.calculate_weighted_rating(self, sim_grp_review_df)
        
        sim_grp_review_df.sort_values(by=['product_function_sim', 'product_ingredient_sim', 'new_rating', 'review_rating'], ascending=False, inplace=True)
        
        recom_product_df = sim_grp_review_df.drop_duplicates(subset=['product_id'], keep='first', ignore_index=True)
        
        recom_product_id_list = recom_product_df['product_id'].tolist()
        
        return recom_product_df # recom_product_id_list
    
#     def check_recommend_products(self, recom_min_rating=1):
#         recom_top5_ingredient_df = RecommendModel.run_recommend_ingredients_function(self)
#         filter_product_df = RecommendModel.filter_product(survey_df, product_df, profile_id, recom_top5_ingredient_df)
#         recom_product_id_list = RecommendModel.run_recommend_products_function(recom_min_rating=1)
#         top_recom_df = pd.concat([filter_product_df[filter_product_df['product_id'] == recom_product_id] for recom_product_id in recom_product_id_list[:top_n]], axis=0)
#         return top_recom_df

    def check_recommend_products(self, recom_min_rating=1, top_n=10):
        recom_top5_ingredient_df = self.run_recommend_ingredients_function()  # 수정된 부분: self를 통해 메서드 호출
        filter_product_id_list, filter_product_df = RecommendModel.filter_product(self, self.survey_df, self.product_df, self.profile_id, recom_top5_ingredient_df)
        recom_product_id_list = self.run_recommend_products_function(recom_min_rating=1)  # 수정된 부분: self를 통해 메서드 호출
        top_recom_df = pd.concat([filter_product_df[filter_product_df['product_id'] == recom_product_id] for recom_product_id in recom_product_id_list[:top_n]], axis=0)
        return top_recom_df

    def recommendation_product_lfm(self, survey_row, recom_top5_ingredient_df):
        # 피클파일 불러오기 및 주요 변수 선언
        profile_id = survey_row['profile_id']
        survey_df = survey_row.to_frame().T # 시리즈를 데이터프레임으로
        
        user_feature_list = [
            'survey_age_group', 'survey_sex', 'survey_pregnancy', 'survey_operation', 'survey_alcohol', 'survey_smoking',
            'HF01', 'HF02', 'HF03', 'HF04', 'HF05', 'HF06', 'HF07', 'HF08', 'HF09', 'HF10',
            'HF11', 'HF12', 'HF13', 'HF14', 'HF15', 'HF16', 'HF17', 'HF18', 'HF19', 'HF20',
            'HF21', 'HF22', 'HF23', 'HF24', 'HF25',
            'DI01', 'DI02', 'DI03', 'DI04', 'DI05', 'DI06', 'DI07', 'DI08', 'DI09', 'DI10',
            'DI11', 'DI12', 'DI13', 'DI14', 'DI15', 'DI16', 'DI17',
            'AL01', 'AL02', 'AL03', 'AL04', 'AL05', 'AL06', 'AL07', 'AL08', 'AL09', 'AL10',
            'AL11', 'AL12', 'AL13', 'AL14', 'AL15', 'AL16', 'AL17', 'AL18', 'AL19', 'AL20',
        ]

       
        # self.function_list = [
        # 'HF01', 'HF02', 'HF03', 'HF04', 'HF05', 'HF06', 'HF07', 'HF08', 'HF09', 'HF10',
        # 'HF11', 'HF12', 'HF13', 'HF14', 'HF15', 'HF16', 'HF17', 'HF18', 'HF19', 'HF20',
        # 'HF21', 'HF22', 'HF23', 'HF24', 'HF25'
        # ]

        # allergy_disease_list = [
        #     'AL01', 'AL02', 'AL03', 'AL04', 'AL05', 'AL06', 'AL07', 'AL08', 'AL09', 'AL10',
        #     'AL11', 'AL12', 'AL13', 'AL14', 'AL15', 'AL16', 'AL17', 'AL18', 'AL19', 'AL20',
        #     'DI01', 'DI02', 'DI03', 'DI04', 'DI05', 'DI06', 'DI07', 'DI08', 'DI09', 'DI10',
        #     'DI11', 'DI12', 'DI13', 'DI14', 'DI15', 'DI16', 'DI17'
        # ]

        # 전처리 및 입력된 DF에서 필요한 column만 추출 - 이전 과정에서 완료됨
        # survey_df.loc[survey_df['survey_sex'] == 0, 'AL05'] = 1
        # survey_df.loc[survey_df['survey_sex'] == 0, 'AL06'] = 1
        # survey_df.loc[(survey_df['survey_sex'] == 1) & (survey_df['DI15'] == 1), 'AL05'] = 1
        # survey_df.loc[(survey_df['survey_sex'] == 1) & (survey_df['DI15'] == 1), 'AL06'] = 1
        # survey_df['ingredient_id'] = survey_df['ingredient_id'].apply(lambda x: x if isinstance(x, list) else [])

        # new_survey_df = survey_df[['profile_id'] + user_feature_list + ['ingredient_id']]

        # new_survey_dict = new_survey_df.to_dict(orient = 'records')[0]

        # profile_id = new_survey_dict['profile_id']
        # del(new_survey_dict['profile_id'])
        # del(new_survey_dict['ingredient_id'])
        
        new_survey_dict = survey_df[user_feature_list].to_dict(orient = 'records')[0]
        new_survey_df = survey_df[['profile_id'] + user_feature_list + ['ingredient_id']]

        # self.user_features_list.append([profile_id, new_survey_dict])
        self.user_features_list.append([survey_row['profile_id'], new_survey_dict])

        temp_id = 99999999
        new_survey_df = pd.concat([new_survey_df, pd.DataFrame({
            'profile_id': temp_id, 'survey_age_group':survey_row['survey_age_group'], 'survey_sex':survey_row['survey_sex'],
            'survey_pregnancy':0, 'survey_operation':0, 'survey_alcohol':0, 'survey_smoking':0,
            'HF01':0, 'HF02':1, 'HF03':0, 'HF04':0, 'HF05':0, 'HF06':0, 'HF07':0, 'HF08':0, 'HF09':0, 'HF10':0,
            'HF11':0, 'HF12':0, 'HF13':0, 'HF14':0, 'HF15':0, 'HF16':0, 'HF17':0, 'HF18':0, 'HF19':0, 'HF20':0,
            'HF21':0, 'HF22':0, 'HF23':0, 'HF24':0, 'HF25':0,
            'DI01':0, 'DI02':0, 'DI03':0, 'DI04':0, 'DI05':0, 'DI06':0, 'DI07':0, 'DI08':0, 'DI09':0, 'DI10':0,
            'DI11':0, 'DI12':0, 'DI13':0, 'DI14':0, 'DI15':0, 'DI16':0, 'DI17':0,
            'AL01':0, 'AL02':0, 'AL03':0, 'AL04':0, 'AL05':0, 'AL06':0, 'AL07':0, 'AL08':0, 'AL09':0, 'AL10':0,
            'AL11':0, 'AL12':0, 'AL13':0, 'AL14':0, 'AL15':0, 'AL16':0, 'AL17':0, 'AL18':0, 'AL19':0, 'AL20':0,
            'ingredient_id':[[]]
        }, index=[0])], ignore_index=True)

        ranking_dict = new_survey_df[user_feature_list].to_dict(orient = 'records')[1]
        
        # del(ranking_dict['profile_id'])
        # del(ranking_dict['ingredient_id'])

        self.user_features_list.append([temp_id, ranking_dict])
        
        # new_survey_df['HF_sum'] = 0 # 왜 요걸로 안하쥬??
        new_survey_df['HF_sum'] = new_survey_df[[
            'HF01', 'HF02', 'HF03', 'HF04', 'HF05', 'HF06', 'HF07', 'HF08', 'HF09', 'HF10',
            'HF11', 'HF12', 'HF13', 'HF14', 'HF15', 'HF16', 'HF17', 'HF18', 'HF19', 'HF20',
            'HF21', 'HF22', 'HF23', 'HF24', 'HF25'
        ]].sum(axis=1)
        
        new_survey_df.loc[new_survey_df['HF_sum'] == 0, 'HF02'] = 1

        # Add the new user to the dataset and provide their features
        self.dataset.fit_partial(users=[profile_id, temp_id], user_features=user_feature_list)
        user_features = self.dataset.build_user_features(self.user_features_list,normalize=True)

        # print(new_survey_df)
        
        # print(profile_id, temp_id)
        
        # Get the user and item mapping dictionary
        user_mapping = self.dataset.mapping()[0]
        item_mapping = self.dataset.mapping()[2]

        # filter_product_id_list, filter_product_df = RecommendModel.filter_product(self, self.survey_df, self.product_df, self.profile_id, recom_top5_ingredient_df)
        
        for idx in [profile_id, temp_id]:
            user_id = user_mapping[idx]
            reverse_item_mapping = {v: k for k, v in item_mapping.items()}
            num_items = max(item_mapping.values()) + 1
            item_indices = list(range(num_items))

            # Predict scores for all items for the given user
            scores = self.model.predict(user_id, item_indices, user_features=user_features, item_features=self.item_features)
            # Get the top N items with the highest scores
            top_items = sorted(zip(item_indices, scores), key=lambda x: -x[1]) [:200]
            # Convert item indices back to item IDs
            product_list = [reverse_item_mapping[item_index] for item_index, _ in top_items]
            
            # recommended_product_list = [product for product in product_list if product in filter_product_id_list]
            # print(len(product_list2), product_list2)


            # Filter recommended items via survey
            profile_row = new_survey_df[new_survey_df['profile_id'] == idx].iloc[-1]
            
            # if recommended ingredient is empty
            if not profile_row['ingredient_id']:

                # if recommended ingredient is empty and health fucntion is also empty
                if profile_row['HF_sum'] == 0:
                    recommended_product_list = []
                    for product in product_list:
                        # print(f'recommend_product_list 0 : {recommended_product_list}')
                        product_row = self.product_df[self.product_df['product_id'] == product].iloc[-1]
                        for allergy_disease in self.allergy_disease_list:
                            cont_var = False
                            if profile_row[allergy_disease] == 1 and product_row[allergy_disease] == 1:
                                cont_var = True
                                break
                        if cont_var == True:
                            continue
                        if profile_row['survey_pregnancy'] == 1 and (product_row['P3'] == 1 or product_row['P2'] == 1 or product_row['P1'] == 1):
                            continue
                        if profile_row['survey_operation'] == 1 and product_row['OPERATION'] == 1:
                            continue
                        if profile_row['survey_smoking'] == 1 and product_row['SMOKE'] == 1:
                            continue
                        if profile_row['survey_age_group'] == 0 and (product_row['KIDS'] == 1 or product_row['ADULT'] == 1):
                            continue
                        if profile_row['survey_age_group'] == 10 and (product_row['TEENAGER'] == 1 or product_row['ADULT'] == 1):
                            continue
                        if profile_row['survey_sex'] == 1 and product_row['MALE'] == 1:
                            continue
                        if profile_row['survey_age_group'] == 60 and product_row['OLD'] == 1:
                            continue
                        recommended_product_list.append(product)
                        # print(f'recommend_product_list 0end : {recommended_product_list}')
                
                # if recommended ingredient is empty BUT health function is present
                else:
                    recommended_product_dict = dict.fromkeys(product_list,0)
                    # print(f'recommended_product_dict no_i : {recommended_product_dict}')
                    for product in product_list:
                        product_row = self.product_df[self.product_df['product_id'] == product].iloc[-1]
                        for function in self.function_list:
                            if profile_row[function] == 1 and product_row[function] == 1:
                                for allergy_disease in self.allergy_disease_list:
                                    cont_var = False
                                    if profile_row[allergy_disease] == 1 and product_row[allergy_disease] == 1:
                                        cont_var = True
                                        break
                                if cont_var == True:
                                    continue
                                if profile_row['survey_pregnancy'] == 1 and (product_row['P3'] == 1 or product_row['P2'] == 1 or product_row['P1'] == 1):
                                    continue
                                if profile_row['survey_operation'] == 1 and product_row['OPERATION'] == 1:
                                    continue
                                if profile_row['survey_smoking'] == 1 and product_row['SMOKE'] == 1:
                                    continue
                                if profile_row['survey_age_group'] == 0 and (product_row['KIDS'] == 1 or product_row['ADULT'] == 1):
                                    continue
                                if profile_row['survey_age_group'] == 10 and (product_row['TEENAGER'] == 1 or product_row['ADULT'] == 1):
                                    continue
                                if profile_row['survey_sex'] == 1 and product_row['MALE'] == 1:
                                    continue
                                if profile_row['survey_age_group'] == 60 and product_row['OLD'] == 1:
                                    continue
                                recommended_product_dict[product] += 1
                                # print(f'recommended_product_dict no_i end : {recommended_product_dict}')
                    recommended_product_list = []
                    for i in range(5,-1,-1):
                        if len(recommended_product_list) + len([k for k, v in recommended_product_dict.items() if v == i]) < 100:
                            recommended_product_list += [k for k, v in recommended_product_dict.items() if v == i]
                        else:
                            # recommended_product_list += random.sample([k for k, v in recommended_product_dict.items() if v == i], 100 - len(recommended_product_list))
                            recommended_product_list += [k for k, v in recommended_product_dict.items() if v == i] # 여기!!!!!!!!!!!!!!
                            break
                            
            # recommended ingredient is present (health function is already utilized during ingredient recommendation)
            else:
                recommended_product_dict = dict.fromkeys(product_list,0)
                for product in product_list:
                    product_row = self.product_df[self.product_df['product_id'] == product].iloc[-1]
                    for ingredient in profile_row['ingredient_id']:
                        if ingredient in product_row['ingredient_id']:
                            for allergy_disease in self.allergy_disease_list:
                                cont_var = False
                                if profile_row[allergy_disease] == 1 and product_row[allergy_disease] == 1:
                                    cont_var = True
                                    break
            
                            if cont_var == True:
                                continue
                            if profile_row['survey_pregnancy'] == 1 and (product_row['P3'] == 1 or product_row['P2'] == 1 or product_row['P1'] == 1):
                                continue
                            if profile_row['survey_operation'] == 1 and product_row['OPERATION'] == 1:
                                continue
                            if profile_row['survey_smoking'] == 1 and product_row['SMOKE'] == 1:
                                continue
                            if profile_row['survey_age_group'] == 0 and (product_row['KIDS'] == 1 or product_row['ADULT'] == 1):
                                continue
                            if profile_row['survey_age_group'] == 10 and (product_row['TEENAGER'] == 1 or product_row['ADULT'] == 1):
                                continue
                            if profile_row['survey_sex'] == 1 and product_row['MALE'] == 1:
                                continue
                            if profile_row['survey_age_group'] == 60 and product_row['OLD'] == 1:
                                continue
                            recommended_product_dict[product] += 1
                
                recommended_product_list = []
                for i in range(5,-1,-1):
                    if len(recommended_product_list) + len([k for k, v in recommended_product_dict.items() if v == i]) < 100:
                        recommended_product_list += [k for k, v in recommended_product_dict.items() if v == i]
                    else:
                        # recommended_product_list += random.sample([k for k, v in recommended_product_dict.items() if v == i], 100 - len(recommended_product_list))
                        recommended_product_list += [k for k, v in recommended_product_dict.items() if v == i] # 여기!!!!!!!!!!!!!!
                        break

            globals()["profile_{}".format(idx)] = recommended_product_list # [:5]


        return globals()["profile_{}".format(profile_id)], globals()["profile_{}".format(temp_id)] # , product_list
    
    
        #     check_name_dict = RecommendModel.create_check_name_dict(recom_ingredient_df, 5) 
        # check_prefix = set()
        
        # for idx, survey_row in recom_ingredient_df.iterrows():
        #     name_value = survey_row['ingredient_name']
        #     prefix = name_value[:5]
            
        #     if prefix in check_prefix:
        #         continue
        #     check_prefix.add(prefix)
            
        #     if prefix in check_name_dict:
        #         values = check_name_dict[prefix]
        #         selected_value = random.choice(values)
        #         drop_value = recom_ingredient_df[(recom_ingredient_df['ingredient_name'].str.startswith(prefix)) & (recom_ingredient_df['ingredient_name'] != selected_value)].index
        #         recom_ingredient_df.drop(drop_value, inplace=True)
        #         recom_ingredient_df.reset_index(drop=True, inplace=True)