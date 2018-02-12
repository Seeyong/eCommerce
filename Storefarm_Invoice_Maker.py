import pandas as pd
import numpy as np
import datetime
import xlsxwriter

'''
Step.1 - 스토어팜에서 발주하려는 업체 상품 체크
Step.2 - '선택주문 엑셀다운로드' 버튼 누름
Step.3 - '다운로드' 디렉토리의 해당 엑셀 파일 이름 Cmd + C(복사)
Step.4 - 프로그램 실행 후, "Insert the file(excel) name :" 가 뜨면 다운받은 엑셀 파일 이름 넣고 Enter
Step.5 - '데스크탑'에서 발주서로 변환된 엑셀(.xlsx) 파일 확인
'''

# 변환 가능한 변수(주요 사항만)
'''
1. 다운받은 파일 경로
2. 자신의 업체명
3. 발주하려는 파트너사 업체 리스트(업체명)
4. 변환한 파일 생성 경로
'''

def main():
    #다운받은 파일 경로
    download_path = '../user/Downloads/'

    #자신의 업체명
    my_company = 'Awesome Company'

    #발주하려는 파트너사 업체 리스트(업체명)
    partner_list = ['Apple', 'Facebook', 'Amazon', 'Netflix', 'Google']

    #변환한 파일 생성 경로
    creating_path = '../user/Desktop/'

# -----------------------위 네가지 사항을 업체에 맞게 변경 가능-------------------------------//

    #스토어팜에서 다운받은 엑셀 파일 찾기
    file_name = input("Insert the file(excel) name :")

    #스토어팜 엑셀 파일 읽어오기
    original = pd.read_excel(download_path + file_name + '.xls')

    #필터링 하고자 하는 column LIST
    title_lists = ['상품주문번호', '주문번호', '구매자명', '구매자ID'
        , '수취인명', '결제일', '상품번호', '상품명', '상품종류'
        , '옵션정보', '수량', '옵션가격', '상품가격', '상품별 총 주문금액'
        , '수취인연락처1', '수취인연락처2', '배송지', '구매자연락처'
        , '우편번호', '배송메세지', '주문일시', '(수취인연락처1)'
        , '(수취인연락처2)', '(우편번호)', '(기본주소)', '(상세주소)', '(구매자연락처)']

    #숫자 int64로 받아오기 column LIST
    integer_list = ['상품주문번호','주문번호','상품번호']
    original[integer_list] = original[integer_list].astype(np.int64)

    #발주 업체 이름 추출
    partner_name = ""
    product_name = original['상품명'].tolist()
    sep_product_name= []
    for i in product_name:
        sep_product_name = i.split(" ")
    for i in partner_list:
        if i in sep_product_name:
            partner_name = i

    #필터링을 거친 DataFrame
    submit = pd.DataFrame(original[title_lists])

    #전화번호 Format으로 통일
    submit['(구매자연락처)'] = submit['구매자연락처']
    submit['(수취인연락처1)'] = submit['수취인연락처1']
    submit['(수취인연락처2)'] = submit['수취인연락처2']

    now = datetime.datetime.now()

    #최종적인 발주서 엑셀 파일 이름
    invoive_name = my_company + ' ' + partner_name + ' 발주서_' + str(now.year) + str(now.month) + str(now.day)

    #엑셀 파일로 변환 및 생성
    writer = pd.ExcelWriter(creating_path + invoive_name + '.xlsx', engine='xlsxwriter')
    submit.to_excel(writer, index=False, sheet_name=str(now.year) + str(now.month) + str(now.day))
    workbook = writer.book
    worksheet = writer.sheets[str(now.year) + str(now.month) + str(now.day)]

    #각 Column 별 적합한 formating
    format1 = workbook.add_format({'num_format': '0'})
    format2 = workbook.add_format({'font_color': 'red', 'bold': True})
    format3 = workbook.add_format({'num_format': '₩#,##0'})
    worksheet.set_column('A:B', None, format1)
    worksheet.set_column('G:G', None, format1)
    worksheet.set_column('V:V', None, format1)
    worksheet.set_column('K:K', None, format2)
    worksheet.set_column('M:N', None, format3)

    writer.save()

if __name__ == "__main__":
    main()