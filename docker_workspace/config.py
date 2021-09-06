import transformers


DEVICE = 'cpu'
MAX_LEN = 512
TRAIN_BATCH_SIZE = 8
VALID_BATCH_SIZE = 4
EPOCHS = 10
BERT_PATH = "/root/docker_data/bert_base_uncased"
MODEL_PATH = "/root/docker_data/model.bin"
TRAINING_FILE = "/root/docker_data/IMDB_dataset.csv"
TOKENIZER = transformers.BertTokenizer.from_pretrained(
    BERT_PATH,
    do_lower_case =True
)
