"""ECC auto-router plugin.

Adds a pre_llm_call hook that maps the current user task to the minimum
relevant ECC plugin skill(s), then injects a short routing directive into the
current user turn context.
"""

from __future__ import annotations

import re
from typing import List

# Keep mapping minimal and deterministic.
_RULES = [
    # Security first when explicit
    (re.compile(r"\b(security|vuln|vulnerability|audit|pentest|threat|xss|sqli|csrf)\b", re.I),
     ["ecc-security:security-review"]),

    # Language/domain primary
    (re.compile(r"\b(django|flask|fastapi|pytorch|python|pytest|mypy|ruff)\b", re.I),
     ["ecc-python:python-patterns"]),
    (re.compile(r"\b(rust|cargo|clippy|tokio)\b", re.I),
     ["ecc-rust:rust-patterns"]),
    (re.compile(r"\b(next\.js|nextjs|nuxt|nestjs|typescript|javascript|react|node)\b", re.I),
     ["ecc-typescript:frontend-patterns"]),
    (re.compile(r"\b(spring|springboot|java|kotlin|gradle|maven|ktor)\b", re.I),
     ["ecc-java-kotlin:springboot-patterns"]),
    (re.compile(r"\b(golang|\bgo\b|gin|fiber)\b", re.I),
     ["ecc-go:golang-patterns"]),
    (re.compile(r"\b(c\+\+|cpp|cmake)\b", re.I),
     ["ecc-cpp:cpp-coding-standards"]),
    (re.compile(r"\b(c#|dotnet|\.net|asp\.net)\b", re.I),
     ["ecc-dotnet:dotnet-patterns"]),
    (re.compile(r"\b(swift|swiftui|xcode|ios)\b", re.I),
     ["ecc-swift:swift-concurrency-6-2"]),
    (re.compile(r"\b(flutter|dart)\b", re.I),
     ["ecc-dart-flutter:dart-flutter-patterns"]),
    (re.compile(r"\b(laravel|php)\b", re.I),
     ["ecc-php:laravel-patterns"]),
    (re.compile(r"\b(perl)\b", re.I),
     ["ecc-perl:perl-patterns"]),

    # DevOps
    (re.compile(r"\b(ci/cd|deploy|deployment|docker|kubernetes|k8s|pipeline|terraform)\b", re.I),
     ["ecc-devops:deployment-patterns"]),
]

_IMPLEMENTATION_HINT = re.compile(
    r"\b(implement|build|create|add|feature|bug|fix|refactor|rewrite|patch)\b", re.I
)


def _route_skills(user_message: str) -> List[str]:
    picks: List[str] = []

    for pattern, skills in _RULES:
        if pattern.search(user_message):
            for s in skills:
                if s not in picks:
                    picks.append(s)
            # one primary skill only
            break

    if not picks:
        picks.append("ecc-core:tdd-workflow")

    # add core tdd workflow only for implementation-ish requests
    if _IMPLEMENTATION_HINT.search(user_message) and "ecc-core:tdd-workflow" not in picks:
        picks.append("ecc-core:tdd-workflow")

    # hard cap: one primary + one cross-cutting
    return picks[:2]


def on_pre_llm_call(*, user_message: str = "", **kwargs):
    if not user_message:
        return None

    skills = _route_skills(user_message)
    if not skills:
        return None

    lines = [
        "[ECC Auto-Router]",
        "Before proceeding, load these plugin skill(s) with skill_view in this order:",
    ]
    for s in skills:
        lines.append(f"- {s}")

    lines.append("Use only the minimum relevant set. If any skill is missing, continue with closest available one.")

    return {"context": "\n".join(lines)}


def register(ctx):
    ctx.register_hook("pre_llm_call", on_pre_llm_call)
