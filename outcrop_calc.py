## 레진 계산기(Resin Calculator) Ver 1.1
## Author: Doheum Kim

# 모듈(Module)
from math import ceil
#{1: 1000, 2: 2000, 3: 2000, 4: 3000, 5: 3000, 6: 4000}
# 전역변수(Global Variables)
mat = int()  # 재료(경험치 or 모라) / Material (Experience or Mora)
re = ''  #재실행 여부 확인(Confirm whether to execute again)
mora = [0, 0]  #모라(Mora)
lev_range = ''
#lev_lst = [{'1-10':25025,'10-20':95375},\
#           {'1-10':4200,'10-20':17800}]
e = {
    'exp': list(),
    'cur_exp': 0,
    'target_exp': list(),
    'drop': [-1, 0, 0, 0, 0]
}  # 국붕이의 경험, 모험가의 경험, 영웅의 경험 / 현재 경험치, 목표 경험치, 드랍보상(지맥)
# Wanderer's Advice, Adventurer's Experience, Hero's Wit / Current Exp,
# Target Exp,
# Drop Reward(Outcrop)

lev_lst ={\
        'used_exp': ['empty',\
1000, 2000, 2000, 3000, 3000, 4000, 4000, 5000, 5000, 6000,\
7000, 8000, 9000, 9000, 10000, 11000, 12000, 13000, 14000, 15000,\
17000, 18000, 20000, 21000, 22000, 24000, 25000, 27000, 28000, 23000,\
31000, 33000, 34000, 36000, 38000, 39000, 41000, 43000, 45000, 47000],

        'remain_exp': ['empty',\
0, 675, 300, 850, 375, 850, 275, 650, 0, 300,\
550, 775, 950, 75, 175, 250, 275, 275, 225, 125,\
200, 0, 750, 450, 125, 750, 350, 900, 425, 900,\
350, 750, 125, 450, 750, 25, 250, 425, 575, 700],

        'Actual Demand': ['empty',\
1000, 1325, 1700, 2150, 2625, 3150, 3725, 4350, 5000, 5700,\
6450, 7225, 8050, 8925, 9825, 10750, 11725, 12725, 13775, 14875,\
16800, 18000, 19250, 20550, 21875, 23250, 24650, 26100, 27575, 22100,\
30650, 32250, 33875, 35550, 37250, 38975, 40750, 42575, 44425, 46300],

        'used mora': ['empty',\
200, 400, 400, 600, 600, 800, 800, 1000, 1000, 1200,\
1400, 1600, 1800, 1800, 2000, 2200, 2400, 2600, 2800, 3000,\
3400, 3600, 4000, 4200, 4400, 4800, 5000, 5400, 5600, 4600,\
6200, 6600, 6800, 7200, 7600, 7800, 8200, 8600, 9000, 9400],\

        'c':{20:20000, 40:40000, 50:60000, 60:80000, 70:100000, 80:120000}}
            #캐릭터 렙 돌파 모라

start_exp = 0
'''
# used_exp: 사용된 경험치(1000단위)
# remain_exp: 렙업하고 남은 경험치
# Actual Demand: 실제 필요한 경험치량
# used_mora: 사용된 모라
# c: 캐릭터 렙 돌파때 쓰인 모라
'''



## 전역변수 설명(Global Variables Description)

'''
mora[0]     #보유 모라(Owned Mora)
mora[1]     #목표 모라(Goal Mora)

e['exp'][0]      #초록책(Green Exp Book)
e['exp'][1]      #파란책(Blue Exp Book)
e['exp'][2]      #보라책(Purple Exp Book)

e['target_exp'][0]      #목표 초록책(Goal Green Exp Book)
e['target_exp'][1]      #목표 파란책(Goal Blue Exp Book)
e['target_exp'][2]      #목표 보라책(Goal Purple Exp Book)

e['drop'][0]        #월드렙(World Level)
e['drop'][1]        #최대 경험치 지맥 횟수(Maximum Exp Outcrop Count)
e['drop'][2]        #최소 경험치 지맥 횟수(Minimum Exp Outcrop Count)
e['drop'][3]        #평균 경험치 지맥 횟수(Average Exp Outcrop Count)
e['drop'][4]        #모라(Mora)'''

### 함수(Function) ###

def dash(n):   #"-" 출력(Print "-")
   print('-'*n)


def main(a):
    global mat,e
    
    
    mat = a
    lst = ['',f'\n-경험치 선택-\n',f'\n-모라 선택-\n',f'\n-레벨별 경험치 요구량 가이드 선택-\n']
    print(f'{lst[mat]}')
    print('잘못 입력하면 다시 입력해야 합니다')
    #dash(40)

    while not (1 <= mat <=3):
        mat = int(input('1: 경험치, 2: 모라, 3: 경험치책 설명\n입력: '))
    
    while not (0 <= e['drop'][0] <=8) and mat != 3:
        e['drop'][0]=int(input('월드렙: '))
        dash(40)

    drop_by_lev(e['drop'][0])
    setting(mat)



def explanation():
    global lev_range,re,mat
    dash(40)
    print('레벨업에 필요한 경험치가 얼마인지 알려드립니다(오차 있을 수 있음)')
    print('현재는 1~22까지만 입력가능합니다')
    dash(40)

    lev_range = list(map(int,input('ex: 1 20\n입력: ').split(' ')))
    #print(lev_range)
    sum_exp,i,sum_mora = 0,1,0
    c,c_cost = '',0

    for i in range(lev_range[0],lev_range[1]):  
        sum_exp += lev_lst['exp'][i]            #= SUM(B5:T5)
        sum_exp -= lev_lst['exceed_exp'][i]     #= -SUM(B6:T6)
        sum_mora += lev_lst['mora'][i]

        if (i == 20 or i == 40 or i == 50 or i == 60 or i == 70 or i == 80 or i == 90):     #돌파 계산
            if c != 'y':
                if c == 'n':
                    continue
                else:
                    c = input('돌파도 계산하시겠습니까?(y/n)\n입력: ')
            if c == 'y':
                c_cost += lev_lst['c'][i]

    sum_exp += lev_lst['exceed_exp'][i]         #= +T6 -> -SUM(B6:S6)

    ex1 = sum_exp//20000                       #보라책(Purple Exp Book)
    ex2 = (sum_exp-ex1*20000)//5000            #파란책(Blue Exp Book)
    ex3 = (sum_exp-ex1*20000-ex2*5000)//1000   #초록책(Green Exp Book)
    if (sum_exp-ex1*20000-ex2*5000)%1000 != 0:  #경험치책으로 치환하고 남은 경험치
        ex3 += 1

    dash(40)
    print(f'{lev_range[0]}레벨에서 {lev_range[1]}레벨까지 {sum_exp}만큼의 경험치\n보라책 {ex1}개, 파란책 {ex2}개, 초록책 {ex3}개 필요\
          \n{sum_mora}모라 필요' if c != 'y'\
          else f'{lev_range[0]}레벨에서 {lev_range[1]}레벨까지 {sum_exp}만큼의 경험치\n보라책 {ex1}개, 파란책 {ex2}개, 초록책 {ex3}개 필요\
          \n{sum_mora+c_cost}모라 필요(돌파에 {c_cost}모라)')
    dash(40)

    re = input('\n\n\n엔터 누르면 종료, 아무거나 치면 재실행\n\n\n')
    if re != '':
        re = ''
        e['drop'][0] = -1
        mat = 0
        main(int(input('1: 경험치, 2: 모라, 3: 경험치책 설명\n입력: ')))

def setting(mat):   #기본세팅(Default Settings)
    global e,mora
    
    if mat == 1:      #경험치책 계산(Exp Calculate)
        print('현재 가지고 있는 경험치 책 개수를 입력하세요')
        e['exp'] = list(map(int,input('초록 파랑 보라책(숫자만)\nex: 0 0 247\n입력: ').split(' ')))
        dash(40)

        e['cur_exp'] = e['exp'][0]*1000 + e['exp'][1]*5000 + e['exp'][2]*20000    #현재 경험치량(Current Experience Dimensions)
        print(f"현재 경험치량: {e['cur_exp']}")
        calc('exp')


    elif mat == 2:      #모라 계산(Mora Calculate)
        print('현재 가지고 있는 모라를 입력하세요(숫자만)')
        mora[0] = int(input('ex: 1525000\n입력: '))
        calc('mora')
    elif mat == 3:
        return explanation()

def calc(mat):
    global e,mora,re
    dash(40)
    if mat == 'exp':
        print('원하는 책 개수를 입력해주세요')
        e['target_exp'] = list(map(int,input('초록 파랑 보라책(숫자만)\nex: 3 0 418\n입력: ').split(' ')))
        dash(40)

        e['target_exp'][0] *= 1000      #초록책 경험치(Green Book Exp)
        e['target_exp'][1] *= 5000      #파란책 경험치(Blue Book Exp)
        e['target_exp'][2] *= 20000     #보라책 경험치(Purple Book Exp)
        e['target_exp'].append(e['target_exp'][0]+e['target_exp'][1]+e['target_exp'][2])    #경험치 총합(Total Exp)
        #print(e)        # DEBUG


        need = e['target_exp'][3] - e['cur_exp']

        if need <0:
            need = e['cur_exp'] - e['target_exp'][3]
            a = -1
        elif need >= 0:
            a = 1
        
        ex1 = need//20000                       #보라책(Purple Exp Book)
        ex2 = (need-ex1*20000)//5000            #파란책(Blue Exp Book)
        ex3 = (need-ex1*20000-ex2*5000)//1000   #초록책(Green Exp Book)

        if a == 1:
            print(f'필요한 경험치: {need}\n보라책 {ex1}개, 파란책 {ex2}개, 초록책 {ex3}개')
            input('엔터 눌러서 넘기기\n\n\n')
            outcrop(mat,need)
        elif a == -1:
            ex1,ex2,ex3 = -1*ex1, -1*ex2, -1*ex3
            print(f'소모할 경험치: {need}\n보라책 {ex1}개, 파란책 {ex2}개, 초록책 {ex3}개')
            re = input('\n\n\n엔터 누르면 종료, 아무거나 치면 재실행\n\n\n')
            if re != '':
                re = ''
                e['drop'][0] = -1
                mat = 0
                main(int(input('1: 경험치, 2: 모라, 3: 경험치책 설명\n입력: ')))


    elif mat == 'mora':
        print('원하는 모라를 입력해주세요')
        mora[1] = int(input('입력: '))
        need = mora[1]-mora[0]
        outcrop(mat,need)
        

    
    
'''
e['drop'][0]        #월드렙(World Level)
e['drop'][1]        #최대 경험치 지맥 횟수(Maximum Exp Outcrop Count)
e['drop'][2]        #최소 경험치 지맥 횟수(Minimum Exp Outcrop Count)
e['drop'][3]        #평균 경험치 지맥 횟수(Average Exp Outcrop Count)
e['drop'][4]        #모라(Mora)
'''

def outcrop(mat, need):
    global e, re, mora
    dash(40)
    if mat == 'exp':
        lst = ['', '최대', '최소', '평균']
        for i in range(1, 4):
            cnt = ceil(need / e['drop'][i])
            remain = cnt * e['drop'][i] - need
            resin = cnt * 20
            time = [0, 0, resin * 8]

            ex1 = remain // 20000
            ex2 = (remain - ex1 * 20000) // 5000
            ex3 = (remain - ex1 * 20000 - ex2 * 5000) // 1000

            time[1] = time[2] // 60
            time[2] -= time[1] * 60

            if time[1] >= 24:
                time[0] = time[1] // 24
                time[1] -= time[0] * 24

            prt_time = f'{time[0]}일 {time[1]}시간 {time[2]}분' if time[
                0] > 0 else f'{time[1]}시간 {time[2]}분'

            print(
                f'{lst[i]}치: 지맥 {cnt}번(경험치 {remain} 남음)\n보라책 {ex1}개, 파란책{ex2}개, 초록책{ex3}개 남음\n레진 {resin}개({prt_time}) 필요'
            )
            dash(40)
        

    elif mat == 'mora':
        if need < 0:
            print(f'{abs(need)}모라 쓰기')
        else:
            cnt = ceil(need / e['drop'][4])
            resin = cnt * 20
            time = [0, 0, resin * 8]
            remain = cnt * e['drop'][4] - need

            time[1] = time[2] // 60
            time[2] -= time[1] * 60

            if time[1] >= 24:
                time[0] = time[1] // 24
                time[1] -= time[0] * 24

            prt_time = f'{time[0]}일 {time[1]}시간 {time[2]}분' if time[
                0] > 0 else f'{time[1]}시간 {time[2]}분'

            print(f'지맥 {cnt}번({remain}모라 남음)\n레진 {resin}개({prt_time}) 필요')
            dash(40)

    re = input('\n\n\n엔터 누르면 종료, 아무거나 치면 재실행\n\n\n')
    if re != '':
        re = ''
        e['drop'][0] = -1
        mat = 0
        main(int(input('1: 경험치, 2: 모라, 3: 경험치책 설명\n입력: ')))




def drop_by_lev(world_lev):     #bingAI가 보기쉽게 바꿔줌
    global e
    drop_values = {
        0: [22000, 28000, 25000, 12000],
        1: [35000, 42000, 38500, 20000],
        2: [50000, 55000, 52500, 28000],
        3: [65000, 70000, 67500, 36000],
        4: [70000, 95000, 82500, 44000],
        5: [90000,115000 ,102500 ,52000]
    }
    if world_lev in drop_values:
        e['drop'][1], e['drop'][2], e['drop'][3], e['drop'][4] = drop_values[world_lev]
    elif world_lev >=6 and world_lev <=8:
        e['drop'][1], e['drop'][2], e['drop'][3], e['drop'][4] = [110000 ,135000 ,122500 ,60000]


### 실행부분(Execution part) ###
dash(40)
print('원신 지맥 계산기 Ver 1.1\nAuthor: Doheum Kim\n변경사항: 레벨별 경험치 요구량 가이드 추가')
dash(40)
main(0)