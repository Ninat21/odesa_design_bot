import re
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse


@dataclass(frozen=True)
class ExtractedFact:
    fact_type: str
    value: str
    confidence: float


URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
AGE_RE = re.compile(
    r"\b(?:мені|мне)\s+(\d{1,2})\s*(?:рок(?:и|ів)?|лет|года?)\b",
    re.IGNORECASE,
)
ROLE_RE = re.compile(
    r"\b((?:(?:графічн|графическ|продуктов|бренд|інтерфейс|"
    r"интерфейс|веб|web|ux[\s/]*ui|ui[\s/]*ux|motion|3d)\w*\s+)?"
    r"(?:дизайнер\w*|ілюстратор\w*|иллюстратор\w*|фотограф\w*|"
    r"маркетолог\w*|архітектор\w*|архитектор\w*|художник\w*|"
    r"художниц\w*|копірайтер\w*|копирайтер\w*|розробник\w*|"
    r"разработчик\w*|програміст\w*|программист\w*))\b",
    re.IGNORECASE,
)
PERSONAL_RE = re.compile(
    r"\b(?:я|мені|мне|мій|моя|моє|мої|мой|мое|мои|"
    r"працюю|работаю|займаюся|занимаюсь)\b",
    re.IGNORECASE,
)
HOBBY_RE = re.compile(
    r"\b(?:моє\s+хобі|мое\s+хобби|я\s+захоплююся|"
    r"я\s+увлекаюсь)\s*[:—\-]?\s*([^.!?\n]{2,100})",
    re.IGNORECASE,
)
PERSONAL_LINK_RE = re.compile(
    r"\b(?:мій|моя|моє|мой|мое|my|мої|мои)\s+"
    r"(?:інстаграм|инстаграм|instagram|behance|linkedin|"
    r"портфоліо|портфолио|portfolio|сайт)",
    re.IGNORECASE,
)


def clean_url(url: str) -> str:
    return url.rstrip(".,;:!?)]}")


def extract_profile_facts(
    text: str,
    message_date: datetime,
    username: str | None = None,
) -> list[ExtractedFact]:
    facts: list[ExtractedFact] = []
    personal = bool(PERSONAL_RE.search(text))

    age = AGE_RE.search(text)
    if age:
        facts.append(
            ExtractedFact(
                "age",
                f"{age.group(1)} (на {message_date.strftime('%d.%m.%Y')})",
                0.98,
            )
        )

    if personal:
        role = ROLE_RE.search(text)
        if role:
            facts.append(ExtractedFact("profession", role.group(1).strip(), 0.90))

        hobby = HOBBY_RE.search(text)
        if hobby:
            facts.append(ExtractedFact("hobby", hobby.group(1).strip(), 0.92))

    for raw_url in URL_RE.findall(text):
        url = clean_url(raw_url)
        parsed = urlparse(url)
        domain = parsed.netloc.lower().removeprefix("www.")
        path = parsed.path.lower()
        username_match = bool(username and username.lower() in path)
        explicitly_personal = bool(PERSONAL_LINK_RE.search(text))
        if not (username_match or explicitly_personal):
            continue

        if domain in {"instagram.com", "behance.net", "linkedin.com"}:
            facts.append(ExtractedFact("social", url, 0.97))
        elif re.search(r"портфол|portfolio", text, re.IGNORECASE):
            facts.append(ExtractedFact("portfolio", url, 0.95))
        elif re.search(r"\b(?:мій|мой|my)\s+сайт\b", text, re.IGNORECASE):
            facts.append(ExtractedFact("website", url, 0.95))

    return list(dict.fromkeys(facts))
