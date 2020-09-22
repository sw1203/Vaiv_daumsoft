# 텍스트 처리를 위한 Linux 기본 명령어 및 개념

* [고급 Bash 스크립팅 가이드](https://wiki.kldp.org/HOWTO/html/Adv-Bash-Scr-HOWTO/x12718.html)
* [Bash Shell Script 소개](https://mug896.github.io/bash-shell/index.html)

## 심볼릭 링크
* 링크를 연결하여 원본 파일을 직접 사용하는 것과 같은 효과를 내는 링크
* 윈도우의 바로가기와 비슷한 개념
* 어떤 파일을 가리키고 있는 파일로 원본 파일을 수정하면 심볼릭 링크도 수정
* 심볼릭 링크를 수정하면 원본 파일도 수정
* 심볼릭 링크 설정 방법
```
ln -s [원본 파일] [심볼릭 링크 파일명]
```
## 하드링크
* 파일을 가리키는 이름을 하나 더 만드는 것이라 생각하면 됨
* 원본 파일 A를 지우더라도 하드링크 B는 내용을 간직
* 하드링크도 심볼릭 링크와 마찬가지로 수정 시 서로에게 영향을 줌
* 하드링크 설정 방법
```
ln [원본 파일] [하드링크 파일명]
```

## chmod, chown, chgrp
* chomod
    * 기존 파일 또는 디렉토리에 대한 접근 권한을 변경할 때 사용
    * 접근 권한 변경은 파일 소유자나 root만 가능
    ```
    chmod [권한][파일명]
    ```
    * [명령참고](https://corej21.tistory.com/47)

* chown
    * 파일 또는 디렉토리의 소유자, 소유그룹 수정에 사용
    * root 권한이 필요
    ```
    chown [소유권자]:[소유그룹] [파일명]
    ```
    * -R 옵션을 사용하면 디렉토리 하위 파일들 까지 모두 소유권이 변경
    * [명령참고](https://corej21.tistory.com/47)
    
* chgrp
    * 파일 또는 디렉토리의 사용자 그룹을 변경
    ```
    chgrp [소유그룹] [파일명]
    ```
    * [명령참고](https://eunguru.tistory.com/93)
    
## umask
* 앞으로 만들어질 파일에 영향을 미치는 명령
* 명령으로 지정한 8진수는 새로 만들어질 파일에서 제거될 권한을 명시한 것
```
umask [옵션] [값]
```
* [명령참고](https://jhnyang.tistory.com/63)

## wildcard, globbing, escaping, quoting
* wildcard
    * 무언가를 검색할 때, 더울 빠르고 수월하게 검색하게 도와주는 역할
    * 종류
        1. `*` : 길이 0 이상의 임의의 문자열 ex) ade* : ade로 시작하는 모든 파일
        2. `?` : 임의의 문자 1개 ex) ??a?? : 총 5글자인데 가운데가 a인 모든 파일
        3. `[]` : []안에 있는 모든 한 문자 ex) [de]a : da, ea
        4. `{}` : {}안에 있는 모든 한 단어 ex) {a,b,cde} : a, b, cde 
            * `{}`에 단어가 하나만 들어가있거나, 아무것도 안들어 있는 경우 `{}`는 아무런 기능이 없는 문자 취급

* globbing
    * wildcard에 의해 매칭된 파일들로 치환되는 것
    * 파일이름을 다룰 때만 적용되는 것은 아니며 어떤 스트링이나 변수값에라도 glob 문자가 있으면 발생하므로 주의
    * [참고자료](https://mug896.github.io/bash-shell/exp_and_sub/filename_expansion.html)
    
* escaping
    * 특수 문자를 일반 문자로 사용하려고 해당 문자 앞에 \을 붙이는 것
    * shell에서 escape를 할때 `\` 문자 외에 quote를 사용할 수 있음
    * [참고자료](https://mug896.github.io/bash-shell/quotes.html)
    
* quoting
    * 공백으로 분리되는 여러 개의 스트링을 하나의 인수로 만들 때 사용
    * 라인 개행이나 둘 이상의 공백을 유지하기 위해 사용
    * 단어분리, globbing 발생을 방지하기 위해 사용 ex) ls -al 'ca*'을 수행 시 ca* 파일의 정보를 보여줌
    * shell 키워드, 메타문자, alias와 같이 shell에서 특수기능을 하는 문자, 단어를 단순히 명령문의 스트링으로 만들기 위해

## alias
* 특정 단어를 입력했을 때 미리 설정해둔 명령어가 실행될 수 있도록 설정하는 기능
* 명령어 단축키라고 생각하면 된다.
```
1. 별칭 설정: alias [별칭]='[명령어]'
2. 별칭 목록 확인: alias
3. 별칭 삭제: unalias [별칭] 
```
* `=` 앞뒤에 공백이 들어가서는 안됨
* 위 방법으로 등록한 별칭은 영구적이지 않음
* [별칭 영구 설정방법](https://velog.io/@exploit017/LinuxDebian-%EB%B3%84%EC%B9%ADAlias-%EB%82%98%EB%A7%8C%EC%9D%98-%EB%A6%AC%EB%88%85%EC%8A%A4-%EB%AA%85%EB%A0%B9%EC%96%B4-%EB%A7%8C%EB%93%A4%EA%B8%B0)

## 함수
* 함수 선언 및 사용
```
function 함수명(){
함수내용
}

함수명
```

* 함수 인자 전달
```
test_func()
{
    func_a=$1
    func_b=$2

    echo "$func_a $func_b"
}

test_func 인자1 인자2
```

* 함수 결과값 전달
    * 결과값이 문자열이라면 함수 안에서 echo로 출력 후 함수 호출시 `(악센트 부호)을 사용해 출력 값을 변수에 받아 사용해도 된다.
```
test_func()
{
    echo "결과값"
    return 결과값
}

result=`test_func`

echo $?
```

* [참고자료](https://net711.tistory.com/entry/%EB%B0%B0%EC%89%AC-%EC%89%98-%ED%95%A8%EC%88%98)

## 명령 우선순위 변경하기
* nice 명령어
    * 프로세스가 실행될 때 실행 우선순위를 조정 (NI값을 변경)
    * 커다란 프로그램을 컴파일 할 때와 값이 CPU나 메모리를 많이 쓰게 되는 경우 사용
    * 시스템 속도를 저하시키기 때문에 다른 프로세스에게 우선순위 값을 줄 때 사용
    * -20 ~ 19 까지 순위 값을 조정할 수 있으며, -20이 우선순위가 가장 높고 19가 가장 낮음
    * 기본 nice 값은 보통 0으로 시작
    * 일반 유저는 값을 증가만 시킬 수 있음 (우선순위가 높은 특수 프로세스를 지키기 위해서)
```
nice [-n 조정수치][프로세스]
nice [프로세스] -> 기존 값에서 10 증가
```

* renice
    * 실행중인 프로세스에 대한 nice 값을 변경
    * 기존의 NI값에 상관없이 지정한 NI 값이 바로 설정된다.
    * root만이 우선순위 값을 감소 가능
    
```
renice [옵션] [변경할 NI값] [PID]
```

* [참고자료](https://chloro.tistory.com/106)

## Redirection
* 데이터 흐름의 방향을 나타냄
* redirection 기호
    1. `<` : 입력
    2. `>>` : 출력(추가)
    3. `>` : 출력
* `>`,`>>`의 우측값은 파일 설명자 번호가 오는 경우는 & 기호를 붙여줘야 한다.
* `>>`와 `>`의 차이
    * `>`의 경우 기존 파일을 덮어 씌우나 `>>`는 기존 파일에 이어서 내용이 추가
    * python의  open에서 `w`와 `a`라 생각하면 쉬울 듯하다.
* [참고자료](https://webdir.tistory.com/256)

## /dev/null
* /deb/null 파일은 항상 비어있으며, /dev/null에 전송된 데이터는 버려짐
* 어떠한 작업의 출력 내용을 보고 싶지 않을때, 이곳으로 출력을 보내면 보이지 않음
* 파일 설명자 설명
    1. `0` : 표준 입력 (/dev/stdin)
    2. `1` : 표준 출력 (/dev/stdout)
    3. `2` : 표준 오류(진단) 출력 (/dev/stderr)
```
# 표준 출력만 무시하는 경우
echo Hello 1> /dev/null

# 표준 오류 출력만 무시하는 경우
script.sh 2> /dev/null

# 표준 오류를 버리는 법
script.sh > /deb/null 2>&1
```
* 표준 오류를 버리는 명령어 분석
    * \>/dev/null 2>&1은 앞에 1이 생략되어진 형태
    * 1>/dev/null : 표준 출력은 /dev/null로 redirect 해라
    * 2>&1 : 표준 오류를 표준 출력으로 보내라는 뜻인데 표준 출력을 기록하지 않으므로 표준 오류도 기록하지 말라는 의미가 됨    
* [참고자료 1](https://jybaek.tistory.com/115)
* [참고자료 2](https://m.blog.naver.com/PostView.nhn?blogId=byacj&logNo=220750309439&proxyReferer=https:%2F%2Fwww.google.com%2F)

## 파이프 (Pipe)
* 한 명령의 표준 출력을 다른 명령의 표준 입력을 사용하기 위한 것
* 파이프 실행이 종료되었을 때의 종료 상태 값은 마지막 명령의 종료 상태 값이 사용되기 때문에 중간에 false(1)로 종료된 명령이 있더라도 마지막 명령이 true(0)이면 파이프 종료 상태 값은 true
* `set -o pipefail` 옵션을 설정하면 중간에 false로 종료된 명령이 있을 경우 파이프 종료 상태 값은 false
    * pipefail 옵션을 디폴트 상태로 돌리고 싶으면 `set +o pipefail`
* `PIPESTATUS`라는 변수는 파이프로 연결된 모든 명령들의 종료 상태 값을 가지고 있음

## xargs
* 한 명령의 출력을 다른 명령어의 인자값으로 전달
```
find / -name *.mp3 | xargs rm
```

## sed
* 원본 파일에 변형을 주지 않고 단지 출력되는 결과를 변화시켜 보여주는 역할
* [참고자료](https://hyunkie.tistory.com/51)

## 정규 표현식 (Regular Expression)
* 데이터 검색, 복잡한 패턴 매칭을 도와줌
* [참고자료](https://rfriend.tistory.com/373)

## vi(m)
* 유닉스/리눅스 환경에서 사용하는 텍스트 편집기
* vim은 vi를 향상시킨 버전
* [명령어](https://zzsza.github.io/development/2018/07/20/vim-tips/)

## AWK
* RECORD와 FIELD라는 개념을 이용해 입력 스트림으로부터 데이터를 자동으로 분리함으로써 특정 항목을 지정하고 추출하기 쉽게 해줌
* 기본적으로 산술연산자와 수학 함수를 제공하므로 문제를 쉽게 해결 가능
* sed는 처리 단위가 라인이고 awk는 레코드
* awk는 레코드 구분자와 필드 구분자를 지정할 수 있음
* print문은 기본적으로 출력에 OFS(Output Field Seperator)와 ORS(Output Record Seperator)를 사용
* [참고자료](https://mug896.github.io/awk-script/index.html)

## wget
* Web Get의 약어
* 네트워크 상에서 데이터를 다운로드 받을 때 사용하는 명령어
* HTTP, HTTPS, FTP 프로토콜을 지원
* [참고자료](https://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_wget)

## curl
* 다양한 프로토콜을 지원하는 데이터 전송용 command line tool
* HTTP, HTTPS, FTP, SFTP, SMTP 등을 지원
* [참고자료](https://www.lesstif.com/software-architect/curl-http-get-post-rest-api-14745703.html)

## jq
* JSON 포맷의 데이터를 다루는 커맨드라인 유틸리티
* [참고자료](https://www.44bits.io/ko/post/cli_json_processor_jq_basic_syntax)