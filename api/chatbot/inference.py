import os, copy, json, torch


def change_format(answers):
    dataset = {}
    for answer in answers:
        dataset[answer.input] = {'index': answer.pk - 1, 'answer': answer.output, 'query': answer.query}
    return dataset


def log_save(uid, query, dataset, top_idx_list, preds, idx_dic):
    output = []
    for top in top_idx_list:
        data = dataset[idx_dic[top]]
        question = data.input
        idx = data.pk
        answer = data.output
        output.append([idx, question, answer, preds[top] / 5])
    answer_dict = {str(i): {"sentence": str(int(output[i][3] * 100) / 100) + ": " + output[i][1], "num": output[i][0],
                 "output": output[i][2], "pred": output[i][3]} for i in range(len(top_idx_list))}
    log_dict = copy.deepcopy(answer_dict)
    log_writer(uid, query, log_dict)
    return


def log_writer(uid, query, output):
    log_dict = dict()
    log_dir = 'api/chatbot/log'
    log_name = f"{uid}.json"
    log_path = os.path.join(log_dir, log_name)
    context = []
    last_index = '0'
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            prior_context = json.load(f)
            last_index = list(prior_context.keys())[-1]
            context = prior_context[last_index]['context'].copy()
            log_dict = prior_context
            last_index = str(int(last_index)+1)
    context.append(query)
    context.append(output['0']['output'])
    log_dict[last_index] = dict()
    log_dict[last_index]['context'] = context
    log_dict[last_index]['output'] = output
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_dict, f, ensure_ascii=False, indent='\t')
    return


def koelectra_chatbot(uid, query, model, tokenizer, device, dataset=None):
    questions, example = [], []
    idx_dic, idx_key = {}, 0
    for idx, question in enumerate(dataset.values_list('query')):
        for q in question[0]:
            example.append((query, q))
            idx_dic[idx_key] = idx
            idx_key += 1
    batch = tokenizer.batch_encode_plus(
        example,
        max_length=64,
        pad_to_max_length=True,
        add_special_tokens=True,
        truncation=True
    )
    model.to(device)
    model.eval()
    with torch.no_grad():
        inputs = {
            "input_ids": torch.LongTensor([a for a in batch["input_ids"]]).to(device),
            "attention_mask": torch.LongTensor([a for a in batch["attention_mask"]]).to(device),
            "token_type_ids": torch.LongTensor([a for a in batch["token_type_ids"]]).to(device)
        }
        outputs = model(**inputs)
    preds = outputs[0].detach().cpu().numpy()
    preds = preds.reshape(-1)
    top_idx_list = preds.argsort().tolist()
    top_idx_list.reverse()
    log_save(uid, query, dataset, top_idx_list[:5], preds, idx_dic)
    idx = top_idx_list[0]
    return dataset[idx_dic[idx]], preds[idx]/5
