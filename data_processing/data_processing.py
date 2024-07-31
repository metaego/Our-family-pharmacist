import pandas as pd
import numpy as np
import re
import json
from pandas import json_normalize
from konlpy.tag import Hannanum
from stopwords import stopwords
from updated_nouns_words import updated_nouns_words

# 쉼표를 기준으로 특정 컬럼의 행을 나누는 함수
def normalize_table(df, split_column_name):
    # 새로운 데이터프레임을 위한 빈 리스트 생성
    new_data = []
    for row in range(len(df)):
        codes = df[split_column_name].iloc[row].split(',')  # 쉼표를 기준으로 분리
        for code in codes:
            new_data.append(list(df.iloc[row][:-1]) + [code])  # 각 행에서 마지막 열을 제외한 값과 code를 함께 추가

    # 새로운 데이터프레임 생성
    new_df = pd.DataFrame(new_data, columns=list(df.columns[:-1]) + [split_column_name])  # 새로운 열 추가
    return new_df



# 영양성분명에서 개별인정원료의 인정번호 추출해서 개별 컬럼에 저장하고, 인정번호가 제거된 영양성분명 개별 컬럼에 저장된 df 구하는 함수 정의
def extract_auth_num(df, raw_name_col, cleaned_name_col, auth_num_col):
    # 기능성 원료 인정번호 패턴
    auth_num_pattern = r'\([^()]*제[0-9\-]+호[^()]*\)'

    cleand_auth_nums = []
    cleaned_names = []

    for raw_name in df[raw_name_col]:
    # 1. 'ingredient_raw_name'컬럼 텍스트에서 개별인정원료의 인정번호 추출
        auth_num_match = re.search(auth_num_pattern, raw_name)
        if auth_num_match:
            auth_num = re.findall(r'제[0-9\-]+호', auth_num_match.group()) # group()은 re.search()의 결과인 object에서 실제로 매칭된 문자열을 반환
            auth_num_str = ''.join(auth_num) # findall은 리스트로 반환하기 때문에 문자열로 변환
            cleaned_auth_num_str = re.sub(r'\s', '', auth_num_str) # whitespace 삭제
            cleand_auth_nums.append(cleaned_auth_num_str) # cleand_auth_nums 리스트에 추가
        else:
            cleand_auth_nums.append(np.nan) # 개별인정원료 인정번호가 없을 경우 결측치로 대체
        
        # 2. 'ingredient_raw_name'컬럼 텍스트에서 기능성 원료 인정번호 삭제
        cleaned_name = re.sub(auth_num_pattern, '', raw_name)
        # cleaned_names 리스트에 추가
        cleaned_names.append(cleaned_name) 

    # 기능성 원료 인정번호만 추출한 문자열이 담긴 리스트를 컬럼값으로 추가
    df[auth_num_col] = cleand_auth_nums

    # 기능성 원료 인정번호 삭제된 문자열이 담긴 리스트를 컬럼값으로 추가 => 서비스상에 노출될 텍스트
    df[cleaned_name_col] = cleaned_names
    return df


# `ingredient_grp_name` 컬럼 생성하는 함수 정의 - 수정함!
def create_ingredient_grp_name(df, origin_name_col, grp_name_col, update_ingredient_grp_name_dict, cleaned_name_col=None):
    bracket_strs = []
    grp_names = []
    for name in df[origin_name_col]:
        grp_name_mask = r'\([^)]+\)' # 소괄호와 그 안의 모든 문자열
        if re.search(r'\[[^\]]+\]', name):
            grp_name_mask = r'\([^)]+\)\[[^\]]+\]' # 소괄호와 대괄호와 안의 모든 문자열
        # elif re.search(r'\<[^\>]+\>', name):
        #     grp_name_mask = r'\<[^\>]+\>' # 꺽쇠 기호 안의 모든 문자열 - `ingredient_name` 처리에서 소괄호로 대체함
        
        grp_name = re.sub(grp_name_mask, '', name)
        grp_name = grp_name.strip() # 앞 뒤 공백 삭제
        grp_names.append(grp_name)
        
        if cleaned_name_col is not None:     
            bracket_str = re.search(grp_name_mask, name) 
            if bracket_str:
                bracket_strs.append(bracket_str.group())
            else:
                bracket_strs.append(np.nan)
    
    df[grp_name_col] = grp_names
    
    if cleaned_name_col is not None:        
        df[cleaned_name_col] = bracket_strs
        
    for key, values in update_ingredient_grp_name_dict.items():
        for value in values:
            df.loc[df[grp_name_col].str.contains(value), grp_name_col] = key
    
    return df


# 데이터프레임의 특정 컬럼값에 존재하는 특수문자를 리스트 형태로 가져오는 함수정의
def find_special_chars(df, col_name):
    # notnull()로 결측치가 아닌 문자열만 확인해야 오류가 나지 않는다.
    df = df.loc[df[col_name].notnull(), col_name]
    
    # 해당 컬럼의 모든 문자열 결합
    combined_text = ' '.join(df)
    
    # 특수문자만 추출
    special_chars = re.findall(r'[^가-힣A-Za-z0-9\s]', combined_text)
    
    # 추출된 특수문자를 집합(set)으로 변환하여 중복 제거 후 다시 list로 가져온다.
    unique_special_chars = list(set(special_chars))
    
    return unique_special_chars


# 특정 문자(열)가 들어가있는 데이터프레임 생성하는 함수정의
def find_chars_df(df, col_name_list, check_chars_list):
    check_chars_df = pd.DataFrame(columns=df.columns) # 결과를 저장할 데이터프레임
    
    for col_name in col_name_list:
        for char in check_chars_list:
            mask_1 = df[col_name].notnull()
            mask_2 = df[col_name].str.contains(char, regex=False) # 특수 문자를 처리하기 위해 `regex=False` 사용
             
            if mask_2.any():
                df2 = df[(mask_1) & (mask_2)]
                check_chars_df = pd.concat([check_chars_df, df2], axis=0, ignore_index=True)
                
            else:
                print(f'{col_name} 컬럼값에 "{char}" 문자열이 없습니다.')
                
    # 중복 제거
    check_chars_df.drop_duplicates(subset=col_name_list, inplace=True, ignore_index=True)
    
    return check_chars_df


# 정규식을 이용해 텍스트 정제하여 데이터프레임 생성
def cleaned_product_df_data(df, col_name, cleaned_col_name):
    # null값일 경우 정규식 전처리가 불가능하기 때문에 null값이 없는 행만 전처리 진행
    data = df[df[col_name].notnull()][col_name]
    
    # 전처리하는 행의 인덱스를 리스트로 저장
    index_list = data.index.to_list()
    
    # 정제된 텍스트를 넣어줄 빈 리스트 생성
    cleaned_text_list = []
    
    # 데이터프레임의 컬럼값들을 순회하기 위해 for 구문 사용
    for cleaned_text in data:
        
        # 'null' 제거
        if 'null' in cleaned_text:
            cleaned_text = re.sub(r'null', '', cleaned_text)
        
        # '(국문)' 또는 '[국문]' 또는 '(영문)' 또는 '[영문]'이라는 문자 제거
        if '(국문)' in cleaned_text or '(영문)' in cleaned_text or '[국문]' in cleaned_text or '[영문]' in cleaned_text:
            # '(영문)' 또는 '[영문]'과 해당 문자열 뒤에 모든 문자열 제거
            cleaned_text = re.sub(r'(\(영문\)|\[영문\])[\s\S]*', '', cleaned_text)
            # '(국문)' 또는'[국문]'이라는 문자 제거
            cleaned_text = re.sub(r'\(국문\)|\[국문\]', '', cleaned_text)
            
        # '(기타기능II)' 또는 '(기타II 등급)' 또는 '(기타 II)' 또는 '(기타Ⅱ)' 또는 '(생리활성기능)' 또는'(생리활성기능2등급)'이라는 문자가 있을 경우 띄어쓰기로 대체
        if '(기타' in cleaned_text or '(생리활성기능' in cleaned_text:
            cleaned_text = re.sub(r'\(기타[^)]*\)|\(생리활성기능[^)]*\)', ' ', cleaned_text)
            
        # '&#8228;' 문자 ' '로 대체
        if '&#8228;' in cleaned_text:
            cleaned_text = re.sub(r'&#8228;', ' ', cleaned_text)
        
        # 영문 사이에 "'" 기호가 사용된 경우가 아니면 제거
        if "'" in cleaned_text:
            alphabet_pattern = r"[a-zA-Z]"
            cleaned_text = re.sub(alphabet_pattern, lambda x: x.group(0).replace("'", "\x00"), cleaned_text)
            cleaned_text = re.sub(r"\'", "", cleaned_text)
            cleaned_text = re.sub(r"\x00", "\'", cleaned_text)
            
        if '?' in cleaned_text:
            cleaned_text = re.sub(r'영\?유아', '영\·유아', cleaned_text)
            cleaned_text = re.sub(r'-\?', '', cleaned_text)
            cleaned_text = re.sub(r'\?-', '', cleaned_text)
            cleaned_text = re.sub(r'\n-\?', '\n', cleaned_text)
            cleaned_text = re.sub(r'섭\?십시오', '섭취하십시오', cleaned_text)
            cleaned_text = re.sub(r'드\?시오', '드시오', cleaned_text)
            
            # 위 예외사항을 제외하고 '?' 기호는 ' '로 대체
            cleaned_text = re.sub(r'\?', ' ', cleaned_text)
            
        # '-'가 문장 구분자로 사용되는 경우에만 제거(그 외에는 남겨 둔다)
        if '-' in cleaned_text:
            # 구분자로 사용되는 '\n-'의 경우 제거
            cleaned_text = re.sub(r'\n\-', '\n', cleaned_text)
            # '-'로 시작하는 경우 제거 
            cleaned_text = re.sub(r'^[\-]', '', cleaned_text)
            
        # '/' 기호가 문장 구분자로 사용하는 경우는 제거
        if '/' in cleaned_text:
            number_pattern = r'\d+/\d+'  # 숫자 사이의 '/'
            
            word_patterns = [
                r'구아검/구아검가수분해물',
                r'식물스테롤/식물스테롤에스테르',
                r'이눌린/치커리추출물',
                r'키토산/키토올리고당',
                r'루테인/지아잔틴',
                r'판토텐산/비오틴',
                r'엠에스엠/MSM',
                r'NAG/N-아세틸글루코사민'   
            ]
            
            bracket_pattern = r'\[.*?/.*?\]'
            
            # [] 안의 '/'가 있는 경우, 숫자 사이에 분수 기호로 '/'가 있는 경우, word_patterns 문자열과 같이 '/'가 있는 경우
            # 다른 문자열로 대체
            cleaned_text = re.sub(bracket_pattern, lambda x: x.group(0).replace('/', '\x00'), cleaned_text)
            cleaned_text = re.sub(number_pattern, lambda x: x.group(0).replace('/', '\x00'), cleaned_text)
            for word_pattern in word_patterns:
                cleaned_text = re.sub(word_pattern, lambda x: x.group(0).replace('/', '\x00'), cleaned_text)
            
            # 남은 '/'기호를 '\n'으로 대체    
            cleaned_text = re.sub(r'\/', '\n', cleaned_text)
            
            # temp 문자열을 원래대로 되돌림
            cleaned_text = re.sub(r'\x00', '\/', cleaned_text)

        if '_' in cleaned_text: 
            cleaned_text = re.sub(r'\_', ' ', cleaned_text)
            
        # 영문 사이에 '`' 기호가 사용된 경우가 아니면 제거
        if '`' in cleaned_text:
            alphabet_pattern = r'[a-zA-Z]'
            cleaned_text = re.sub(alphabet_pattern, lambda x: x.group(0).replace('`', '\x00'), cleaned_text)
            cleaned_text = re.sub(r'\`', '', cleaned_text)
            cleaned_text = re.sub(r'\x00', '\`', cleaned_text)
        
        # ']'가 '}'로 오타난 경우 예외사항 처리    
        if '}' in cleaned_text:
            word_patterns = [r'\[은행잎추출물\}', r'\[회화나무열매추출물\}', r'\[비타민 C\}', r'\[비타민 B12\}']
            for word_pattern in word_patterns:
                cleaned_text = re.sub(word_pattern, lambda x: x.group(0).replace('}', ']'), cleaned_text)
                
        if '®' in cleaned_text:
            cleaned_text = re.sub(r'\®', '\Ⓡ', cleaned_text)
            
        if '₂' in cleaned_text:
            cleaned_text = re.sub(r'\₂', '\2', cleaned_text)
            
        if '∙' in cleaned_text:
            # 예외사항 처리
            cleaned_text = re.sub(r'영∙\유아', '영\·유아', cleaned_text)
            # '\n'으로 대체
            cleaned_text = re.sub(r'\∙', '\n', cleaned_text)

        # '⦁' -> '⋅'로 대체 후 일괄처리
        cleaned_text = re.sub(r'\⦁', '\⋅', cleaned_text)
        # 'ㆍ' -> '⋅'로 대체 후 일괄처리
        cleaned_text = re.sub(r'\ㆍ', '\⋅', cleaned_text)
        if '⋅' in cleaned_text:
            # 예외사항 처리
            cleaned_text = re.sub(r'영\⋅유아', '영\·유아', cleaned_text)
            cleaned_text = re.sub(r'간\⋅신장⋅심장질환', '간\·신장·심장질환', cleaned_text)
            cleaned_text = re.sub(r'뮤코다당\⋅단백', '뮤코다당\·단백', cleaned_text)
            # '\n'으로 대체
            cleaned_text = re.sub(r'⋅', '\n', cleaned_text)
            
        if 'ㅇ' in cleaned_text:
            # 예외사항 처리
            cleaned_text = re.sub(r'성분\ㅇ르', '성분을', cleaned_text)
            # '제거
            cleaned_text = re.sub(r'\ㅇ', '', cleaned_text)
         
        if '．' in cleaned_text:
            # 예외사항 처리
            cleaned_text = re.sub(r'[0-9]+[\．]', lambda x: x.group(0).replace('．', '.'), cleaned_text)
            # '제거
            cleaned_text = re.sub(r'\．', '\n', cleaned_text)
            
        #  '〔', '〕' 일 경우 '[', ']'으로 대체하여 일괄처리
        cleaned_text = re.sub(r'\〔', '\[', cleaned_text)  
        cleaned_text = re.sub(r'\〕', '\]', cleaned_text) 
        # 예외처리 후 대괄호 삭제    
        cleaned_text = re.sub(r'\][a-zA-Z0-9가-힣\s]+', lambda x: x.group(0).replace(']', ']\n'), cleaned_text)
        
        cleaned_text = re.sub(r'\[', '', cleaned_text)
        cleaned_text = re.sub(r'\]', '', cleaned_text)        
        
        # 특수문자 숫자 -> 숫자 처리
        cleaned_text = re.sub(r'\１', '1', cleaned_text)
        cleaned_text = re.sub(r'\５', '5', cleaned_text)
        cleaned_text = re.sub(r'\７', '7', cleaned_text)
             
        # '(가)' or '[가]' 와 같이 소괄호와 대괄호 안에 '가', '나', '다'... 만 있을 경우 제거
        # 괄호 안에 공백이 같이 있을 경우 함께 제거 필요
        cleaned_text = re.sub(r'\[[가나다라마바사아자차카타파하\s]]*\]|\([가나다라마바사아자차카타파하\s]*\)', '', cleaned_text)
        
        # '(1)' 소괄호와 대괄호 안에 숫자만 있을 경우 => '\n'으로 대체
        # 괄호 안에 숫자와 공백이 같이 있을 경우 함께 처리 필요
        cleaned_text = re.sub(r'[\n]*(\[[0-9\s]*\])|[\n]*(\([0-9\s]*\))', '\n', cleaned_text)
        
        # '1)', '2)'와 같은 문자열 => '\n'으로 대체
        cleaned_text = re.sub(r'([\n]*[0-9]+\))', '\n', cleaned_text)
        
        # '1.' 같이 숫자 뒤에 '.'이 있을 경우 => '\n'으로 대체
        cleaned_text = re.sub(r'[\n]*[0-9]+[.]', '\n', cleaned_text)
        
        # 구분자를 나타내는 숫자, 한글 특수문자 -> '\n'으로 대체
        cleaned_text = re.sub(r'[ⓛ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑴⑵⑶⑷⑸⑹⑺⑻⓵⓶⓷⓻⓼➀➁➂➃➅➆㉮㉯㉰㉱㉮㉯㉰㉱]+', '\n', cleaned_text)
        
        # 구분자를 나타내는 경우 -> '\n'으로 대체
        cleaned_text = re.sub(r'[\■\○\●\*\–\ㅍ\／]+', '\n', cleaned_text)
        
        # '‘', '’', '“', '”', '"' 일 경우 ''으로 대체하여 제거
        cleaned_text = re.sub(r'[\‘\’\"\“\”]+', '', cleaned_text)  
        
        #  '，' -> ','으로 대체
        cleaned_text = re.sub(r'\，', '\,', cleaned_text)  
        
        #  '：' -> ':'으로 대체 후 일괄 처리
        cleaned_text = re.sub(r'\，', '\,', cleaned_text)    
        
        # # '+R-45' 예외 상황 처리 => ''으로 대체하여 제거
        # cleaned_text = re.sub(r'\+R-45', '', cleaned_text) 
        
        # '섭취 시 주의사항 : ' 예외 상황 처리 => ''으로 대체하여 제거
        cleaned_text = re.sub(r'섭취 시 주의사항 : ', '', cleaned_text) 
        
        # '=' 특수문자 제거
        cleaned_text = re.sub(r'\=', '', cleaned_text) 
        
        # '임산부.수유부' 예외 사항 처리 => '.' 기호를 ','로 대체
        cleaned_text = re.sub(r'임산부\.수유부', '임산부, 수유부', cleaned_text)
        
        # '&', '․', '・', '‧', '·', '‧' '･', '•', '𐩐' 특수문자 하나로 통일 => '·'
        cleaned_text = re.sub(r'[\․\·\‧\･\‧\・\&\•\･]+', '·', cleaned_text)
        
        # 특수문자 제거
        # 1. 소괄호 안에 특수 문자가 있는 경우, 소괄호와 그 안의 특수문자를 제거        
        # 2. 예외사항을 제외한 모든 특수문자 => '\n'로 대체
        cleaned_text = re.sub(r'(?!\([^)]+\))[^a-zA-Z0-9가-힣\s\n\)\<\>\-\.\,\:\·β\ß\+\/\~\Ⓡ\±\℃\™\∼\㈜\%]+', '\n', cleaned_text)

        # '다', '음', '오' 다음에 ',' 이 오는 경우 ',' => ',' 를 '\n'로 대체
        cleaned_text = re.sub(r'다\,+[\n]*', '다\n', cleaned_text)
        cleaned_text = re.sub(r'음\,+[\n]*', '음\n', cleaned_text)
        cleaned_text = re.sub(r'오\,+[\n]*', '오\n', cleaned_text)
    
        # linebreak 전후에 whitespace 제거
        cleaned_text = re.sub(r'\n[\s]+', '\n', cleaned_text)
        cleaned_text = re.sub(r'[\s]+\n', '\n', cleaned_text)     
        # white space가 2번이상 나올 경우 ' ' 로 대체   
        cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)
        # linebreak 이후 '-' 기호 '\n' 로 대체
        cleaned_text = re.sub(r'[\n]+[\s\-\)]+', '\n', cleaned_text)
        # white space 뒤에 '-' 기호가 나올경우 ' '띄어쓰기로 대체
        cleaned_text = re.sub(r'[\s]+[\-]', ' ', cleaned_text)
        
        # 양쪽 공백문자 제거, 탭 제거
        cleaned_text = cleaned_text.strip()   
        
        # # '\n'기준으로 split
        # cleaned_text = cleaned_text.split('\n')
        
        # '·', '-', '+', whitespace로 시작할 경우 제거
        cleaned_text = re.sub(r"^[\·\-\+\s]+", "", cleaned_text)
        # cleaned_text = [re.sub(r"^[\·\-\+\s]+", "", x) for x in cleaned_text]
            
        # 텍스트 정제후 데이터를 리스트에 추가
        cleaned_text_list.append(cleaned_text)
        
    
    # 기존 데이터프레임에 정제된 데이터가 담길 수 있게 컬럼 생성 후 값 추가
    df[cleaned_col_name] = np.nan
    
    for idx in range(len(index_list)):
        # 데이터프레임의 열에 리스트를 할당
        df.at[index_list[idx], cleaned_col_name] = cleaned_text_list[idx]
        
    # # 문장 내 중복 제거
    # def remove_duplicates_preserve_order(seq):
    #     seen = set()
    #     return [x for x in seq if not (x in seen or seen.add(x))]
    
    # df[cleaned_col_name] = df[cleaned_col_name].apply(lambda x: '\n'.join(remove_duplicates_preserve_order(x.split('\n'))) if isinstance(x, str) else x)
        
    return df, cleaned_text_list

# Hannanum으로 명사 분석하는 함수 정의
def process_with_hannanum_for_stopwords(words, stopwords, updated_nouns_words):
    hannanum = Hannanum()
    nonus_words = []
    for word in words:
        # nonus = extract_nouns(hannanum, word)
        nonus = hannanum.nouns(word)
        nonus_word = ' '.join(nonus)
        # 해당 리스트에 없을 경우 문자열로 변환 / 있을 경우에는 원래 문자열 그대로 word로 지정
        if nonus_word in updated_nouns_words: 
            nonus_word = word
            
        if nonus_word not in stopwords: # 불용어 제거
            nonus_words.append(nonus_word)
            
    nonus_words = ' '.join(nonus_words) # 문자열로 변환
    return nonus_words

# 불용어를 확인하기 위한 text 전처리와 Hannanum 명사 분석하는 함수정의
def process_text_for_stopwords(text_list, stopwords, updated_nouns_words):
    # 텍스트 리스트를 평탄화하여 하나의 리스트로 변환
    flatten_list = [text for sublist in text_list for text in sublist.split('\n')]
    
    # 특수문자를 ' '로 대체하고 단어별로 split
    cleaned_data = [re.sub(r'[^가-힣A-Za-z0-9]', ' ', x) for x in flatten_list]
    cleaned_data = [x.split() for x in cleaned_data]
    
    # 중복 제거
    check_text_df = pd.DataFrame({'origin_text': flatten_list, 'word_text': cleaned_data})
    check_text_df.drop_duplicates(subset=['origin_text'], inplace=True, ignore_index=True)
    
    # Hannanum 명사 분석
    check_text_df['hannanum'] = check_text_df['word_text'].apply(lambda words: process_with_hannanum_for_stopwords(words, stopwords, updated_nouns_words))
    
    return check_text_df


# 형태소 분석기로 건강기능, 주의사항 content 관련 컬럼의 텍스트를 명사화하는 함수 정의
def created_text_to_nonus(df, text_col, text_nonus_col):
    global stopwords
    
    hannanum = Hannanum()
    
    cleaned_function_datas = []
    
    for text in df[text_col]:
        text_lists = []
        if pd.notnull(text): # 결측치가 아닐 경우 - 리스트일 경우
            for line in text.split('\n'):
                # 특수문자 제거 및 단어별로 분리
                clean_words = [re.sub(r'[^가-힣A-Za-z0-9]', ' ', line).split()]

                # 형태소 분석을 통해 명사 추출 및 불용어 제거
                nonus_words = []
                for words in clean_words:
                    for word in words:
                        nonus_word = ' '.join(hannanum.nouns(word))
                        if nonus_word in updated_nouns_words: 
                            nonus_word = word
                        if nonus_word not in stopwords: # 불용어 제거
                            nonus_words.append(nonus_word)
                            
                text_lists.append(' '.join(nonus_words))
        else:
            text_lists = text
        cleaned_function_datas.append(text_lists)

    # 새로운 컬럼에 명사화된 TEXT 데이터 추가
    df[text_nonus_col] = cleaned_function_datas
    df[text_nonus_col] = df[text_nonus_col].apply(lambda x : re.sub(r'\,', '', ', '.join(x)) if isinstance(x, list) else np.nan)

    return df


def create_dict_col(df, col_name, code_dict):
    for key, values in code_dict.items():
        df[f'{key}'] = 0
        for value in values:
            df.loc[(df[col_name].notnull())& (df[col_name].str.contains(value)), [f'{key}']] = 1
    return df


# 건강기능 코드 컬럼에 모든 행이 0인 경우가 있는지 확인하는 함수
def check_zero_value(df, code_dict):
    # 확인할 컬럼명 리스트에 담기
    check_cols = list(code_dict.keys())
    
    # 각 행별로 해당 컬럼의 모든 값이 0인지 확인하는 mask 생성
    mask = (df[check_cols] == 0).all(axis=1)
    
    # 행의 모든 값이 0인 경우 행 인덱스를 리스트에 추가
    zero_idx_list = mask[mask].index.tolist()
    
    # 분류가 하나도 되지 않은 행만 가져와 데이터프레임 생성
    check_zero_value_df = df.loc[zero_idx_list]
    
    return check_zero_value_df


def create_json_code_col(df, code_list, code_json_col):    
    # 코드 JSON 컬럼 데이터 생성
    # key : 코드(코드컬럼명), value : 해당 영양성분 데이터프레임 행의 코드컬럼값(0 또는 1)
    code_json = []
    for idx in range(len(df)):
        code_dict_data = {}
        for code in code_list:
            code_dict_data[code] = df.iloc[idx][code]
        code_json.append(code_dict_data)
    
    # 코드 JSON 컬럼 - dict 형태로 생성
    df[code_json_col] = code_json
    
    return df

# com_code table 생성하는 함수 정의
def expand_codes(df, pk_col, code_col, com_code_grp_dict):
    expanded_rows = []

    for idx, row in df.iterrows():
        id = row[pk_col]
        codes_dict = row[code_col]
        
        for code, value in codes_dict.items():
            if value == 1:
                for com_code_grp, com_code_rule in com_code_grp_dict.items():
                    if re.sub(r'[0-9]', '', code) in com_code_rule:
                        expanded_rows.append({pk_col: id, 'com_code_grp': com_code_grp, 'com_code': code})

    return pd.DataFrame(expanded_rows)

