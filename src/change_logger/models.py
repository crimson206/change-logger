from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field


class ChangelogMode(str, Enum):
    INIT = "init"
    UPDATE = "update"


class LevelBump(str, Enum):
    NO_RELEASE = "no_release"
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"


class Actor(BaseModel):
    """Git actor (author/committer/tagger)"""

    name: str
    email: str


class Version(BaseModel):
    """Version information"""

    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    def __str__(self) -> str:
        version_str = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version_str += f"-{self.prerelease}"
        if self.build:
            version_str += f"+{self.build}"
        return version_str


class ParsedCommit(BaseModel):
    """Parsed commit information"""

    short_hash: str
    long_hash: str
    type: str
    scope: Optional[str] = None
    description: str
    body: Optional[str] = None
    footer: Optional[str] = None
    breaking_change: bool = False
    bump: LevelBump = LevelBump.NO_RELEASE
    include_in_changelog: bool = True

    def is_merge_commit(self) -> bool:
        # 실제 구현에서는 commit 메시지나 부모 수를 확인
        return "Merge" in self.description


class ParseError(BaseModel):
    """Parse error information"""

    commit_hash: str
    error_message: str
    type: str = "unknown"
    bump: LevelBump = LevelBump.NO_RELEASE


class Release(BaseModel):
    """Release information"""

    tagger: Actor
    committer: Actor
    tagged_date: datetime
    elements: Dict[str, List[ParsedCommit]] = Field(default_factory=dict)
    version: Version


class ReleaseHistory(BaseModel):
    """Complete release history"""

    unreleased: Dict[str, List[ParsedCommit]] = Field(default_factory=dict)
    released: Dict[str, Release] = Field(
        default_factory=dict
    )  # Version을 str key로 사용


class ReleaseNotesContext(BaseModel):
    """Context for generating release notes"""

    repo_name: str
    repo_owner: str
    hvcs_type: str  # "github", "gitlab", etc.
    version: Version
    release: Release = Field(..., description="some descriptoin.")
    mask_initial_release: bool = False
    license_name: Optional[str] = None


class ChangelogContext(BaseModel):
    """Context for generating changelog"""

    repo_name: str
    repo_owner: str
    hvcs_type: str  # "github", "gitlab", etc.
    history: ReleaseHistory
    changelog_mode: ChangelogMode
    prev_changelog_file: str
    changelog_insertion_flag: str
    mask_initial_release: bool = False


# 예시 데이터 구조
def example_data():
    # 예시 버전
    version = Version(major=1, minor=2, patch=3)

    # 예시 액터
    actor = Actor(name="John Doe", email="john@example.com")

    # 예시 커밋
    commit = ParsedCommit(
        short_hash="abc1234",
        long_hash="abc1234567890",
        type="feat",
        scope="auth",
        description="add user authentication",
        body="Implemented JWT-based authentication system",
        breaking_change=False,
        bump=LevelBump.MINOR,
    )

    # 예시 릴리즈
    release = Release(
        tagger=actor,
        committer=actor,
        tagged_date=datetime.now(),
        elements={"feat": [commit]},
        version=version,
    )

    # 예시 릴리즈 히스토리
    history = ReleaseHistory(unreleased={"feat": [commit]}, released={"1.2.3": release})

    # 예시 체인지로그 컨텍스트
    context = ChangelogContext(
        repo_name="my-project",
        repo_owner="myorg",
        hvcs_type="github",
        history=history,
        changelog_mode=ChangelogMode.UPDATE,
        prev_changelog_file="CHANGELOG.md",
        changelog_insertion_flag="<!-- CHANGELOG -->",
        mask_initial_release=False,
    )

    return context


# Pydantic 모델 구조 출력 방법들
def print_model_structure():
    context = example_data()

    print("=== 모델 구조 확인 방법들 ===")

    # 1. model_dump() - 딕셔너리로 변환
    print("\n1. model_dump() - 딕셔너리 형태:")
    print(context.model_dump())

    # 2. model_dump_json() - JSON 문자열로 변환 (예쁘게 포맷팅)
    print("\n2. model_dump_json(indent=2) - JSON 형태:")
    print(context.model_dump_json(indent=2))

    # 3. model_fields - 필드 정보 확인
    print("\n3. model_fields - 필드 정보:")
    for field_name, field_info in context.model_fields.items():
        print(f"  {field_name}: {field_info}")

    # 4. __str__() - 기본 문자열 표현
    print("\n4. str(model) - 기본 문자열:")
    print(str(context))

    # 5. __repr__() - 개발자용 표현
    print("\n5. repr(model) - 개발자용 표현:")
    print(repr(context))

    # 6. 특정 필드만 출력
    print("\n6. 특정 필드만 접근:")
    print(f"repo_name: {context.repo_name}")
    print(f"history.unreleased keys: {list(context.history.unreleased.keys())}")

    # 7. 스키마 정보
    print("\n7. model_json_schema() - JSON 스키마:")
    schema = context.model_json_schema()
    import json

    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    print_model_structure()
