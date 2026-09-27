from memory.detector import MemoryDetector


def test_detector_recognizes_name():
    detector = MemoryDetector()

    assert detector.should_remember("My name is Alex.")


def test_detector_recognizes_favorite():
    detector = MemoryDetector()

    assert detector.should_remember("My favorite color is green.")


def test_detector_recognizes_pet():
    detector = MemoryDetector()

    assert detector.should_remember("My dog is named Max.")


def test_detector_rejects_normal_question():
    detector = MemoryDetector()

    assert not detector.should_remember("What is the weather today?")


def test_detector_rejects_empty_message():
    detector = MemoryDetector()

    assert not detector.should_remember("")


def test_detector_ignores_whitespace():
    detector = MemoryDetector()

    assert not detector.should_remember("   ")