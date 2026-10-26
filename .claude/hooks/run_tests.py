# Claude Code Stop 훅: 답변이 끝날 때 pytest를 돌리고, 실패하면 Claude가 이어서 고치게 함
import json
import os
import subprocess
import sys

data = json.load(sys.stdin)


def show(message):
    # CLI 창에만 표시되고 Claude에게는 전달되지 않는 메시지
    print(json.dumps({"systemMessage": message}, ensure_ascii=False))
    sys.exit(0)


project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
if not os.path.isdir(os.path.join(project_dir, "tests")):
    sys.exit(0)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider"],
    cwd=project_dir,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)
output = (result.stdout + result.stderr).strip()
summary = output.splitlines()[-1] if output else ""

if "No module named pytest" in output:
    show("⚠️ pytest가 설치되어 있지 않아 테스트를 건너뜁니다: python -m pip install pytest")

if result.returncode == 0:
    show(f"✅ pytest 통과 ({summary})")

if result.returncode == 5:
    sys.exit(0)  # 테스트 없음

# 이미 테스트 실패로 한 번 이어서 작업했다면 더 막지 않고 멈춤 (무한 반복 방지)
if data.get("stop_hook_active"):
    show(f"❌ pytest 실패가 남아 있습니다 ({summary})")

print(json.dumps({
    "decision": "block",
    "reason": f"pytest 실패:\n{output[-3000:]}\n\n테스트가 통과하도록 코드를 고쳐줘.",
}, ensure_ascii=False))
