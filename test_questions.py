"""
Test script to validate question detection for common interview questions.
Run this to verify the question detector is working properly.
"""

from realtime_processor import QuestionDetector

# Common interview questions by category
TEST_QUESTIONS = {
    "Problem Solving": [
        "Tell me about a time you faced a challenging technical problem. How did you solve it?",
        "Describe a time when you had to make a quick decision with incomplete information.",
        "Give an example of when you identified a potential problem before it became serious.",
        "Walk me through your process for debugging a complex system.",
        "Describe a time when your solution failed. What did you learn?",
    ],
    "Teamwork & Collaboration": [
        "Describe a time when you worked closely with a team to deliver a project.",
        "Tell me about a time you had a conflict with a coworker. How did you handle it?",
        "How do you ensure effective communication between technical and non-technical team members?",
        "Give an example of when you supported a team member struggling with their work.",
        "Tell me about a time you helped improve team efficiency or collaboration.",
    ],
    "Leadership & Initiative": [
        "Describe a time when you took the lead on a project.",
        "Tell me about a time when you motivated others to achieve a difficult goal.",
        "Share an example of when you had to delegate tasks effectively.",
        "Have you ever introduced a new idea or process that improved outcomes?",
        "Describe how you handle mentoring or guiding junior engineers.",
    ],
    "Time Management & Prioritization": [
        "Tell me about a time you had multiple competing deadlines. How did you prioritize?",
        "Describe a project that required significant time management.",
        "How do you stay organized when juggling multiple projects?",
        "Give an example of when you missed a deadline and how you handled it.",
    ],
    "Adaptability & Learning": [
        "Describe a time you had to learn a new technology or tool quickly.",
        "How do you handle changes in project scope or direction?",
        "Tell me about a time when your project priorities shifted unexpectedly.",
        "What do you do to stay current in your field?",
    ],
    "Communication": [
        "Tell me about a time you had to explain a complex technical issue to a non-technical audience.",
        "How do you handle misunderstandings on a team?",
        "Give an example of how you've handled feedback—either giving or receiving it.",
        "Describe a time you had to persuade others to adopt your idea.",
    ],
    "Ethics & Accountability": [
        "Describe a situation where you made a mistake. How did you handle it?",
        "Tell me about a time when you disagreed with a decision but had to support it.",
        "How do you ensure integrity in your work and reporting?",
    ]
}

def test_question_detection():
    """Test the question detector against all common interview questions."""

    print("=" * 80)
    print("QUESTION DETECTION TEST")
    print("=" * 80)
    print()

    total_questions = 0
    detected_questions = 0
    failed_questions = []

    for category, questions in TEST_QUESTIONS.items():
        print(f"\n📋 {category}")
        print("-" * 80)

        for question in questions:
            total_questions += 1
            is_detected = QuestionDetector.is_question(question)

            if is_detected:
                detected_questions += 1
                print(f"✅ {question[:70]}...")
            else:
                print(f"❌ {question[:70]}...")
                failed_questions.append((category, question))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Questions: {total_questions}")
    print(f"Detected: {detected_questions}")
    print(f"Missed: {len(failed_questions)}")
    print(f"Success Rate: {(detected_questions/total_questions)*100:.1f}%")

    if failed_questions:
        print("\n" + "=" * 80)
        print("MISSED QUESTIONS")
        print("=" * 80)
        for category, question in failed_questions:
            print(f"\n[{category}]")
            print(f"  {question}")

    print("\n" + "=" * 80)

    if detected_questions == total_questions:
        print("🎉 ALL QUESTIONS DETECTED SUCCESSFULLY!")
    else:
        print(f"⚠️  {len(failed_questions)} questions need attention")

    print("=" * 80)


if __name__ == "__main__":
    test_question_detection()
