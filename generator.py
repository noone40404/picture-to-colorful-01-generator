## 在 https://www.text-image.com/convert/ 上传文件并下载 html
## 将文件地址填入程序末尾并运行
## 注意生成的一行内默认是125字符，不是的话去下面改一下

from bs4 import BeautifulSoup

def html_to_cpp_converter(input_html_path,output_cpp_path):
    with open(input_html_path,"r",encoding="utf-8") as file:
        html_content=file.read()

    soup=BeautifulSoup(html_content,"html.parser")

    # 遍历所有字符
    data_pairs=[]  # 颜色和字符的对应关系
    for tag in soup.find_all("b"):  # 查找所有<b>标签
        style=tag.get("style","")  # 获取style属性
        color_code=None
        if "color:" in style:
            color_code=style.split("color:")[1].split(";")[0].strip()  # 提取颜色代码
        text=tag.get_text(strip=True)  # 标签中的文本内容
        if color_code and text:
            for char in text:  # 遍历文本中每个字符
                data_pairs.append((color_code,char))  # 将颜色和字符作为一个元组加入列表

    # 合并相邻且颜色相同的字符
    optimized_data=[]
    current_color=None  # 当前颜色
    current_text=""  # 当前文本

    for color,char in data_pairs:  # 遍历所有颜色和字符的对应关系
        if color==current_color:  # 如果颜色未改变
            current_text+=char  # 将字符追加到当前文本
        else:  # 如果颜色改变
            if current_color is not None:  # 如果当前颜色存在
                optimized_data.append((current_color,current_text))  # 将当前颜色和文本保存
            current_color=color  # 更新当前颜色
            current_text=char  # 重置当前文本为当前字符

    if current_color is not None:  # 处理最后一组颜色和文本
        optimized_data.append((current_color,current_text))

    # 初始化C++代码的内容
    cpp_code_lines=[]
    cpp_code_lines.append('#include <bits/stdc++.h>\n')
    cpp_code_lines.append('#include <windows.h>\n')
    cpp_code_lines.append('#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004\n')
    cpp_code_lines.append('using namespace std;\n')
    cpp_code_lines.append('void setConsoleColor(const string& colorCode) {\n')
    cpp_code_lines.append('    cout << "\\033[38;2;" << colorCode << "m";\n')
    cpp_code_lines.append('}\n')
    cpp_code_lines.append('void resetConsoleColor() {\n')
    cpp_code_lines.append('    cout << "\\033[0m";\n')
    cpp_code_lines.append('}\n\n')

    # 函数：
    cpp_code_lines.append('void enableAnsiSupport() {\n')
    cpp_code_lines.append('    HANDLE hOut=GetStdHandle(STD_OUTPUT_HANDLE);\n')
    cpp_code_lines.append('    DWORD dwMode=0;\n')
    cpp_code_lines.append('    GetConsoleMode(hOut,&dwMode);\n')
    cpp_code_lines.append('    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;\n')
    cpp_code_lines.append('    SetConsoleMode(hOut,dwMode);\n')
    cpp_code_lines.append('}\n\n')

    cpp_code_lines.append('int main() {\n')

    #cpp_code_lines.append('enableAnsiSupport();\n') # 根据实际情况是否启用该函数

    char_count=0  # 初始化字符计数器
    for color,text in optimized_data:  # 遍历优化后的颜色和文本数据
        rgb=color.lstrip('#')  # 去掉颜色代码前的#号
        r,g,b=int(rgb[:2],16),int(rgb[2:4],16),int(rgb[4:],16)  # 将颜色代码转换为RGB数值
        cpp_code_lines.append(f'    setConsoleColor("{r};{g};{b}"); ')  # 调用setConsoleColor设置颜色
        cpp_code_lines.append(f'    cout<<"{text}"; ')  # 输出文本
        char_count+=len(text)  # 累计字符数
        if char_count >= 125:  # 125是生成的字符画的宽度
            cpp_code_lines.append('    cout<<endl;\n')
            char_count=0  # 重置字符计数器

    cpp_code_lines.append('    resetConsoleColor();\n')
    cpp_code_lines.append('    cout<<endl;\n')
    cpp_code_lines.append('    return 0;\n')
    cpp_code_lines.append('}\n')

    with open(output_cpp_path,"w",encoding="utf-8") as cpp_file:
        cpp_file.writelines(cpp_code_lines)

input_html_path="input.html"  # 替换为输入HTML文件的路径
output_cpp_path="output.cpp"  # 替换为生成的C++文件的路径
html_to_cpp_converter(input_html_path,output_cpp_path)
