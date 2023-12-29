from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
'''OCR主函数：'''

def MAIN(img_path:str,output_name:str='ImgOutputResult',show=False):#输出示例：[[[428.0, 285.0], [701.0, 285.0], [701.0, 336.0], [428.0, 336.0]], ('主管、主办：中', 0.9802922010421753)]
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    response = []
    for line in result[0]:
        response.append(str(line[1][0]))
    return response
    #for idx in range(len(result)): #这是原来的，看不出有什么意义。
        #res = result[idx]
        #for line in res:
        #    response.append(line)
        #return response


    # 用图片显示结果
    if show==True:
        from PIL import Image
        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('ImgOutput'+output_name+'.jpg')
        print("图片展示：ImgOutput"+ output_name)



'''获取文件夹下所有文件的路径，此处可以传入操作'''
def file_name(PATH='INPUT',show=False):
    import os
    try:
        for root, dirs, files in os.walk(PATH):
            for file in files:
                file_path = os.path.join(root, file)
                # print(file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 这里不需要处理文件内容，所以我们只是打开并立即关闭文件
                    # 但您可以修改这里来执行其他操作，例如读取文件内容

                    #为下面的输出路径使用：下面两行是去除PATH前面的INPUT
                    list = str(root).split('\\')
                    Loss_First_Path_response = [list[1] if len(list) > 1 else ''][0]

                    #创建缺失的文件夹
                    output_file_path = './OUTPUT/'+Loss_First_Path_response+'/OUTPUT_'+file+'.txt'
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                    with open(str(output_file_path), 'w', encoding='utf-8') as f:
                        response = MAIN(root + '/' + file, file, show)
                        #print(response)
                        for line in response:
                            f.write(str(line) + '\n')
                print(f"File: {file_path}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == '__main__':
    file_name('C:/Users/Administrator/Desktop/OCR/OCR_PaddlsOCR/INPUT',show=False)
    #print(MAIN('C:/Users/Administrator/Desktop/OCR/OCR_PaddlsOCR/INPUT/《安装》2021.03 004.png'))