
import os

def load_parameters(filepath="params.txt"):
   
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到配置文件: {filepath}")

    params_dict = {}
    
   
    with open(filepath, "r", encoding="utf-8") as file:
        code_str = file.read()
 
    exec(code_str, {}, params_dict)
    

    clean_params = {k: v for k, v in params_dict.items() if not k.startswith("__")}
    
    return clean_params


if __name__ == "__main__":
    my_config = load_parameters("parameters.txt")
    print("成功加载以下参数：")
    for key, value in my_config.items():
        print(f"  {key}: {value}")