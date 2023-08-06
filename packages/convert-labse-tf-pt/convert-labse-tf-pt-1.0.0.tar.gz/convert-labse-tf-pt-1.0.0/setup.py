# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['convert_labse_tf_pt']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.6.3,<8.0.0',
 'loguru>=0.5.3,<0.6.0',
 'tensorflow-hub>=0.11.0,<0.12.0',
 'tensorflow>=2.4.0,<3.0.0',
 'torch<1.6',
 'transformers>=4.1.1,<5.0.0']

entry_points = \
{'console_scripts': ['convert_labse = convert_labse_tf_pt.convert:main']}

setup_kwargs = {
    'name': 'convert-labse-tf-pt',
    'version': '1.0.0',
    'description': 'Convert LaBSE model from TensorFlow to PyTorch.',
    'long_description': '---\nlanguage:\n  - af\n  - am\n  - ar\n  - as\n  - az\n  - be\n  - bg\n  - bn\n  - bo\n  - bs\n  - ca\n  - ceb\n  - co\n  - cs\n  - cy\n  - da\n  - de\n  - el\n  - en\n  - eo\n  - es\n  - et\n  - eu\n  - fa\n  - fi\n  - fr\n  - fy\n  - ga\n  - gd\n  - gl\n  - gu\n  - ha\n  - haw\n  - he\n  - hi\n  - hmn\n  - hr\n  - ht\n  - hu\n  - hy\n  - id\n  - ig\n  - is\n  - it\n  - ja\n  - jv\n  - ka\n  - kk\n  - km\n  - kn\n  - ko\n  - ku\n  - ky\n  - la\n  - lb\n  - lo\n  - lt\n  - lv\n  - mg\n  - mi\n  - mk\n  - ml\n  - mn\n  - mr\n  - ms\n  - mt\n  - my\n  - ne\n  - nl\n  - no\n  - ny\n  - or\n  - pa\n  - pl\n  - pt\n  - ro\n  - ru\n  - rw\n  - si\n  - sk\n  - sl\n  - sm\n  - sn\n  - so\n  - sq\n  - sr\n  - st\n  - su\n  - sv\n  - sw\n  - ta\n  - te\n  - tg\n  - th\n  - tk\n  - tl\n  - tr\n  - tt\n  - ug\n  - uk\n  - ur\n  - uz\n  - vi\n  - wo\n  - xh\n  - yi\n  - yo\n  - zh\n  - zu\ntags:\n  - bert\n  - sentence_embedding\n  - multilingual\n  - google\nlicense: Apache-2.0\ndatasets:\n  - CommonCrawl\n  - Wikipedia\n---\n\n# LaBSE\n\n## Project\n\nThis project is an implementation to convert LaBSE from TensorFlow to PyTorch.\n\n## Model description\n\nLanguage-agnostic BERT Sentence Encoder (LaBSE) is a BERT-based model trained for sentence embedding for 109 languages. The pre-training process combines masked language modeling with translation language modeling. The model is useful for getting multilingual sentence embeddings and for bi-text retrieval.\n\n- Model: [HuggingFace\'s model hub](https://huggingface.co/setu4993/LaBSE).\n- Paper: [arXiv](https://arxiv.org/abs/2007.01852).\n- Original model: [TensorFlow Hub](https://tfhub.dev/google/LaBSE/1).\n- Blog post: [Google AI Blog](https://ai.googleblog.com/2020/08/language-agnostic-bert-sentence.html).\n\n## Usage\n\nUsing the model:\n\n```python\nimport torch\nfrom transformers import BertModel, BertTokenizerFast\n\n\ntokenizer = BertTokenizerFast.from_pretrained("setu4993/LaBSE")\nmodel = BertModel.from_pretrained("setu4993/LaBSE")\nmodel = model.eval()\n\nenglish_sentences = [\n    "dog",\n    "Puppies are nice.",\n    "I enjoy taking long walks along the beach with my dog.",\n]\nenglish_inputs = tokenizer(english_sentences, return_tensors="pt", padding=True)\n\nwith torch.no_grad():\n    english_outputs = model(**english_inputs)\n```\n\nTo get the sentence embeddings, use the pooler output:\n\n```python\nenglish_embeddings = english_outputs.pooler_output\n```\n\nOutput for other languages:\n\n```python\nitalian_sentences = [\n    "cane",\n    "I cuccioli sono carini.",\n    "Mi piace fare lunghe passeggiate lungo la spiaggia con il mio cane.",\n]\njapanese_sentences = ["犬", "子犬はいいです", "私は犬と一緒にビーチを散歩するのが好きです"]\nitalian_inputs = tokenizer(italian_sentences, return_tensors="pt", padding=True)\njapanese_inputs = tokenizer(japanese_sentences, return_tensors="pt", padding=True)\n\nwith torch.no_grad():\n    italian_outputs = model(**italian_inputs)\n    japanese_outputs = model(**japanese_inputs)\n\nitalian_embeddings = italian_outputs.pooler_output\njapanese_embeddings = japanese_outputs.pooler_output\n```\n\nFor similarity between sentences, an L2-norm is recommended before calculating the similarity:\n\n```python\nimport torch.nn.functional as F\n\n\ndef similarity(embeddings_1, embeddings_2):\n    normalized_embeddings_1 = F.normalize(embeddings_1, p=2)\n    normalized_embeddings_2 = F.normalize(embeddings_2, p=2)\n    return torch.matmul(\n        normalized_embeddings_1, normalized_embeddings_2.transpose(0, 1)\n    )\n\n\nprint(similarity(english_embeddings, italian_embeddings))\nprint(similarity(english_embeddings, japanese_embeddings))\nprint(similarity(italian_embeddings, japanese_embeddings))\n```\n\n## Details\n\nDetails about data, training, evaluation and performance metrics are available in the [original paper](https://arxiv.org/abs/2007.01852).\n\n### BibTeX entry and citation info\n\n```bibtex\n@misc{feng2020languageagnostic,\n      title={Language-agnostic BERT Sentence Embedding},\n      author={Fangxiaoyu Feng and Yinfei Yang and Daniel Cer and Naveen Arivazhagan and Wei Wang},\n      year={2020},\n      eprint={2007.01852},\n      archivePrefix={arXiv},\n      primaryClass={cs.CL}\n}\n```\n\n## License\n\nThis repository and the conversion code is licensed under the MIT license, but the **model** is distributed with an Apache-2.0 license.\n',
    'author': 'Setu Shah',
    'author_email': 'setu+labse@setu.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/setu4993/convert-labse-tf-pt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
