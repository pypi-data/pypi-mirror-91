
import requests
import json
import base64

api_info = {
    "F1": {
        "func": "DNN语言模型",
        "des": "中文DNN语言模型接口用于输出切词结果并给出每个词在句子中的概率值,判断一句话是否符合语言表达习惯。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/0k6z52fb4"
    },
    "F2": {
        "func": "短文本相似度",
        "des": "依托全网海量优质数据和深度神经网络技术，为您提供高精度的短文本相似度服务，帮助快速实现推荐、检索、排序等应用；短文本相似度计算：提供两个短文本之间的语义相似度计算能力，输出的相似度是一个介于0到1之间的实数值，输出数值越大，则代表语义相似程度相对越高；短文本相似聚合：通过语义相似度计算，判断两个短文本的语义表述是否相近，从而实现相似短文本的聚合或去重",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/ek6z52frp"
    },
    "F3": {
        "func": "通用文字识别（标准含位置版）",
        "des": "基于业界领先的深度学习技术，提供多场景、多语种、高精度的整图文字检测和识别服务。在通用文字识别的基础上，返回文字在图片中的位置信息，方便用户进行版式的二次处理。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/vk3h7y58v"
    },
    "F4": {
        "func": "通用文字识别（标准版）",
        "des": "多场景、多语种、高精度的整图文字检测和识别服务，多项ICDAR指标居世界第一；可识别20种语言，最高可享每天50000次免费调用",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/zk3h7xz52"
    },
    "F5": {
        "func": "通用文字识别, 图片参数为远程url图片",
        "des": "",
        "owner": "百度",
        "doc_url": ""
    },
    "F6": {
        "func": "通用文字识别（高精度版）",
        "des": "在通用文字识别的基础上，提供更高精度的识别服务，支持更多语种识别（丹麦语、荷兰语、马来语、瑞典语、印尼语、波兰语、罗马尼亚语、土耳其语、希腊语、匈牙利语），并将字库从1w+扩展到2w+，能识别所有常用字和大部分生僻字",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/1k3h7y3db"
    },
    "F7": {
        "func": "依存句法分析",
        "des": "依存句法分析接口可自动分析文本中的依存句法结构信息，利用句子中词与词之间的依存关系来表示词语的句法结构信息（如“主谓”、“动宾”、“定中”等结构关系），并用树状结构来表示整句的结构（如“主谓宾”、“定状补”等）。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/nk6z52eu6"
    },
    "F8": {
        "func": "词法分析",
        "des": "向用户提供分词、词性标注、专名识别三大功能；能够识别出文本串中的基本词汇（分词），对这些词汇进行重组、标注组合后词汇的词性，并进一步识别出命名实体。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/fk6z52f2u"
    },
    "F9": {
        "func": "logo商标识别",
        "des": "该请求用于检测和识别图片中的台标、品牌商标等logo信息。即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中logo的名称、位置和置信度。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Ok3bcxc59"
    },
    "F10": {
        "func": "通用物体和场景识别高级版",
        "des": "可识别超过10万类常见物体和场景，接口返回大类及细分类的名称，并支持获取识别结果对应的百科信息；还可使用EasyDL定制训练平台，定制识别分类标签。广泛适用于图像或视频内容分析、拍照识图等业务场景",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Xk3bcxe21"
    },
    "F11": {
        "func": "词法分析（定制版）",
        "des": "向用户提供分词、词性标注、专名识别三大功能；用户在控制台中进行个性化配置，支持自定义专有名词词表与规则，通过定制版可有效识别应用场景中的小众词汇与类别。",
        "owner": "百度",
        "doc_url": ""
    },
    "F12": {
        "func": "词向量表示",
        "des": "词向量表示接口提供中文词向量的查询功能。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/fk6z52elw"
    },
    "F13": {
        "func": "词义相似度",
        "des": "输入两个词，得到两个词的相似度结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/Fk6z52fjc"
    },
    "F14": {
        "func": "评论观点抽取",
        "des": "提取评论句子的关注点和评论观点，并输出评论观点标签及评论观点极性。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/ok6z52g8q"
    },
    "F15": {
        "func": "情感倾向分析",
        "des": "对只包含单一主体主观信息的文本，进行自动情感倾向性判断（积极、消极、中性），并给出相应的置信度。为口碑分析、话题监控、舆情分析等应用提供基础技术支持，同时支持用户自行定制模型效果调优。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/zk6z52hds"
    },
    "F16": {
        "func": "文章标签",
        "des": "文本标签服务对文章的标题和内容进行深度分析，输出能够反映文章关键信息的主题、话题、实体等多维度标签以及对应的置信度，该技术在个性化推荐、文章聚合、内容检索等场景具有广泛的应用价值。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/7k6z52ggx"
    },
    "F17": {
        "func": "文章分类",
        "des": "对文章按照内容类型进行自动分类，首批支持娱乐、体育、科技等26个主流内容类型，为文章聚类、文本内容分析等应用提供基础技术支持。 目前支持的一级粗粒度分类类目如下：1、国际 2、体育 3、娱乐 4、社会 5、财经 6、时事 7、科技 8、情感 9、汽车 10、教育 11、时尚 12、游戏 13、军事 14、旅游 15、美食 16、文化 17、健康养生 18、搞笑 19、家居 20、动漫 21、宠物 22、母婴育儿 23、星座运势 24、历史 25、音乐 26、综合",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/wk6z52gxe"
    },
    "F18": {
        "func": "文本纠错",
        "des": "识别输入文本中有错误的片段，提示错误并给出正确的文本结果。支持短文本、长文本、语音等内容的错误识别，纠错是搜索引擎、语音识别、内容审查等功能更好运行的基础模块之一。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/Ik6z52gp8"
    },
    "F19": {
        "func": "对话情绪识别接口",
        "des": "针对用户日常沟通文本背后所蕴含情绪的一种直观检测，可自动识别出当前会话者所表现出的一级和二级细分情绪类别及其置信度，针对正面和负面的情绪，还可给出参考回复话术。帮助企业更全面地把握产品服务质量、监控客户服务质量。在自动监控中如果发现有负面情绪出现，可以及时介入人工处理，帮助在有限的人工客服条件下，降低客户流失。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/rk6z52hlz"
    },
    "F20": {
        "func": "新闻摘要摘取",
        "des": "自动抽取新闻文本中的关键信息，进而生成指定长度的新闻摘要",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/Gk6z52hu3"
    },
    "F21": {
        "func": "调用通用文字识别（含位置信息版）, 图片参数为远程url图片",
        "des": "",
        "owner": "百度",
        "doc_url": ""
    },
    "F22": {
        "func": "通用文字识别（高精度含位置版）",
        "des": "提供多场景、多语种、高精度的整图文字检测和识别服务，支持生僻字识别，并支持20种语言识别，相对于通用文字识别（含位置信息版）该产品精度更高，但是识别耗时会稍长",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/tk3h7y2aq"
    },
    "F23": {
        "func": "网络图片文字识别",
        "des": "针对网络图片进行专项优化，支持识别艺术字体或背景复杂的文字内容。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Sk3h7xyad"
    },
    "F24": {
        "func": "网络图片文字识别, 图片参数为远程url图片",
        "des": "",
        "owner": "百度",
        "doc_url": ""
    },
    "F25": {
        "func": "身份证识别",
        "des": "支持对二代居民身份证正反面所有8个字段进行结构化识别，包括姓名、性别、民族、出生日期、住址、身份证号、签发机关、有效期限，识别准确率超过99%；同时支持身份证正面头像检测，并返回头像切片的base64编码及位置信息。同时，支持对用户上传的身份证图片进行图像风险和质量检测，可识别图片是否为复印件或临时身份证，是否被翻拍或编辑，是否存在正反颠倒、模糊、欠曝、过曝等质量问题。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/rk3h7xzck"
    },
    "F26": {
        "func": "银行卡识别",
        "des": "支持对主流银行卡的卡号、有效期、发卡行、卡片类型4个关键字段进行结构化识别，识别准确率超过99%。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/ak3h7xxg3"
    },
    "F27": {
        "func": "驾驶证识别",
        "des": "支持对机动车驾驶证正本所有9个字段进行结构化识别，包括证号、姓名、性别、国籍、住址、出生日期、初次领证日期、准驾车型、有效期限",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Vk3h7xzz7"
    },
    "F28": {
        "func": "行驶证识别",
        "des": "对机动车行驶证主页及副页所有21个字段进行结构化识别，包括号牌号码、车辆类型、所有人、品牌型号、车辆识别代码、发动机号码、核定载人数、质量、尺寸、检验记录等。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y3ks"
    },
    "F29": {
        "func": "车牌识别",
        "des": "支持识别中国大陆机动车蓝牌、黄牌（单双行）、绿牌、大型新能源（黄绿）、领使馆车牌、警牌、武警牌（单双行）、军牌（单双行）、港澳牌、农用车牌、民航车牌的地域编号和车牌号，并能同时识别图像中的多张车牌。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/ck3h7y191"
    },
    "F30": {
        "func": "营业执照识别",
        "des": "支持对不同版式营业执照的证件编号、社会信用代码、单位名称、地址、法人、类型、成立日期、有效日期、经营范围等关键字段进行结构化识别",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/sk3h7y3zs"
    },
    "F31": {
        "func": "通用票据识别",
        "des": "针对票据字体做了专项优化的通用文字识别版本，支持对医疗票据、银行兑票、购物小票等各类票据的票面内容进行识别，并按行返回结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/6k3h7y11b"
    },
    "F32": {
        "func": "短语音识别标准版",
        "des": "短语音识别标准版可以将语音精准识别为文字，适用于手机语音输入、语音搜索、智能语音对话等场景。包含中文普通话输入法、英语、粤语、四川话、远场5个识别模型。其中Android，iOS，Linux SDK支持超过60秒的实时场语音识别。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/Ek39uxgre"
    },
    "F40": {
        "func": "通用物体和场景识别",
        "des": "该请求用于通用物体及场景识别，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的多个物体及场景标签。",
        "owner": "百度",
        "doc_url": "https://cloud.baidu.com/doc/IMAGERECOGNITION/s/Xk3bcxdum"
    },
    "F41": {
        "func": "图像主体检测",
        "des": "用户向服务请求检测图像中的主体位置。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Xk3bcxdum"
    },
    "F42": {
        "func": "植物识别",
        "des": "该请求用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出植物识别结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Mk3bcxe9i"
    },
    "F43": {
        "func": "动物识别",
        "des": "该请求用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出动物识别结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Zk3bcxdfr"
    },
    "F44": {
        "func": "菜品识别",
        "des": "该请求用于菜品识别。即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片的菜品名称、卡路里信息、置信度。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/tk3bcxbb0"
    },
    "F45": {
        "func": "地标识别",
        "des": "该请求用于识别地标，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的地标识别结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/jk3bcxbih"
    },
    "F46": {
        "func": "果蔬识别",
        "des": "该请求用于识别果蔬类食材，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的果蔬食材结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/wk3bcxevq"
    },
    "F47": {
        "func": "红酒识别",
        "des": "该服务用于识别红酒标签，即对于输入的一张图片（可正常解码，长宽比适宜，且酒标清晰可见），输出图片中的红酒名称、国家、产区、酒庄、类型、糖分、葡萄品种、酒品描述等信息。可识别数十万中外常见红酒。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/Tk3bcxctf"
    },
    "F48": {
        "func": "货币识别",
        "des": "识别图像中的货币类型，以纸币为主，正反面均可准确识别，接口返回货币的名称、代码、面值、年份信息；可识别各类近代常见货币，如美元、欧元、英镑、法郎、澳大利亚元、俄罗斯卢布、日元、韩元、泰铢、印尼卢比等。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGERECOGNITION/pk3bcxavy"
    },
    "F49": {
        "func": "翻拍识别",
        "des": "该请求用于识别一张图片，即对于输入的一张图片，能够识别出通过手机翻拍出的商品陈列照片",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/EASYDL/dk3tmho35"
    },
    "F50": {
        "func": "饮品检测",
        "des": "支持识别普通货架/货柜上陈列的饮品",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/EASYDL/1k38n3jqg"
    },
    "F51": {
        "func": "日化品检测",
        "des": "支持识别普通货架/货柜上陈列的日化用品",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/EASYDL/1k38n3jqg"
    },
    "F52": {
        "func": "车型识别",
        "des": "识别图片中车辆的具体车型，可识别常见的3000+款车型（小汽车为主），输出车辆的品牌型号、颜色、年份、位置信息；支持返回对应识别结果的百度百科词条信息，包含词条名称、百科页面链接、百科图片链接、百科内容简介。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/VEHICLE/tk3hb3eiv"
    },
    "F53": {
        "func": "车辆检测",
        "des": "包括小汽车、卡车、巴士、摩托车、三轮车5类",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/VEHICLE/rk3hb3flg"
    },
    "F54": {
        "func": "车流统计",
        "des": "包括小汽车、卡车、巴士、摩托车、三轮车5类",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/VEHICLE/yk3hb3eqk"
    },
    "F55": {
        "func": "车辆属性识别",
        "des": "包括小汽车、卡车、巴士、摩托车、三轮车5类",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/VEHICLE/mk3hb3fde"
    },
    "F56": {
        "func": "车辆外观损伤识别",
        "des": "包括小汽车、卡车、巴士、摩托车、三轮车5类",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/VEHICLE/fk3hb3f5w"
    },
    "F57": {
        "func": "车辆分割",
        "des": "小汽车为主",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/VEHICLE/dk3hb3eyf"
    },
    "F58": {
        "func": "情感倾向分析",
        "des": "对只包含单一主体主观信息的文本，进行自动情感倾向性判断（积极、消极、中性），并给出相应的置信度。为口碑分析、话题监控、舆情分析等应用提供基础技术支持，同时支持用户自行定制模型效果调优。",
        "owner": "",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/zk6z52hds"
    },
    "F59": {
        "func": "黑白图像上色",
        "des": "智能识别黑白图像内容并填充色彩，使黑白图像变得鲜活",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/Bk3bclns3"
    },
    "F60": {
        "func": "图像风格转换",
        "des": "将图像转化成卡通画、铅笔画、彩色铅笔画，或者哥特油画、彩色糖块油画、呐喊油画、神奈川冲浪里油画、奇异油画、薰衣草油画等共计9种风格，可用于开展趣味活动，或集成到美图应用中对图像进行风格转换",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/xk3bclo77"
    },
    "F61": {
        "func": "图像审核",
        "des": "/",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/ANTIPORN/jk42xep4e"
    },
    "F62": {
        "func": "人像动漫化",
        "des": "运用世界领先的对抗生成网络，结合人脸检测、头发分割、人像分割等技术，为用户量身定制千人千面的二次元动漫形象，并且可通过参数设置，生成戴口罩的二次元动漫人像",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/Mk4i6olx5"
    },
    "F63": {
        "func": "图像去雾",
        "des": " 对浓雾天气下拍摄，导致细节无法辨认的图像进行去雾处理",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/8k3bclp1l"
    },
    "F64": {
        "func": "图像对比度增强",
        "des": "\n调整过暗或者过亮图像的对比度，使图像更加鲜明",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/ek3bclnzn"
    },
    "F65": {
        "func": "图像无损放大",
        "des": "图片无损放大通过对像素的描点，算法，自动对像素填充放大的图片，使图片放大后也清楚",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/ok3bclnkg"
    },
    "F66": {
        "func": "拉伸图像恢复",
        "des": "自动识别过度拉伸的图像，将图像内容恢复成正常比例",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/Rk3bclp97"
    },
    "F67": {
        "func": "图像清晰度增强",
        "des": "对压缩后的模糊图像实现智能快速去噪，优化图像纹理细节，使画面更加自然清晰",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/IMAGEPROCESS/5k4i6mzqk"
    },
    "F68": {
        "func": "对话情绪识别",
        "des": "帮助企业更全面地把握产品服务质量、监控客户服务质量。在自动监控中如果发现有负面情绪出现，可以及时介入人工处理，帮助在有限的人工客服条件下，降低客户流失。",
        "owner": "",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/rk6z52hlz"
    },
    "F69": {
        "func": "评论观点抽取",
        "des": "",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/ok6z52g8q"
    },
    "F70": {
        "func": "词法分析",
        "des": "向用户提供分词、词性标注、专名识别三大功能；能够识别出文本串中的基本词汇（分词），对这些词汇进行重组、标注组合后词汇的词性，并进一步识别出命名实体。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/tk6z52czc"
    },
    "F71": {
        "func": "词向量表示",
        "des": "词向量表示接口提供中文词向量的查询功能。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/fk6z52elw"
    },
    "F72": {
        "func": "词义相似度",
        "des": "输入两个词，得到两个词的相似度结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/Fk6z52fjc"
    },
    "F73": {
        "func": "依存句法分析",
        "des": "依存句法分析接口可自动分析文本中的依存句法结构信息，利用句子中词与词之间的依存关系来表示词语的句法结构信息（如“主谓”、“动宾”、“定中”等结构关系），并用树状结构来表示整句的结构（如“主谓宾”、“定状补”等）。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/nk6z52eu6"
    },
    "F74": {
        "func": "DNN语言模型",
        "des": "中文DNN语言模型接口用于输出切词结果并给出每个词在句子中的概率值,判断一句话是否符合语言表达习惯。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/0k6z52fb4"
    },
    "F75": {
        "func": "短文本相似度",
        "des": "短文本相似度接口用来判断两个文本的相似度得分。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/ek6z52frp"
    },
    "F76": {
        "func": "文本纠错",
        "des": "识别输入文本中有错误的片段，提示错误并给出正确的文本结果。支持短文本、长文本、语音等内容的错误识别，纠错是搜索引擎、语音识别、内容审查等功能更好运行的基础模块之一。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/Ik6z52gp8"
    },
    "F77": {
        "func": "文本审核",
        "des": "/",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/ANTIPORN/Rk3h6xb3i"
    },
    "F78": {
        "func": "数字识别",
        "des": "对图片中的数字进行提取和识别，自动过滤非数字内容，仅返回数字内容及其位置信息，识别准确率超过99%",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Ok3h7y1vo"
    },
    "F79": {
        "func": "手写文字识别",
        "des": "支持对图片中的手写中文、手写数字进行检测和识别，针对不规则的手写字体进行专项优化，识别准确率可达90%以上。\n\n",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/hk3h7y2qq"
    },
    "F80": {
        "func": "表格文字识别",
        "des": "对图片中的表格文字内容进行提取和识别，结构化输出表头、表尾及每个单元格的文字内容。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Ik3h7y238"
    },
    "F81": {
        "func": "二维码识别",
        "des": "对图片中的二维码、条形码进行检测和识别，返回存储的文字信息\n\n",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/qk3h7y5o7"
    },
    "F82": {
        "func": "办公文档识别",
        "des": "可对办公类文档版面进行分析，输出图、表、标题、文本的位置，并输出分版块内容的OCR识别结果，支持中、英两种语言，手写、印刷体混排多种场景。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/ykg9c09ji"
    },
    "F83": {
        "func": "短语音识别标准版",
        "des": "短语音识别可以将 60 秒以下的音频识别为文字，适用于语音对话、语音控制、语音输入等场景。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/Ek39uxgre"
    },
    "F84": {
        "func": "短语音识别极速版",
        "des": "将60秒以内的完整音频文件识别为文字，专有GPU服务集群，识别响应速度较标准版API提升2倍及识别准确率提升15%。适用于近场短语音交互，如手机语音搜索、聊天输入等场景。 支持上传完整的录音文件，录音文件时长不超过60秒。实时返回识别结果",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/jkhq0ohzz"
    },
    "F85": {
        "func": "音频文件转写（创建任务）",
        "des": "根据音频url、音频格式、语言id以及采样率等参数创建音频转写任务",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/ck5diijkt"
    },
    "F86": {
        "func": "音频文件转写（查询结果）",
        "des": "根据task_id的数组批量查询音频转写任务结果",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/6k5dilahb"
    },
    "F87": {
        "func": "呼叫中心音频文件转写（创建任务）",
        "des": "根据音频url、音频格式、语言id以及采样率等参数创建音频转写任务",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/Jkfhon3y6"
    },
    "F88": {
        "func": "呼叫中心音频文件转写（查询结果）",
        "des": "根据task_id的数组批量查询音频转写任务结果",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/7kfhp2nr4"
    },
    "F89": {
        "func": "在线语音合成",
        "des": "语音合成可将文字信息转化为声音信息，适用于手机APP、儿童故事机、智能机器人等多种应用场景。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/SPEECH/Gk38y8lzk"
    },
    "F101": {
        "func": "文章标签",
        "des": "\n文本标签服务对文章的标题和内容进行深度分析，输出能够反映文章关键信息的主题、话题、实体等多维度标签以及对应的置信度，该技术在个性化推荐、文章聚合、内容检索等场景具有广泛的应用价值",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/7k6z52ggx"
    },
    "F102": {
        "func": "文章分类",
        "des": "对文章按照内容类型进行自动分类，首批支持娱乐、体育、科技等26个主流内容类型，为文章聚类、文本内容分析等应用提供基础技术支持",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/wk6z52gxe"
    },
    "F103": {
        "func": "新闻摘要",
        "des": "基于深度语义分析模型，自动抽取新闻文本中的关键信息并生成指定长度的新闻摘要。可用于热点新闻聚合、新闻推荐、语音播报、APP消息Push等场景",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/Gk6z52hu3"
    },
    "F104": {
        "func": "地址识别",
        "des": "针对快递、电商行业中客户在线提交的大量非结构化地址单据，该接口可以帮助精准提取快递填单文本中的姓名、电话、地址信息，通过自然语言处理辅助地址识别做自动补充和纠正，生成标准规范的结构化信息，大幅提升企业处理单据的效率。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/NLP/vk6z52h5n"
    },
    "F105": {
        "func": "身份证识别",
        "des": "针身份证生成标准规范的结构化信息，大幅提升处理单据的效率",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/rk3h7xzck"
    },
    "F106": {
        "func": "银行卡识别",
        "des": "针身份证生成标准规范的结构化信息，大幅提升处理单据的效率",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/ak3h7xxg3"
    },
    "F107": {
        "func": "营业执照识别",
        "des": "可结构化识别各类版式的营业执照，返回证件编号、社会信用代码、单位名称、地址、法人、类型、成立日期、有效日期、经营范围等关键字段信息",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/sk3h7y3zs"
    },
    "F108": {
        "func": "名片识别",
        "des": "支持对各类名片的9个关键字段进行结构化识别，包括姓名、公司、职位、邮编、邮箱、电话、网址、地址、手机号",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/5k3h7xyi2"
    },
    "F109": {
        "func": "护照识别",
        "des": "支持对中国大陆护照个人资料页所有11个字段进行结构化识别，包括国家码、护照号、姓名、姓名拼音、性别、出生地点、出生日期、签发地点、签发日期、有效期、签发机关",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Wk3h7y1gi"
    },
    "F110": {
        "func": "户口本识别",
        "des": "结构化识别户口本内常住人口登记卡的全部 22 个字段，包括户号、姓名、与户主关系、性别、出生地、民族、出生日期、身份证号、曾用名、籍贯、宗教信仰、身高、血型、文化程度、婚姻状况、兵役状况等",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/ak3h7xzk7"
    },
    "F111": {
        "func": "港澳通行证识别",
        "des": "支持对大陆居民往来港澳通行证的证件号码、姓名、姓名拼音、出生日期、性别、有效期限、签发地点7个关键字段进行结构化识别",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/4k3h7y0ly"
    },
    "F112": {
        "func": "台湾通行证识别",
        "des": "支持对大陆居民往来台湾通行证的证件号码、姓名、姓名拼音、出生日期、性别、有效期限、签发地点7个关键字段进行结构化识别",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/kk3h7y2yc"
    },
    "F113": {
        "func": "出生医学证明",
        "des": "结构化识别出生医学证明的6个关键字段，包括新生儿姓名、性别、出生时间、父亲姓名、母亲姓名、出生证编号；可用于新生儿身份登记、入学登记、生育险报销等场景",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/mk3h7y1o6"
    },
    "F114": {
        "func": "人体关键点识别",
        "des": "检测图片中的所有人体，输出每个人体的21个主要关键点，包含头顶、五官、脖颈、四肢等部位，同时输出人体的坐标信息和数量。支持多人检测、人体位置重叠、遮挡、背面、侧面、中低空俯拍、大动作等复杂场景。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/BODY/0k3cpyxme"
    },
    "F115": {
        "func": "人体检测和属性识别",
        "des": "检测图像中的所有人体并返回每个人体的矩形框位置，识别人体的静态属性和行为，共支持22种属性，包括：性别、年龄阶段、上下身服饰（含类别/颜色）、是否戴帽子、是否戴口罩、是否戴眼镜、背包、是否吸烟、是否使用手机、人体朝向等",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/BODY/Ak3cpyx6v"
    },
    "F116": {
        "func": "人流量统计",
        "des": "识别和统计图像当中的人体个数（静态统计，不支持追踪和去重）",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/BODY/7k3cpyy1t"
    },
    "F120": {
        "func": "通用文字识别",
        "des": "",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/1k3h7y3db"
    },
    "F121": {
        "func": "火车票识别",
        "des": "支持对红、蓝火车票的13个关键字段进行结构化识别，包括车票号码、始发站、目的站、车次、日期、票价、席别、姓名、座位号、身份证号、售站、序列号、时间。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Ok3h7y35u"
    },
    "F122": {
        "func": "出租车票识别",
        "des": "支持识别全国各大城市出租车票的 12 个关键字段，包括发票号码、代码、车号、日期、时间、总金额、燃油附加费、叫车服务费、省、市、单价、里程。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Zk3h7xxnn"
    },
    "F123": {
        "func": "通用票据识别",
        "des": "针对票据字体做了专项优化的通用文字识别版本，支持对医疗票据、银行兑票、购物小票等各类票据的票面内容进行识别，并按行返回结果。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/6k3h7y11b"
    },
    "F124": {
        "func": "银行支票识别",
        "des": "\\",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F125": {
        "func": "定额发票识别",
        "des": "支持对各类定额发票的发票代码、发票号码、金额、发票所在地、发票金额小写、省、市7个关键字段进行结构化识别。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/lk3h7y4ev"
    },
    "F126": {
        "func": "公式识别",
        "des": "支持对试卷中的数学公式及题目内容进行识别，可提取公式部分进行单独识别，也可对题目和公式进行混合识别，并返回Latex格式公式内容及位置信息，便于进行后续处理",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Ok3h7xxva"
    },
    "F127": {
        "func": "仪器仪表盘读数识别",
        "des": "适用于不同品牌、不同型号的仪器仪表盘读数识别，广泛适用于各类血糖仪、血压仪、燃气表、电表等，可识别表盘上的数字、英文、符号，支持液晶屏、字轮表等表型。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Jkafike0v"
    },
    "F128": {
        "func": "试卷分析与识别",
        "des": "可对文档版面进行分析，输出图、表、标题、文本的位置，并输出分版块内容的OCR识别结果，支持中、英两种语言，手写、印刷体混排多种场景",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/jk9m7mj1l"
    },
    "F129": {
        "func": "医疗发票识别",
        "des": "支持识别全国各地门诊/住院发票的 业务流水号、发票号、住院号、病例号、姓名、性别、社保卡号、金额大/小写 等 16 个关键字段，其中北京地区票据识别效果最佳",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yke30j1hq"
    },
    "F130": {
        "func": "保险单识别",
        "des": "支持对保险单中的投保人、被保人、受益人的各项信息及保费、保险种类等字段进行识别，暂支持识别各类人身保险保单",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Wk3h7y0eb"
    },
    "F131": {
        "func": "门脸文字识别",
        "des": "针对含有门脸/门头的图片进行专项优化，支持识别门脸/门头上的文字内容。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/wk5hw3cvo"
    },
    "F132": {
        "func": "行程单识别",
        "des": "支持对飞机行程单的24个字段进行结构化识别，包括电子客票号、印刷序号、姓名、始发站、目的站、航班号、日期、时间、票价、身份证号、承运人、民航发展基金、保险费、燃油附加费、其他税费、合计金额、填开日期、订票渠道、客票级别、座位等级、销售单位号、签注、免费行李、验证码。 同时，支持单张行程单上的多航班信息识别。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/Qk3h7xzro"
    },
    "F133": {
        "func": "VIN码识别",
        "des": "支持对车辆挡风玻璃处的车架号码进行识别。",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/zk3h7y51e"
    },
    "F134": {
        "func": "车辆合格证识别",
        "des": "支持对车辆合格证的23个关键字段进行结构化识别，包括合格证编号、发证日期、车辆制造企业名、车辆品牌、车辆名称、车辆型号、车架号、车身颜色、发动机型号、发动机号、燃料种类、排量、功率、排放标准、轮胎数、轴距、轴数、转向形式、总质量、整备质量、驾驶室准乘人数、最高设计车速、车辆制造日期",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y3sc"
    },
    "F160": {
        "func": "汽车票识别",
        "des": "对全国范围内不同版式的汽车票进行结构化识别，包括发票代码、发票号码、到达站、出发站、日期、时间、金额、身份证号、姓名9个字段；可用于企业税务核算及内部报销等场景，有效提升财税报销的业务效率",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F161": {
        "func": "通行费发票识别",
        "des": "对全国范围内不同版式的过路费、过桥费发票进行结构化识别，包括发票代码、发票号码、入口、出口、日期、时间、金额、省、市9个字段；可用于企业税务核算及内部报销等场景，有效提升财税报销的业务效率",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F162": {
        "func": "混贴票据识别",
        "des": "对粘贴在同一张A4纸上的多张不同种类票据进行自动切分并识别，可返回每张票据的位置、种类及票面的结构化识别结果。已支持增值税发票、定额发票、卷票、火车票、出租车票、行程单、机动车销售发票、汽车票、通行费发票9类票据的混贴情况",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F163": {
        "func": "增值税发票识别",
        "des": "结构化识别增值税普票、专票、电子发票、卷票的所有关键字段，包括发票基本信息、销售方及购买方信息、商品信息、价税信息等，其中四要素识别准确率超过99%",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F164": {
        "func": "定额发票识别",
        "des": "对各类定额发票进行结构化识别，可识别发票代码、发票号码、金额、发票所在地、发票金额小写、省、市7个关键字段",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F165": {
        "func": "增值税卷票识别",
        "des": "结构化识别增值税普票、专票、电子发票、卷票的所有关键字段，包括发票基本信息、销售方及购买方信息、商品信息、价税信息等，其中四要素识别准确率超过99%",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F166": {
        "func": "机动车销售发票",
        "des": "对全国范围内不同版式的汽车票进行结构化识别，包括发票代码、发票号码、到达站、出发站、日期、时间、金额、身份证号、姓名9个字段；可用于企业税务核算及内部报销等场景，有效提升财税报销的业务效率",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F167": {
        "func": "银行回单识别",
        "des": "支持对各大银行的收付款回单关键字段进行结构化识别，包括：收/付款人户名、账号、开户银行、交易日期、大小写金额、流水号，其余信息按行返回",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F168": {
        "func": "银行支票识别",
        "des": "支持对转账支票、现金支票、普通支票等多类银行支票的7个关键字段进行结构化识别，包括：银行名称、出票日期、出票人账号、收款人、 付款行名称、金额、用途",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F169": {
        "func": "银行汇票识别",
        "des": "支持对普通商业承兑汇票、普通银行承兑汇票、电子商业承兑汇票等多类汇票的21个关键字段进行结构化识别，包括：收/付款人账号、出票金额、出票日期、承兑人信息等",
        "owner": "百度",
        "doc_url": "https://ai.baidu.com/ai-doc/OCR/yk3h7y9u3"
    },
    "F301": {
        "func": "手写文字识别",
        "des": "手写文字识别(Handwriting words Recognition)基于深度神经网络模型的端到端文字识别系统，将图片（来源如扫描仪或数码相机）中的手写字体转化为计算机可编码的文字，支持中英文。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/wordRecg/API.html#%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E"
    },
    "F302": {
        "func": "印刷文字识别",
        "des": "通用文字识别(General words Recognition)基于深度神经网络模型的端到端文字识别系统，将图片（来源如扫描仪或数码相机）中的文字转化为计算机可编码的文字，支持中英文。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/textRecg/API.html#%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E"
    },
    "F303": {
        "func": "印刷文字识别（多语种)",
        "des": "印刷文字识别（多语种），通过 OCR（光学字符识别 Optical Character Recognition）技术，自动对文档 OCR 进行识别，返回文档上的纯文本信息，可以省去用户手动录入的过程， 并会返回图片中文字的坐标位置，方便二次开发。 自动完成文档 OCR 信息的采集，可以很方便对接客户的后台数据系统，给用户带来极大的便利。 该印刷文字识别接口支持语种包括：中(简体和繁体)、英、日、韩、德、法、意、葡、西、荷，接口会自动判断文字语种。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/printed-word-recognition/API.html#接口要求"
    },
    "F304": {
        "func": "银行卡识别",
        "des": "银行卡识别，通过 OCR（光学字符识别 Optical Character Recognition）技术，自动对银行卡进行识别，返回银行卡原件上的银行卡卡号、有效日期、发卡行、卡片类型（借记卡&信用卡）、持卡人姓名（限信用卡）等信息，可以省去用户手动录入的过程，自动完成银行卡信息的结构化和图像数据的采集，可以很方便对接客户的后台数据系统，给用户带来极大的便利。采特有的图像处理技术，在识别银行卡图片过程中，还可以对银行卡图片上的卡号图像，方便用户保存。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/bankCardRecg/API.html"
    },
    "F305": {
        "func": "身份证识别 intsig",
        "des": "身份证识别，通过OCR（光学字符识别 Optical Character Recognition）技术，对身份证正反面图片进行识别，返回身份证图片上的姓名、民族、住址、身份证号、签发机关和有效期等信息，可以省去用户手动录入的过程，自动完成身份证信息的结构化和图像数据的采集，可以很方便对接客户的后台数据系统，给用户带来极大的便利。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/idCardRecg/API.html"
    },
    "F306": {
        "func": "增值税发票识别 intsig",
        "des": "增值税发票识别，通过OCR（光学字符识别 Optical Character Recognition）技术，对增值税发票（中文简体）图像切边、压缩、增强、校正，将发票上的文字信息识别并导出。使用扫描仪或手机拍摄，即可批量快速扫描发票，节省大量人工录入时间。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/VAT-invoice-recg/API.html"
    },
    "F307": {
        "func": "营业执照识别",
        "des": "营业执照识别，对营业执照图片进行识别，返回营业执照图片上的注册号、名称、类型、住所、法定代表人、注册资本、成立日期、营业期限和经营范围等信息，可以省去用户手动录入的过程，自动完成营业执照信息的结构化和图像数据的采集，可以很方便对接客户的后台数据系统，给用户带来极大的便利，方便用户保存。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/business_license/API.html"
    },
    "F308": {
        "func": "车牌识别 JD",
        "des": "基于深度学习技术，利用光学字符识别技术，可对输入的图片自动识别车牌字段信息，识别准确率业内领先，稳定可靠。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/vehicleLicensePlateRecg/API.html"
    },
    "F309": {
        "func": "行驶证识别 JD",
        "des": "基于深度学习技术，识别机动车行驶证正页的关键字段，包括号牌号码、车辆类型、所有人、住址、使用性质、品牌型号、车辆识别代号、发动机号码、注册日期、发证日期等字段，准确可靠。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/vehicleRecg/API.html"
    },
    "F310": {
        "func": "出租车发票识别",
        "des": "出租车发票识别，对出租车发票图片进行识别，返回 车牌号、日期、上下车时间、单价、里程、金额、号码等信息，通过批量扫描出租车发票，帮助企业节省大量人力财力，降低风险。 同样用于内部OA系统中，发票报销时，使用出租车发票识别，可以快速收集出租车发票信息。给用户带来极大的便利，方便用户保存。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/taxi_ticket/newAPI.html"
    },
    "F311": {
        "func": "火车票识别",
        "des": "火车票识别，基于深度神经网络模型的端到端文字识别系统，可以自动地从图片中定位火车票区域，识别出其中包含的信息。可以省去用户手动录入的过程，自动完成火车票信息的结构化和图像数据的采集，可以很方便的用于报销等系统中，给用户带来极大的便利。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/train_ticket/API.html"
    },
    "F312": {
        "func": "驾驶证识别 JD",
        "des": "可对输入的图片自动识别驾驶证信息，兼顾驾驶证首页和副页，提取驾驶人员的身份信息，输出关键字段，识别准确率高，稳定可靠。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/DriversLicenseRecg/API.html"
    },
    "F313": {
        "func": "增值税发票识别",
        "des": "增值税发票识别，对增值税发票图片进行识别，返回图片上的发票号码、开票日期、购买方信息、金额、单价等信息。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/vat_invoice/API.html"
    },
    "F314": {
        "func": "人脸比对",
        "des": "基于讯飞自研的人脸算法，可实现对比两张照片中的人脸信息，判断是否是同一个人并返回相似度得分。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/face/xffaceComparisonRecg/API.html#接口说明"
    },
    "F315": {
        "func": "机器翻译",
        "des": "机器翻译，基于讯飞自主研发的机器翻译引擎，已经支持包括英、日、法、西、俄等10多种语言(其中维语、藏语暂不对外提供)，效果更优质，已在讯飞翻译机上应用并取得优异成绩，详细请参照 语种列表 。通过调用该接口，将源语种文字转化为目标语种文字。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/xftrans/API.html"
    },
    "F316": {
        "func": "文本纠错",
        "des": "对输入文本进行校对，校对包括拼写、语法、搭配、实体纠错、标点、领导人职称、政治用语及数字纠错等。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/textCorrection/API.html#接口说明"
    },
    "F317": {
        "func": "歌曲识别",
        "des": "歌曲识别技术分为歌曲原声识别以及哼唱识别。歌曲原声识别通过听筒收集音乐播放信息，生成音频指纹，在曲库中识别到对应的歌曲。 哼唱识别通过用户对着话筒哼唱小段歌曲，系统自动识别并检索出所哼唱的歌曲。现仅支持哼唱识别，原声识别效果仍在优化中，暂时未能开放，敬请期待。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/voiceservice/song-recognition/API.html#接口说明"
    },
    "F318": {
        "func": "中文分词",
        "des": "指的是将汉字序列切分成词序列。汉语中，词是承载语义的最基本的单元。分词是信息检索、文本分类、情感分析等多项中文自然语言处理任务的基础",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/lexicalAnalysis/API.html#接口说明"
    },
    "F319": {
        "func": "依存句法分析",
        "des": "依存语法(Dependency Parsing, DP) 通过分析语言单位内成分之间的依存关系揭示其句法结构。直观来讲，依存句法分析识别句子中的“主谓宾”、“定状补”这些语法成分，并分析各成分之间的关系。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/dependencyParsing/API.html#接口说明"
    },
    "F320": {
        "func": "语义角色标注",
        "des": "语义角色标注(Semantic Role Labeling, SRL) 是一种浅层的语义分析技术，标注句子中某些短语为给定谓词的论元 (语义角色)，如施事、受事、时间和地点等。其能够对问答系统、信息抽取和机器翻译等应用产生推动作用。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/semanticRoleLabeling/API.html#接口说明"
    },
    "F321": {
        "func": "词性标注",
        "des": "词性标注(Part-of-speech Tagging, POS)是给句子中每个词一个词性类别的任务。这里的词性类别可能是名词、动词、形容词或其他。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/lexicalAnalysis/API.html#接口说明"
    },
    "F322": {
        "func": "命名实体识别",
        "des": "命名实体识别(Named Entity Recognition, NER)是在句子的词序列中定位并识别人名、地名、机构名等实体的任务。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/lexicalAnalysis/API.html#接口说明"
    },
    "F323": {
        "func": "语义依存 (依存树)",
        "des": "语义依存 (依存树) 分析(Semantic Dependency Parsing, SDP)，分析句子各个语言单位之间的语义关联，并将语义关联以依存结构呈现。使用语义依存刻画句子语义，好处在于不需要去抽象词汇本身，而是通过词汇所承受的语义框架来描述该词汇，而论元的数目相对词汇来说数量总是少了很多的。语义依存分析目标是跨越句子表层句法结构的束缚，直接获取深层的语义信息。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/semanticDependence/API.html#接口说明"
    },
    "F324": {
        "func": "语义依存 (依存图)",
        "des": "语义依存 (依存图) 分析(Semantic Dependency Graph Parsing, SDGP) 是在语义依存树基础上做了突破，使得对连动、兼语、概念转位等汉语中常见的现象的分析更全面深入。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/semantic-dependence-graph/API.html"
    },
    "F325": {
        "func": "情感分析",
        "des": "以哈工大社会计算与信息检索研究中心研发的 “语言技术平台（LTP）” 为基础，为用户提供针对 中文（简体） 文本的情感分析服务。情感分析(Sentiment Analysis) 是文本分类的一个分支，是对带有情感色彩（褒义贬义/正向负向）的主观性文本进行分析，以确定该文本的观点、喜好、情感倾向。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/nlp/emotion-analysis/API_v1.html"
    },
    "F326": {
        "func": "名片识别",
        "des": "名片识别，通过OCR（光学字符识别 Optical Character Recognition）技术，对纸质名片进行识别，返回名片上的姓名、手机、电话、公司、部门、职位、传真、邮箱、网站、地址等关键信息，可以省去用户手动录入的过程，自动完成名片信息的结构化和数据的采集，可以很方便对接客户的后台数据系统，给用户带来极大的便利。该名片识别接口支持中文（简体和繁体）名片、英文、以及 16种小语种 名片，接口可以 自动识别名片语种。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/businessCardRecg/API.html"
    },
    "F327": {
        "func": "营业执照识别 intsig",
        "des": "营业执照识别，通过 OCR（光学字符识别 Optical Character Recognition）技术，对营业执照图片进行识别，返回营业执照图片上的注册号、名称、类型、住所、法定代表人、注册资本、成立日期、营业期限和经营范围等信息，可以省去用户手动录入的过程，自动完成营业执照信息的结构化和图像数据的采集，可以很方便对接客户的后台数据系统，给用户带来极大的便利，方便用户保存。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/words/businessLicenseRecg/API.html"
    },
    "F328": {
        "func": "人脸比对 sensetime",
        "des": "基于商汤的人脸算法，对两张通过接口上传的人脸照片进行比对，来判断是否为同一个人。若上传的照片中包含 exif 方向信息，我们会按此信息旋转、翻转后再做后续处理。同时，我们还提供自动旋转功能，当照片方向混乱且 exif 方向信息不存在或不正确的情况下，服务会根据照片中人脸方向来检查可能正确的方向，并按照正确的方向提供人脸检测结果。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/face/faceComparisonRecg/API.html#接口说明"
    },
    "F329": {
        "func": "人脸水印照比对",
        "des": "人脸水印照比对，对通过接口上传的人脸照片和一个人脸水印照片进行比对，来判断是否为同一个人。若上传的照片中包含 exif 方向信息，我们会按此信息旋转、翻转后再做后续处理。同时，我们还提供自动旋转功能，当照片方向混乱且 exif 方向信息不存在或不正确的情况下，服务会根据照片中人脸方向来检查可能正确的方向，并按照正确的方向提供人脸检测结果。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/face/faceWaterPhotoComparisonRecg/API.html#接口说明"
    },
    "F330": {
        "func": "性别年龄识别",
        "des": "性别年龄识别，即机器对说话者的年龄大小以及性别属性进行分析，可以通过收到的音频数据判定发音人的性别（男，女）及年龄范围（小孩，中年，老人），对语音内容和语种不做限制。",
        "owner": "讯飞",
        "doc_url": "https://www.xfyun.cn/doc/voiceservice/sound-feature-recg/API.html#%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E"
    },
    "F601": {
        "func": "增值税发票卷票识别",
        "des": "发票凭证系列提供企业报销所需的八大类发票的结构化识别以及混贴发票的自动分割与识别。发票覆盖增值税发票专票、普票和电子发票、火车票、增值税发票卷票、机票行程单、出租车票、定额发票等。",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042852.html?spm=5176.12127959.1247871.1.246e5ef7LgRATb#sku=yuncode3685200001"
    },
    "F602": {
        "func": "增值税发票识别/OCR文字识别",
        "des": "准确识别发票代码，发票号码，发票日期，校验码，发票税额，受票方名称等15个常见字段",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi027758.html?spm=5176.12127959.1247871.2.246e5ef7LgRATb&innerSource=search#sku=yuncode2175800000"
    },
    "F603": {
        "func": "印刷文字识别-机动车发票识别",
        "des": "27个字段结构化输出，准确率高",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi029811.html?spm=5176.12127959.1247871.3.246e5ef7LgRATb&innerSource=search#sku=yuncode2381100002"
    },
    "F604": {
        "func": "印刷文字识别-火车票识别/OCR文字识别",
        "des": "在线大流量：依托阿里云技术实力，提供稳定的大流量在线服务 识别精度高：业界最新深度学习技术，充分利用海量标注数据，提供高质量的识别结果，身份证准确率到达99% 高度定制化：针对众多具体的OCR应用场景，进行了大量的模型优化\r\n",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi020096.html?spm=5176.12127959.1247871.4.246e5ef7LgRATb&innerSource=search#sku=yuncode1409600000"
    },
    "F605": {
        "func": "印刷文字识别-票据混贴智能分区识别",
        "des": "覆盖8大常见票据，自动切割与子图识别，支持私有化部署",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00034969.html?spm=5176.12127959.1247871.5.246e5ef7LgRATb#sku=yuncode2896900001"
    },
    "F606": {
        "func": "出租车机打发票识别/OCR文字识别",
        "des": "提供稳定的大流量在线服务 识别精度高：业界最新深度学习技术，充分利用海量标注数据，提供高质量的识别结果",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi027786.html?spm=5176.12127959.1247871.6.246e5ef7LgRATb&innerSource=search#sku=yuncode2178600000"
    },
    "F607": {
        "func": "定额发票识别",
        "des": "准确率高、效率快、结构化输出",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00034964.html?spm=5176.12127959.1247871.7.246e5ef7LgRATb#sku=yuncode2896400002"
    },
    "F608": {
        "func": "机票行程单识别",
        "des": "机票行程单全字段识别，支持私有化部署",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00035385.html?spm=5176.12127959.1247871.8.246e5ef7LgRATb#sku=yuncode2938500002"
    },
    "F609": {
        "func": "身份证识别",
        "des": "提供稳定的大流量在线服务 识别精度高：业界最新深度学习技术，充分利用海量标注数据，提供高质量的识别结果，身份证准确率到达99% 高度定制化：针对众多具体的OCR应用场景，进行了大量的模型优化",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi010401.html?spm=5176.12127946.1247857.1.438b323eXGrDFJ&innerSource=search"
    },
    "F610": {
        "func": "身份证混贴识别",
        "des": "身份证OCR识别支持二代身份证正反面所有字段的识别，包括姓名、性别、民族、出生日期、住址、公民身份证号、签发机关、有效期限，为用户提供最方便快捷的身份证信息录入体验。基于达摩院强大的深度学习算法和OCR技术，各字段精度均处于业界领先水平，身份证号码识别准确率达到99.9%以上，姓名识别准确率98%以上。此外，读光OCR还提供身份证混贴识别接口，支持身份证正反面同时识别，一次扫描识别页面所有字段。",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042846.html?spm=5176.12127946.1247857.2.438b323eXGrDFJ"
    },
    "F611": {
        "func": "行驶证识别/OCR文字识别",
        "des": "提供稳定的大流量在线服务 识别精度高：业界最新深度学习技术，充分利用海量标注数据，提供高质量的识别结果 高度定制化：针对众多具体的OCR应用场景，进行了大量的模型优化",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57002003/cmapi011791.html?spm=5176.12127946.1247857.4.438b323eXGrDFJ&innerSource=search#sku=yuncode579100000"
    },
    "F612": {
        "func": "行驶证副页识别",
        "des": "基于阿里云OCR的深度学习，个人证照类识别提供个人身份识别所需的身份证、名片、行驶证、驾驶证、护照、户口本、不动产权证、房产证等证件的结构化识别服务，且阿里云OCR可满足此类卡证的自动分类功能，即无需提前进行卡证分类，系统可自动判断所属卡证类型并返回结构化信息。",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042884.html?spm=5176.12127946.1247857.5.438b323eXGrDFJ#sku=yuncode3688400001"
    },
    "F613": {
        "func": "行驶证混贴识别",
        "des": "阿里云行驶证支持对行驶证正页、副页关键字段的自动定位和识别。其中，行驶证的总体准确率和召回率在93%以上，适应模糊、光照不均、透视畸变、任意背景等实际应用中存在的各种情况，并可实现自动裁边、修正倾斜等。同时，也支持对正副页在同一张图片的场景进行自动分割与结构化识别。",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042847.html?spm=5176.12127946.1247857.6.438b323eXGrDFJ#sku=yuncode3684700001"
    },
    "F614": {
        "func": "银行卡识别/OCR文字识别",
        "des": "在线大流量：依托阿里云技术实力，提供稳定的大流量在线服务 识别精度高：业界最新深度学习技术，充分利用海量标注数据，提供高质量的识别结果，身份证准确率到达99% 高度定制化：针对众多具体的OCR应用场景，进行了大量的模型优化",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi016870.html?spm=5176.12127946.1247857.7.438b323eXGrDFJ&innerSource=search"
    },
    "F615": {
        "func": "驾驶证识别/OCR文字识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57002002/cmapi010402.html?spm=5176.12127946.1247857.8.438b323eXGrDFJ&innerSource=search"
    },
    "F616": {
        "func": "护照识别/OCR文字识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi016682.html?spm=5176.12127946.1247857.9.438b323eXGrDFJ&innerSource=search#sku=yuncode1068200007"
    },
    "F617": {
        "func": "多卡证智能分类识别",
        "des": "对输入的常见卡证进行自动分类、支持私有化部署",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00034972.html?spm=5176.12127946.1247857.10.438b323eXGrDFJ#sku=yuncode2897200001"
    },
    "F618": {
        "func": "卡证合集/OCR文字识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi031271.html?spm=5176.12127946.1247857.11.438b323eXGrDFJ#sku=yuncode2527100002"
    },
    "F619": {
        "func": "名片识别/OCR文字识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi013591.html?spm=5176.12127946.1247857.12.438b323eXGrDFJ&innerSource=search"
    },
    "F620": {
        "func": "户口页识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi030100.html?spm=5176.12127946.1247857.13.438b323eXGrDFJ&innerSource=search"
    },
    "F621": {
        "func": "户口户主页识别",
        "des": "基于阿里云OCR的深度学习，个人证照类识别提供个人身份识别所需的身份证、名片、行驶证、驾驶证、护照、户口本、不动产权证、房产证等证件的结构化识别服务，且阿里云OCR可满足此类卡证的自动分类功能，即无需提前进行卡证分类，系统可自动判断所属卡证类型并返回结构化信息",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042883.html?spm=5176.12127946.1247857.14.438b323eXGrDFJ#sku=yuncode3688300001"
    },
    "F622": {
        "func": "通用文字识别",
        "des": "识别准确率高，识别速度快，服务稳定，技术精深",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi020020.html?spm=5176.12127985.1247880.1.64174f58dShvIm&innerSource=search"
    },
    "F623": {
        "func": "网络UGC图片文字识别",
        "des": "适用于多种网络PS图片，原生数字图，通用图片， 具有高准确率，高实时性，且支持海量数据",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi023869.html?spm=5176.12127985.1247880.3.64174f58dShvIm&innerSource=search#sku=yuncode1786900000"
    },
    "F624": {
        "func": "电商图片文字识别",
        "des": "支持多种电商数据类型图片：主图，详情图，评价图， 商业资质图。具有高准确率，高实时性，且可处理海量数据。",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi023874.html?spm=5176.12127985.1247880.2.64174f58dShvIm&innerSource=search#sku=yuncode1787400000"
    },
    "F625": {
        "func": "社区贴吧图片文字识别",
        "des": "适用于多种发帖图片，如贴吧，图像分享网站，社交媒体图片 具有高准确率，高实时性，且支持海量数据",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi023871.html?spm=5176.12127985.1247880.4.64174f58dShvIm&innerSource=search#sku=yuncode1787100000"
    },
    "F626": {
        "func": "文档小说图片文字识别",
        "des": "适用于多种纯文字类书籍，出文字文档的文字识别 具有高准确率，高实时性，且支持海量数据",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi023866.html?spm=5176.12127985.1247880.5.64174f58dShvIm&innerSource=search#sku=yuncode1786600000"
    },
    "F627": {
        "func": "二维码识别",
        "des": "高精度检测模型，可识别",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi033158.html?spm=5176.12127985.1247880.6.64174f58dShvIm#sku=yuncode2715800004"
    },
    "F628": {
        "func": "英文专项识别",
        "des": "高精度的英文识别能力 兼容旋转、表格等基础功能",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi032063.html?spm=5176.12127985.1247880.8.64174f58dShvIm#sku=yuncode2606300001"
    },
    "F629": {
        "func": "日语识别",
        "des": "阿里云多语言系列覆盖了几大语系，覆盖十余个国家的语言检测识别。适用于国际化所需的各类图文识别与信息翻译。通用多语言识别模型可自动对语言模型进行分类检测，更加通用灵活。专用语言模型提供特定语言识别模型，精准度更高",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043312.html?spm=5176.12127985.1247880.9.64174f58dShvIm#sku=yuncode3731200001"
    },
    "F630": {
        "func": "俄语识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043313.html?spm=5176.12127985.1247880.10.64174f58dShvIm#sku=yuncode3731300001"
    },
    "F631": {
        "func": "韩文识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043314.html?spm=5176.12127985.1247880.11.64174f58dShvIm#sku=yuncode3731400001"
    },
    "F632": {
        "func": "泰文识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043315.html?spm=5176.12127985.1247880.12.64174f58dShvIm#sku=yuncode3731500001"
    },
    "F633": {
        "func": "OCR拉丁语识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043316.html?spm=5176.12127985.1247880.13.64174f58dShvIm#sku=yuncode3731600001"
    },
    "F634": {
        "func": "多语言分词-中文分词通用",
        "des": "包含基本语义粒度，更小的检索粒度以及扩展检索粒度，基于阿里核心业务沉淀，在通用、电商、文娱领域都处于领先水平，除中文外，还支持英文小粒度分词、泰语分词，通过多年的语料及算法研发积累，可在短时间内分析海量文本，帮助客户更好更精确的挖掘出文本价值",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/61384.html?spm=a2c4g.11186623.6.548.116b385cs7PcCw"
    },
    "F635": {
        "func": "词性标注",
        "des": "包含基本语义粒度，更小的检索粒度以及扩展检索粒度，基于阿里核心业务沉淀，在通用、电商、文娱领域都处于领先水平，服务可用性高达 99.9%，根据调用量动态调整，支持上亿量级的调用及数据监控，通过多年的语料及算法研发积累，可在短时间内分析海量文本，帮助客户更好更精确的挖掘出文本价值",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/61378.html?spm=a2c4g.11186623.6.549.364335fd65VSmo"
    },
    "F636": {
        "func": "命名实体",
        "des": "依托阿里大生态，历经多个领域业务场景锤炼，覆盖电商、娱乐、新闻等多个领域，基于百亿级别的数据反馈建立分析模型，提升模型的精度和适配性，结合细分领域，构建细粒度标签，实体类别超过50个，应对层出不穷的新品牌、新品类、新电影等，构建自动的专名识别机制，定期增量更新\n",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/61387.html?spm=a2c4g.11186623.6.550.55d02349B2Js5N"
    },
    "F637": {
        "func": "情感分析",
        "des": "",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/61389.html?spm=a2c4g.11186623.6.551.6e7b48bcXYhf3S"
    },
    "F638": {
        "func": "中心词提取",
        "des": "使用电商标题中心词以及类目进行训练，通过给每个词计算一个相关性分数来衡量每个词与句子的相关性程度，进而识别并提取出句子的中心词。",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/90742.html?spm=a2c4g.11186623.6.552.110879748T6hkX"
    },
    "F639": {
        "func": "智能文本分类",
        "des": "对用户输入的一段文本，映射到具体的类目上。\n\n支持的类目体系可以是平层类目或者以树状形式组织的层次类目，系统内置两种默认分类体系：新闻资讯领域类目体系、电商领域类目体系。其中：\n\n新闻资讯分为15个类目（健康、观点、旅游、经济、房产、文娱、社会、国际、消费、从政、数码、汽车、教育、体育、防腐前沿）；\n电商领域类目为17个分类，（数码／科技、游戏、汽车/摩托车/电动车、穿搭／时尚、美容/个人护理、摄影、动漫/二次元、园艺、萌宠、母婴、旅游、家居／生活百货、美食、运动／户外、文娱/影视、星座、其他）。\n同时支持对用户输入的文本，识别出其中的关键词，并给出每个关键词的类别信息（产品词、品牌词、人物等）。关键词会根据文本所属的不同领域信息来进行抽取。目前支持新闻资讯领域和电商领域的关键词打标。",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/90737.html?spm=a2c4g.11186623.6.553.69416889DDjI3n"
    },
    "F640": {
        "func": "文本信息抽取",
        "des": "",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/90731.html?spm=a2c4g.11186623.6.554.53ee7890J4UXkz"
    },
    "F641": {
        "func": "商品评价解析",
        "des": "技术积累来自阿里电商平台全量商品的评价处理，包括对评价内容的解析，确保排序优先输出对消费者决策有帮助的评价；\r\n\r\n提炼商品的关键属性，搭建符合行业特性的标签体系，帮助消费者快速了解买过用户的体验；\r\n\r\n支持“评价体或微博体” 的情感分析：对用户的评价进行结构化，分为商品、服务、物流三大类并且进行情感分析，可协助商家有针对性地展开售后服务；\r\n\r\n支持商品属性维度的情感分析：对于覆盖行业的商品，进行关键属性的提炼及情感打分，让商家第一时间全面了解店铺已售商品的消费者印象，对后续销售方向提供决策依据；",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/64231.html?spm=a2c4g.11186623.6.555.6dbb3dbfJOABd5"
    },
    "F642": {
        "func": "地址抽取",
        "des": "从自然文本中提取出地址片段。将碎片化的地址信息提取归类。去除地址信息以外的信息杂质，抽取后的地址规范标准。\n\n例如从文章文本，快递物流运单，案件卷宗，客服聊天记录等信息中抽取地址数据，并且纠错之后输出标准化地址数据",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/169628.html?spm=a2c4g.11174283.6.563.2fb930f4WoovO0"
    },
    "F643": {
        "func": "姓名抽取",
        "des": "有些业务场景需要从物流单据的地址信息中提取出收件人和寄件人的姓名信息使用，这样的需求可以通过姓名抽取功能完成。",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/169631.html?spm=a2c4g.11186623.6.564.326f3661RCuRhF"
    },
    "F644": {
        "func": "电话号码抽取",
        "des": "需要提取收件人和寄件人的联络电话号码，此种需求则可以通过电话号码抽取来满足。\r\n\r\n该服务可以从物流运单中精准识别，抽取手机或者固话文本信息。将其他的信息都剔除干净",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/169632.html?spm=a2c4g.11186623.6.565.3d0419a69VVVVc"
    },
    "F645": {
        "func": "行政区划识别",
        "des": "该项服务可以根据输入的地址（可以是完整的地址信息或不完整的地址信息）或者POI信息（如小区名称，酒吧商店名称等等），识别出所对应的行政区划。同时，行政区划识别支持对缺失的行政区划进行补全，最终系统会输出的内容是：行政区划编码 + 省+ 市 + 区+ 街道等",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/169633.html?spm=a2c4g.11186623.6.566.4c4315c2pcuiQL"
    },
    "F646": {
        "func": "邮政编码查询",
        "des": "输入地址，输出地址所对应的邮政编码",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/169635.html?spm=a2c4g.11186623.6.567.53a136cdXXPcgV"
    },
    "F647": {
        "func": "机器翻译",
        "des": "通用版翻译以解决全场景语言障碍为目标，多领域适用，现可支持。通用版翻译引擎致力于解决全场景语言障碍，多领域适用，可快速实现一种语言到另一种语言的自动翻译。依托阿里巴巴领先的自然语言处理技术和海量数据优势，通用版翻译覆盖全球214种语言",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/158244.html?spm=a2c4g.11186623.6.564.2385e93dBbgDgu"
    },
    "F648": {
        "func": "语音合成",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://help.aliyun.com/document_detail/84435.html?spm=a2c4g.11186623.6.609.637231a9ZkdN0B"
    },
    "F649": {
        "func": "出生证明识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043620.html?spm=5176.12127946.1247857.3.438b323eXGrDFJ"
    },
    "F650": {
        "func": "车辆登记证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00038697.html?spm=5176.12127952.1247870.4.6224529fIKBqYx#sku=yuncode3269700001"
    },
    "F651": {
        "func": "车牌识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi020094.html?spm=5176.12127952.1247870.5.6224529fIKBqYx#sku=yuncode1409400000"
    },
    "F652": {
        "func": "vin码识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi023049.html?spm=5176.12127952.1247870.7.6224529fIKBqYx#sku=yuncode1704900000"
    },
    "F653": {
        "func": "医疗器械生产许可证",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042848.html?spm=5176.12127972.1245136.1.359c45489rzz77#sku=yuncode3684800001"
    },
    "F654": {
        "func": "医疗器械经营许可证",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042850.html?spm=5176.12127972.1245136.2.359c45489rzz77#sku=yuncode3685000001"
    },
    "F655": {
        "func": "第二类医疗器械经营备案凭证",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042851.html?spm=5176.12127972.1245136.3.359c4548ZsuGc6#sku=yuncode3685100001"
    },
    "F656": {
        "func": "银行开户许可证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042885.html?spm=5176.12127972.1245136.4.359c4548ZsuGc6#sku=yuncode3688500001"
    },
    "F657": {
        "func": "营业执照识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi013592.html?spm=5176.12127972.1245136.5.359c4548ZsuGc6&innerSource=search_%E5%8D%B0%E5%88%B7%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E8%90%A5%E4%B8%9A%E6%89%A7%E7%85%A7#sku=yuncode759200000"
    },
    "F658": {
        "func": "公章识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57002003/cmapi029878.html?spm=5176.12127972.1245136.6.359c4548ZsuGc6&innerSource=search#sku=yuncode2387800002"
    },
    "F659": {
        "func": "房产证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi028523.html?spm=5176.12127972.1245136.7.359c4548ZsuGc6#sku=yuncode2252300000"
    },
    "F660": {
        "func": "不动产权证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi032590.html?spm=5176.12127972.1245136.8.359c4548ZsuGc6&innerSource=search_%E4%B8%8D%E5%8A%A8%E4%BA%A7%E6%9D%83%E8%AF%81#sku=yuncode2659000001"
    },
    "F661": {
        "func": "食品经营许可证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi033384.html?spm=5176.12127972.1245136.9.359c4548R9AN3F#sku=yuncode2738400001"
    },
    "F662": {
        "func": "食品生产许可证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00034966.html?spm=5176.12127972.1245136.10.359c4548R9AN3F#sku=yuncode2896600002"
    },
    "F663": {
        "func": "商标注册证识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00034968.html?spm=5176.12127972.1245136.11.359c4548R9AN3F#sku=yuncode2896800001"
    },
    "F664": {
        "func": "文档结构化还原识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi032068.html?spm=5176.12127997.1247897.2.1f9670ed6ZDS7C#sku=yuncode2606800001"
    },
    "F665": {
        "func": "表格识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi024968.html?spm=5176.12127997.1247897.3.1f9670ed6ZDS7C&innerSource=search#sku=yuncode1896800002"
    },
    "F666": {
        "func": "题目识别",
        "des": "读光题目识别可对教育中的题目进行有效识别。通过对题目的元素进行打标，提升题目的识别效果。目前主要覆盖的标签类型包含但不限于：公式、手写体、印刷体、下划线、图片等，是拍照搜题等功能的基础原子能力",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043052.html?spm=5176.13747602.1402579.1.5bce2cfczTIebD#sku=yuncode3705200001"
    },
    "F667": {
        "func": "英语作文识别",
        "des": "阿里云试题作业OCR识别产品能力，主要针对教育应用场景中对试题题目、数学公式、速算题目等信息的智能化识别需求，通过对通用OCR高精度识别能力的教育场景迭代优化，为用户提供数学试题图片中题目文本及数学公式的识别、速算题目文字的检测和识别等服务，并返回题目框位置与内容，为智慧教学场景下的拍照搜题、板书识别、自动阅卷等应用提供关键基石技术能力。",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043291.html?spm=5176.13747602.1402579.2.5bce2cfczTIebD#sku=yuncode3729100001"
    },
    "F668": {
        "func": "练习册试卷结构化识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00042623.html?spm=5176.13747602.1402579.3.5bce2cfczTIebD#sku=yuncode3662300001"
    },
    "F669": {
        "func": "板书/笔记识别",
        "des": "试题作业OCR识别产品能力，主要针对教育应用场景中对试题题目、数学公式、速算题目等信息的智能化识别需求，通过对通用OCR高精度识别能力的教育场景迭代优化，为用户提供数学试题图片中题目文本及数学公式的识别、速算题目文字的检测和识别等服务，并返回题目框位置与内容，为智慧教学场景下的拍照搜题、板书识别、自动阅卷等应用提供关键基石技术能力",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043474.html?spm=5176.13747602.1402579.4.5bce2cfczTIebD#sku=yuncode3747400001"
    },
    "F670": {
        "func": "数学公式识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043292.html?spm=5176.13747602.1402579.5.5bce2cfczTIebD#sku=yuncode3729200001"
    },
    "F671": {
        "func": "答题卡主观题识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043294.html?spm=5176.13747602.1402579.6.5bce2cfczTIebD#sku=yuncode3729400001"
    },
    "F672": {
        "func": "口算判题",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00043293.html?spm=5176.13747602.1402579.7.5bce2cfczTIebD#sku=yuncode3729300001"
    },
    "F673": {
        "func": "试卷识别",
        "des": "/",
        "owner": "阿里",
        "doc_url": "https://market.aliyun.com/products/57124001/cmapi00035522.html?spm=5176.13747602.1402579.8.5bce2cfczTIebD#sku=yuncode2952200001"
    },
    "F901": {
        "func": "中文分词",
        "des": "对文本进行分词处理",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0009.html"
    },
    "F902": {
        "func": "命名实体识别（基础版）",
        "des": "对文本进行命名实体识别分析，目前支持人名、地名、时间、组织机构类实体的识别。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0010.html"
    },
    "F903": {
        "func": "命名实体识别（领域版）",
        "des": "对文本进行命名实体识别分析，目前支持通用、商务和娱乐领域。\n\n通用领域：支持人名、地名、组织机构、时间点、日期、百分比、货币额度、序数词、计量规格词、民族、职业、邮箱、国家、节日的实体的识别。\n商务领域：支持公司名、品牌名、职业、职位、邮箱、手机号码、电话号码、IP地址、身份证号、网址的实体的识别。\n娱乐领域：支持电影名、动漫、书名、互联网、歌名、产品名、电视剧名、电视节目名的实体的识别。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0060.html"
    },
    "F904": {
        "func": "文本相似度（基础版）",
        "des": "对文本对进行相似度计算。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0025.html"
    },
    "F905": {
        "func": "句向量",
        "des": "输入句子，返回对应的句向量。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0026.html"
    },
    "F906": {
        "func": "实体链接",
        "des": "针对通用领域的文本进行实体链接分析，识别出其中的实体，并返回实体相关信息。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0061.html"
    },
    "F907": {
        "func": "关键词抽取",
        "des": "根据指定文本，抽取其中最能够反映文本主题或者意思的词汇。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0084.html"
    },
    "F908": {
        "func": "情感分析（基础版）",
        "des": "针对通用领域的用户评论进行情感分析。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0015.html"
    },
    "F909": {
        "func": "情感分析（领域版）",
        "des": "领域情感分析，针对未知领域，电商，汽车领域的用户评论进行情感分析。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0056.html"
    },
    "F910": {
        "func": "意图理解",
        "des": "针对天气类、报时、新闻类、笑话类、翻译类、提醒类、闹钟类、音乐类8个领域进行意图理解。意图理解包括对用户的问题，陈述进行领域识别以及对对应领域所包含的实体进行抽取",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0062.html"
    },
    "F911": {
        "func": "文本分类",
        "des": "针对广告领域的自动分类，判断是否是广告。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0017.html"
    },
    "F912": {
        "func": "文本摘要（基础版）",
        "des": "对文本生成摘要。\r\n文本摘要（基础版）和文本摘要（领域版）基于不同算法实现，对相同文本，基础版和领域版的结果有所差别。根据测试数据，领域版效果一般优于基础版。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0013.html"
    },
    "F913": {
        "func": "文本摘要（领域版）",
        "des": "根据不同领域的语料训练特定领域的摘要模型，能有效提升文本摘要的效果。\r\n文本摘要（基础版）和文本摘要（领域版）基于不同算法实现，对相同文本，基础版和领域版的结果有所差别。根据测试数据，领域版效果一般优于基础版。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0071.html"
    },
    "F914": {
        "func": "诗歌生成",
        "des": "根据用户的输入生成诗歌。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0070.html"
    },
    "F915": {
        "func": "语种识别",
        "des": "语种识别是为了识别文本所属的语种。对于用户输入的文本，返回识别出的所属语种。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-nlp/nlp_03_0055.html"
    },
    "F916": {
        "func": "多粒度分词",
        "des": "给定一个句子输入，输出不同粒度的所有单词的层次结构。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/sdkreference-nlp/nlp_06_0091.html"
    },
    "F917": {
        "func": "一句话语音识别",
        "des": "一句话识别接口，用于短语音的同步识别。一次性上传整个音频，响应中即返回识别结果",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-sis/sis_03_0040.html"
    },
    "F918": {
        "func": "名人识别",
        "des": "分析并识别图片中包含的明星及网红人物，返回人物信息及人脸坐标。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-image/image_03_0027.html"
    },
    "F919": {
        "func": "图像标签",
        "des": "图像标签服务准确识别自然图片中数百种场景、上千种通用物体及其属性。让智能相册管理、照片检索和分类、基于场景内容或者物体的广告推荐等功能更加直观。使用时用户发送待处理图片，返回图片标签内容及相应置信度。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-image/image_03_0025.html"
    },
    "F920": {
        "func": "翻拍识别",
        "des": "零售行业通常根据零售店的销售量进行销售奖励，拍摄售出商品的条形码上传后台是常用的统计方式。翻拍识别利用深度神经网络算法判断条形码图片为原始拍摄，还是经过二次翻拍、打印翻拍等手法二次处理的图片。利用翻拍识别，可以检测出经过二次处理的不合规范图片，使得统计数据更准确、有效。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-image/image_03_0026.html"
    },
    "F921": {
        "func": "内容审核 - 文本",
        "des": "分析并识别用户上传的文本内容是否有敏感内容（如色情、政治等），并将识别结果返回给用户。",
        "owner": "华为",
        "doc_url": "https://support.huaweicloud.com/api-moderation/moderation_03_0018.html"
    },
    "F1201": {
        "func": "文本纠错",
        "des": "提供对中文文本的自动纠错功能，能够识别输入文本中的错误片段，定位错误并给出正确的文本结果；支持长度不超过2000字的长文本纠错。\n此功能是基于千亿级大规模互联网语料和LSTM、BERT等深度神经网络模型进行训练，并持续迭代更新，以保证效果不断提升，是搜索引擎、语音识别、内容审核等功能更好运行的基础之一。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/271/35509"
    },
    "F1202": {
        "func": "依存句法分析",
        "des": "句法依存分析接口能够分析出句子中词与词之间的相互依存关系，并揭示其句法结构，包括主谓关系、动宾关系、核心关系等等，可用于提取句子主干、提取句子核心词等，在机器翻译、自动问答、知识抽取等领域都有很好的应用。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/271/35510"
    },
    "F1203": {
        "func": "词向量",
        "des": "词向量接口能够将输入的词语映射成一个固定维度的词向量，用来表示这个词语的语义特征。词向量是很多自然语言处理技术的基础，能够显著提高它们的效果。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35505"
    },
    "F1204": {
        "func": "句向量",
        "des": "句向量接口能够将输入的句子映射成一个固定维度的向量，用来表示这个句子的语义特征，可用于文本聚类、文本相似度、文本分类等任务，能够显著提高它们的效果。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35507"
    },
    "F1205": {
        "func": "词相似度",
        "des": "词相似度接口能够基于词向量技术来计算两个输入词语的余弦相似度，相似度数值越大的两个词语在语义上越相似。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35504"
    },
    "F1206": {
        "func": "句子相似度",
        "des": "句子相似度接口能够基于深度学习技术来计算一个源句子和多个目标句子的相似度，相似度分值越大的两个句子在语义上越相似。目前仅支持短文本（不超过500字符）的相似度计算，长文本的相似度计算也即将推出。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/44681"
    },
    "F1207": {
        "func": "闲聊（对话机器人）",
        "des": "闲聊服务基于腾讯领先的NLP引擎能力、数据运算能力和千亿级互联网语料数据的支持，同时集成了广泛的知识问答能力，可实现上百种自定义属性配置，以及儿童语言风格及说话方式，从而让聊天变得更睿智、简单和有趣。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/271/39416"
    },
    "F1208": {
        "func": "实体信息查询",
        "des": "输入实体名称，返回实体相关的信息如实体别名、实体英文名、实体详细信息、相关实体等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/271/39420"
    },
    "F1209": {
        "func": "实体关系查询",
        "des": "输入两个实体，返回两个实体间的关系，例如马化腾与腾讯公司不仅是相关实体，二者还存在隶属关系（马化腾属于腾讯公司）。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/271/39419"
    },
    "F1210": {
        "func": "文本摘要摘取",
        "des": "利用人工智能算法，自动抽取文本中的关键信息并生成指定长度的文本摘要。可用于新闻标题生成、科技文献摘要生成和商品评论摘要等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35499"
    },
    "F1211": {
        "func": "关键词提取",
        "des": "基于关键词提取平台，通过对文本内容进行深度分析，提取出文本内容中的关键信息，为用户实现诸如新闻内容关键词自动提取、评论关键词提取等提供基础服务。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35498"
    },
    "F1212": {
        "func": "情感分析",
        "des": "情感分析接口能够对带有情感色彩的主观性文本进行分析、处理、归纳和推理，识别出用户的情感倾向，是积极还是消极，并且提供各自概率。\n该功能基于千亿级大规模互联网语料和LSTM、BERT等深度神经网络模型进行训练，并持续迭代更新，以保证效果不断提升。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35497"
    },
    "F1213": {
        "func": "文本分类",
        "des": "文本分类接口能够对用户输入的文本进行自动分类，将其映射到具体的类目上，用户只需要提供待分类的文本，而无需关注具体实现。\n该功能基于千亿级大规模互联网语料和LSTM、BERT等深度神经网络模型进行训练，并持续迭代更新，以保证效果不断提升。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35496"
    },
    "F1214": {
        "func": "相似词查询",
        "des": "相似词接口能够基于同义词库及词向量技术，检索出与输入词语在语义上最相似的若干个词语，可广泛用于检索系统、问答系统、文档归档等场景。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35493"
    },
    "F1215": {
        "func": "词法分析",
        "des": "词法分析接口提供以下三个功能：\n1、智能分词：将连续的自然语言文本，切分成具有语义合理性和完整性的词汇序列；\n2、词性标注：为每一个词附上对应的词性，例如名词、代词、形容词、动词等；\n3、命名实体识别：快速识别文本中的实体，例如人名、地名、机构名等。\n所有的功能均基于千亿级大规模互联网语料进行持续迭代更新，以保证效果不断提升，用户无需担心新词发现、歧义消除、调用性能等问题。目前词法分析已经在泛互联网、金融、政务等不同垂直领域提供业务支持，并取得良好的效果",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/api/271/35494"
    },
    "F1216": {
        "func": "英文识别",
        "des": "本接口支持图像英文文字的检测和识别，返回文字框位置与文字内容。支持多场景、任意版面下的英文、字母、数字和常见字符的识别，同时覆盖英文印刷体和英文手写体识别。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/34938"
    },
    "F1217": {
        "func": "通用印刷体识别",
        "des": "本接口支持图像整体文字的检测和识别。可以识别中文、英文、中英文、日语、韩语、西班牙语、法语、德语、葡萄牙语、越南语、马来语、俄语、意大利语、荷兰语、瑞典语、芬兰语、丹麦语、挪威语、匈牙利语、泰语，阿拉伯语20种语言，且各种语言均支持与英文混合的文字识别。适用于印刷文档识别、网络图片识别、广告图文字识别、街景店招牌识别、菜单识别、视频标题识别、头像文字识别等场景。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/33526"
    },
    "F1218": {
        "func": "通用印刷体识别（高精度版）",
        "des": "本接口支持图像整体文字的检测和识别。支持中文、英文、中英文、数字和特殊字符号的识别，并返回文字框位置和文字内容。\r\n适用于文字较多、版式复杂、对识别准召率要求较高的场景，如试卷试题、网络图片、街景店招牌、法律卷宗等场景。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/34937"
    },
    "F1219": {
        "func": "通用印刷体识别（精简版）",
        "des": "本接口支持图像整体文字的检测和识别。支持中文、英文、中英文、数字和特殊字符号的识别，并返回文字框位置和文字内容。适用于快速文本识别场景。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37831"
    },
    "F1220": {
        "func": "通用手写体识别",
        "des": "本接口支持图片内手写体文字的检测和识别，针对手写字体无规则、字迹潦草、模糊等特点进行了识别能力的增强。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36212"
    },
    "F1221": {
        "func": "快速文本检测",
        "des": "本接口通过检测图片中的文字信息特征，快速判断图片中有无文字并返回判断结果，帮助用户过滤无文字的图片。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37830"
    },
    "F1222": {
        "func": "广告文字识别",
        "des": "本接口支持广告商品图片内文字的检测和识别，返回文本框位置与文字内容。\n产品优势：针对广告商品图片普遍存在较多繁体字、艺术字的特点，进行了识别能力的增强。支持中英文、横排、竖排以及倾斜场景文字识别。文字识别的召回率和准确率能达到96%以上。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/49524"
    },
    "F1223": {
        "func": "身份证识别",
        "des": "本接口支持中国大陆居民二代身份证正反面所有字段的识别，包括姓名、性别、民族、出生日期、住址、公民身份证号、签发机关、有效期限，识别准确度达到99%以上。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/33524"
    },
    "F1224": {
        "func": "护照识别（中国大陆）",
        "des": "本接口支持中国大陆地区护照个人资料页多个字段的检测与识别。已支持字段包括英文姓名、中文姓名、国家码、护照号、出生地、出生日期、国籍英文、性别英文、有效期、签发地点英文、签发日期、持证人签名、护照机读码（MRZ码）等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37840"
    },
    "F1225": {
        "func": "名片识别",
        "des": "本接口支持名片各字段的自动定位与识别，包含姓名、电话、手机号、邮箱、公司、部门、职位、网址、地址、QQ、微信、MSN等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36214"
    },
    "F1226": {
        "func": "银行卡识别",
        "des": "本接口支持对中国大陆主流银行卡的卡号、银行信息、有效期等关键字段的检测与识别。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36216"
    },
    "F1227": {
        "func": "事业单位法人证书识别",
        "des": "本接口支持事业单位法人证书关键字段识别，包括注册号、有效期、住所、名称、法定代表人等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38299"
    },
    "F1228": {
        "func": "组织机构代码证识别",
        "des": "本接口支持组织机构代码证关键字段的识别，包括代码、有效期、地址、机构名称等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38298"
    },
    "F1229": {
        "func": "不动产权证识别",
        "des": "本接口支持不动产权证关键字段的识别，包括使用期限、面积、用途、权利性质、权利类型、坐落、共有情况、权利人、权利其他状况等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38300"
    },
    "F1230": {
        "func": "通用印刷体识别（高速版）",
        "des": "本接口支持图片中整体文字的检测和识别，返回文字框位置与文字内容。相比通用印刷体识别接口，识别速度更快、支持的 QPS 更高。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/33525"
    },
    "F1231": {
        "func": "企业证照识别",
        "des": "本接口支持智能化识别各类企业登记证书、许可证书、企业执照、三证合一类证书，结构化输出统一社会信用代码、公司名称、法定代表人、公司地址、注册资金、企业类型、经营范围等关键字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38849"
    },
    "F1232": {
        "func": "户口本识别",
        "des": "本接口支持居民户口簿户主页及成员页关键字段的识别，包括姓名、户别、地址、籍贯、身份证号码等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/40036"
    },
    "F1233": {
        "func": "房产证识别",
        "des": "本接口支持房产证关键字段的识别，包括房地产权利人、共有情况、登记时间、规划用途、房屋性质、房屋坐落等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/40037"
    },
    "F1234": {
        "func": "港澳台通行证识别",
        "des": "本接口支持对卡式港澳台通行证的识别，包括签发地点、签发机关、有效期限、性别、出生日期、英文姓名、姓名、证件号等字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37074"
    },
    "F1235": {
        "func": "表格识别（V1)（内部文字）",
        "des": "本接口支持图片内表格文档的检测和识别，返回每个单元格的文字内容，支持将识别结果保存为 Excel 格式。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/34936"
    },
    "F1236": {
        "func": "算式识别",
        "des": "本接口支持作业算式题目的自动识别，目前覆盖 K12 学力范围内的 14 种题型，包括加减乘除四则运算、分数四则运算、竖式四则运算、脱式计算等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/34939"
    },
    "F1237": {
        "func": "公式识别",
        "des": "本接口支持识别主流初高中数学符号和公式，返回公式的 Latex 格式文本。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38293"
    },
    "F1238": {
        "func": "数学试题识别",
        "des": "本接口支持数学试题内容的识别和结构化输出，包括通用文本解析和小学/初中/高中数学公式解析能力（包括91种题型，180种符号）。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38294"
    },
    "F1239": {
        "func": "保险单据识别",
        "des": "本接口支持病案首页、费用清单、结算单、医疗发票四种保险理赔单据的文本识别和结构化输出。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38848"
    },
    "F1240": {
        "func": "印章识别",
        "des": "印章识别已支持各类印章，包括发票章，财务章等，适用于公文，票据等场景。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/45807"
    },
    "F1241": {
        "func": "车辆VIN码识别",
        "des": "本接口支持图片内车辆识别代号（VIN）的检测和识别。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/34935"
    },
    "F1242": {
        "func": "车牌识别",
        "des": "本接口支持对中国大陆机动车车牌的自动定位和识别，返回地域编号和车牌号信息。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36211"
    },
    "F1243": {
        "func": "驾驶证识别",
        "des": "本接口支持驾驶证主页和副页所有字段的自动定位与识别，重点字段的识别准确度达到99%以上。\r\n驾驶证主页：包括证号、姓名、性别、国籍、住址、出生日期、初次领证日期、准驾车型、有效期限。\r\n驾驶证副页：包括证号、姓名、档案编号、记录。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36213"
    },
    "F1244": {
        "func": "行驶证识别",
        "des": "本接口支持行驶证主页和副页所有字段的自动定位与识别。\r\n行驶证主页：车牌号码、车辆类型、所有人、住址、使用性质、品牌型号、识别代码、发动机号、注册日期、发证日期、发证单位。\r\n行驶证副页：号牌号码、档案编号、核定载人数、总质量、整备质量、核定载质量、外廓尺寸、准牵引总质量、备注、检验记录",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36209"
    },
    "F1245": {
        "func": "机动车登记证书识别",
        "des": "本接口支持国内机动车登记证书主要字段的结构化识别，包括机动车所有人、身份证明名称、号码、车辆型号、车辆识别代号、发动机号、制造厂名称等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38297"
    },
    "F1246": {
        "func": "网约车驾驶证书识别",
        "des": "本接口支持网约车驾驶证关键字段的识别，包括姓名、证号、起始日期、截止日期、发证日期。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/47165"
    },
    "F1247": {
        "func": "网约车运输证识别",
        "des": "本接口支持网约车运输证关键字段的识别，包括交运管许可字号、车辆所有人、车辆号牌、起始日期、截止日期、发证日期。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/47325"
    },
    "F1248": {
        "func": "运单识别",
        "des": "本接口支持市面上主流版式电子运单的识别，包括收件人和寄件人的姓名、电话、地址以及运单号等字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/34934"
    },
    "F1249": {
        "func": "增值税发票识别",
        "des": "本接口支持增值税专用发票、增值税普通发票、增值税电子发票全字段的内容检测和识别，包括发票代码、发票号码、打印发票代码、打印发票号码、开票日期、合计金额、校验码、税率、合计税额、价税合计、购买方识别号、复核、销售方识别号、开票人、密码区1、密码区2、密码区3、密码区4、发票名称、购买方名称、销售方名称、服务名称、备注、规格型号、数量、单价、金额、税额、收款人等字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/36210"
    },
    "F1250": {
        "func": "出租车发票",
        "des": "本接口支持出租车发票关键字段的识别，包括发票号码、发票代码、金额、日期、上下车时间、里程、车牌号、发票类型及所属地区等字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37072"
    },
    "F1251": {
        "func": "定额发票识别",
        "des": "本接口支持定额发票的发票号码、发票代码、金额(大小写)、发票消费类型、地区及是否有公司印章等关键字段的识别。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37073"
    },
    "F1252": {
        "func": "火车票识别",
        "des": "本接口支持火车票全字段的识别，包括编号、票价、姓名、座位号、出发时间、出发站、到达站、车次、席别、发票类型及序列号等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37071"
    },
    "F1253": {
        "func": "购车发票识别",
        "des": "本接口支持机动车销售统一发票和二手车销售统一发票的识别，包括发票号码、发票代码、合计金额、合计税额等二十多个字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37076"
    },
    "F1254": {
        "func": "过路过桥费发票识别",
        "des": "本接口支持对过路过桥费发票的发票代码、发票号码、日期、小写金额等关键字段的识别。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37833"
    },
    "F1255": {
        "func": "轮船票识别",
        "des": "本接口支持识别轮船票的发票代码、发票号码、日期、姓名、票价、始发地、目的地、姓名、时间、发票消费类型、省、市、币种字段。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37834"
    },
    "F1256": {
        "func": "汽车票识别",
        "des": "本接口支持识别公路汽车客票的发票代码、发票号码、日期、姓名、票价等字段",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37838"
    },
    "F1257": {
        "func": "通用机打发票识别",
        "des": "本接口支持对通用机打发票的发票代码、发票号码、日期、购买方识别号、销售方识别号、校验码、小写金额等关键字段的识别。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37837"
    },
    "F1258": {
        "func": "机票行程单识别",
        "des": "本接口支持机票行程单关键字段的识别，包括姓名、身份证件号码、航班号、票价 、合计、电子客票号码、填开日期等。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/37075"
    },
    "F1259": {
        "func": "二维码和条形码识别",
        "des": "本接口支持条形码和二维码的识别（包括 DataMatrix 和 PDF417）",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/866/38292"
    },
    "F1260": {
        "func": "文本翻译",
        "des": "提供中文到英文、英文到中文的等多种语言的文本内容翻译服务， 经过大数据语料库、多种解码算法、翻译引擎深度优化，在新闻文章、生活口语等不同语言场景中都有深厚积累，翻译结果专业评价处于行业领先水平。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/551/15619"
    },
    "F1262": {
        "func": "语种识别",
        "des": "可自动识别文本内容的语言种类，轻量高效，无需额外实现判断方式，使面向客户的服务体验更佳。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/551/15620"
    },
    "F1261": {
        "func": "批量文本翻译",
        "des": "文本翻译的批量接口",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/551/40566"
    },
    "F1263": {
        "func": "基础语音合成",
        "des": "可以将任意文本转化为语音，实现让机器和应用张口说话。 腾讯TTS技术可以应用到很多场景，比如，移动APP语音播报新闻；智能设备语音提醒；依靠网上现有节目或少量录音，快速合成明星语音，降低邀约成本；支持车载导航语音合成的个性化语音播报。",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/1073/37995"
    },
    "F1264": {
        "func": "语音识别（一句话语音识别）",
        "des": "本接口用于对60秒之内的短音频文件进行识别\n支持中文普通话、英语、粤语、日语、上海话方言。\n支持本地语音文件上传和语音URL上传两种请求方式，音频时长不能超过60s。\n音频格式支持wav、mp3；采样率支持8000Hz或者16000Hz；采样精度支持16bits；声道支持单声道",
        "owner": "腾讯",
        "doc_url": "https://cloud.tencent.com/document/product/1093/35646"
    },
    "F1501": {
        "func": "文本流畅度",
        "des": "获取句子的困惑度（是否流畅），并定位不流畅的词汇。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/language_smooth.html"
    },
    "F1502": {
        "func": "机器翻译",
        "des": "基于先进的自然语言处理能力完成中英双语翻译。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/nmt.html"
    },
    "F1503": {
        "func": "语言模型填空",
        "des": "填充句子中缺省的关键词。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/language_cloze.html"
    },
    "F1504": {
        "func": "新闻热词生成",
        "des": "依据新闻文稿生成对应热点词汇。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/hotword.html"
    },
    "F1505": {
        "func": "评论观点抽取",
        "des": "提取输入的评论的观点标签。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/comment.html"
    },
    "F1506": {
        "func": "情感分析",
        "des": "判断输入的文本的情感极性类别。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/sentiment.html"
    },
    "F1507": {
        "func": "词法分析",
        "des": "提供中文分词、词性标注、命名实体识别三个功能，解析自然语言中的基本语言元素，并赋予词性，进一步将文本中的特定类型的事物名称或符号识别出来，使机器能更准确的理解内容，支撑自然语言的准确理解。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/lexer.html"
    },
    "F1508": {
        "func": "词向量",
        "des": "将自然语言中的词，映射为固定维度的空间向量，实现自然语言的标准化量化，提升自然语言处理的效果。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/word-vector.html"
    },
    "F1509": {
        "func": "句法分析",
        "des": "提供文本中词与词之间的依存关系和句法结构信息（如：主谓宾、定状补），帮助机器实现对用户意图的准确理解。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/systax.html"
    },
    "F1510": {
        "func": "文本分类",
        "des": "识别用户话术的领域信息，当前版本在13个领域上进行分类：歌曲、广播、故事、百科、天气、时间、新闻、生活查询、岀行、股票、购物、音箱指令、家居指令、闲聊、翻译、计算机、闹钟。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/textclassification.html"
    },
    "F1511": {
        "func": "短文本相似度",
        "des": "短文本相似度API提供不同短文本之间相似度的计算，输出的相似度是一个介于0到1之间的实数值，越大则相似度越高。这个相似度值可以直接用于结果排序，也可以作为一维基础特征作用于更复杂的系统。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/similarity.html"
    },
    "F1512": {
        "func": "短语挖掘",
        "des": "短语挖掘API主要用于语料中的新词识别，领域关键词抽取等工作。使用者可以传入一段待抽取的文本，API结果将返回从文本中识别的短语。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/market/fagougou/phrasedig.html"
    },
    "F1513": {
        "func": "闲聊",
        "des": "对非业务场景的消息进行响应，满足用户日常沟通及问答需求。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/chatbot.html"
    },
    "F1514": {
        "func": "同义词",
        "des": "近义词及相关词查询。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/corpus_synonyms.html"
    },
    "F1515": {
        "func": "聚类",
        "des": "对输入的文本数据进行聚类。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/corpus_aggregation.html"
    },
    "F1516": {
        "func": "机器阅读理解",
        "des": "让机器同人类一样拥有阅读文本的能力，提炼文本信息并正确的回答相关问题。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/thirdDocs/7/e37b51e1719844f081f2d28b549ec219-631.html"
    },
    "F1517": {
        "func": "词义相似度",
        "des": "根据输入的两个词语，计算两个词语的相似度，相似度越大的两个词在词义上越相似。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/word-similarity.html"
    },
    "F1518": {
        "func": "自定义智能写作",
        "des": "根据输入的sku及生成短文的数量等条件，智能创作营销文案。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/nlp/custom-intelligent-creation.html"
    },
    "F1519": {
        "func": "商品信息抽取",
        "des": "从商品描述中抽取商品相关属性。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/thirdDocs/7/80a20c5d4150491ebc081eb85fd29d55-632.html"
    },
    "F1520": {
        "func": "车牌识别",
        "des": "基于业界领先的深度学习技术，利用光学字符识别技术，可对输入的图片自动识别车牌字段信息，识别准确率业内领先，稳定可靠。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/plate.html"
    },
    "F1521": {
        "func": "车辆检测",
        "des": "车辆检测API能够准确地检测出图片中车辆的位置，返回其坐标与置信度。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/traffic/vehicle_detection.html"
    },
    "F1522": {
        "func": "垃圾分类识别",
        "des": "提供通过文本或图片或语音进行垃圾分类查询的能力。用户可选择通过传入单个垃圾名称进行文本形式的查询，也可通过传入图片进行图片形式的查询，也可以传入语音进行语音形式的查询。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/garbageClassification.html"
    },
    "F1523": {
        "func": "车型识别",
        "des": "车型识别 (car classification) API 为用户提供汽车车系(包含汽车品牌和系列， 如奥迪品牌S4系列）分类识别功能， 输入一张非旋转的汽车图片，返回识别结果, 可识别的汽车种类目前一共775种。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/car_class.html"
    },
    "F1524": {
        "func": "犬类识别",
        "des": "犬类识别 (dog classification) API 为用户提供狗种类识别功能， 输入一张非旋转的狗类图片，返回识别结果，目前可识别狗种类为120类。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/dog_class.html"
    },
    "F1525": {
        "func": "颜色识别",
        "des": "本API可以对输入图片的颜色分布进行分析，输出图片的N个关键颜色的色值（RGB和Hex）及其在图片中的占比。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/color_extraction.html"
    },
    "F1526": {
        "func": "货架商品检测",
        "des": "密集场景下货架商品检测接口，根据请求的图片，检测出图片中货架上商品的目标框，并返回检测结果。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/shelf/shelf_detection.html"
    },
    "F1527": {
        "func": "时尚搭配",
        "des": "本API可以根据输入的服饰图片，给出若干套与此服饰搭配的商品组合，如下图所示。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/thirdDocs/7/7d8dfdee3cdf451db7346e4653c7df5d-584.html"
    },
    "F1528": {
        "func": "通用商品识别",
        "des": "通用商品识别接口识别图片中主体显著物体，进行识别，返回商品的细粒度类别信息。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/recognize_product.html"
    },
    "F1529": {
        "func": "疫情物资识别",
        "des": "本接口能够识别图片中的医疗防疫物资，包括口罩、手套、防护服、护目镜、额温枪、防护面屏、消毒产品等。支持返回识别物品的一级类目和二级类目，以及型号、执行标准等额外信息。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/medical_material_recognize.html"
    },
    "F1530": {
        "func": "酒标识别",
        "des": "发送图片二进制数据，直接返回葡萄酒识别结果信息。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/market/9kacha/wineRec.html"
    },
    "F1531": {
        "func": "智能鉴黄",
        "des": "基于业界领先的深度学习图像识别技术，对图片影像的肤色、姿态和场景等进行智能识别 ，准确快速的输出每张图片“色情”、\"低俗”、“性感”、“正常”的概率，其中色情图片准确 率高达 99.95%，有效的规避涉黄风险，让您的内容轻松过审核，成倍的解放审核人力。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/sexy.html"
    },
    "F1532": {
        "func": "特定人物识别",
        "des": "特定人物识别主要用于对传入的图片中所有人脸进行分析，判断是否为特定审核人物。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/image/leaderRec.html"
    },
    "F1533": {
        "func": "文本智能审核",
        "des": "深入理解文本中的涉黄、涉政、暴恐等场景的违法违规信息，辅助人工高效精准定位文本内容风险问题，降低运营审核人力成本。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/censor/censor_text.html"
    },
    "F1534": {
        "func": "通用文字识别",
        "des": "基于业界领先的深度学习技术，利用光学字符识别技术，将图片上的文字转换为可编辑的文本，为您提供场景丰富、的整图文字检测和识别服务。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/universal.html"
    },
    "F1535": {
        "func": "驾驶证识别",
        "des": "驾驶证识别，可对输入的图片自动识别驾驶证信息，兼顾驾驶证首页和副页，提取驾驶人员的身份信息，输出关键字段。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/driver.html"
    },
    "F1536": {
        "func": "行驶证识别",
        "des": "基于业界领先的深度学习技术，识别机动车行驶证正页的关键字段识别，包括号牌号码、车辆类型、所有人、住址、使用性质、品牌型号、车辆识别代号、发动机号码、注册日期、发证日期等关键字段，准确可靠。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/vehicle.html"
    },
    "F1537": {
        "func": "身份证识别",
        "des": "识别二代居民身份证正反面的关键字段识别，包括姓名、性别、民族、出生日期、住址、身份证号、签发机关、有效期限，识别准确率业内领先，稳定可靠。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/idcard.html"
    },
    "F1538": {
        "func": "增值税发票识别",
        "des": "基于业界领先的基于业界领先的深度学习技术，识别发票代码，发票号码，购方名称，购方税号等20个关键字段，准确可靠。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/invoice.html"
    },
    "F1539": {
        "func": "营业执照识别",
        "des": "识别营业执照的关键字段，包括企业名称、法定代表人、经营场所、经营期限、社会信用代码等。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/business.html"
    },
    "F1540": {
        "func": "银行卡识别",
        "des": "基于业界领先的深度学习技术，识别银行卡号，日期，卡类型，银行名称，卡号位数等多个关键字段，准确可靠。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/ocr/bankcard.html"
    },
    "F1541": {
        "func": "人体检测",
        "des": "人体检测API主要用于对传入的图片中所有人体的位置进行检测，返回其坐标值以及置信度。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/body/human_detect.html"
    },
    "F1542": {
        "func": "人脸口罩识别",
        "des": "基于业界领先的深度学习技术，利用人脸识别技术针对当下疫情防控，检测人群中是否有未戴口罩着，大大减少人工防疫成本，且准确度高于业界领先水平。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/face/mask_detect.html"
    },
    "F1543": {
        "func": "人脸对比",
        "des": "人脸 1比1 比对 API 主要用于对传入的两张图的人脸进行比较，得到两张脸的相似度。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/face/faceCompare.html"
    },
    "F1544": {
        "func": "人脸检测与属性分析",
        "des": "人脸自然属性识别 API 主要用于对传入的图片中所有人脸的自然属性判别，主要有：人脸框，人脸关键点信息，人脸姿态估计，9种自然属性，分别为（性别、年龄、种族、微笑、颜值，是否带墨镜，是否带眼镜，人脸是否遮挡，是否有胡子）以及 5 种情绪(惊讶，高兴，悲伤，生气，平静)的分析。使用者可以根据实际的使用场景选择所需的属性判别结果，api结果将返回人脸位置及相应的属性值。不适用于大规模人脸很小的合影照。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/face/faceProp.html"
    },
    "F1545": {
        "func": "人体关键点检测",
        "des": "人体关键点检测API能够准确地估计出图片或视频中的人体14个主要关键点，包括：左右手肘、左右手腕、左右肩膀、头、脖子、左右脚踝、左右膝盖和左右臀等。进而能够在多个场景形式下，对站立、坐姿、运动多个姿态进行估计，从而实现对动作姿态的检测识别。可以用于游戏互动、视频直播、AR/VR、便携式可穿戴设备等场景下的人体姿态识别。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/body/pose.html"
    },
    "F1546": {
        "func": "行人重识别",
        "des": "行人重识别API能够根据图片中一个行人的服饰，肤色，身高，体态等人体特点，提取行人的特征，返回其特征矩阵。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/body/personreid.html"
    },
    "F1547": {
        "func": "细粒度人像分割",
        "des": "细粒度人像分割API能够对图片中人像进行像素级识别，可识别出帽子，头发，手套，太阳眼镜，上衣，连衣裙，大衣，袜子，裤子，连体裤，围巾，裙子，脸，左右手臂，左右腿，左右鞋这20个类别。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/body/human_parsing.html"
    },
    "F1548": {
        "func": "人脸解析",
        "des": "人脸解析（Face Parsing）是将人的头发及五官构成分解成若干区域。 本API为用户提供人脸解析以及分割功能，输入一张人脸图片，返回人的面部分割结果，一共为11类(括号中为区域分类ID): 背景(0), 脸部皮肤(1), 左眉毛(2), 右眉毛(3), 左眼(4), 右眼(5), 鼻子(6), 上唇(7), 口中(8), 下唇(9), 头发(10)。",
        "owner": "京东",
        "doc_url": "https://aidoc.jd.com/face/face_parser.html"
    },
    "F1801": {
        "func": "身份证识别",
        "des": "检测和识别中华人民共和国第二代身份证的关键字段内容，并支持返回身份证正反面信息、身份证照片分类判断结果。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/5671702"
    },
    "F1802": {
        "func": "驾驶证识别（V1）",
        "des": "检测和识别中华人民共和国机动车驾驶证（以下称“驾照”）图像为结构化的文字信息。目前只支持驾照主页正面，不支持副页正面反面。驾照图像须为正拍（垂直角度拍摄），但是允许有一定程度的旋转角度；仅支持图像里有一个驾照的主页正面，如果同时出现多页、或正副页同时出现，可能会返回空结果。 ",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/5671704"
    },
    "F1803": {
        "func": "驾驶证识别（V2）",
        "des": "检测和识别中华人民共和国机动车驾驶证（以下称“驾照”）图像，并转化为结构化的文字信息。只可识别驾照正本(main sheet)正面和副本(second sheet)正面，一张照片最多可识别一个正本正面和一个副本正面。驾照图像须为正拍（垂直角度拍摄），但是允许有一定程度的旋转角度；图片最小 100*100 像素，长宽不得超过4096像素，否则会抛出错误；支持图像里有一个或多个驾照的正本正面或副本正面，仅返回置信度最高的一个正本识别结果和一个副本识别结果，如果没有则该项返回为空。 ",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/26872594"
    },
    "F1804": {
        "func": "行驶证识别",
        "des": "检测和识别中华人民共和国机动车行驶证（以下称“行驶证”）图像为结构化的文字信息。目前只支持行驶证主页正面，不支持副页正面反面。行驶证图像须为正拍（垂直角度拍摄），但是允许有一定程度的旋转角度；仅支持图像里有一个行驶证的主页正面，如果同时出现多页、或正副页同时出现，可能会返回空结果。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/5671706"
    },
    "F1805": {
        "func": "银行卡识别（V1）",
        "des": "检测和识别各类银行卡，并返回银行卡卡片边框坐标、银行卡号码、所属银行及支持的金融组织服务。支持任意角度的识别。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/28070070"
    },
    "F1806": {
        "func": "银行卡识别（Beta）",
        "des": "检测和识别银行卡，并返回银行卡卡片边框坐标及识别出的银行卡号。当前 Beta 版本一次只支持识别一张银行卡，图像内有多张卡时，返回识别结果置信度最高的银行卡。支持任意角度的识别",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/10069553"
    },
    "F1807": {
        "func": "车牌识别（V1）",
        "des": "调用者传入一张图片文件或图片URL，检测并返回图片中车牌框并识别车牌颜色和车牌号。当传入图片中有多个车牌时，按照车牌框大小排序依次输出。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/33915254"
    },
    "F1808": {
        "func": "通用文字识别（V1）",
        "des": "调用者提供图片文件或者图片URL，进行图片分析，找出图片中出现的文字信息。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/7776484"
    },
    "F1809": {
        "func": "场景与物体识别",
        "des": "调用者提供图片文件或者图片URL，进行图片分析，识别图片场景和图片主体。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/5671708"
    },
    "F1810": {
        "func": "人脸融合",
        "des": "使用本 API，可以对模板图和融合图中的人脸进行融合操作。融合后的图片中将包含融合图中的人脸特征，以及模板图中的其他外貌特征与内容。返回值是一段 JSON，包含融合完成后图片的 Base64 编码。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/20813963"
    },
    "F1811": {
        "func": "人体检测和人体属性分析",
        "des": "调用者提供图片文件或者图片URL，进行图片分析，分析出性别和穿着的衣服的颜色。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/10071565"
    },
    "F1812": {
        "func": "美颜美型",
        "des": "对图片进行美颜和美白。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/34878217"
    },
    "F1813": {
        "func": "美颜美型（V2）",
        "des": "支持对图片中人像进行对美颜美型处理，以及对图像增加滤镜等。美颜包括：美白和磨皮；美型包括：大眼、瘦脸、小脸和去眉毛等处理。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/134252584"
    },
    "F1814": {
        "func": "骨骼点检测",
        "des": "调用者提供图片文件或者图片URL，进行图片分析，找出人体和骨骼关节点。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/37664576"
    },
    "F1815": {
        "func": "人体抠像 (V2)",
        "des": "调用者提供图片文件或者图片URL，进行图片分析，返回抠出来的人像图片。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/40608240"
    },
    "F1816": {
        "func": "人脸检测",
        "des": "传入图片进行人脸检测和人脸分析。可以检测图片内的所有人脸，对于每个检测出的人脸，会给出其唯一标识 face_token，可用于后续的人脸分析、人脸比对等操作。对于正式 API Key，支持指定图片的某一区域进行人脸检测。本 API 支持对检测到的人脸直接进行分析，获得人脸的关键点和各类属性信息。对于试用 API Key，最多只对人脸框面积最大的 5 个人脸进行分析，其他检测到的人脸可以使用 Face Analyze API 进行分析。对于正式 API Key，支持分析所有检测到的人脸。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/4888373"
    },
    "F1817": {
        "func": "手势识别",
        "des": "调用者提供图片文件或者图片URL，检测图片中出现的所有的手部，并返回其在图片中的矩形框位置与相应的手势含义。",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/10065649"
    },
    "F1818": {
        "func": "人脸皮肤检测分析",
        "des": "对人脸皮肤肤色，肤龄，眼皮，眼袋，痘痘、斑点、痣待每个矩形框置进行分析",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/140781002"
    },
    "F1819": {
        "func": "重建3D人脸效果",
        "des": "根据用户提供的单张或多张单人脸图片，构建用户的3D人脸效果。图片提供质量越高，3D建模效果越清晰",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/124332617"
    },
    "F1820": {
        "func": "人体检测",
        "des": "检测图片内的所有人体，并且支持对检测到的人体直接进行分析，获得每个人体的各类属性信息",
        "owner": "旷视",
        "doc_url": "https://console.faceplusplus.com.cn/documents/10071565"
    },
    "F2101": {
        "func": "文本翻译",
        "des": "将一段源语言文本转换成目标语言文本，可根据语言参数的不同实现多国语音之间的互译。",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2102": {
        "func": "语音翻译",
        "des": "将一段源语言音频文件转换成目标语言文本/语音，大大减轻传统文本翻译的读写成本",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2103": {
        "func": "图片翻译",
        "des": "基于文字识别与文本翻译技术，结合组段和渲染技术，满足用户翻译图片文字的需求，提升输入效率",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2104": {
        "func": "整题识别（含公式）",
        "des": "基于有道机器学习团队业界领先的深度学习技术，将自然场景下图片上的题目文字、数字及公式信息，通过定位和检测，智能识别为可编辑的文本信息，轻松实现题目电子化",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E6%95%B4%E9%A2%98%E8%AF%86%E5%88%AB%EF%BC%88%E5%90%AB%E5%85%AC%E5%BC%8F%EF%BC%89%E6%9C%8D%E5%8A%A1/%E6%95%B4%E9%A2%98%E8%AF%86%E5%88%AB%EF%BC%88%E5%90%AB%E5%85%AC%E5%BC%8F%EF%BC%89%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2105": {
        "func": "名片识别",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E5%90%8D%E7%89%87%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E5%90%8D%E7%89%87%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2106": {
        "func": "表格OCR",
        "des": "自动定位并识别图片中表格的位置、结构及文字内容，结构化返回可编辑的表格结果。支持用户上传报表、带有表格的图片等",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E8%A1%A8%E6%A0%BCOCR%E6%9C%8D%E5%8A%A1/%E8%A1%A8%E6%A0%BCOCR%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2107": {
        "func": "购物小票识别",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E8%B4%AD%E7%89%A9%E5%B0%8F%E7%A5%A8%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E8%B4%AD%E7%89%A9%E5%B0%8F%E7%A5%A8%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2108": {
        "func": "身份证识别",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E8%BA%AB%E4%BB%BD%E8%AF%81%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E8%BA%AB%E4%BB%BD%E8%AF%81%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2109": {
        "func": "通用文字识别",
        "des": "将自然场景下图片上的文字内容，通过定位和检测，智能识别为可编辑的文本信息",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2110": {
        "func": "语音合成",
        "des": "将文字转语音的服务，可根据设置参数设置合成多国多音色语音，发音自然流畅",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90TTS/API%E6%96%87%E6%A1%A3/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90%E6%9C%8D%E5%8A%A1/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html#section-9"
    },
    "F2111": {
        "func": "拍照搜题",
        "des": "有道智云拍照搜题服务基于文字识别技术，结合组段和渲染技术，满足用户拍照搜题的需求",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%8B%8D%E7%85%A7%E6%90%9C%E9%A2%98/API%E6%96%87%E6%A1%A3/%E6%8B%8D%E7%85%A7%E6%90%9C%E9%A2%98%E6%9C%8D%E5%8A%A1/%E6%8B%8D%E7%85%A7%E6%90%9C%E9%A2%98%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2112": {
        "func": "整页拍搜批改",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E6%8B%8D%E7%85%A7%E6%90%9C%E9%A2%98/API%E6%96%87%E6%A1%A3/%E6%95%B4%E9%A1%B5%E6%8B%8D%E6%90%9C%E6%89%B9%E6%94%B9%E6%9C%8D%E5%8A%A1/%E6%95%B4%E9%A1%B5%E6%8B%8D%E6%90%9C%E6%89%B9%E6%94%B9%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2113": {
        "func": "题目识别切分",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E9%A2%98%E7%9B%AE%E8%AF%86%E5%88%AB%E5%88%87%E5%88%86/API%E6%96%87%E6%A1%A3/%E9%A2%98%E7%9B%AE%E8%AF%86%E5%88%AB%E5%88%87%E5%88%86%E6%9C%8D%E5%8A%A1/%E9%A2%98%E7%9B%AE%E8%AF%86%E5%88%AB%E5%88%87%E5%88%86%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2114": {
        "func": "英文作文批改（图像识别）",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E9%A2%98%E7%9B%AE%E8%AF%86%E5%88%AB%E5%88%87%E5%88%86/API%E6%96%87%E6%A1%A3/%E9%A2%98%E7%9B%AE%E8%AF%86%E5%88%AB%E5%88%87%E5%88%86%E6%9C%8D%E5%8A%A1/%E9%A2%98%E7%9B%AE%E8%AF%86%E5%88%AB%E5%88%87%E5%88%86%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html"
    },
    "F2115": {
        "func": "英文作文批改（文本识别）",
        "des": "/",
        "owner": "有道",
        "doc_url": "https://ai.youdao.com/DOCSIRMA/html/%E4%BD%9C%E6%96%87%E6%89%B9%E6%94%B9/API%E6%96%87%E6%A1%A3/%E8%8B%B1%E8%AF%AD%E4%BD%9C%E6%96%87%E6%89%B9%E6%94%B9%EF%BC%88%E6%96%87%E6%9C%AC%E8%BE%93%E5%85%A5%EF%BC%89/%E8%8B%B1%E8%AF%AD%E4%BD%9C%E6%96%87%E6%89%B9%E6%94%B9%EF%BC%88%E6%96%87%E6%9C%AC%E8%BE%93%E5%85%A5%EF%BC%89-API%E6%96%87%E6%A1%A3.html"
    },
    "F2401": {
        "func": "身份证OCR识别",
        "des": "对大陆居民二代身份证正反面的所有字段进行结构化识别，包括姓名、性别、民族、出生日期、住址、身份证号、签发机关、有效期限；并支持检测身份证正面的头像信息，并返回其位置及头像切片的 base64。",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2402": {
        "func": "护照OCR识别",
        "des": "对护照的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2403": {
        "func": "结婚证OCR识别",
        "des": "对结婚证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2404": {
        "func": "银行卡OCR识别",
        "des": "对银行卡证件全字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2405": {
        "func": "军官证OCR识别",
        "des": "对军官证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2406": {
        "func": "外国人永久居留证OCR识别",
        "des": "对外国人永久居留证关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2407": {
        "func": "出生证明OCR识别",
        "des": "对出生证明的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2408": {
        "func": "临时身份证OCR识别",
        "des": "对临时身份证关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2409": {
        "func": "港澳台居民来往大陆证OCR识别",
        "des": "对港澳台居民来往大陆通行证关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2410": {
        "func": "户口本OCR识别",
        "des": "对户口本的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2411": {
        "func": "社保卡OCR识别",
        "des": "对社保卡上的全部字段进行识别,支持任意方向的图像自动识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2412": {
        "func": "增值税发票OCR识别",
        "des": "对增值税发票的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2413": {
        "func": "火车票OCR识别",
        "des": "火车票识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2414": {
        "func": "出租车票OCR识别",
        "des": "出租车票识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2415": {
        "func": "行程单OCR识别",
        "des": "行程单识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2416": {
        "func": "定额发票OCR识别",
        "des": "定额发票识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2417": {
        "func": "电子承兑汇票OCR识别",
        "des": "对电子承兑汇票上的全部字段进行识别,支持任意方向的图像自动识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2418": {
        "func": "银行回单OCR识别",
        "des": "可对银行回单上的全部字段进行识别,支持任意方向的图像自动识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2419": {
        "func": "VIN码OCR识别",
        "des": "对VIN码的全字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2420": {
        "func": "行驶证OCR识别",
        "des": "对行驶证正反面识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2421": {
        "func": "驾驶证OCR识别",
        "des": "对驾驶证正反面的文本识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2422": {
        "func": "机动车发票OCR识别",
        "des": "对机动车发票关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2423": {
        "func": "车辆登记证OCR识别",
        "des": "对机动车登记证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2424": {
        "func": "车辆合格证OCR识别",
        "des": "对机动车合格证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2425": {
        "func": "车牌OCR识别",
        "des": "对同一张图片中多个车牌的识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2426": {
        "func": "二手车发票OCR识别",
        "des": "对二手车发票的识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2427": {
        "func": "不动产证OCR识别",
        "des": "对不动产权证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2428": {
        "func": "不动产登记证明OCR识别",
        "des": "对不动产登记证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2429": {
        "func": "房产证OCR识别",
        "des": "可OCR识别全国统一的不动产权证、不动产登记证明 房产证识别覆盖全国所有省市版式，自动区分版式，无需手动选择 支持手机拍照图、扫描图、复印件的识别 暂不支持青海、西藏地区的房产证识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2430": {
        "func": "营业执照OCR识别",
        "des": "对营业执照的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2431": {
        "func": "开户许可证OCR识别",
        "des": "对开户许可证的关键字段识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2432": {
        "func": "组织机构代码证OCR识别",
        "des": "对组织机构代码证上的关键字段进行识别,支持任意方向的图像自动识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2433": {
        "func": "通用票据OCR识别",
        "des": "火车票识别,出租车票识别 支持行程单识别,定额发票识别 支持卷票识别,增值税发票识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2434": {
        "func": "通用文字OCR识别",
        "des": "对通用文字的识别",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2435": {
        "func": "通用表格OCR识别",
        "des": "对表格上的全部字段进行识别,支持任意方向的图像自动识别,如需要还原表格,可以根据识别结果中的left,top,width,height位置信息进行还原",
        "owner": "译图智讯",
        "doc_url": "http://www.etoplive.com/apidoc.do"
    },
    "F2701": {
        "func": "文本翻译",
        "des": "通过使用HTTP的方式向平台服务发送待翻译的文本和目标翻译语言，即可收到翻译结果。",
        "owner": "搜狗",
        "doc_url": "https://ai.sogou.com/doc/?url=/docs/content/mt"
    },
    "F2702": {
        "func": "一句话识别",
        "des": "在所有音频处理完毕后接受识别结果。一句话识别请求仅限于时间不超过 1 分钟的音频数据",
        "owner": "搜狗",
        "doc_url": "https://ai.sogou.com/doc/?url=/docs/content/asr/recognize"
    },
    "F2703": {
        "func": "语音翻译",
        "des": "通过使用 HTTP协议调用的方式向平台服务发送音频，即可收到文字转录与翻译结果。",
        "owner": "搜狗",
        "doc_url": "https://ai.sogou.com/doc/?url=/docs/content/mt-speech/"
    },
    "F2704": {
        "func": "通用语音合成",
        "des": "/",
        "owner": "搜狗",
        "doc_url": "https://ai.sogou.com/doc/?url=/docs/content/tts/"
    },
    "F2705": {
        "func": "录音文件识别（上传音频）",
        "des": "录音文件识别可以处理最长 180 分钟的语音音频数据。在提交转写任务后，用户可以通过搜狗AI开放平台统一异步任务查询接口来轮询进度和结果。",
        "owner": "搜狗",
        "doc_url": "https://ai.sogou.com/doc/?url=/docs/content/asr/longrunning-recognize"
    },
    "F2706": {
        "func": "录音文件识别（获取进度）",
        "des": "录音文件识别可以处理最长 180 分钟的语音音频数据。在提交转写任务后，用户可以通过搜狗AI开放平台统一异步任务查询接口来轮询进度和结果。",
        "owner": "搜狗",
        "doc_url": "https://ai.sogou.com/doc/?url=/docs/content/asr/longrunning-recognize"
    },
    "F3001": {
        "func": "通用文字识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3002": {
        "func": "身份证识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3003": {
        "func": "车牌识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3004": {
        "func": "营业执照识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3005": {
        "func": "多票据识别（含发票）",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3006": {
        "func": "港澳台通行证识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3007": {
        "func": "表格文档识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3008": {
        "func": "发票验真",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3009": {
        "func": "集装箱号识别",
        "des": "/",
        "owner": "薪火科技",
        "doc_url": "https://www.xinhuokj.com/doc"
    },
    "F3301": {
        "func": "银行卡识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3302": {
        "func": "车牌识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3303": {
        "func": "文档识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3304": {
        "func": "营业执照识别",
        "des": "",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/License.html"
    },
    "F3305": {
        "func": " VIN码识别",
        "des": "",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/VIN.html"
    },
    "F3306": {
        "func": "车辆登记证识别",
        "des": "",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/carRegister.html"
    },
    "F3307": {
        "func": "不动产登记证识别",
        "des": "",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/realty.html"
    },
    "F3308": {
        "func": "未知发票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3309": {
        "func": "增值税发票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3310": {
        "func": "机动车发票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3311": {
        "func": "火车票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3312": {
        "func": "发票自动分类",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3313": {
        "func": "PDF电子票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3314": {
        "func": "定额票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3315": {
        "func": "出租车发票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3316": {
        "func": "行程单发票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3317": {
        "func": "通用机打发票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3318": {
        "func": "身份证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3319": {
        "func": "行驶证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3320": {
        "func": "驾驶证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3321": {
        "func": "名片识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3322": {
        "func": "人脸识别（对比）",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3323": {
        "func": "人证对比",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3324": {
        "func": "房产证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3325": {
        "func": "车辆合格证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3326": {
        "func": "承兑汇票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3327": {
        "func": "福建社会保障卡识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3328": {
        "func": "二代身份证背面识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3329": {
        "func": "临时身份证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3330": {
        "func": "厦门社会保障卡识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3331": {
        "func": "登机牌识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3332": {
        "func": "律师证信息页识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3333": {
        "func": "律师证照片页识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3334": {
        "func": "深圳居住证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3335": {
        "func": "香港入境小票识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3336": {
        "func": "全民健康保险卡识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3337": {
        "func": "台湾身份证正面识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3338": {
        "func": "台湾身份证反面识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3339": {
        "func": "文档识别（英文）",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3340": {
        "func": "文档识别（繁体中文）",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3341": {
        "func": "微博识别功能",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html?sul=Appendices1"
    },
    "F3342": {
        "func": "户口本识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3343": {
        "func": "驾驶证副页识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3344": {
        "func": "行驶证副页识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3345": {
        "func": "港澳台居民居住证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3346": {
        "func": "港澳台居民居住证识别（反面）",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3347": {
        "func": "外国人永久居留身份证识别\t",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3348": {
        "func": "身份证、驾驶证、行驶证自动分类\t",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3349": {
        "func": "居住证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3350": {
        "func": "香港永久居民身份证识别",
        "des": "/",
        "owner": "翔云",
        "doc_url": "https://www.netocr.com/apiCenter/index.html"
    },
    "F3601": {
        "func": "短文本语音合成",
        "des": "将短文本（ ≤ 500 字符 ）转换成自然流畅的语音，可流式播放，支持多种音色，并提供调节音量、语速、音高、亮度等功能。适用于智能客服、语音交互、导航播报等场景",
        "owner": "云知声",
        "doc_url": "https://ai-doc.unisound.com/ttsshort/WebAPI.html#%E5%8F%91%E9%9F%B3%E4%BA%BA%E5%88%97%E8%A1%A8"
    },
    "F3602": {
        "func": "一句话识别",
        "des": "把语音(≤60秒)转换成对应的文字信息，适用于较短的语音交互场景，如语音搜索、语音输入、语音控制等",
        "owner": "云知声",
        "doc_url": "https://ai-doc.unisound.com/asronesentence/WebAPI.html#%E4%BA%8C%E3%80%81%E6%8E%A5%E5%8F%A3demo"
    },
    "F3900": {
        "func": "通用文本识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_general.html"
    },
    "F3901": {
        "func": "通用表格识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_table_api.html"
    },
    "F3902": {
        "func": "印章识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_seal.html"
    },
    "F3903": {
        "func": "财务报表识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_financial_report.html"
    },
    "F3904": {
        "func": "行驶证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vehicle_license.html"
    },
    "F3905": {
        "func": "驾驶证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_driver_license.html"
    },
    "F3906": {
        "func": "车辆登记证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vehicle_register.html"
    },
    "F3907": {
        "func": "车辆合格证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vehicle_cert.html"
    },
    "F3908": {
        "func": "车牌识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_lpr.html"
    },
    "F3909": {
        "func": "VIN码识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vin.html"
    },
    "F3910": {
        "func": "新车发票识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vehicle_invoice.html"
    },
    "F3911": {
        "func": "二手车发票识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vehicle_invoice2.html"
    },
    "F3912": {
        "func": "电子保单识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_e_policy.html"
    },
    "F3913": {
        "func": "身份证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_id_card.html"
    },
    "F3914": {
        "func": "身份证质检",
        "des": "检测图片上身份证合规性，多张证件返回多个结果",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v2_id_card_check.html"
    },
    "F3915": {
        "func": "银行卡识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_bank_card.html"
    },
    "F3916": {
        "func": "临时身份证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_temp_id.html"
    },
    "F3917": {
        "func": "结婚证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_marriage_proof.html"
    },
    "F3918": {
        "func": "护照识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_passport.html"
    },
    "F3919": {
        "func": "出生证明识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_birth_cert.html"
    },
    "F3920": {
        "func": "户口本识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_hukou_proof.html"
    },
    "F3921": {
        "func": "军官证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_junguanzheng.html"
    },
    "F3922": {
        "func": "名片识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_business_card.html"
    },
    "F3923": {
        "func": "澳门身份证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_macau_id_card.html"
    },
    "F3924": {
        "func": "香港身份证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_hk_id.html"
    },
    "F3925": {
        "func": "外国人永久居留证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_foreigner_greencard.html"
    },
    "F3926": {
        "func": "内地居民往来港澳通行证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://api.exocr.com/ocr/v1/ga_pass"
    },
    "F3927": {
        "func": "港澳台居民往来内地通行证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://api.exocr.com/ocr/v1/gat_pass"
    },
    "F3928": {
        "func": "营业执照识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_business_license.html"
    },
    "F3929": {
        "func": "房产证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_realestate_cert.html"
    },
    "F3930": {
        "func": "不动产登记证识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_realestate_register.html"
    },
    "F3931": {
        "func": "银行支票识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_check_book.html"
    },
    "F3932": {
        "func": "银行承兑汇票识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_bank_cdhp.html"
    },
    "F3933": {
        "func": "药品清单识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_medicine_list.html"
    },
    "F3934": {
        "func": "财务发票混合识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v2_fapiao.html"
    },
    "F3935": {
        "func": "增值税发票识别",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_invoice.html"
    },
    "F3936": {
        "func": "新车发票",
        "des": "/",
        "owner": "易道博识",
        "doc_url": "http://open.exocr.com:7080/doc/v1_vehicle_invoice_c.html"
    },
    "F4201": {
        "func": "文本纠错",
        "des": "/",
        "owner": "用友",
        "doc_url": "https://api.yonyoucloud.com/apilink/serviceTest/f777ad1d-b1a9-41ee-a47a-763bd722d260_true?apiPk=287b9b59-0786-42c5-adc7-00d061b40622"
    },
    "F4202": {
        "func": "短文本相似度",
        "des": "/",
        "owner": "用友",
        "doc_url": "https://api.yonyoucloud.com/apilink/serviceTest/f777ad1d-b1a9-41ee-a47a-763bd722d260_true?apiPk=4a3e17b9-9f7b-4099-86e8-8daab2844771"
    },
    "F4501": {
        "func": "英文作文批改（预处理）",
        "des": "输入一篇英文作文的图片URL或者base64值，输出识别的文本内容，以及可能的的识别错误位置，用户修正识别错误后，调用英文作文批改主接口进行批改",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/console/abilitytype/ability/abilitydetail?categoryId=1&id=103"
    },
    "F4502": {
        "func": "思维导图评估",
        "des": "用户输入一张思维导图图片，返回这张图片的检测结果以及四色分级结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=12"
    },
    "F4503": {
        "func": "口算题识别",
        "des": "输入一张口算题作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=158"
    },
    "F4504": {
        "func": "特殊字符识别",
        "des": "输入一张特殊字符作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=163"
    },
    "F4505": {
        "func": "脱式计算识别",
        "des": "输入一张脱式计算作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=159"
    },
    "F4506": {
        "func": "英语单字符识别",
        "des": "输入一张英语单字符作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=160"
    },
    "F4507": {
        "func": "比较大小识别",
        "des": "输入一张比较大小作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=161"
    },
    "F4508": {
        "func": "运算符识别",
        "des": "输入一张运算符作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=162"
    },
    "F4509": {
        "func": "选择题识别",
        "des": "输入一张选择题作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=164"
    },
    "F4510": {
        "func": "数字识别",
        "des": "输入一张数字识别作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=165"
    },
    "F4511": {
        "func": "英文单词识别",
        "des": "输入一张英文单词作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=175"
    },
    "F4512": {
        "func": "数字排序识别",
        "des": "输入一张数字排序作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=167"
    },
    "F4513": {
        "func": "中文单位识别",
        "des": "输入一张中文单位作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=168"
    },
    "F4514": {
        "func": "比例识别",
        "des": "输入一张比例作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=169"
    },
    "F4515": {
        "func": "几何识别",
        "des": "输入一张几何作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=170"
    },
    "F4516": {
        "func": "代数识别",
        "des": "输入一张代数作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=171"
    },
    "F4517": {
        "func": "中文数字识别",
        "des": "输入一张中文数字作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=172"
    },
    "F4518": {
        "func": "不带参数表达式识别",
        "des": "输入一张不带参数表达式作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=173"
    },
    "F4519": {
        "func": "带参数表达式识别",
        "des": "输入一张带参数表达式作答图片，返回识别结果",
        "owner": "好未来",
        "doc_url": "https://openai.100tal.com/documents/article/page?fromWhichSys=console&id=174"
    },
    "F4520": {
        "func": "人头检测",
        "des": "用户输入一张图片，检测共有多少个人在图中，且同时返回每张人脸的位置，适用于脸部大面积遮挡或未漏出脸的情况。 主要应用场景为线上考试的监考场景，或者摄像头遮挡时学生检测；",
        "owner": "",
        "doc_url": "https://openai.100tal.com/documents/article/page?id=101"
    },
    "F4521": {
        "func": "人脸检测",
        "des": "用户输入一张图片，选择需要分析的人脸属性。返回人脸位置并返回需要分析的属性，当前可识别微笑，并判断置信度;可检测人脸关键点（landmark)和明暗度（lightness），若未选择属性（properties为空)，则只返回人脸检测结果。",
        "owner": "",
        "doc_url": "https://openai.100tal.com/documents/article/page?id=5"
    },
    "F4522": {
        "func": "课堂人数检测",
        "des": "传入一张照片，返回图片中学生人数和非学生人数（含家长和老师）及对应位置。",
        "owner": "",
        "doc_url": "https://openai.100tal.com/documents/article/page?id=213"
    },
    "F4523": {
        "func": "人体属性",
        "des": "用户输入一张图片，检测所有人体并返回检测到的人体数、每个人体的矩形框位置、矩形框中人体的属性、及其判断置信度。 适合场景：线下教室；",
        "owner": "",
        "doc_url": "https://openai.100tal.com/documents/article/page?id=4"
    },
    "F4801": {
        "func": "头部分割",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=14"
    },
    "F4802": {
        "func": "皮肤分析",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=87&type=api&lang=zh"
    },
    "F4803": {
        "func": "人脸关键点检测",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=45&type=api&lang=zh"
    },
    "F4804": {
        "func": "宏观人脸分析",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=49"
    },
    "F4805": {
        "func": "微观人脸分析",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc/?id=53&type=api&lang=zh"
    },
    "F4806": {
        "func": "头发分析",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc/?id=79&type=api&lang=zh"
    },
    "F4807": {
        "func": "五官分割",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc/?id=9&type=api&lang=zh"
    },
    "F4808": {
        "func": "头发分割",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc/?id=16&type=api&lang=zh"
    },
    "F4809": {
        "func": "服饰识别",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=85&type=api&lang=zh"
    },
    "F4810": {
        "func": "人体外轮廓点检测",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=131&type=api&lang=zh"
    },
    "F4811": {
        "func": "手势识别",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=132&type=api&lang=zh"
    },
    "F4812": {
        "func": "肢体关键点检测",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=6"
    },
    "F4813": {
        "func": "人像分割",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=15&type=api&lang=zh"
    },
    "F4814": {
        "func": "皮肤分割",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=17&type=api&lang=zh"
    },
    "F4815": {
        "func": "图像美学评分",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=88&type=api&lang=zh"
    },
    "F4816": {
        "func": "食物分割",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=133&type=api&lang=zh"
    },
    "F4817": {
        "func": "食物识别",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=135&type=api&lang=zh"
    },
    "F4818": {
        "func": "图像分类",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=146&type=api&lang=zh"
    },
    "F4819": {
        "func": "图像深度估计",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=148&type=api&lang=zh"
    },
    "F4820": {
        "func": "美颜技术",
        "des": "/",
        "owner": "美图",
        "doc_url": "https://ai.meitu.com/doc?id=96"
    },
    "F5101": {
        "func": "机器翻译",
        "des": "/",
        "owner": "思必驰",
        "doc_url": "https://cloud.aispeech.com/docs/2041"
    },
    "F5401": {
        "func": "人脸比对",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goFace"
    },
    "F5402": {
        "func": "名片识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goNamecard"
    },
    "F5403": {
        "func": "文档识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goDoc"
    },
    "F5404": {
        "func": "表单识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goTemplateForm"
    },
    "F5405": {
        "func": "银行卡识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goBankcard"
    },
    "F5406": {
        "func": "护照识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goPassport"
    },
    "F5407": {
        "func": "驾驶证识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goDriver"
    },
    "F5408": {
        "func": "行驶证识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goDriving"
    },
    "F5409": {
        "func": "车牌识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goPlate"
    },
    "F5410": {
        "func": "企业三证识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goTemplate"
    },
    "F5411": {
        "func": "增值税发票识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goVatInvoice"
    },
    "F5412": {
        "func": "户口本识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goBooklet"
    },
    "F5413": {
        "func": "购车发票识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goTicket"
    },
    "F5414": {
        "func": "军官证识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goOfficer"
    },
    "F5415": {
        "func": "港澳通行证",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goTrafficpermit"
    },
    "F5416": {
        "func": "Vin码识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goVin"
    },
    "F5417": {
        "func": "驾驶证副页识别",
        "des": "/",
        "owner": "云脉",
        "doc_url": "http://www.yunmaiocr.com/goDriverSubPage"
    },
    "FSA01": {
        "func": "简历解析",
        "des": "ResumeSDK的服务基于http+json格式的方式提供服务，以同时支持各种不同开发语言的客户端调用。ResumeSDK提供SaaS模式和独立部署两种形式的服务模式：1.SaaS模式：服务部署在我司服务器上，客户通过远程API调用的方式使用简历分析服务，按调用次数收费；2.独立部署：服务部署在客户自己的服务器上，客户自行运维和管控服务，无调用次数和期限的限制；",
        "owner": "RESUMESDK",
        "doc_url": "http://www.resumesdk.com/docs/rs-parser.html"
    },
    "FSA02": {
        "func": "简历解析",
        "des": "小析简历解析云服务平台提供先进的简历解析和简历挖掘技术解决方案，致力于人力资源行业智能化这一进程。通过技术提升行业工作效率，减少人力资源管理成本；同时帮助招聘和猎头行业更 好地进行内容业务数据处理，提供工作效率。",
        "owner": "小析智能",
        "doc_url": "https://wiki.xiaoxizn.com/"
    }
}

api_info = json.dumps(api_info)

def file_to_base64(input_init):
    cont = open(input_init['file_path'], 'rb').read()
    base_cont = base64.b64encode(cont)
    base_cont = base_cont.decode('utf-8')# if sys.version.startswith('3') else base_cont  # 兼容python2与python3
    input_init['file_base64'] = base_cont

    return input_init


def get_dict_from_path(_path):
    # load json dict from json file
    # output form: dictionary
    #f = open(_path, 'r', encoding='gbk')
    # f = open(_path, 'r', encoding='utf-8')
    # _dict = json.load(f)
    # f.close()
    _dict = json.loads(_path)
    return _dict


def write_json_from_dict(_dict, _path, simple_write=True):
    
    with open(_path, 'w') as f_log:
        if simple_write:
            f_log.write(json.dumps(_dict, indent=4, ensure_ascii=False))
        else:
            f_log.write(json.dumps(_dict))
        
    return _dict


def bert_similarity(root_str, cand_str):
    url = "http://ai03cn.haetek.com:9090/ltp"
    data = {
        "model_name": "bert",
        "model_action": "similarity",
        "extra_data": {
            "root_str": root_str,
            "cand_str": cand_str
        },
        "model_type": ""
    }
    res = requests.post(url=url, json=data)
    return json.loads(res.text)


def search_F(query, max_size=3):

    _dict = get_dict_from_path(api_info)
    
    key_list = []
    value_list = []
    for _key in _dict:
        key_list.append(_key)
        value_list.append(_dict[_key]['func'])
        
    res = bert_similarity(query, value_list)['result_data']
    pair_res = [[key_list[_id],res[_id]] for _id in range(len(res))]
    
    sorted_pair = sorted(pair_res, key=lambda item: item[1], reverse=True)[:max_size]
    res_list = [{'func_name':item[0], 'score':round(item[1],4), **_dict[item[0]]} for item in sorted_pair]
    
    return res_list


def run(model_action, user_id, secret_key, input_unit={}, params={}):
    """
    调用服务器接口
    :param model_action: F1/F2/F3/...
    :param user_id: user_sample
    :param secret_key: key_sample
    :param input_unit: 不可为空
    :param params: 可为空
    :return:
    """
    url = 'https://web08cn.haetek.com:9292/api_merger'
    data = {"model_name": "api_merger",
            "model_action": model_action,
            "extra_data": {
                "user_id": user_id,
                "secret_key": secret_key,
                "input_unit": input_unit,
                "params": params
            }
            }
    resp = requests.post(url=url, json=data)
    res_data = json.loads(resp.text)
    #print(res_data)
    return res_data




    


