# claude-hook-autotest

Claude Code가 답변을 마칠 때마다 **pytest를 자동으로 실행**하고, 테스트가 실패하면 Claude가 멈추지 않고 **스스로 이어서 고치게** 만드는 Stop 훅 예제입니다.

## 동작 방식

```
Claude 답변 끝 → Stop 훅 실행 → pytest
                                  ├─ 통과 / 테스트 없음 → 그대로 종료
                                  └─ 실패 → 실패 내용을 Claude에게 전달 → Claude가 이어서 수정
```

- 무한 반복 방지: 한 번 이어서 고친 뒤(`stop_hook_active: true`)에는 다시 막지 않고 종료합니다.
- pytest가 설치되어 있지 않으면 테스트를 건너뜁니다.

## 파일 구성

| 파일 | 설명 |
|---|---|
| `.claude/settings.json` | Stop 훅 등록 (이 프로젝트에서만 동작) |
| `.claude/hooks/run_tests.py` | pytest를 실행하고, 실패 시 `{"decision": "block"}`을 출력하는 훅 스크립트 |
| `calc.py` | 테스트 대상 예제 코드 (`add`, `subtract`, `divide`) |
| `tests/test_calc.py` | pytest 테스트 |
| `pytest.ini` | pytest 설정 (`tests` 폴더에서 `calc.py`를 불러올 수 있게 함) |

## 사용 방법

1. pytest 설치

   ```
   python -m pip install pytest
   ```

2. 이 폴더에서 Claude Code 실행

   ```
   claude
   ```

3. 테스트해 보기: Claude에게 `calc.py의 add를 빼기로 바꿔줘`라고 요청하면, 답변이 끝날 때 훅이 `test_add` 실패를 잡아내고 Claude가 이어서 코드를 고칩니다.

테스트를 직접 실행하려면:

```
python -m pytest -q
```

## 내 코드에 적용하기

`tests` 폴더에 `test_`로 시작하는 파일을 추가하면 훅이 자동으로 함께 실행합니다. 훅 스크립트는 수정할 필요가 없습니다.
