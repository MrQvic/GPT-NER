import os
from base_access import AccessBase
from logger import get_logger
import json
import argparse
from dataset_name import FULL_DATA
import random

random.seed(1)
logger = get_logger(__name__)

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mrc-dir", type=str, help="directory for the mrc input")
    parser.add_argument("--mrc-name", type=str, help="file name for the mrc input")
    parser.add_argument("--gpt-dir", type=str, help="directory for the gpt input")
    parser.add_argument("--gpt-name", type=str, help="file name for the gpt input")
    parser.add_argument("--data-name", type=str, help="dataset name for the input")
    parser.add_argument("--write-dir", type=str, help="directory for the output")
    parser.add_argument("--write-name", type=str, help="file name for the output")
    
    return parser

def read_mrc_data(dir_, prefix="test"):
    file_name = os.path.join(dir_, f"mrc-ner.{prefix}")
    return json.load(open(file_name, encoding="utf-8"))

def read_results(dir_, prefix="test"):
    print(f"Reading results from {os.path.join(dir_, prefix)}")
    file_name = os.path.join(dir_, prefix)
    file = open(file_name, "r")
    results = []
    for line in file:
        results.append(line.strip())
    file.close()
    return results

def transferPrompt(mrc_data, gpt_results, data_name="CONLL"):
    print("Creating verification prompts...")
    
    def get_words(labeled_sentence):
        word_list = []
        words = labeled_sentence.strip().split()
        flag = False
        last_ = ""
        for idx_, word in enumerate(words):
            if len(word) > 2 and word[0] == '@' and word[1] == '@':
                last_ = idx_
                flag = True
            if flag and len(word) > 2 and word[-1] == '#' and word[-2] == '#':
                word_list.append((" ".join(words[last_:idx_+1])[2:-2], last_))
                flag = False
        return word_list

    prompts = []
    entity_index = []
    prompts_nums = []
    
    for item_idx in range(len(mrc_data)):
        print(f"Processing item {item_idx + 1}/{len(mrc_data)}")
        
        item_ = mrc_data[item_idx]
        context = item_["context"]
        origin_label = item_["entity_label"]
        transfered_label, sub_prompt = FULL_DATA[data_name][origin_label]
        upper_transfered_label = transfered_label[0].upper() + transfered_label[1:]
        entity_list = get_words(gpt_results[item_idx].strip())

        prompts_num = 0
        for entity, entity_idx in entity_list:
            prompt = f"Verify if this word is a {transfered_label} entity. {upper_transfered_label} entities {sub_prompt}.\n\n"
            prompt += f"Sentence: {context}\nWord: \"{entity}\"\n"
            prompt += f"Is this a {transfered_label} entity? Answer only 'yes' or 'no'."
            
            prompts.append(prompt)
            entity_index.append((entity_idx, len(entity.strip().split())))
            prompts_num += 1
            
            print(f"\nPrompt {prompts_num}:")
            print("------------------------")
            print(prompt)
            print("------------------------")
            
        prompts_nums.append(prompts_num)
    
    return prompts, entity_index, prompts_nums

def construct_results(gpt_results, entity_index, prompts_num, verify_results):
    print("Constructing final results...")
    
    def justify(string_):
        if len(string_) >= 3 and string_[:3].lower() == "yes":
            return "yes"
        if len(string_) >= 2 and string_[:2].lower() == "no":
            return "no"
        return ""

    results = []
    start_ = 0
    for idx_, item in enumerate(gpt_results):
        print(f"Processing result {idx_ + 1}/{len(gpt_results)}")
        
        words_list = item.strip().split()
        now_num = prompts_num[idx_]
        for sub_idx in range(now_num):
            num = start_ + sub_idx
            verification = verify_results[num].strip()
            print(f"Verification result: {verification}")
            
            if justify(verification) == "yes":
                continue
            elif justify(verification) == "no":
                start_index, len_ = entity_index[num]
                words_list[start_index] = words_list[start_index][2:]
                words_list[start_index+len_-1] = words_list[start_index+len_-1][:-2]
        start_ += now_num
        results.append(" ".join(words_list))
    return results

def write_file(labels, dir_, last_name):
    print("Writing results...")
    file_name = os.path.join(dir_, last_name)
    file = open(file_name, "w")
    for line in labels:
        file.write(line.strip()+'\n')
    file.close()

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    openai_access = AccessBase(
        model="llama3.1",  # or your chosen Ollama model
        temperature=0.0,
        max_tokens=512
    )

    mrc_test = read_mrc_data(dir_=args.mrc_dir, prefix=args.mrc_name)
    gpt_results = read_results(dir_=args.gpt_dir, prefix=args.gpt_name)

    prompts, entity_idx, prompts_nums = transferPrompt(
        mrc_data=mrc_test, 
        gpt_results=gpt_results, 
        data_name=args.data_name
    )
    
    verify_results = openai_access.get_multiple_sample(prompts)
    
    final_results = construct_results(
        gpt_results=gpt_results,
        entity_index=entity_idx,
        prompts_num=prompts_nums,
        verify_results=verify_results
    )

    write_file(labels=final_results, dir_=args.write_dir, last_name=args.write_name)