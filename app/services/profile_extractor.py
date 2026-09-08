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
ROLE_PATTERN = (
    r"(?:(?:графічн\w*|графическ\w*|продуктов\w*|бренд[\s-]?|"
    r"інтерфейс\w*|интерфейс\w*|веб[\s-]?|web[\s-]?|"
    r"ux[\s/]*ui|ui[\s/]*ux|motion[\s-]?|3d[\s-]?)\s*)?"
    r"(?:дизайнер(?:ка|кою|ом)?|ілюстратор(?:ка|ом)?|"
    r"иллюстратор(?:ка|ом)?|фотограф(?:ка|ом)?|маркетолог(?:ом)?|"
    r"архітектор(?:ка|ом)?|архитектор(?:ка|ом)?|художник(?:ом)?|"
    r"художниця|копірайтер(?:ка|ом|кою)?|копирайтер(?:ом)?|"
    r"розробник(?:ом)?|разработчик(?:ом)?|програміст(?:ом)?|"
    r"программист(?:ом)?)"
)
ROLE_RE = re.compile(rf"\b({ROLE_PATTERN})\b", re.IGNORECASE)
SELF_ROLE_RE = re.compile(
    rf"\bя\b(?:\s+[\wʼ'’-]+){{0,4}}?\s+\b({ROLE_PATTERN})\b",
    re.IGNORECASE,
)
WORK_ROLE_RE = re.compile(
    rf"\b(?:працюю|работаю|працювала|работала|"
    rf"за\s+фахом|за\s+освітою|по\s+профессии)\b"
    rf"(?:\s+[\wʼ'’-]+){{0,6}}\s+\b({ROLE_PATTERN})\b",
    re.IGNORECASE,
)
INTRO_RE = re.compile(
    r"\b(?:всім\s+привіт|всем\s+привет|мене\s+звати|"
    r"меня\s+зовут)\b",
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
INTRO_NAME_RE = re.compile(
    r"\b(?:мене\s+звати|меня\s+зовут)\s+([\wʼ'’-]+)",
    re.IGNORECASE,
)
NEGATED_ROLE_RE = re.compile(
    rf"\bне\b(?:\s+[\wʼ'’-]+){{0,2}}\s+\b{ROLE_PATTERN}\b",
    re.IGNORECASE,
)
QUOTED_TEXT_RE = re.compile(r"[«“\"](?:.|\n)*?[»”\"]")


def clean_url(url: str) -> str:
    return url.rstrip(".,;:!?)]}")


def introduction_matches_author(text: str, first_name: str | None) -> bool:
    introduced = INTRO_NAME_RE.search(text[:500])
    if introduced is None or not first_name:
        return True
    return introduced.group(1)[0].casefold() == first_name[0].casefold()


def extract_profile_facts(
    text: str,
    message_date: datetime,
    username: str | None = None,
    first_name: str | None = None,
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
        identity_text = QUOTED_TEXT_RE.sub(" ", text)
        author_intro = introduction_matches_author(text, first_name)
        intro = INTRO_RE.search(identity_text[:120])
        identity_context = intro is not None or len(text) <= 250
        role = SELF_ROLE_RE.search(identity_text[:180]) if author_intro else None
        if role is None and author_intro:
            role = WORK_ROLE_RE.search(identity_text[:180])
        if role is None and author_intro and intro:
            role = ROLE_RE.search(identity_text[:180])
        if (
            role
            and identity_context
            and not NEGATED_ROLE_RE.search(identity_text[:250])
        ):
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
