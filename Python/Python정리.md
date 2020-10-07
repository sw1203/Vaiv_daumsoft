## Vectorization
- 데이터를 벡터화해서 연산하는 것을 일컫음
- 반복문을 통해 연산하는 것보다 속도가 훨씬 빠름
- 데이터의 값이 많아질수록 속도가 더 차이남
- [코드](https://github.com/sw1203/Vaiv_daumsoft/blob/master/Python/code/vectorization.py)

## Broadcasting
- 다른 차원을 가지고 있는 배열들 간 어떤 조건을 만족했을 시 산술연산을 가능하도록 배열을 자동적으로 변환하는 것
- broadcasting이 가능한 조건
    - 두 배열 간의 연산에서 최소한 하나의 배열의 차원이 1(1행또는 1열)이라면 가능
    - 차원의 짝이 맞는 경우 가능하다.
- [코드](https://github.com/sw1203/Vaiv_daumsoft/blob/master/Python/code/braodcasting.py)

## Mutable
- 변경 가능한 객체
- call by reference 속성을 가짐
- list, dict, set, byte array
- [참고자료](https://dpdpwl.tistory.com/82)

## Immutable
- 변경 불가능한 객체
- call by value의 성격을 띰
- int, float, complex, string, tuple, frown set, bytes
- [참고자료](https://wikidocs.net/32277)

## 얕은 복사(shallow copy)
- 새로운 객체(변수)를 만든 후에 원본에 접근할 수 있는 참조를 입력(서로 다른 변수명이지만 본질적으로 같은 대상을 의미하므로 하나의 변수를 수정시 다른 변수도 수정)
- 가변형(mutable) 자료형에 대해서 적용이 가능
    - mutable 자료형은 같은 주소에서 값이 변경이 가능
    - immutable 자료형은 본질적으로 변경이 불가능하므로 재배정을 통해 변수를 바꿈
 
## 깊은 복사(deep copy)
- 새로운 객체(변수)를 만든 뒤에 원본의 복사본을 변수에 입력(서로 값만 같을 뿐 본질적으로 서로 다르기 때문에 한 변수가 수정될 시 다른 변수가 수정되지 않음)
- [참고자료](https://wikidocs.net/16038)

## subprocess 모듈
- 파이썬으로 시작한 자식 프로세스는 병렬로 실행이 가능하여 CPU 코어를 모두 이용해 프로그램의 처리량을 극대화 할 수 있다.
- 파이썬에서 서브프로세스(자식 프로세스)를 실행하기 위해 사용하는 모듈
- 쉘에서 pipe를 통해 프로세스의 출력을 다른 프로세스의 입력으로 전환할 수 있듯이, 자식 프로세스의 입출력을 다른 프로세스의 입출력을 통해 받는 것이 가능
- [참고자료1](http://blog.naver.com/PostView.nhn?blogId=sagala_soske&logNo=221280201722&parentCategoryNo=&categoryNo=118&viewDate=&isShowPopularPosts=true&from=search)
- [참고자료2](https://github.com/shoark7/Effective-Python/blob/master/files/BetterWay36_Usesubprocess.md)
- [official document](https://docs.python.org/3/library/subprocess.html)