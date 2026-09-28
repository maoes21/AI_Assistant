from memory.detector import MemoryDetector


def test_detector_creates_candidate_for_name():
    detector = MemoryDetector()

    candidate = detector.detect("My name is Alex.")

    assert candidate is not None
    assert candidate.content == "User's name is Alex."


def test_detector_creates_candidate_for_favorite_color():
    detector = MemoryDetector()

    candidate = detector.detect("My favorite color is green.")

    assert candidate is not None
    assert candidate.content == "User's favorite color is green."


def test_detector_creates_candidate_for_dog():
    detector = MemoryDetector()

    candidate = detector.detect("My dog is named Max.")

    assert candidate is not None
    assert candidate.content == "User's dog is named Max."


def test_detector_creates_candidate_for_cat():
    detector = MemoryDetector()

    candidate = detector.detect("My cat is named Luna.")

    assert candidate is not None
    assert candidate.content == "User's cat is named Luna."


def test_detector_creates_candidate_for_location():
    detector = MemoryDetector()

    candidate = detector.detect("I live in Denmark.")

    assert candidate is not None
    assert candidate.content == "User lives in Denmark."


def test_detector_creates_candidate_for_workplace():
    detector = MemoryDetector()

    candidate = detector.detect("I work at Microsoft.")

    assert candidate is not None
    assert candidate.content == "User works at Microsoft."


def test_detector_creates_candidate_for_job():
    detector = MemoryDetector()

    candidate = detector.detect("I work as a programmer.")

    assert candidate is not None
    assert candidate.content == "User works as a programmer."


def test_detector_creates_candidate_for_job_description():
    detector = MemoryDetector()

    candidate = detector.detect("My job is software development.")

    assert candidate is not None
    assert candidate.content == "User's job is software development."


def test_detector_creates_candidate_for_dog_ownership():
    detector = MemoryDetector()

    candidate = detector.detect("I have a dog.")

    assert candidate is not None
    assert candidate.content == "User has a dog."


def test_detector_creates_candidate_for_cat_ownership():
    detector = MemoryDetector()

    candidate = detector.detect("I have a cat.")

    assert candidate is not None
    assert candidate.content == "User has a cat."


def test_detector_rejects_normal_question():
    detector = MemoryDetector()

    assert detector.detect("What is the weather today?") is None


def test_detector_rejects_empty_message():
    detector = MemoryDetector()

    assert detector.detect("") is None


def test_detector_ignores_whitespace():
    detector = MemoryDetector()

    assert detector.detect("   ") is None